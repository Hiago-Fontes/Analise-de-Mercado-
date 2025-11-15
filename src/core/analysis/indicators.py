import pandas as pd
import numpy as np


def compute_volatility(prices: pd.Series, trading_days: int = 252) -> float:
    returns = prices.pct_change().dropna()
    if returns.empty:
        return float("nan")
    return float(returns.std() * (trading_days ** 0.5))


def max_drawdown(prices: pd.Series) -> float:
    if prices.empty:
        return float("nan")
    cummax = prices.cummax()
    drawdown = prices / cummax - 1.0
    return float(drawdown.min())


def trailing_dividend_yield(df: pd.DataFrame) -> float:
    # Espera colunas: close, dividend
    if df.empty:
        return 0.0
    total_div = df["dividend"].fillna(0).sum()
    last_price = df["close"].iloc[-1]
    if last_price <= 0:
        return 0.0
    # Aproximação: soma de dividendos no período / último preço
    return float(total_div / last_price)


def simple_market_regime(market: pd.Series) -> str:
    # Regime com base em média móvel: 50 > 200 => risk-on, senão risk-off
    if len(market) < 200:
        return "unknown"
    ma50 = market.rolling(50).mean()
    ma200 = market.rolling(200).mean()
    if ma50.iloc[-1] > ma200.iloc[-1]:
        return "risk-on"
    return "risk-off"
