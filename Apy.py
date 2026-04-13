import streamlit as st
import requests
from datetime import datetime
import pytz

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" 
HOST = "free-api-live-football-data.p.rapidapi.com"

st.set_page_config(page_title="OscarBet VIP", layout="centered")

# --- FUNCIONES DE APOYO ---
def get_today_colombia():
    tz = pytz.timezone('America/Bogota')
    return datetime.now(tz).strftime('%Y-%m-%d')

def fetch_data(endpoint, params=None):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=12)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Error del servidor: {res.status_code}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# --- INTERFAZ PRINCIPAL ---
st.title("⚽ OscarBet: Inteligencia Deportiva")
st.sidebar.header(f"📍 Barranquilla\n📅 {get_today_colombia()}")

menu = st.sidebar.radio("SECCIONES", ["🔍 Buscador & Stats", "📅 Cartelera Hoy", "🎯 Pronósticos Pro"])

# --- SECCIÓN: BUSCADOR ---
if menu == "🔍 Buscador & Stats":
    st.subheader("Análisis Técnico de Equipos")
    query = st.text_input("Escribe el equipo (ej: Junior, Real Madrid):")
    btn_buscar = st.button("🔍 Analizar Equipo")
    
    if query or btn_buscar:
        with st.spinner(f"Buscando a {query}..."):
            search = fetch_data("/football-get-team-search", {"search": query})
            if search and 'data' in search and len(search['data']) > 0:
                team = search['data'][0]
                st.success(f"✅ Equipo: {team['team_name']}")
                
                # Estadísticas
                stats = fetch_data("/football-get-team-statistics", {"team_id": team['team_id']})
                if stats and 'data' in stats:
                    s = stats['data']
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Corners AVG", s.get('corners_avg', 'N/D'))
                    col2.metric("Tiros Puerta", s.get('shots_on_target_avg', 'N/D'))
                    col3.metric("Goles Favor", s.get('goals_scored_avg', 'N/D'))
                    
                    # Lógica de apuesta
                    st.divider()
                    st.markdown("### 💡 Recomendación de Apuesta")
                    c_avg = float(s.get('corners_avg', 0))
                    g_avg = float(s.get('goals_scored_avg', 0))
                    
                    if c_avg > 5.2:
                        st.success(f"🔥 **ALTA PROBABILIDAD:** Over 8.5 Corners (Promedio: {c_avg})")
                    if g_avg > 1.5:
                        st.success(f"⚽ **ALTA PROBABILIDAD:** Over 1.5 Goles Equipo")
                else:
                    st.info("Estadísticas detalladas no disponibles para este equipo.")
            else:
                st.warning("No se encontró el equipo. Revisa la ortografía.")

# --- SECCIÓN: CARTELERA ---
elif menu == "📅 Cartelera Hoy":
    fecha = get_today_colombia()
    st.subheader(f"Partidos para Hoy: {fecha}")
    data = fetch_data("/football-get-all-matches-by-date", {"date": fecha})
    
    if data and 'data' in data:
        for league in data['data'][:8]:
            with st.expander(f"🏆 {league['league_name']}"):
                for match in league['matches']:
                    st.write(f"🏠 {match['home_name']} **{match.get('score', 'vs')}** {match['away_name']} 🚀")
    else:
        st.write("No hay partidos registrados para hoy o la API alcanzó su límite.")

# --- SECCIÓN: PRONÓSTICOS ---
elif menu == "🎯 Pronósticos Pro":
    st.subheader("Picks del Algoritmo")
    st.info("Analizando tendencias de tiros a puerta y posesión...")
    st.write("1. **Local gana o empata:** Si tiros a puerta > 4.5")
    st.write("2. **Ambos marcan:** Basado en promedio de goles > 1.2 en ambos equipos.")
