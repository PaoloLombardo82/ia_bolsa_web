# news_nlp.py

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime

def buscar_noticias(query):
    """Buscar noticias en Google News"""
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

    try:
        response = requests.get(url, headers=headers)
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.text)

        noticias = []
        for item in root.findall('.//item')[:5]:
            title = item.find('title').text
            noticias.append(title)

        return noticias
    except Exception as e:
        print(f"❌ Error al buscar noticias: {e}")
        return []

def analizar_sentimiento(noticias):
    """Analiza el sentimiento promedio de las noticias"""
    total_polaridad = 0
    conteo = 0

    for noticia in noticias:
        blob = TextBlob(noticia)
        polaridad = blob.sentiment.polarity
        total_polaridad += polaridad
        conteo += 1

    return total_polaridad / conteo if conteo > 0 else 0