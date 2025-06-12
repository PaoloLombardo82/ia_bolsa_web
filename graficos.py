# graficos.py

import plotly.graph_objs as go
from datetime import datetime
import os

def generar_grafico(data, ticker):
    """Genera un gráfico interactivo del precio y RSI"""

    fig = go.Figure()

    # Precio Close
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], name='Precio'))
    fig.update_layout(title=f"Precio y Medias Móviles de {ticker}", xaxis_title="Fecha", yaxis_title="Precio USD")

    # RSI
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.update_layout(title="RSI (Índice de Fuerza Relativa)", yaxis_range=[0, 100])

    # Guardar como HTML
    carpeta_salida = r"C:\Users\Pablo\Desktop\ia_bolsa_web\graficos_html"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    ruta_archivo = os.path.join(carpeta_salida, f"{ticker}_{datetime.now().strftime('%Y%m%d_%H%M')}.html")
    fig.write_html(ruta_archivo)
    
    print(f"📊 Gráfico guardado: {ruta_archivo}")
    return ruta_archivo