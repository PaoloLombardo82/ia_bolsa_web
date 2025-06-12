# run_daily.py

import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import telegram
from config import ACTIVOS_ANALIZAR

# Ruta del archivo log
LOG_FILE = r"C:\Users\Pablo\Desktop\ia_bolsa_web\log.txt"

def log(mensaje):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{fecha_hora}] {mensaje}\n")

load_dotenv()

async def enviar_mensaje_telegram(mensaje):
    """Enviar mensaje por Telegram usando async"""
    try:
        async with telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN")) as bot:
            await bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=mensaje)
            log("✅ Notificación enviada por Telegram")
    except Exception as e:
        log(f"❌ Error al enviar mensaje por Telegram: {e}")

def descargar_datos(ticker, periodo="2y"):
    import yfinance as yf
    data = yf.download(ticker, period=periodo, auto_adjust=True)[['Close']].dropna()
    data.columns = ['close']
    close_series = data['close'].squeeze()
    return data, close_series

def calcular_indicadores(data, close_series):
    import ta
    data['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
    data['MACD'] = ta.trend.MACD(close_series).macd()
    data['SMA_20'] = close_series.rolling(window=20).mean()
    data['SMA_50'] = close_series.rolling(window=50).mean()
    return data.dropna()

def entrenar_modelo(data):
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np

    features = ['RSI', 'MACD', 'SMA_20', 'SMA_50']
    X = data[features]
    y = np.where(data['close'].shift(-1) > data['close'], 1, 0)
    X = X[:-1]
    y = y[:-1]

    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X, y)

    return modelo, X.iloc[-1].values.reshape(1, -1)

def ejecutar_prediccion(ticker):
    """Ejecuta predicción para un activo"""
    try:
        print(f"🔍 Analizando: {ticker}")
        log(f"🔍 Analizando: {ticker}")

        data, close_series = descargar_datos(ticker)
        data = calcular_indicadores(data, close_series)
        modelo, muestra = entrenar_modelo(data)
        probabilidad = modelo.predict_proba(muestra)[0]

        rsi_actual = data['RSI'].iloc[-1]
        sma_20 = data['SMA_20'].iloc[-1]
        sma_50 = data['SMA_50'].iloc[-1]

        # Buscar noticias relevantes
        from news_nlp import buscar_noticias, analizar_sentimiento
        query = ticker.replace("-USD", "").replace("-F", "")
        noticias = buscar_noticias(query)
        polaridad = analizar_sentimiento(noticias)

        # Calcular probabilidad ajustada con NLP
        ajuste_nlp = 0.1 * polaridad
        probabilidad_alza = max(0.05, min(0.95, probabilidad[1] + ajuste_nlp))
        probabilidad_baja = 1 - probabilidad_alza

        mensaje = f"🔔 SEÑAL DE TRADING MANUAL\n"
        mensaje += f"📈 ACTIVO: {ticker}\n"
        mensaje += f"🔹 Probabilidad de alza: {probabilidad_alza:.2%}\n"
        mensaje += f"🔹 Probabilidad de baja: {probabilidad_baja:.2%}\n"
        mensaje += f"🔹 RSI: {rsi_actual:.2f} ({'🟢 Sobrevendido' if rsi_actual < 30 else '🔴 Sobrecompra' if rsi_actual > 70 else '🟡 Normal'})\n"
        mensaje += f"🔹 Tendencia técnica: {'🟢 Alcista' if sma_20 > sma_50 else '🔴 Bajista'}\n"
        mensaje += f"🔹 Sentimiento de noticias: {'🟢 Positivo' if polaridad > 0.2 else '🔴 Negativo' if polaridad < -0.2 else '🟡 Neutro'}\n"

        mensaje += "\n📰 Últimas noticias:\n"
        for n in noticias[:3]:
            mensaje += f"- {n}\n"

        mensaje += f"\n🗓️ Hora: {datetime.now().strftime('%H:%M')}"

        return mensaje
    except Exception as e:
        print(f"⚠️ Error procesando {ticker}: {e}")
        log(f"⚠️ Error procesando {ticker}: {e}")
        return ""

def main():
    """Función principal que ejecuta el análisis diario"""
    print("🔄 Iniciando análisis diario...")
    log("🔄 Iniciando análisis diario...")

    UMBRAL_PROBABILIDAD = 0.70

    for ticker in ACTIVOS_ANALIZAR:
        mensaje = ejecutar_prediccion(ticker)

        if mensaje:
            asyncio.run(enviar_mensaje_telegram(mensaje))
        else:
            print(f"⚠️ No se pudo generar predicción para {ticker}")

if __name__ == "__main__":
    print("⏰ Iniciando predicción diaria...")
    print("📍 Carpeta actual:", os.getcwd())
    main()