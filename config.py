# config.py

ACTIVOS_ANALIZAR = {
    "Criptos": ["BTC-USD", "ETH-USD", "XRP-USD", "ADA-USD", "SOL-USD"],
    "Acciones": ["AAPL", "TSLA", "NVDA", "MSFT", "AMZN", "GOOGL", "META", "NFLX"],
    "Materias Primas": ["GC=F", "CL=F", "SI=F", "NG=F"],
    "ETFs": ["SPY", "QQQ", "VTI", "VOO"]
}

# Lista plana para usar internamente
ALL_TICKERS = [ticker for sublist in ACTIVOS_ANALIZAR.values() for ticker in sublist]