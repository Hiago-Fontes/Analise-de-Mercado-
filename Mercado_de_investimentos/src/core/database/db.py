import sqlite3
import os

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS assets (
    ticker TEXT PRIMARY KEY,
    name   TEXT,
    class  TEXT
);

CREATE TABLE IF NOT EXISTS prices (
    ticker TEXT,
    date   TEXT,
    close  REAL,
    dividend REAL DEFAULT 0,
    PRIMARY KEY (ticker, date)
);

CREATE INDEX IF NOT EXISTS idx_prices_ticker_date ON prices(ticker, date);

CREATE TABLE IF NOT EXISTS econ_indicators (
    name TEXT,
    date TEXT,
    value REAL,
    PRIMARY KEY (name, date)
);

CREATE TABLE IF NOT EXISTS recommendations (
    ticker TEXT PRIMARY KEY,
    score REAL,
    volatility REAL,
    max_drawdown REAL,
    dividend_yield REAL,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,
    path TEXT,
    created_at TEXT
);
"""

def get_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
