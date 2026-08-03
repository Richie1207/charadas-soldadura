import streamlit as st
import time
import random
import os

# Configuración de la página
st.set_page_config(page_title="Charadas de Soldadura", layout="wide")

# --- DISEÑO VIBRANTE DE CONCURSO (AZUL MARINO, DORADO Y NARANJA) ---
estilo_css = """
<style>
/* Fondo principal Azul Marino vibrante con figuras Naranja y Dorado */
.stApp {
    background-color: #0A192F; /* Azul marino profundo y elegante */
    background-image: 
        /* Figura dorada arriba derecha */
        linear-gradient(135deg, rgba(255, 215, 0, 0.4) 0%, transparent 30%),
        /* Figura naranja abajo izquierda */
        linear-gradient(315deg, rgba(255, 102, 0, 0.4) 0%, transparent 30%),
        /* Círculos flotantes tipo focos de escenario */
        radial-gradient(circle at 85% 70%, rgba(255, 102, 0, 0.25) 0%, transparent 30%),
        radial-gradient(circle at 15% 30%, rgba(255, 215, 0, 0.2) 0%, transparent 30%);
}

/* Ocultar visualmente la barra del reproductor de audio */
audio {
    display: none;
}

/* Estilo espectacular para los botones de las cajas */
div.stButton > button {
    background: linear-gradient(90deg, #FF6B00, #FFD700);
    color: #0A192F !important;
    border: 3px solid #FFFFFF;
    border-radius: 12px;
    font-weight: 900;
    font-size: 22px;
    box-shadow: 0px 6px 15px rgba(255, 107, 0, 0.5);
    transition: all 0.3s ease;
}
div.stButton > button * {
    color: #0A192F !important; /* Fuerza el color oscuro en el texto del botón */
    font-weight: bold;
}
div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 8px 25px rgba(255, 215, 0, 0.8);
    border: 3px solid #0A192F;
}
div.stButton > button:disabled {
    background: #1A2530;
    color: #7F8C8D !important;
    border: 2px solid #2C3E50;
    box-shadow: none;
}
div.stButton > button:disabled * {
    color: #7F8C8D !important;
}

/* Tarjeta brillante para que la pregunta se lea perfecto */
.tarjeta-pregunta {
    background: rgba(255, 255, 255, 0.95);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    border: 6px solid #FFD700;
    text-align: center;
    margin-top: 20px;
}
</style>
"""
st.markdown(estilo_css, unsafe_allow_html=True)

# ✅ SOLUCIÓN AL BOTÓN
def volver_al_tablero():
    st.session_state.caja_actual = None

# Base de datos de preguntas
preguntas_base = [
    {"pregunta": "Línea continua de metal fundido que une de forma permanente las piezas.", "respuesta": "Cordón de Soldadura"},
    {"pregunta": "Capa de residuos e impurezas solidificada sobre el metal. Se elimina con piqueta.", "respuesta": "Escoria"},
    {"pregunta": "Defecto estructural donde el metal absorbe aire por falta de gas protector.", "respuesta": "Porosidad"},
    {"pregunta": "Gastos operativos obligatorios que se pagan sí o sí (ej. alquiler).", "respuesta": "Costes Fijos"},
    {"pregunta": "Pérdida de valor y desgaste de la maquinaria por su uso continuo.", "respuesta": "Amortización"},
    {"pregunta": "Momento exacto donde las ventas igualan a los gastos (beneficio cero).", "respuesta": "Punto de Equilibrio"}
]

# Variables de estado
if 'cajas_abiertas' not in st.session_state:
    st.session_state.cajas_abiertas = []
if 'caja_actual' not in st.session_state:
    st.session_state.caja_actual = None
if 'mezcla' not in st.session_state:
    random.shuffle(preguntas_base)
    st.session_state.mezcla = preguntas_base

# --- PANTALLA 1: EL TABLERO DE CAJAS ---
if st.session_state.caja_actual is None:
    
    # 🌟 PORTADA Y PRESENTACIÓN 🌟
    st.markdown("<h1 style='text-align: center; color: #FFD700; font-size: 65px; margin-top: 20px; text-shadow: 3px 3px 10px rgba(0,0,0,0.8);'>Fabricación de Mesa Industrial:<br>Técnica y Rentabilidad</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #FFFFFF; text-shadow: 1px 1px 5px rgba(0,0,0,0.8);'>Presentado Por: Carlos Sierra y Ricardo García</h2>", unsafe_allow_html=True)
    
    st.markdown("<br><h3 style='text-align: center; color: #FF6B00; font-size: 35px; text-shadow: 1px 1px 5px rgba(0,0,0,0.8);'>🎁 Selecciona el número de caja para tu equipo:</h3><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    columnas = [col1, col2, col3, col1, col2, col3]
    
    for i in range(6):
        caja_num = i + 1
        with columnas[i]:
            if caja_num in st.session_state.cajas_abiertas:
                st.button(f"❌ Caja {caja_num} (Abierta)", disabled=True, key=f"btn_{caja_num}", use_container_width=True)
            else:
                if st.button(f"🎁 Abrir Caja {caja_num}", key=f"btn_{caja_num}", use_container_width=True):
                    st.session_state.caja_actual = st.session_state.mezcla[i]
                    st.session_state.cajas_abiertas.append(caja_num)
                    st.rerun()

# --- PANTALLA 2: LA PREGUNTA Y EL TIEMPO ---
else:
    q = st.session_state.caja_actual
    
    # Pregunta envuelta en la tarjeta blanca de alto contraste
    st.markdown(f"<div class='tarjeta-pregunta'><h1 style='color: #0A192F; font-size: 55px; margin: 0;'>{q['pregunta']}</h1></div>", unsafe_allow_html=True)
    
# 🎵 MÚSICA INVISIBLE CON RUTA RELATIVA 🎵
    ruta_audio = "musica.webm"
    if os.path.exists(ruta_audio):
        st.audio(ruta_audio, format="audio/webm", autoplay=True)
    else:
        st.warning(f"🎵 No se encuentra el archivo en la ruta: {ruta_audio}")
    
    st.write("") # Espacio
    
    # Cronómetro gigante y brillante
    temporizador = st.empty()
    for segundos in range(70, -1, -1):
        temporizador.markdown(f"<h1 style='text-align: center; font-size: 110px; color: #FF3333; text-shadow: 4px 4px 15px rgba(0,0,0,0.8); margin-top: 10px;'>⏱️ {segundos}</h1>", unsafe_allow_html=True)
        time.sleep(1)
        
    # 🎯 MOSTRAR LA RESPUESTA AL FINAL 🎯
    st.markdown(f"<div style='background: linear-gradient(90deg, #1b5e20, #2e7d32); padding: 25px; border-radius: 15px; border: 4px solid #66bb6a; box-shadow: 0 10px 30px rgba(0,0,0,0.5);'><h2 style='text-align: center; color: white; margin: 0;'>✅ La respuesta correcta era: <br><b style='font-size: 50px; color: #FFD700;'>{q['respuesta']}</b></h2></div>", unsafe_allow_html=True)
    st.write("") # Espacio en blanco
    
    # ✅ BOTÓN PARA VOLVER
    st.button("⬅️ Volver al tablero de cajas", use_container_width=True, on_click=volver_al_tablero)