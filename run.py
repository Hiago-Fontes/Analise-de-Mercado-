import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

# Adiciona o diretório raiz do projeto ao path do Python
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

try:
    from src.core.database.db import init_db, get_db
    from src.core.analysis.data_sources import ensure_seed_data, ingest_latest
    from src.core.analysis.scoring import build_recommendations
    from src.core.analysis.report import generate_monthly_report
except ImportError as e:
    print(f"ERRO ao importar módulos: {e}")
    sys.exit(1)

app = Flask(__name__, template_folder=os.path.join(PROJECT_ROOT, "src/app/templates"), static_folder=os.path.join(PROJECT_ROOT, "src/app/static"))
app.secret_key = os.environ.get("APP_SECRET", "dev-secret-key")

# Sempre usar a pasta 'data' do projeto (nunca /tmp)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "market.sqlite")

@app.before_request
def setup():
    """Inicializar banco de dados na primeira requisição"""
    if not hasattr(setup, 'initialized'):
        try:
            init_db(DB_PATH)
            ensure_seed_data(DB_PATH)
            setup.initialized = True
        except Exception as e:
            print(f"ERRO ao inicializar banco: {e}")
            import traceback
            traceback.print_exc()

@app.route("/")
def index():
    """Página inicial"""
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"ERRO ao renderizar index: {e}")
        import traceback
        traceback.print_exc()
        return f"Erro: {e}", 500

@app.post("/analyze")
def analyze():
    """Analisar tickers"""
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
        print(f"ERRO ao analisar: {e}")
        import traceback
        traceback.print_exc()
        flash(f"Erro na análise: {e}", "danger")
        return redirect(url_for("index"))

@app.get("/recommendations")
def recommendations():
    """Mostrar recomendações"""
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
        # Converter sqlite3.Row para dict para compatibilidade com Jinja2
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
    """Gerar relatório mensal"""
    month = request.args.get("month")
    try:
        if not month:
            month = datetime.now().strftime("%Y-%m")
        rep_path, summary = generate_monthly_report(DB_PATH, month)
        flash(f"Relatório gerado em {rep_path}", "success")
        return render_template("report.html", month=month, summary=summary)
    except Exception as e:
        print(f"ERRO ao gerar relatório: {e}")
        import traceback
        traceback.print_exc()
        flash(f"Erro ao gerar relatório: {e}", "danger")
        return redirect(url_for("index"))

@app.errorhandler(500)
def handle_500(e):
    """Tratador de erros 500"""
    print(f"ERRO 500: {e}")
    import traceback
    traceback.print_exc()
    return f"Erro interno do servidor: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
