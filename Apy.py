import streamlit as st
import requests

# --- CONFIGURACIÓN ---
RAPIDAPI_KEY = "731523aab8msh1eff435e26d4b72p159696jsn88d8d69b6799" 
HOST = "metrx-factory.p.rapidapi.com"

st.set_page_config(page_title="OscarBet VIP", layout="centered")
st.title("⚽ OscarBet: Inteligencia Metrx")

def fetch_metrx():
    # Usamos el endpoint exacto que te dio el 200 OK
    url = f"https://{HOST}/match-metrics"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": HOST}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        return res.json()
    except:
        return None

st.subheader("🔥 Partidos Analizados (Próximas Horas)")

data = fetch_metrx()

if data and data.get('success'):
    # Entramos a la lista 'result' que vimos en tu imagen
    resultados = data.get('result', [])
    
    if resultados:
        st.success(f"Se encontraron {len(resultados)} partidos listos.")
        
        for item in resultados:
            # Extraemos la info según tus pantallazos
            m = item.get('match', {})
            home = m.get('homeTeam', {}).get('name', 'Local')
            away = m.get('awayTeam', {}).get('name', 'Visitante')
            liga = m.get('competition', {}).get('name', 'Liga')
            
            # Extraemos las probabilidades (Odds) que se ven en tus fotos
            performance = item.get('performance', {})
            p_home = performance.get('homeTeam', {}).get('index', 0)
            p_away = performance.get('awayTeam', {}).get('index', 0)

            with st.expander(f"🏟️ {home} vs {away}"):
                st.write(f"🏆 **Competencia:** {liga}")
                st.write(f"⏰ **Inicio:** {m.get('start')}")
                
                col1, col2 = st.columns(2)
                col1.metric("Índice Local", f"{p_home:.2f}")
                col2.metric("Índice Visita", f"{p_away:.2f}")
                
                # Lógica de recomendación OscarBet
                st.divider()
                if p_home > p_away:
                    st.success(f"🎯 Sugerencia: Fuerte tendencia a favor de {home}")
                else:
                    st.info(f"🎯 Sugerencia: Partido muy parejo o inclinado a {away}")
    else:
        st.warning("La API respondió pero la lista de partidos está vacía ahora mismo.")
else:
    st.error("No se pudo conectar. Revisa que tu suscripción en RapidAPI siga activa.")
    if data: st.write(data) # Para ver el error si vuelve a salir
