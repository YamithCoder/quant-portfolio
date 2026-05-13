import yfinance as yf
import pandas as pd

def ohlc_analysis(ticker, start, end):
    # 1. DOWNLOAD & QUALITY CHECK
    raw_data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    
    print(f"\n[DATA QUALITY REPORT: {ticker}]")
    print(f"Shape: {raw_data.shape} | Duplicates: {raw_data.duplicated().sum()}")
    print(f"Data Types:\n{raw_data.dtypes}")
    
    # 2. CLEANING & DAILY RETURNS (Pre-calculation)
    # Importante: ffill() antes de cualquier cálculo para evitar sesgos por huecos
    df = raw_data.copy().ffill()
    df['daily_return'] = df['Close'].pct_change()
    

    monthly_ohlc = df['Close'].resample('ME').ohlc()    
    monthly_vol = df['daily_return'].resample('ME').std()
    # 3. Combinamos ambos 
    monthly = pd.concat([monthly_ohlc, monthly_vol], axis=1)
    # Renombramos columnas y calculamos el Retorno Mensual
    monthly.columns = ['Open', 'High', 'Low', 'Close', 'Volatility']
    monthly['Return'] = (monthly['Close'] / monthly['Open']) - 1
    
    # 4. QUARTERLY RETURNS (Retorno por trimestre)
    # Usamos la fórmula compuesta: producto de (1 + retornos diarios) - 1
    quarterly_returns = df['daily_return'].resample('QE').apply(lambda x: (1 + x).prod() - 1)
    
    # 5. OUTPUTS FORMATEADOS
    print(f"\n── {ticker} · Monthly Summary 2024 ──────────")
    monthly_display = monthly.copy()
    monthly_display.index = monthly_display.index.month # Solo el número del mes
    
    format_dict = {
        'Open': '${:.2f}', 'High': '${:.2f}', 'Low': '${:.2f}', 
        'Close': '${:.2f}', 'Return': '{:.2%}', 'Volatility': '{:.2%}'
    }
    for col, fmt in format_dict.items():
        monthly_display[col] = monthly_display[col].map(lambda x, f=fmt: f.format(x))
    print(monthly_display)
    
    # 6. IDENTIFICACIÓN DE EXTREMOS
    best_m = monthly['Return'].idxmax().month
    best_m_val = monthly['Return'].max()
    
    vol_m = monthly['Volatility'].idxmax().month
    vol_m_val = monthly['Volatility'].max()
    
    print(f"\nBest month:       {best_m} (return: {best_m_val:.2%})")
    print(f"Most volatile:    {vol_m} (volatility: {vol_m_val:.2%})")
    
    # 7. QUARTERLY SUMMARY
    print("\n── Quarterly Returns ────────────────────")
    quarterly_display = quarterly_returns.copy()
    quarterly_display.index = [f"Q{i}" for i in range(1, len(quarterly_display)+1)]
    print(quarterly_display.map(lambda x: f"{x:.2%}"))

    return monthly

# Ejecución
nvda_monthly = ohlc_analysis("NVDA", "2024-01-01", "2024-12-31")