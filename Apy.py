import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" 
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet VIP", layout="centered")
st.title("⚽ OscarBet: Central Metrx")

def fetch(endpoint):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json()
    except:
        return None

st.subheader("🚀 Buscando Señal de Partidos...")

# LISTA DE RUTAS POSIBLES SEGÚN TU CAPTURA
rutas_a_probar = ["/match-metrics", "/match_metrics", "/matches", "/metrics", "/performance"]
data_final = None
ruta_exitosa = ""

for r in rutas_a_probar:
    with st.spinner(f"Probando ruta: {r}"):
        res = fetch(r)
        # Si la respuesta tiene 'success': True, encontramos la mina de oro
        if res and isinstance(res, dict) and res.get('success') == True:
            data_final = res
            ruta_exitosa = r
            break

if data_final:
    st.success(f"✅ ¡Conectado con éxito vía {ruta_exitosa}!")
    # Navegamos en la estructura que vimos en tus fotos: result -> match
    partidos = data_final.get('result', [])
    if partidos:
        for item in partidos:
            m = item.get('match', {})
            home = m.get('homeTeam', {}).get('name', 'Equipo A')
            away = m.get('awayTeam', {}).get('name', 'Equipo B')
            st.write(f"🏟️ **{home}** vs **{away}**")
            st.caption(f"ID: {m.get('id')} | Inicio: {m.get('start')}")
            st.divider()
    else:
        st.warning("Se conectó, pero no hay partidos en la lista ahora.")
else:
    st.error("❌ Ninguna ruta funcionó.")
    st.info("Oscar, verifica en RapidAPI que la URL del endpoint sea exactamente la misma que estamos probando.")
    # Mostramos el último error para ver qué dijo la API
    st.write("Último intento fallido:")
    st.json(fetch("/match-metrics"))
