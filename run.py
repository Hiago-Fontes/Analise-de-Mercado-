import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, has_request_context
from datetime import datetime

# Adiciona o diretório raiz do projeto ao path do Python
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.core.database.db import init_db, get_db
from src.core.analysis.data_sources import ensure_seed_data, ingest_latest
from src.core.analysis.scoring import build_recommendations
from src.core.analysis.report import generate_monthly_report

app = Flask(__name__, template_folder=os.path.join(PROJECT_ROOT, "src/app/templates"), static_folder=os.path.join(PROJECT_ROOT, "src/app/static"))
app.secret_key = os.environ.get("APP_SECRET", "dev-secret-key")

# Injetar has_request_context no contexto do Jinja2
@app.context_processor
def inject_has_request_context():
    return dict(has_request_context=has_request_context)

DB_PATH = os.path.join(PROJECT_ROOT, "data", "market.sqlite")

@app.before_request
def setup():
    if not hasattr(setup, 'initialized'):
        init_db(DB_PATH)
        ensure_seed_data(DB_PATH)
        setup.initialized = True

@app.route("/")
def index():
    return render_template("index.html")

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
    return render_template("recommendations.html", rows=recs)

@app.get("/report")
def report():
    month = request.args.get("month")
    try:
        if not month:
            month = datetime.now().strftime("%Y-%m")
        rep_path, summary = generate_monthly_report(DB_PATH, month)
        flash(f"Relatório gerado em {rep_path}", "success")
        return render_template("report.html", month=month, summary=summary)
    except Exception as e:
        flash(f"Erro ao gerar relatório: {e}", "danger")
        return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
