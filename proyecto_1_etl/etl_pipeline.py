# ── PROYECTO 1 · ETL Pipeline ─────────────────────────
# Descarga, limpieza y validación de datos financieros reales
# Fuente: Yahoo Finance · Autor: [tu nombre]

import yfinance as yf
import pandas as pd

def pipeline_etl(ticker, start, end):
    #Extracción
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    #Inspeccion
    print(f"── Control de Calidad · {ticker} ───────────")
    print(f"Filas totales: {df.shape[0]}")
    print(f"Valores nulos: {df.isnull().sum().sum()}")
    print(f"Filas duplicadas: {df.duplicated().sum()}")
    print("-" * 40)

    #Limpieza
    df_limpio = df[["Close", "Volume"]].copy()
    df_limpio = df_limpio.dropna()

    #Calculos
    df_limpio["retorno_diario"] = df_limpio["Close"].pct_change()
    df_limpio["retorno_acumulado"] =(1 + df_limpio["retorno_diario"]).cumprod() - 1

    #Deteccion de errores
    outliers = df_limpio[df_limpio["retorno_diario"].abs() > 0.15]
    if len(outliers) > 0:
        print(f"¡Alerta! Se detectaron {len(outliers)} outliers")

    return df_limpio

df_final = pipeline_etl("AAPL", "2024-01-01", "2024-12-31")
print(df_final.head())

