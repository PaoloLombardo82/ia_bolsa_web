# utils.py

import yfinance as yf
import pandas as pd
import ta

def descargar_datos(ticker, periodo="2y"):
    """Descarga datos históricos de un ticker"""
    data = yf.download(ticker, period=periodo, auto_adjust=True)[['Close']].dropna()
    data.columns = ['close']
    close_series = data['close'].squeeze()
    return data, close_series

def calcular_indicadores(data, close_series):
    """Calcula RSI, MACD, SMA_20, SMA_50"""
    data['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
    data['MACD'] = ta.trend.MACD(close_series).macd()
    data['SMA_20'] = close_series.rolling(window=20).mean()
    data['SMA_50'] = close_series.rolling(window=50).mean()
    return data.dropna()