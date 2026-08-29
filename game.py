import streamlit as st
import time
import random
import os

# Configuración de la página
st.set_page_config(page_title="Charadas de Soldadura", layout="wide")

# --- ESTILOS GLOBALES Y ELEMENTOS COMUNES ---
estilos_comunes = """
<style>
/* Ocultar los reproductores de audio por completo */
audio {
    display: none !important;
}

/* Botones de cajas elegantes: Azul oscuro con borde dorado (destacan en el fondo claro) */
div.stButton > button {
    background: linear-gradient(135deg, #1A365D 0%, #0F1D32 100%);
    color: #FFFFFF !important;
    border: 2px solid #D4AF37;
    border-radius: 12px;
    font-weight: 700;
    font-size: 22px;
    box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
}
div.stButton > button * {
    color: #FFFFFF !important;
    font-weight: bold;
    letter-spacing: 1px;
}
div.stButton > button:hover {
    transform: translateY(-4px);
    background: linear-gradient(135deg, #2A4365 0%, #13284A 100%);
    box-shadow: 0px 12px 30px rgba(212, 175, 55, 0.4);
    border: 2px solid #FFD700;
}
div.stButton > button:disabled {
    background: #E2E8F0;
    color: #A0AEC0 !important;
    border: 2px solid #CBD5E0;
    box-shadow: none;
}
div.stButton > button:disabled * {
    color: #A0AEC0 !important;
}

/* Tarjeta elegante para la pregunta (Pantalla 2) */
.tarjeta-pregunta {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    border: 3px solid #D4AF37;
    text-align: center;
    margin-top: 20px;
}
</style>
"""
st.markdown(estilos_comunes, unsafe_allow_html=True)

def volver_al_tablero():
    st.session_state.caja_actual = None

preguntas_base = [
    {"pregunta": "Línea continua de metal fundido que une de forma permanente las piezas.", "respuesta": "Cordón de Soldadura"},
    {"pregunta": "Son pequeñas partículas que se producen al soldar y se depositan alrededor del cordón y se pueden evitar con spray. ¿Cómo se llaman?", "respuesta": "Proyecciones"},
    {"pregunta": "Defecto estructural donde el metal absorbe aire por falta de gas protector.", "respuesta": "Porosidad"},
    {"pregunta": "Gastos operativos obligatorios que se pagan sí o sí (ej. alquiler).", "respuesta": "Costes Fijos"},
    {"pregunta": "Pérdida de valor y desgaste de la maquinaria por su uso continuo.", "respuesta": "Amortización"},
    {"pregunta": "Momento exacto donde las ventas igualan a los gastos (beneficio cero).", "respuesta": "Punto de Equilibrio"}
]

if 'cajas_abiertas' not in st.session_state:
    st.session_state.cajas_abiertas = []
if 'caja_actual' not in st.session_state:
    st.session_state.caja_actual = None
if 'mezcla' not in st.session_state:
    random.shuffle(preguntas_base)
    st.session_state.mezcla = preguntas_base

# --- PANTALLA 1: EL TABLERO DE CAJAS (FONDO CLARO Y ELEGANTE) ---
if st.session_state.caja_actual is None:
    
    # Inyectar CSS dinámico solo para la pantalla 1
    st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(212, 175, 55, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 85% 30%, rgba(26, 54, 93, 0.05) 0%, transparent 40%),
            linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 🎵 MÚSICA DE FONDO 🎵
    ruta_fondo = "fondo.mp3"
    if os.path.exists(ruta_fondo):
        st.audio(ruta_fondo, format="audio/mp3", autoplay=True, loop=True)
    
    st.markdown("<h1 style='text-align: center; color: #1A365D; font-size: 55px; margin-top: 10px; font-family: serif; letter-spacing: 2px;'>Fabricación de Mesa Industrial</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #B7791F; font-size: 24px; font-weight: 600; letter-spacing: 1px;'>Técnica y Rentabilidad</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4A5568; font-size: 18px;'>Presentado Por: Carlos Sierra y Ricardo García</p>", unsafe_allow_html=True)
    
    st.markdown("<br><h3 style='text-align: center; color: #2D3748; font-size: 28px;'>🎁 Seleccione la Caja Misteriosa de su Equipo</h3><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    columnas = [col1, col2, col3, col1, col2, col3]
    
    for i in range(6):
        caja_num = i + 1
        with columnas[i]:
            if caja_num in st.session_state.cajas_abiertas:
                st.button(f"❌ Caja {caja_num} (Abierta)", disabled=True, key=f"btn_{caja_num}", use_container_width=True)
            else:
                if st.button(f"✨ Caja Misteriosa {caja_num}", key=f"btn_{caja_num}", use_container_width=True):
                    st.session_state.caja_actual = st.session_state.mezcla[i]
                    st.session_state.cajas_abiertas.append(caja_num)
                    st.rerun()

# --- PANTALLA 2: LA PREGUNTA Y EL TIEMPO (FONDO DE TENSIÓN) ---
else:
    # Inyectar CSS dinámico solo para la pantalla 2
    st.markdown("""
    <style>
    .stApp {
        background-color: #070D1B;
        background-image: radial-gradient(circle at 50% 50%, #1E3A8A 0%, #050914 80%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    q = st.session_state.caja_actual
    
    st.markdown(f"<div class='tarjeta-pregunta'><h1 style='color: #1A365D; font-size: 38px; font-weight: 800; margin: 0;'>{q['pregunta']}</h1></div>", unsafe_allow_html=True)
    
    # 🎵 MÚSICA DE ACCIÓN / CRONÓMETRO 🎵
    ruta_audio = "musica.webm"
    if os.path.exists(ruta_audio):
        st.audio(ruta_audio, format="audio/webm", autoplay=True)
    
    st.write("")
    
    temporizador = st.empty()
    for segundos in range(70, -1, -1):
        temporizador.markdown(f"<h1 style='text-align: center; font-size: 100px; color: #FC8181; text-shadow: 0 0 20px rgba(252, 129, 129, 0.6); margin-top: 10px;'>⏱️ {segundos}</h1>", unsafe_allow_html=True)
        time.sleep(1)
        
    st.markdown(f"<div style='background: #F0FFF4; padding: 25px; border-radius: 12px; border: 2px solid #38A169; box-shadow: 0 10px 30px rgba(0,0,0,0.5);'><h2 style='text-align: center; color: #22543D; margin: 0;'>✅ Respuesta Correcta: <br><b style='font-size: 45px; color: #2F855A;'>{q['respuesta']}</b></h2></div>", unsafe_allow_html=True)
    st.write("")
    
    st.button("⬅️ Volver al tablero de cajas", use_container_width=True, on_click=volver_al_tablero)
