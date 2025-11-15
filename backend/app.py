from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os
import sys

# Adiciona o diretório raiz do projeto ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.db import init_db, get_db
from analysis.data_sources import ensure_seed_data, ingest_latest
from analysis.scoring import build_recommendations
from analysis.report import generate_monthly_report
from assets_config import CATEGORIAS, TODOS_ATIVOS

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET", "dev-secret")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "market.sqlite")
DB_PATH = os.path.abspath(DB_PATH)

@app.before_request
def setup():
    if not hasattr(setup, 'initialized'):
        init_db(DB_PATH)
        ensure_seed_data(DB_PATH)
        setup.initialized = True

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/assets")
def api_assets():
    """API para obter lista de ativos por categoria"""
    return jsonify({
        "categorias": list(CATEGORIAS.keys()),
        "ativos": {cat: list(ativos.keys()) for cat, ativos in CATEGORIAS.items()},
        "detalhes": {ticker: {"nome": info["nome"], "setor": info["setor"], "tipo": info["tipo"]} 
                     for ticker, info in TODOS_ATIVOS.items()}
    })

@app.post("/analyze")
def analyze():
    try:
        tickers_raw = request.form.get("tickers", "")
        tickers = [t.strip().upper() for t in tickers_raw.split(",") if t.strip()]
        if not tickers:
            flash("Informe ao menos um ticker (ex.: PETR4.SA, VALE3.SA, KNRI11.SA)", "warning")
            return redirect(url_for("index"))

        # Ingestão de dados (preços + indicadores)
        ingest_latest(DB_PATH, tickers)
        # Gera recomendações
        build_recommendations(DB_PATH)
        return redirect(url_for("recommendations"))
    except Exception as e:
        flash(f"Erro na análise: {e}", "danger")
        return redirect(url_for("index"))

@app.get("/recommendations")
def recommendations():
    try:
        conn = get_db(DB_PATH)
        cur = conn.cursor()
        recs = cur.execute(
            """
            SELECT r.ticker, r.score, r.volatility, r.max_drawdown, r.dividend_yield, a.name
            FROM recommendations r
            JOIN assets a ON a.ticker = r.ticker
            ORDER BY r.score DESC
            LIMIT 50
            """
        ).fetchall()
        conn.close()
        # Converter sqlite3.Row para dict
        rows_dict = [dict(r) for r in recs]
        return render_template("recommendations.html", rows=rows_dict)
    except Exception as e:
        print(f"ERRO ao buscar recomendações: {e}")
        import traceback
        traceback.print_exc()
        flash(f"Erro ao buscar recomendações: {e}", "danger")
        return redirect(url_for("index"))

@app.get("/report")
def report():
    month = request.args.get("month")
    try:
        if not month:
            # mês atual
            month = datetime.now().strftime("%Y-%m")
        rep_path, summary = generate_monthly_report(DB_PATH, month)
        flash(f"Relatório gerado em {rep_path}", "success")
        return render_template("report.html", month=month, summary=summary)
    except Exception as e:
        flash(f"Erro ao gerar relatório: {e}", "danger")
        return redirect(url_for("index"))

if __name__ == "__main__":
    # Executa o app de desenvolvimento
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
