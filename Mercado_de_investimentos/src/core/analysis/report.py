import os
import sys
from datetime import datetime
import pandas as pd

# Adiciona o diretório raiz do projeto ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.core.database.db import get_db


def generate_monthly_report(db_path: str, month: str):
    """
    month: 'YYYY-MM'
    Retorna (path_html, summary_dict)
    """
    conn = get_db(db_path)
    year, mon = month.split("-")
    start = f"{year}-{mon}-01"
    # Fim: próximo mês menos 1 dia (pandas período mensal)
    period = pd.Period(month)
    end = (period.asfreq('M').end_time).strftime("%Y-%m-%d")

    prices = pd.read_sql_query(
        "SELECT ticker, date, close, dividend FROM prices WHERE date BETWEEN ? AND ?",
        conn,
        params=(start, end),
        parse_dates=["date"]
    )  # type: ignore

    if prices.empty:
        raise RuntimeError("Sem dados de preços no período.")

    # Retornos simples por ticker
    last = prices.sort_values(["ticker", "date"]).groupby("ticker").tail(1).set_index("ticker")
    first = prices.sort_values(["ticker", "date"]).groupby("ticker").head(1).set_index("ticker")
    returns = (last["close"] / first["close"] - 1.0).rename("return")
    dividends = prices.groupby("ticker")["dividend"].sum().rename("dividends")
    df_summary = pd.concat([returns, dividends], axis=1).fillna(0)

    # PnL hipotético: carteira equiponderada dos 5 melhores (se houver recomendações)
    recs = pd.read_sql_query("SELECT ticker, score FROM recommendations ORDER BY score DESC LIMIT 5", conn)
    selected = recs["ticker"].tolist() if not recs.empty else df_summary.index.tolist()[:5]
    selected = [t for t in selected if t in df_summary.index]
    if selected:
        eq_weight = 1.0 / len(selected)
    else:
        selected = df_summary.index.tolist()
        eq_weight = 1.0 / max(len(selected), 1)

    df_summary["weight"] = 0.0
    df_summary.loc[selected, "weight"] = eq_weight
    df_summary["pnl"] = df_summary["return"] * df_summary["weight"]

    # Drawdown do período (por ticker)
    dd = []
    for t, g in prices.groupby("ticker"):
        g = g.sort_values("date")
        cummax = g["close"].cummax()
        drawdown = g["close"] / cummax - 1.0
        dd.append(drawdown.min())
    avg_drawdown = float(pd.Series(dd).mean()) if dd else 0.0

    total_return = float(df_summary["pnl"].sum())
    total_divs = float((df_summary["dividends"] * df_summary["weight"]).sum())

    summary = {
        "month": month,
        "selected": selected,
        "portfolio_return": total_return,
        "portfolio_dividends": total_divs,
        "avg_drawdown": avg_drawdown,
    }

    # Render HTML simples
    html = [
        f"<h1>Relatório Mensal — {month}</h1>",
        f"<p>Carteira escolhida: {', '.join(selected) or 'n/a'}</p>",
        f"<p>Retorno da carteira (aprox.): {total_return:.2%}</p>",
        f"<p>Dividendos (aprox.): {total_divs:.4f}</p>",
        f"<p>Drawdown médio no período: {avg_drawdown:.2%}</p>",
        "<h2>Detalhes por ativo</h2>",
        df_summary.to_html(float_format=lambda x: f"{x:.4f}")
    ]
    out_dir = os.path.abspath(os.path.join(os.path.dirname(db_path), "..", "reports"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"report_{month}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    # Registra
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reports(month, path, created_at) VALUES(?,?,?)",
        (month, out_path, datetime.utcnow().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

    return out_path, summary
