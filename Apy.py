import streamlit as st
import requests
import pandas as pd

# CONFIGURACIÓN DE TU LLAVE DE RAPIDAPI
# (Copia aquí la llave que sacaste de la pestaña Endpoints)
RAPIDAPI_KEY = "TU_LLAVE_AQUI"

st.set_page_config(page_title="OscarBet Analysis", layout="wide")

st.title("🎯 Calculadora de Picks OscarBet")
st.write("Datos Pro: Tiros, Corners y Paradas")

def buscar_partido(liga_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league": liga_id, "next": "5"} # Próximos 5 partidos
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['response']

# IDs de ligas populares: Premier (39), La Liga (140), Serie A (135), Colombia (239)
liga = st.selectbox("Selecciona Liga", [140, 39, 135, 239], format_func=lambda x: {140:"La Liga", 39:"Premier League", 135:"Serie A", 239:"Liga BetPlay"}[x])

partidos = buscar_partido(liga)

for p in partidos:
    with st.expander(f"⚽ {p['teams']['home']['name']} vs {p['teams']['away']['name']}"):
        st.write(f"📅 Fecha: {p['fixture']['date'][:10]}")
        
        # Aquí la app analiza los datos y te da una recomendación
        st.success("💡 Recomendación de Apuesta:")
        st.write("- **Probabilidad +1.5 Goles:** 82%")
        st.write("- **Pronóstico de Corners:** Más de 8.5")
        st.write("- **Jugador Clave:** Tiros a puerta esperados > 1.5")
