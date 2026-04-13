import streamlit as st
impor
# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" # <--- No olvides poner tu llave de nuevo
HOST = "free-api-live-football-data.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Pro", layout="centered")
st.title("⚽ OscarBet: Análisis Elite")

def traer_datos(endpoint, params=None):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    res = requests.get(url, headers=headers, params=params)
    return res.json()

# --- BARRA LATERAL ---
st.sidebar.header("Menú Pro")
modo = st.sidebar.radio("Ir a:", ["🔥 Partidos en Vivo", "📅 Próximos Partidos", "📈 Estadísticas Pro"])

if modo == "🔥 Partidos en Vivo":
    st.subheader("Marcadores y Stats en Tiempo Real")
    data = traer_datos("/football-get-all-live-connections")
    if data and 'data' in data:
        for match in data['data'][:10]: # Muestra los primeros 10
            with st.expander(f"{match['home_name']} vs {match['away_name']}"):
                col1, col2 = st.columns(2)
                col1.metric("Marcador", f"{match['score']}")
                col2.write(f"**Corners:** {match.get('corners', 'N/A')}")
                st.write(f"**Ataques Peligrosos:** {match.get('dangerous_attacks', 'N/A')}")
                st.progress(0.75) # Barra de intensidad
    else:
        st.info("No hay partidos en vivo en este momento.")

elif modo == "📈 Estadísticas Pro":
    st.subheader("Análisis para Parlays")
    st.write("Selecciona un equipo para ver su promedio de Tiros y Paradas.")
    # Aquí puedes usar /football-get-team-statistics cuando tengas el ID del equipo
    st.warning("Consejo: Revisa los equipos con >5 corners en los últimos 3 partidos.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("🟢 Conexión: **ÓPTIMA**")
