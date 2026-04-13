import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" 
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Pro", layout="centered")
st.title("⚽ OscarBet: Central de Datos")

def fetch_data(endpoint, params=None):
    url = f"https://{HOST}{endpoint}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": HOST
    }
    try:
        # Quitamos los 'params' fijos para que no bloquee la búsqueda
        res = requests.get(url, headers=headers, timeout=15)
        return res.json()
    except Exception as e:
        return {"error_local": str(e)}

st.subheader("Partidos Disponibles")

# Probamos con el endpoint base que suele ser el más estable
data = fetch_data("/matches")

if data:
    # Si la API devuelve un mensaje de error, lo mostramos para saber
    if "message" in data and "does not exist" in data["message"]:
        st.error("La API dice que esa sección no existe. Probando ruta alternativa...")
        # INTENTO PLAN B: Ruta que vimos en tu captura de pantalla
        data = fetch_data("/match-metrics") 

    # BUSCAR LOS PARTIDOS EN EL JSON
    # Metrx suele guardarlos en 'result' o mandarlos como lista
    partidos = []
    if isinstance(data, dict):
        partidos = data.get('result', data.get('data', []))
    elif isinstance(data, list):
        partidos = data

    if partidos:
        st.success(f"¡Conectado! Mostrando {len(partidos)} partidos.")
        for item in partidos:
            # Estructura según tu captura del 200 OK
            m = item.get('match', item) 
            match_id = m.get('id', 'Sin ID')
            inicio = m.get('start', 'Ver horario')
            
            with st.expander(f"🏟️ Partido ID: {match_id}"):
                st.write(f"**Inicio:** {inicio}")
                st.write("**Estado:** Programado")
                st.button("Analizar Corners", key=match_id)
    else:
        st.warning("No hay partidos en la lista ahora mismo.")
        with st.expander("🛠️ Ver respuesta de la API"):
            st.write(data)
else:
    st.error("No se recibió respuesta. Revisa tu Key.")
