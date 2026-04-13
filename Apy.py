import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" 
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Pro", layout="centered")
st.title("⚽ OscarBet: Central de Datos")

def fetch_data(endpoint):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        return res.json()
    except Exception as e:
        return {"error_local": str(e)}

st.subheader("Buscando Datos Reales...")

# Pedimos los datos
data = fetch_data("/matches/upcoming")

# MOSTRAR TODO SIN FILTROS
if data:
    # 1. Intentamos buscar la lista de partidos
    # Metrx usa 'result' o a veces manda la lista directo
    partidos = data.get('result', []) if isinstance(data, dict) else []
    
    if partidos:
        st.success(f"¡Se encontraron {len(partidos)} partidos!")
        for item in partidos:
            m = item.get('match', {})
            st.write(f"🆔 **ID Partido:** {m.get('id')}")
            st.write(f"⏰ **Inicio:** {m.get('start')}")
            st.divider()
    else:
        st.warning("La conexión funciona, pero la lista de partidos llegó vacía.")
        st.write("Esto es lo que mandó la API exactamente:")
        st.json(data) # Esto nos mostrará el JSON crudo en la pantalla
else:
    st.error("No se recibió nada de la API. Revisa la llave en GitHub.")

st.sidebar.write(f"Estado: Conectado a {HOST}")
