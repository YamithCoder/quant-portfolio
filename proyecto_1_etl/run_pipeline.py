import pandas as pd
import yfinance as yf
import os 

    #Extract information
def run_etl_pipeline(tickers, start, end):
    raw_data = yf.download(tickers, start=start, end=end, auto_adjust=True)
    #Calculate closing prices
    prices = raw_data['Close'].ffill()
    
    #Calculate daily returns
    returns = prices.pct_change()
    
    #Calculation of Cumulative Returns:
    cumulative_returns = (1 + returns).cumprod()
    
    #Outlier Detection: Returns > 15% (Absolute value for crashes or pumps)
    outliers_mask = returns.abs() > 0.15
    outliers_count = outliers_mask.sum().sum()

    #Build Final Dataset (Combining prices and returns)
    df_final = pd.concat([
        prices.add_prefix('close_'),
        returns.add_prefix('return_')
    ], axis=1).dropna()

    #Export to multiple formats
    output_path = "data/clean"
    os.makedirs(output_path, exist_ok=True)
    base_name = f"{output_path}/portafolio_2024"

    df_final.to_csv(f"{base_name}.csv", index=True)
    df_final.to_parquet(f"{base_name}.parquet", index=True)
    df_final.to_json(f"{base_name}.json", orient="records", date_format="iso")

    #Final report
    csv_size = os.path.getsize(f"{base_name}.csv")
    parquet_size = os.path.getsize(f"{base_name}.parquet")
    json_size = os.path.getsize(f"{base_name}.json")

    print("── ETL Pipeline Complete ─────────────────")
    print(f"Tickers:      {' · '.join(tickers)}")
    print(f"Date range:   {df_final.index.date.min()} → {df_final.index.date.max()}")
    print(f"Shape:        {df_final.shape}")
    print(f"Nulls:        {df_final.isnull().sum().sum()}")
    print(f"Outliers:     {outliers_count} days detected")
    print("── Files Exported ────────────────────────")
    print(f"CSV:          {csv_size:,} bytes")
    print(f"Parquet:      {parquet_size:,} bytes")
    print(f"JSON:         {json_size:,} bytes")
    print("Pipeline completed successfully ✓")
    
    return df_final

# Execute the final project
tickers_list = ['AAPL', 'MSFT', 'NVDA', 'BTC-USD']
final_data = run_etl_pipeline(tickers_list, '2024-01-01', '2024-12-31')



