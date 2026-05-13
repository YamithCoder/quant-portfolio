import yfinance as yf
import pandas as pd
import numpy as np

def analyze_multiple_assets(tickers, start, end):
    df =yf.download(tickers=tickers, start=start, end=end, auto_adjust=True)
    prices = df["Close"].copy()
    prices = prices.ffill().dropna()
    returns = prices.pct_change().dropna()
    total_return = (prices.iloc[-1]/ prices.iloc[0]) -1
    volatility = returns.std()
    summary = pd.DataFrame({
        'Total return': total_return,
        'Daily volatility': volatility
    })
    #Format
    print("\n── Rendimiento 2024 ────────────────────")
    summary_fm = summary.copy()

    summary_fm['Total return'] = summary_fm['Total return'].map(lambda x: f"{x:.2%}")
    summary_fm['Daily volatility'] = summary_fm['Daily volatility'].map(lambda x: f"{x:.2%}")
    print(summary_fm)

    print("\n── Correlation matrix ───────────────")
    print(returns.corr().round(2))

    prices_norm = (prices / prices.iloc[0]) * 100
    print("\n── Standardized prices (Base 100) ─────")
    print(prices_norm.head(3))

    return prices, returns, prices_norm

tickers_list = ["AAPL", "MSFT", "NVDA", "BTC-USD", "GLD"]
prices, returns, prices_norm = analyze_multiple_assets(tickers_list, "2024-01-01", "2024-12-31")