import yfinance as yf
import pandas as pd

def statistical_profile(ticker, returns_series):
    # We use .describe() for basic stats and specific methods for the rest
    mean_val = returns_series.mean()
    median_val = returns_series.median()
    std_val = returns_series.std()
    var_val = returns_series.var()
    range_val = returns_series.max() - returns_series.min()
    
    skew_val = returns_series.skew()
    kurt_val = returns_series.kurt()
    
    best_day = returns_series.max()
    worst_day = returns_series.min()
    p95 = returns_series.quantile(0.95)
    p05 = returns_series.quantile(0.05)
    
    # --- Professional Report Printing ---
    print(f"── {ticker} · Statistical Profile ───────────")
    print(f"Period:       {returns_series.index.date.min()} → {returns_series.index.date.max()}")
    print(f"Trading days: {len(returns_series)}")
    
    print(f"Central tendency:")
    print(f"  Mean return:    {mean_val:.4%}")
    print(f"  Median return:  {median_val:.4%}")
    
    print(f"Dispersion:")
    print(f"  Std deviation:  {std_val:.4%}")
    print(f"  Variance:       {var_val:.6%}")
    print(f"  Range:          {range_val:.4%}")
    
    print(f"Shape:")
    print(f"  Skewness:       {skew_val:.4f}")
    print(f"  Kurtosis:       {kurt_val:.4f}")
    
    print(f"Extremes:")
    print(f"  Best day:       {best_day:.4%}")
    print(f"  Worst day:      {worst_day:.4%}")
    print(f"  Best 5% days:   {p95:.4%}")
    print(f"  Worst 5% days:  {p05:.4%}")
    print("-" * 40)

# 1. Download data
tickers = ['AAPL', 'NVDA', 'BTC-USD', 'GLD']
data = yf.download(tickers, start="2024-01-01", end="2024-12-31", auto_adjust=True)['Close']

# 2. Calculate daily returns (Vectorized)
all_returns = data.ffill().pct_change().dropna()

# 3. Apply the profile to specific assets
# You can call them manually to avoid for loops in the print process
statistical_profile("AAPL", all_returns["AAPL"])
statistical_profile("NVDA", all_returns["NVDA"])
statistical_profile("BTC-USD", all_returns["BTC-USD"])
statistical_profile("GLD", all_returns["GLD"])