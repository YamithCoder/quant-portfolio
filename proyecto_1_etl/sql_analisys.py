import pandas as pd
import numpy as np
import yfinance as yf

def financial_sql_analysis(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    prices = df[['Close', 'Volume']].copy()
    prices.columns = ['close', 'volume']
    prices['returns'] = prices['close'].ffill().pct_change()

    top_volume = prices.sort_values('volume', ascending= False).head(5)
    top_returns = prices.sort_values('returns', ascending=False).head(5)
    monthly_avg = prices.groupby(prices.index.month)['close'].mean()

    annual_avg = prices['close'].mean()
    days_above_avg = len(prices[prices['close'] > annual_avg])

    monthly_vol = prices.groupby(prices.index.month)['returns'].std()
    most_volatile_month = monthly_vol.idxmax()
    max_vol_value = monthly_vol.max()

    #Format
    print(f"\n── {ticker} · Financial SQL Analysis ───────")
    print("\nTop 5 High Volume Days:")
    print(top_volume[['volume']].map(lambda x: f"{x:,.0f}"))
    print("\nTop 5 Best Return Days:")
    print(top_returns[['returns']].map(lambda x: f"{x:.2%}"))
    
    print("\nMonthly Average Close Price:")
    print(monthly_avg.map(lambda x: f"${x:.2f}"))
    
    print(f"\nDays above annual average: {days_above_avg}")
    print(f"Most volatile month: {most_volatile_month} (volatility: {max_vol_value:.2%})")

    return prices

# Execution
analysis_data = financial_sql_analysis("AAPL", "2024-01-01", "2024-12-31")