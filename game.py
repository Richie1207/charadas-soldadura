import streamlit as st
import time
import random
import os

# Configuración de la página
st.set_page_config(page_title="Charadas de Soldadura", layout="wide")

# --- VARIABLES DE ESTADO Y FUNCIONES ---
if 'cajas_abiertas' not in st.session_state:
    st.session_state.cajas_abiertas = []
if 'caja_actual' not in st.session_state:
    st.session_state.caja_actual = None
if 'tiempo_detenido' not in st.session_state:
    st.session_state.tiempo_detenido = False

def detener_tiempo():
    st.session_state.tiempo_detenido = True

def volver_al_tablero():
    st.session_state.caja_actual = None
    st.session_state.tiempo_detenido = False

# --- DISEÑO A1: ESTILO "DEAL OR NO DEAL" ---
estilos_comunes = """
<style>
.stApp {
    background-color: #050914;
    background-image: radial-gradient(circle at 50% 0%, #1E3A8A 0%, #0B132B 50%, #02040A 100%);
    background-attachment: fixed;
}
audio {
    display: none !important;
}

/* CAJAS MISTERIOSAS Y BOTONES */
div.stButton > button {
    background: linear-gradient(180deg, #FFDF00 0%, #D4AF37 50%, #997A00 100%);
    color: #000000 !important;
    border: 2px solid #FFF3E0;
    border-radius: 12px;
    font-weight: 900;
    font-size: 26px;
    padding: 20px 0px;
    box-shadow: 0px 10px 20px rgba(0,0,0,0.6), inset 0px 2px 5px rgba(255,255,255,0.7);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
div.stButton > button * {
    color: #000000 !important;
    font-weight: 900;
}
div.stButton > button:hover {
    transform: scale(1.03) translateY(-5px);
    background: linear-gradient(180deg, #FFE55C 0%, #FFDF00 50%, #B38F00 100%);
    box-shadow: 0px 15px 30px rgba(212, 175, 55, 0.5), inset 0px 2px 10px rgba(255,255,255,0.9);
    border: 2px solid #FFFFFF;
}
div.stButton > button:disabled {
    background: linear-gradient(180deg, #2D3748 0%, #1A202C 100%);
    color: #718096 !important;
    border: 2px solid #000000;
    box-shadow: inset 0px 5px 15px rgba(0,0,0,0.8);
    transform: scale(0.98);
}
div.stButton > button:disabled * {
    color: #718096 !important;
}

/* TARJETA DE PREGUNTA */
.tarjeta-pregunta {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    padding: 30px 50px;
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 30px 60px rgba(0,0,0,0.9), inset 0 0 20px rgba(255,255,255,0.03);
    text-align: center;
    margin-top: 10px;
}
.texto-pregunta {
    color: #FFFFFF;
    font-size: 55px !important; /* TAMAÑO CORREGIDO (La mitad del gigante) */
    font-weight: 900;
    line-height: 1.2;
    text-shadow: 3px 5px 12px rgba(0,0,0,0.9);
    margin: 0;
    font-family: 'Helvetica Neue', sans-serif;
}

/* EL DISTRACTOR ANIMADO */
.icono-distractor {
    font-size: 100px;
    margin-bottom: 15px;
    animation: flotar 2.5s ease-in-out infinite, palpitar 1.5s infinite alternate;
}
@keyframes flotar {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
@keyframes palpitar {
    0% { filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.4)); }
    100% { filter: drop-shadow(0 0 50px rgba(255, 215, 0, 1)); }
}
</style>
"""
st.markdown(estilos_comunes, unsafe_allow_html=True)

# Base de datos
preguntas_base = [
    {"pregunta": "Línea continua de metal fundido que une de forma permanente las piezas.", "respuesta": "Cordón de Soldadura", "icono": "⚡"},
    {"pregunta": "Son pequeñas partículas que se producen al soldar y se depositan alrededor del cordón... ¿Cómo se llaman?", "respuesta": "Proyecciones", "icono": "💥"},
    {"pregunta": "Defecto estructural donde el metal absorbe aire por falta de gas protector.", "respuesta": "Porosidad", "icono": "🌪️"},
    {"pregunta": "Gastos operativos obligatorios que se pagan sí o sí (ej. alquiler).", "respuesta": "Costes Fijos", "icono": "🏢"},
    {"pregunta": "Pérdida de valor y desgaste de la maquinaria por su uso continuo.", "respuesta": "Amortización", "icono": "📉"},
    {"pregunta": "Momento exacto donde las ventas igualan a los gastos (beneficio cero).", "respuesta": "Punto de Equilibrio", "icono": "⚖️"}
]

