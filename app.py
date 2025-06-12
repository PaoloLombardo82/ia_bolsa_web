# Ajustes para móvil
st.markdown("""
<style>
    @media screen and (max-width: 600px) {
        body { zoom: 0.8 }
        .stSelectbox, .stButton { width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)
# app.py

import streamlit as st
from utils import descargar_datos, calcular_indicadores
from model import entrenar_modelo
from news_nlp import buscar_noticias, analizar_sentimiento
from graficos import generar_grafico
import config

st.set_page_config(page_title="📈 IA Bolsa", layout="wide")
st.markdown('<style>body {zoom: 0.9;}</style>', unsafe_allow_html=True)
st.title("📱 Analizador Bursátil Móvil")

# Selector de activo
activo_seleccionado = st.selectbox("Elige un activo:", config.ALL_TICKERS)

if st.button("🔍 Analizar"):
    with st.spinner(f"Analizando {activo_seleccionado}..."):
        try:
            data, close_series = descargar_datos(activo_seleccionado)
            data = calcular_indicadores(data, close_series)
            modelo, muestra = entrenar_modelo(data)
            probabilidad = modelo.predict_proba(muestra)[0]

            # Análisis de noticias
            query = activo_seleccionado.replace("-USD", "").replace("-F", "")
            noticias = buscar_noticias(query)
            polaridad = analizar_sentimiento(noticias)

            # Ajuste con NLP
            ajuste_nlp = 0.1 * polaridad
            prob_alza = max(0.05, min(0.95, probabilidad[1] + ajuste_nlp))
            prob_baja = 1 - prob_alza

            rsi_actual = data['RSI'].iloc[-1]
            sma_20 = data['SMA_20'].iloc[-1]
            sma_50 = data['SMA_50'].iloc[-1]
            tendencia = '🟢 Alcista' if sma_20 > sma_50 else '🔴 Bajista'

            col1, col2 = st.columns(2)
            col1.metric("Probabilidad de alza", f"{prob_alza:.2%}")
            col2.metric("Probabilidad de baja", f"{prob_baja:.2%}")

            st.markdown(f"🔹 RSI: {rsi_actual:.2f} → {'🟢 Sobrevendido' if rsi_actual < 30 else '🔴 Sobrecompra' if rsi_actual > 70 else '🟡 Normal'}")
            st.markdown(f"🔹 Tendencia técnica: {tendencia}")
            st.markdown(f"🔹 Sentimiento de noticias: {'🟢 Positivo' if polaridad > 0.2 else '🔴 Negativo' if polaridad < -0.2 else '🟡 Neutro'}")

            # Gráfico interactivo
            from plotly.subplots import make_subplots
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                                subplot_titles=("Precio y Medias Móviles", "RSI"))

            fig.add_trace(go.Scatter(x=data.index, y=data['close'], name='Precio'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50'), row=1, col=1)

            fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'), row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)

            fig.update_layout(height=600, showlegend=True, title_text=f"{activo_seleccionado} - Análisis técnico")
            st.plotly_chart(fig, use_container_width=True)

            # Noticias recientes
            st.subheader("📰 Últimas noticias")
            for n in noticias[:5]:
                st.markdown(f"- {n}")

        except Exception as e:
            st.error(f"❌ Error analizando {activo_seleccionado}: {e}")