import streamlit as st
import requests

# --- CONFIGURACIÓN ---
# ASEGÚRATE DE QUE TU LLAVE ESTÉ AQUÍ DENTRO SIN ESPACIOS
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" # <--- PEGA TU LLAVE AQUÍ
HOST = "free-api-live-football-data.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Analysis", layout="centered")
st.title("⚽ OscarBet: Central de Análisis")

# --- FUNCIÓN DE PRUEBA ---
def probar_conexion():
    url = f"https://{HOST}/football-get-all-leagues"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": HOST
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 403:
            return False, "Error 403: Llave inválida o plan no activado."
        elif response.status_code == 429:
            return False, "Error 429: Te gastaste los créditos del mes."
        else:
            return False, f"Error {response.status_code}"
    except Exception as e:
        return False, str(e)

# --- INTERFAZ ---
st.sidebar.header("Menú")
if st.sidebar.button("🔌 Probar Conexión Real"):
    st.write("Conectando con el servidor de datos...")
    exito, resultado = probar_conexion()
    
    if exito:
        st.success("✅ ¡CONECTADO EXITOSAMENTE!")
        # Mostramos las primeras 5 ligas para confirmar
        ligas = resultado.get('data', [])
        if ligas:
            st.write("Ligas encontradas:")
            for liga in ligas[:5]:
                st.write(f"🏆 {liga.get('league_name')}")
    else:
        st.error(f"❌ FALLO DE CONEXIÓN: {resultado}")
        st.info("Revisa si tu plan en RapidAPI está activo o si la llave está bien escrita.")

st.divider()
st.write("Usa el botón de la izquierda para verificar la señal.")
