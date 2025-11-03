import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ====================================
# CONFIGURACIÓN
# ====================================
st.set_page_config(
    page_title="OCR Ferxxo Vision 💚",
    page_icon="🟢",
    layout="wide",
)

# ====================================
# ESTILO FEID (verde neón / futurista)
# ====================================
STYLE = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Chakra+Petch:wght@400;700&family=Urbanist:wght@300;500;700&display=swap');
:root { --neon:#00FF6A; --ink:#07150b; --ink-soft:#0b3620; }

[data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #b8ffbf 0%, #d4ffd6 55%, #eafff0 100%);
  color: var(--ink);
  font-family: 'Urbanist', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }

/* TITULOS */
h1 {
  font-family: 'Bebas Neue', sans-serif;
  text-align: center;
  font-size: clamp(52px, 7vw, 110px);
  letter-spacing: 1px;
  color: #000;
  text-shadow: 0 0 25px rgba(0,255,106,.7), 0 0 45px rgba(0,255,106,.35);
}
.subhead {
  text-align:center;
  font-family:'Chakra Petch', sans-serif;
  text-transform:uppercase;
  color: var(--ink-soft);
  letter-spacing:.9px;
  margin-top:-6px;
}
.hr {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,255,106,.9), transparent);
  margin: 25px 0;
}

/* CAMARA */
[data-testid="stCameraInput"] video, [data-testid="stCameraInput"] canvas {
  border: 3px solid var(--neon);
  border-radius: 16px;
  box-shadow: 0 0 18px rgba(0,255,106,.6), inset 0 0 8px rgba(0,255,106,.4);
}

/* BOTONES */
.stButton>button {
  background: transparent !important;
  color: var(--neon) !important;
  border: 2px solid var(--neon) !important;
  border-radius: 12px;
  font-family: 'Chakra Petch', sans-serif;
  font-weight: 800;
  text-transform: uppercase;
  padding: .7rem 1.4rem;
  margin: 0.6rem auto;
  transition: transform .25s ease, box-shadow .25s ease;
  animation: pulse 2.4s ease-in-out infinite;
}
.stButton>button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 22px rgba(0,255,106,.6);
}
@keyframes pulse {
  0% { box-shadow: 0 0 10px rgba(0,255,106,.4); }
  50% { box-shadow: 0 0 24px rgba(0,255,106,.8); }
  100% { box-shadow: 0 0 10px rgba(0,255,106,.4); }
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: rgba(230,255,240,.9);
  border-left: 3px solid var(--neon);
}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label {
  font-family: 'Chakra Petch', sans-serif;
  color: var(--ink-soft);
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ====================================
# INTERFAZ PRINCIPAL
# ====================================
st.markdown("<h1>OCR Ferxxo Vision</h1>", unsafe_allow_html=True)
st.markdown("<div class='subhead'>Reconocimiento óptico de caracteres con flow 💚</div>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ====================================
# CÁMARA Y FILTRO
# ====================================
img_file_buffer = st.camera_input("📸 Toma una foto para analizar el texto")

with st.sidebar:
    st.header("⚙️ Configuración")
    filtro = st.radio("Aplicar filtro visual:", ('Con Filtro', 'Sin Filtro'))
    st.caption("Estética Ferxxo — verde neón con energía visual")

# ====================================
# PROCESAMIENTO
# ====================================
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.subheader("🧾 Texto Detectado:")
    st.success(text if text.strip() else "No se detectó texto, intenta ajustar la iluminación o el enfoque 💡")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.caption("🌿 OCR Ferxxo Vision · Hecho con cariño · Estética CaFerxxo")
