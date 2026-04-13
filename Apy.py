import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "https://www.google.com/search?q=731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799&ie=UTF-8&oe=UTF-8&hl=es-co&client=safari" # <--- ¡Pon tu llave de Metrx aquí!
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Pro", layout="centered")
st.title("⚽ OscarBet: Metrx Edition")

def fetch_metrx(endpoint):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json()
    except:
        return None

menu = st.sidebar.radio("MENÚ", ["🏆 Ligas Top", "📅 Próximos Partidos", "🎯 Mi Algoritmo"])

if menu == "🏆 Ligas Top":
    st.subheader("Las mejores 100 Competiciones")
    with st.spinner("Cargando ranking..."):
        data = fetch_metrx("/competitions")
        if data and isinstance(data, list): # Metrx a veces envía una lista directa
            for liga in data[:20]:
                st.write(f"🏆 {liga.get('name', 'Liga')} - **{liga.get('country', 'Mundo')}**")
        elif data and 'data' in data:
            for liga in data['data'][:20]:
                st.write(f"🏆 {liga.get('name')} - **{liga.get('country')}**")
        else:
            st.info("💡 Haz clic en 'Próximos Partidos' para ver la acción de hoy.")

elif menu == "📅 Próximos Partidos":
    st.subheader("Acción para las próximas 8 horas")
    with st.spinner("Buscando partidos..."):
        data = fetch_metrx("/matches/upcoming")
        if data and 'data' in data:
            for m in data['data']:
                with st.expander(f"🕒 {m.get('time', 'S/H')} | {m['home_team']} vs {m['away_team']}"):
                    st.write(f"📊 **Performance Index:** {m.get('performance_index', 'N/A')}")
                    st.write(f"📌 **Liga:** {m.get('competition', 'N/A')}")
        else:
            st.warning("No hay partidos programados en el radar de 8 horas.")

elif menu == "🎯 Mi Algoritmo":
    st.subheader("Predicciones de Inteligencia")
    st.success("Recomendación: Busca partidos donde el Performance Index sea > 75 para el Local.")
