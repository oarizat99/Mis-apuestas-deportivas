import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "https://www.google.com/search?q=731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799&client=safari&hs=CI2U&sca_esv=f0f46d557053f7c4&hl=es-co&sxsrf=ANbL-n75lhcMAYj5NVZ1KXm23rxBfK_pGg%3A1776110825048&ei=6UzdabHYApiNwbkP_sS3EQ&biw=414&bih=624&oq=731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799&gs_lp=EhNtb2JpbGUtZ3dzLXdpei1zZXJwIjI3MzE1MjNhYWI4bXNoMWVmZjQzNWUyNmQ0YjcycDE1OTY5Nmpzbjg4ZDhkNjliNjc5OUjLLlAAWABwAHgAkAECmAGZAaABkgOqAQMwLjO4AQPIAQCYAgCgAgCYAwCIBgGSBwCgB58BsgcAuAcAwgcAyAcAgAgA&sclient=mobile-gws-wiz-serp" 
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet Pro", layout="centered")
st.title("⚽ OscarBet: Central de Datos")

def fetch_data(endpoint, params=None):
    url = f"https://{HOST}{endpoint}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        return res.json()
    except:
        return None

menu = st.sidebar.radio("MENÚ", ["📅 Partidos Metrx", "🔍 Info Cruda"])

if menu == "📅 Partidos Metrx":
    st.subheader("Análisis de Partidos")
    with st.spinner("Leyendo datos de Metrx..."):
        # Usamos el endpoint que te dio el '200 OK'
        data = fetch_data("/matches/upcoming")
        
        if data and data.get('success') == True:
            # Según tu imagen, los partidos están en 'result'
            lista_partidos = data.get('result', [])
            
            if lista_partidos:
                for item in lista_partidos:
                    m = item.get('match', {})
                    # Intentamos sacar los nombres de los equipos
                    # Si la API no da nombres aquí, usamos el ID
                    match_id = m.get('id', 'Sin ID')
                    st.success(f"Partido detectado ID: {match_id}")
                    
                    # Aquí añadiremos los tiros y corners cuando la API los suelte
                    col1, col2 = st.columns(2)
                    col1.write(f"**Inicio:** {m.get('start', 'N/A')}")
                    col2.button("Ver Stats", key=match_id)
            else:
                st.warning("No hay partidos en la lista de resultados ahora mismo.")
        else:
            st.error("La API conectó pero no devolvió resultados exitosos.")

elif menu == "🔍 Info Cruda":
    st.write("Esta sección es para ver si la API cambió algo:")
    raw = fetch_data("/matches/upcoming")
    st.json(raw)
