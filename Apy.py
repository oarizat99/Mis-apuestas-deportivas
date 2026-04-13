import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "https://www.google.com/search?q=731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799&ie=UTF-8&oe=UTF-8&hl=es-co&client=safari#sbfbu=1&pi=731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" 
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Final", layout="centered")
st.title("⚽ OscarBet: Central de Datos")

def fetch_metrx(endpoint):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

menu = st.sidebar.radio("MENÚ", ["📅 Partidos de Hoy", "🏆 Ver Ligas"])

if menu == "📅 Partidos de Hoy":
    st.subheader("Buscando partidos...")
    raw_data = fetch_metrx("/matches/upcoming")
    
    # ESTO ES LO QUE NOS DIRÁ LA VERDAD
    if raw_data:
        # Intento de mostrar datos ordenados
        if isinstance(raw_data, dict) and 'data' in raw_data:
            partidos = raw_data['data']
            if len(partidos) > 0:
                for m in partidos:
                    st.write(f"✅ {m.get('home_team', 'Equipo A')} vs {m.get('away_team', 'Equipo B')}")
            else:
                st.warning("La API conectó, pero dice que no hay partidos en las próximas 8 horas.")
        
        # SI NO MUESTRA NADA ARRIBA, ESTO NOS MUESTRA EL ERROR REAL
        st.divider()
        with st.expander("🛠️ DEBUG: Ver respuesta real de la API"):
            st.write(raw_data)
    else:
        st.error("No se recibió ninguna respuesta de la API.")

elif menu == "🏆 Ver Ligas":
    ligas_raw = fetch_metrx("/competitions")
    st.write("### Respuesta de Ligas:")
    st.write(ligas_raw)