if 'mezcla' not in st.session_state:
    random.shuffle(preguntas_base)
    st.session_state.mezcla = preguntas_base

# --- PANTALLA 1: EL TABLERO ---
if st.session_state.caja_actual is None:
    
    # 🎵 MÚSICA DE FONDO 🎵
    ruta_fondo = "fondo.mp3"
    if os.path.exists(ruta_fondo):
        st.audio(ruta_fondo, format="audio/mp3", autoplay=True, loop=True)
    
    st.markdown("<h1 style='text-align: center; color: #FFFFFF; font-size: 65px; margin-top: 0px; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; text-shadow: 0px 4px 15px rgba(255,215,0,0.4);'>Fabricación Industrial</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #D4AF37; font-size: 26px; font-weight: 400; letter-spacing: 5px; margin-top: -15px; text-transform: uppercase;'>Técnica y Rentabilidad</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 16px; margin-bottom: 40px;'>PRESENTADO POR: CARLOS SIERRA Y RICARDO GARCÍA</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    columnas = [col1, col2, col3, col1, col2, col3]
    
    st.write("") 
    
    for i in range(6):
        caja_num = i + 1
        with columnas[i]:
            if caja_num in st.session_state.cajas_abiertas:
                st.button(f"CAJA {caja_num}", disabled=True, key=f"btn_{caja_num}", use_container_width=True)
            else:
                if st.button(f"CAJA {caja_num}", key=f"btn_{caja_num}", use_container_width=True):
                    st.session_state.caja_actual = st.session_state.mezcla[i]
                    st.session_state.cajas_abiertas.append(caja_num)
                    st.session_state.tiempo_detenido = False
                    st.rerun()
                    
    st.markdown("<br><p style='text-align: center; color: #E2E8F0; font-size: 20px; font-weight: 300;'>Seleccione su caja para jugar</p>", unsafe_allow_html=True)

# --- PANTALLA 2: LA PREGUNTA ---
else:
    st.markdown("""
    <style>
    .stApp {
        background-color: #0A0000;
        background-image: radial-gradient(circle at 50% 50%, #4A0000 0%, #1A0000 60%, #000000 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    q = st.session_state.caja_actual
    
    # 🎵 MÚSICA DE ACCIÓN (solo suena si el tiempo no está detenido) 🎵
    if not st.session_state.tiempo_detenido:
        ruta_audio = "musica.webm"
        if os.path.exists(ruta_audio):
            st.audio(ruta_audio, format="audio/webm", autoplay=True)
    
    # Tarjeta de la pregunta
    st.markdown(f"<div class='tarjeta-pregunta'><div class='icono-distractor'>{q['icono']}</div><p class='texto-pregunta'>{q['pregunta']}</p></div>", unsafe_allow_html=True)
    
    st.write("")
    
    # --- LÓGICA DEL CRONÓMETRO Y RESPUESTA ---
    if not st.session_state.tiempo_detenido:
        
        # Botón para cortar el tiempo (Llama a la función detener_tiempo)
        st.button("🛑 ¡ADIVINÓ! DETENER TIEMPO Y VER RESPUESTA", use_container_width=True, on_click=detener_tiempo)
        
        temporizador = st.empty()
        for segundos in range(70, -1, -1):
            temporizador.markdown(f"<h1 style='text-align: center; font-size: 130px; font-family: monospace; font-weight: 900; color: #FF3333; text-shadow: 0 0 40px rgba(255, 51, 51, 0.8); margin: 10px 0;'>00:{segundos:02d}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
        # Si el tiempo llega a cero sin que le den al botón:
        st.session_state.tiempo_detenido = True
        st.rerun()

    else:
        # --- SE MUESTRA LA RESPUESTA ---
        st.markdown(f"<div style='background: linear-gradient(135deg, #0F5132 0%, #062C19 100%); padding: 30px; border-radius: 16px; border: 2px solid #75B798; box-shadow: 0 15px 40px rgba(0,0,0,0.8); margin-top: 10px;'><h3 style='text-align: center; color: #A3CFBB; margin: 0; font-weight: 400; text-transform: uppercase; font-size: 20px;'>Respuesta Correcta</h3><h2 style='text-align: center; color: #FFFFFF; font-size: 55px; margin: 10px 0 0 0; font-weight: 900; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);'>{q['respuesta']}</h2></div>", unsafe_allow_html=True)
        st.write("")
        
        # --- AHORA SÍ, BOTÓN PARA VOLVER AL TABLERO ---
        st.button("⬅ VOLVER AL ESTUDIO", use_container_width=True, on_click=volver_al_tablero)
