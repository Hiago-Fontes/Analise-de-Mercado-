import os
import sys
from datetime import datetime
import pandas as pd

# Adiciona o diretório raiz do projeto ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db.db import get_db
from .indicators import compute_volatility, max_drawdown, trailing_dividend_yield, simple_market_regime


def build_recommendations(db_path: str):
    conn = get_db(db_path)
    cur = conn.cursor()
    # Carrega preços
    df = pd.read_sql_query("SELECT ticker, date, close, dividend FROM prices", conn, parse_dates=["date"])  # type: ignore
    if df.empty:
        return
    # Mercado de referência: usa SPY se houver, senão média igualitária
    piv = df.pivot(index="date", columns="ticker", values="close").sort_index()
    if "SPY" in piv.columns:
        market = piv["SPY"].dropna()
    else:
        market = piv.mean(axis=1)
    regime = simple_market_regime(market)

    rows = []
    for ticker, g in df.groupby("ticker"):
        g = g.sort_values("date")
        vol = compute_volatility(g["close"])  # anualizado
        mdd = max_drawdown(g["close"])      # negativo
        dy = trailing_dividend_yield(g)
        # Normalizações simples (robustas a NaN):
        vol_n = (vol if pd.notna(vol) else 1.0)
        mdd_n = abs(mdd) if pd.notna(mdd) else 0.5
        dy_n = dy if pd.notna(dy) else 0.0
        # Score: quanto menor vol e mdd e maior dy, melhor.
        score = (1.0 / (1.0 + vol_n)) + (1.0 / (1.0 + mdd_n)) + (dy_n)
        # Penaliza risco em regime risk-off
        if regime == "risk-off":
            score *= 0.9 if vol_n > 0.25 else 1.05
        # Salvar valores normalizados (nunca None)
        rows.append((ticker, score, vol_n if pd.notna(vol) else None, mdd if pd.notna(mdd) else None, dy_n, datetime.utcnow().isoformat(timespec="seconds")))

    cur.execute("DELETE FROM recommendations")
    cur.executemany(
        "INSERT INTO recommendations(ticker, score, volatility, max_drawdown, dividend_yield, created_at) VALUES(?,?,?,?,?,?)",
        rows
    )
    conn.commit()
    conn.close()
