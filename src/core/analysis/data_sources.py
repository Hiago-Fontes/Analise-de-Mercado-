import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adiciona o diretório raiz do projeto ao path do Python
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.core.database.db import get_db

try:
    import yfinance as yf
except Exception:
    yf = None

# DATA_DIR é sempre a pasta 'data' do projeto, não /tmp
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

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


def fetch_prices_online(ticker: str, period="1y") -> pd.DataFrame:
    """Busca preço de UM ticker apenas"""
    if yf is None:
        raise RuntimeError("yfinance não disponível")
    
    try:
        # Usa Ticker object em vez de download para maior robustez
        t = yf.Ticker(ticker)
        data = t.history(period=period)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar {ticker}: {e}")
    
    if data.empty:
        raise RuntimeError(f"Sem dados para {ticker}")
    
    # Usa a coluna 'Close'
    if 'Close' not in data.columns:
        raise RuntimeError(f"Sem coluna 'Close' para {ticker}")
    
    close = data['Close'].copy()
    
    # Formata datas (remove timezone se houver)
    close.index = pd.to_datetime(close.index).strftime("%Y-%m-%d")
    
    df = pd.DataFrame({
        "ticker": ticker,
        "date": close.index,
        "close": close.values,
        "dividend": 0.0
    })
    
    return df


def ingest_latest(db_path: str, tickers: list[str]):
    """Busca preços e grava no banco. Fallback: usa CSV de amostra."""
    conn = get_db(db_path)
    cur = conn.cursor()
    
    # Tenta buscar cada ticker online
    dfs_fetched = []
    tickers_failed = []
    
    for ticker in tickers:
        try:
            print(f"Buscando {ticker} online...")
            df = fetch_prices_online(ticker, period="1y")
            dfs_fetched.append(df)
            print(f"OK - {ticker} buscado com {len(df)} registros")
        except Exception as e:
            print(f"Erro ao buscar {ticker}: {e}")
            tickers_failed.append(ticker)
    
    # Para tickers que falharam, tenta preencher com dados de amostra
    if tickers_failed:
        print(f"Preenchendo com amostra: {tickers_failed}")
        csv_path = os.path.join(DATA_DIR, "sample_prices.csv")
        if os.path.exists(csv_path):
            df_sample = pd.read_csv(csv_path)
            for ticker in tickers_failed:
                df_ticker = df_sample[df_sample["ticker"] == ticker].copy()
                if not df_ticker.empty:
                    dfs_fetched.append(df_ticker)
                    print(f"Usando amostra para {ticker} ({len(df_ticker)} registros)")
                else:
                    print(f"Sem amostra para {ticker}, ignorando")
        else:
            print(f"Arquivo de amostra não encontrado: {csv_path}")
    
    # Se ainda não tem dados, usa amostra de tudo
    if not dfs_fetched:
        print("Nenhum ticker buscado com sucesso, usando amostra completa")
        csv_path = os.path.join(DATA_DIR, "sample_prices.csv")
        if os.path.exists(csv_path):
            df_sample = pd.read_csv(csv_path)
            dfs_fetched.append(df_sample)
            print(f"Usando amostra completa ({len(df_sample)} registros)")
        else:
            raise RuntimeError(f"Sem dados: arquivo de amostra não encontrado em {csv_path}")
    
    if not dfs_fetched:
        raise RuntimeError("Sem dados disponíveis para análise")
    
    # Concatena todos os dados
    df = pd.concat(dfs_fetched, ignore_index=True)
    print(f"Dados consolidados: {len(df)} registros")
    
    # Grava no banco
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
    print(f"Ingestão completa: {len(tickers_set)} ativos com dados")
