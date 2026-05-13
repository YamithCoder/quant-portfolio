import yfinance as yf
import pandas as pd

def build_portfolio_dataset(tickers, start, end):
    raw_data = yf.download(tickers, start=start, end=end, auto_adjust=True)
    
    prices = raw_data['Close']
    returns = prices.ffill().pct_change().dropna()
    
    prices_renamed = prices.add_prefix('close_')
    returns_renamed = returns.add_prefix('return_')
    
    df_final = pd.concat([prices_renamed, returns_renamed], axis=1)
    df_final = df_final.dropna()
    
    # --- Reporte de Calidad ---
    print("── Portfolio Dataset Quality Report ─────")
    print(f"Shape:        {df_final.shape}")
    print(f"Nulls total:  {df_final.isnull().sum().sum()}")
    print(f"Date range:   {df_final.index.date.min()} → {df_final.index.date.max()}")
    print("-" * 40)
    
    # Imprimir las primeras 3 filas
    print(df_final.head(3))
    
    return df_final

# Ejecución del reto
tickers_list = ['AAPL', 'MSFT', 'NVDA', 'BTC-USD']
mi_df_final = build_portfolio_dataset(tickers_list, '2024-01-01', '2024-12-31')