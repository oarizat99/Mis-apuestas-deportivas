import streamlit as st
import requests
import pandas as pd

# --- CONFIGURACIÓN ---
731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799 
HOST = "free-api-live-football-data.p.rapidapi.com"

st.set_page_config(page_title="OscarBet VIP", layout="wide")

# --- FUNCION MAESTRA DE DATOS ---
def fetch_data(endpoint, params=None):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, params=params)
        return res.json()
    except:
        return None

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ OscarBet: Inteligencia Deportiva")

# --- MENÚ LATERAL ---
menu = st.sidebar.radio("SECCIONES", ["📅 Cartelera Hoy", "📊 Buscador & Stats", "🎯 Pronósticos Pro (Algoritmo)"])

# --- SECCIÓN 1: PARTIDOS DE HOY ---
if menu == "📅 Cartelera Hoy":
    st.subheader("Partidos Programados para Hoy")
    with st.spinner("Cargando partidos..."):
        data = fetch_data("/football-get-all-matches-by-date", {"date": "2026-04-13"}) # Cambia la fecha si es necesario
        if data and 'data' in data:
            for league in data['data'][:5]: # Mostramos las primeras 5 ligas top
                st.info(f"🏆 {league['league_name']}")
                for match in league['matches'][:8]:
                    col1, col2, col3 = st.columns([2,1,2])
                    col1.write(f"🏠 **{match['home_name']}**")
                    col2.write(f"🆚 {match['score'] if match['score'] else 'vs'}")
                    col3.write(f"🚀 **{match['away_name']}**")
                    st.divider()
        else:
            st.warning("No se encontraron partidos. Verifica si ya pasaron o intenta refrescar.")

# --- SECCIÓN 2: BUSCADOR & STATS ---
elif menu == "📊 Buscador & Stats":
    st.subheader("Análisis Técnico de Equipos")
    query = st.text_input("Escribe el nombre del equipo (Ej: Junior, Millonarios, Real Madrid):")
    if query:
        search = fetch_data("/football-get-team-search", {"search": query})
        if search and 'data' in search and len(search['data']) > 0:
            team = search['data'][0]
            st.success(f"Analizando a: {team['team_name']}")
            
            stats = fetch_data("/football-get-team-statistics", {"team_id": team['team_id']})
            if stats and 'data' in stats:
                s = stats['data']
                c1, c2, c3 = st.columns(3)
                c1.metric("Corners AVG", s.get('corners_avg', '0'))
                c2.metric("Tiros Puerta", s.get('shots_on_target_avg', '0'))
                c3.metric("Goles Favor", s.get('goals_scored_avg', '0'))
            else:
                st.write("Estadísticas no disponibles por el momento.")

# --- SECCIÓN 3: ALGORITMO DE APUESTAS ---
elif menu == "🎯 Pronósticos Pro (Algoritmo)":
    st.subheader("Recomendaciones de Alta Probabilidad")
    st.caption("Basado en el cruce de datos de Tiros, Goles y Posesión.")
    
    # Aquí simulamos el análisis del algoritmo con los datos de la API
    with st.container():
        st.markdown("### 🔥 Pick del Día")
        st.write("Analizando tendencias actuales...")
        
        # Ejemplo de lógica de recomendación
        col_a, col_b = st.columns(2)
        with col_a:
            st.success("✅ **ALTA PROBABILIDAD: GANA LOCAL**")
            st.write("**Razón:** Local con >60% posesión y >5 tiros a puerta en casa.")
        with col_b:
            st.warning("🎯 **PICK TIROS POR JUGADOR**")
            st.write("Busca al delantero centro: Promedio >1.5 tiros a puerta.")
            
        st.divider()
        st.error("⚠️ RECUERDA: Los datos son informativos. Apuesta con responsabilidad.")

st.sidebar.markdown("---")
st.sidebar.write(f"👤 Usuario: **Oscar Ariza**")
st.sidebar.write("📍 Ciudad: **Barranquilla**")
