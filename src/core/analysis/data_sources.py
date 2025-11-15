import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adiciona o diretório raiz do projeto ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.core.database.db import get_db

try:
    import yfinance as yf
except Exception:
    yf = None

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))

SAMPLE_TICKERS = ["SPY", "AAPL", "VNQ"]


def _read_csv_safe(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def ensure_seed_data(db_path: str):
    """Garante que existam alguns ativos e preços mínimos para rodar offline."""
    os.makedirs(DATA_DIR, exist_ok=True)
    # Tickers
    tickers_csv = os.path.join(DATA_DIR, "sample_tickers.csv")
    if not os.path.exists(tickers_csv):
        pd.DataFrame({
            "ticker": SAMPLE_TICKERS,
            "name": ["S&P 500 ETF", "Apple Inc.", "Vanguard Real Estate ETF"],
            "class": ["EQUITY", "EQUITY", "REIT"]
        }).to_csv(tickers_csv, index=False)
    # Preços sintéticos se não existir
    prices_csv = os.path.join(DATA_DIR, "sample_prices.csv")
    if not os.path.exists(prices_csv):
        dates = pd.date_range(end=datetime.today(), periods=260, freq="B")
        rng = np.random.default_rng(42)
        df_list = []
        for t in SAMPLE_TICKERS:
            base = 100 + rng.normal(0, 1, len(dates)).cumsum()
            dividends = np.where((np.arange(len(dates)) % 21) == 0, 0.05, 0.0)  # dividendos mensais pequenos
            df_list.append(pd.DataFrame({
                "ticker": t,
                "date": dates.strftime("%Y-%m-%d"),
                "close": base + rng.normal(0, 0.5, len(dates)),
                "dividend": dividends
            }))
        pd.concat(df_list).to_csv(prices_csv, index=False)

    # Carrega no DB se vazio
    conn = get_db(db_path)
    cur = conn.cursor()
    existing = cur.execute("SELECT COUNT(1) c FROM assets").fetchone()[0]
    if existing == 0:
        assets = pd.read_csv(tickers_csv)
        cur.executemany(
            "INSERT OR REPLACE INTO assets(ticker, name, class) VALUES(?,?,?)",
            assets[["ticker", "name", "class"]].values.tolist()
        )
        conn.commit()

    prices_count = cur.execute("SELECT COUNT(1) c FROM prices").fetchone()[0]
    if prices_count == 0:
        prices = pd.read_csv(prices_csv)
        cur.executemany(
            "INSERT OR REPLACE INTO prices(ticker, date, close, dividend) VALUES(?,?,?,?)",
            prices[["ticker", "date", "close", "dividend"]].values.tolist()
        )
        conn.commit()
    conn.close()


def fetch_prices_online(tickers, period="1y") -> pd.DataFrame:
    if yf is None:
        raise RuntimeError("yfinance não disponível")
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    if isinstance(data, pd.DataFrame) and "Close" in data.columns:
        close = data["Close"].copy()
    else:
        close = data.copy()
    close.index = close.index.strftime("%Y-%m-%d")
    frames = []
    for t in tickers:
        s = close[t] if t in close.columns else close.squeeze()
        frames.append(pd.DataFrame({
            "ticker": t,
            "date": close.index,
            "close": s.values,
            "dividend": 0.0
        }))
    return pd.concat(frames)


def ingest_latest(db_path: str, tickers: list[str]):
    """Busca preços e grava no banco. Fallback: usa CSV de amostra."""
    conn = get_db(db_path)
    cur = conn.cursor()
    try:
        df = fetch_prices_online(tickers)
    except Exception:
        # Fallback — tenta usar arquivo de amostra e filtrar os tickers
        csv_path = os.path.join(DATA_DIR, "sample_prices.csv")
        df_all = _read_csv_safe(csv_path)
        if df_all.empty:
            raise RuntimeError("Sem dados online e sem amostras locais.")
        df = df_all[df_all["ticker"].isin(tickers)].copy()
        if df.empty:
            df = df_all.copy()  # usa tudo
    # Grava
    cur.executemany(
        "INSERT OR REPLACE INTO prices(ticker, date, close, dividend) VALUES(?,?,?,?)",
        df[["ticker", "date", "close", "dividend"]].values.tolist()
    )
    # Garante assets
    tickers_set = sorted(set(df["ticker"]))
    for t in tickers_set:
        cur.execute(
            "INSERT OR IGNORE INTO assets(ticker, name, class) VALUES(?,?,?)",
            (t, t, "EQUITY")
        )
    conn.commit()
    conn.close()
