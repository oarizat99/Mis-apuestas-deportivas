import streamlit as st
import requests
import pandas as pd

# --- CONFIGURACIÓN ---
# Pega aquí tu llave que empieza por 731523...
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" 
HOST = "free-api-live-football-data.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Analysis", layout="centered")

st.title("⚽ OscarBet: Central de Análisis")
st.subheader("Datos Pro: Tiros, Corners y Paradas")

# --- FUNCIÓN PARA PEDIR DATOS ---
def traer_datos(endpoint):
    url = f"https://{HOST}{endpoint}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": HOST
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        return None

# --- INTERFAZ ---
st.sidebar.header("Panel de Control")
menu = st.sidebar.selectbox("Selecciona una opción", ["Próximos Partidos", "Ligas Disponibles", "Calculadora de Picks"])

if menu == "Ligas Disponibles":
    st.write("Consultando ligas...")
    res = traer_datos("/football-get-all-leagues")
    if res and 'data' in res:
        st.write(res['data'])

elif menu == "Próximos Partidos":
    st.write("Aquí verás los partidos analizados con tu nueva API.")
    # Nota: Esta API usa endpoints específicos para ver los partidos de hoy
    st.info("Pulsa el botón en la barra lateral para actualizar datos.")

elif menu == "Calculadora de Picks":
    st.warning("🎯 Recomendación basada en Stats")
    st.write("Calculando probabilidades de Over/Under y Corners...")
    # Aquí puedes añadir tus fórmulas de apuesta
