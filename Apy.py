import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "https://www.google.com/search?q=731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799&ie=UTF-8&oe=UTF-8&hl=es-co&client=safari" 
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Metrx", layout="centered")

def fetch_metrx(endpoint, params=None):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        return res.json()
    except:
        return None

st.title("⚽ OscarBet: Metrx Edition")

menu = st.sidebar.radio("MENÚ", ["📅 Próximos Partidos", "🔍 Análisis de Ligas"])

if menu == "📅 Próximos Partidos":
    st.subheader("Partidos en las próximas 8 horas")
    # Esta API es genial para ver lo que viene pronto
    data = fetch_metrx("/matches/upcoming")
    
    if data and 'data' in data:
        for match in data['data']:
            with st.expander(f"🕒 {match.get('time', 'S/H')} | {match['home_team']} vs {match['away_team']}"):
                st.write(f"**Competición:** {match.get('competition', 'N/A')}")
                st.write(f"**Índice de Rendimiento:** {match.get('performance_index', 'Buscando...')}")
                st.button("Ver Probabilidades", key=match.get('id'))
    else:
        st.warning("No hay partidos programados para las próximas horas o revisa tu conexión.")

elif menu == "🔍 Análisis de Ligas":
    st.subheader("Top 100 Competiciones")
    # Aprovechamos el feature de 'Competitions 100 strongest'
    ligas = fetch_metrx("/competitions")
    if ligas and 'data' in ligas:
        for liga in ligas['data'][:20]:
            st.write(f"🏆 {liga['name']} ({liga['country']})")
