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
# ESTILO FEID (neón verde / café suave / pro)
# ====================================
STYLE = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Chakra+Petch:wght@400;700&family=Urbanist:wght@300;500;700&display=swap');
:root { 
  --neon:#00FF6A; 
  --ink:#07150b; 
  --ink-soft:#0b3620; 
  --cafe:#5a3e2b; 
  --paper:#ffffff; 
}

/* Fondo y tipografía base */
[data-testid="stAppViewContainer"]{
  background: linear-gradient(180deg, #b8ffbf 0%, #d4ffd6 55%, #f1fff6 100%);
  color: var(--ink);
  font-family:'Urbanist', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
  padding-bottom: 48px;
}
[data-testid="stHeader"]{ background: transparent; }

/* Header suave */
.header-bar{
  width:100%; padding:10px 16px; border-radius:16px; margin: 8px 0 12px;
  background: radial-gradient(900px 220px at 8% 0%, rgba(0,255,106,.22), transparent 70%);
  box-shadow: 0 0 0 1px rgba(0,255,106,.22);
}

/* Títulos */
h1{
  font-family:'Bebas Neue', sans-serif; text-align:center; 
  font-size: clamp(52px, 7vw, 112px);
  letter-spacing:.6px; color:#000;
  text-shadow:0 0 24px rgba(0,255,106,.7), 0 0 44px rgba(0,255,106,.35);
  margin:.35rem 0 .25rem;
}
.subhead{
  text-align:center; font-family:'Chakra Petch', sans-serif; text-transform:uppercase; letter-spacing:.9px;
  color: var(--ink-soft); margin-top:-6px; margin-bottom:12px;
}
.hr{ height:1px; background:linear-gradient(90deg, transparent, rgba(0,255,106,.9), transparent); margin: 20px 0; }

/* Chips */
.chip{
  display:inline-block; padding:.28rem .7rem; border:2px solid var(--neon); border-radius:999px;
  font-family:'Chakra Petch', sans-serif; font-weight:800; letter-spacing:.6px; text-transform:uppercase;
  background:rgba(0,255,106,.12); color:var(--ink-soft); margin-bottom:10px;
}

/* Cards */
.card{
  background: linear-gradient(180deg, rgba(255,255,255,.96), rgba(240,255,248,.94));
  border:1px solid rgba(0,255,106,.28); border-radius:18px; padding:16px;
  box-shadow:0 10px 24px rgba(0,0,0,.06), 0 0 0 2px rgba(0,255,106,.12);
}

/* Imagen hero con borde neón */
.hero-img{
  display:block; margin:0 auto; border-radius:18px;
  border:4px solid var(--neon); max-height:460px; width:100%;
  box-shadow:0 0 18px rgba(0,255,106,.55), inset 0 0 10px rgba(0,255,106,.45);
  object-fit:cover; transition: transform .28s ease;
}
.hero-img:hover{ transform: scale(1.015); }

/* Cámara */
[data-testid="stCameraInput"] video, [data-testid="stCameraInput"] canvas {
  border: 3px solid var(--neon);
  border-radius: 16px;
  box-shadow: 0 0 18px rgba(0,255,106,.6), inset 0 0 8px rgba(0,255,106,.4);
}

/* Botones pro */
.stButton>button{
  background:transparent !important; color:var(--neon) !important;
  border:2px solid var(--neon) !important; border-radius:12px;
  font-family:'Chakra Petch', sans-serif; font-weight:800; text-transform:uppercase; letter-spacing:.6px;
  padding:.7rem 1.6rem; display:block; margin:.8rem auto;
  transition: transform .25s ease, box-shadow .25s ease;
  animation: pulse 2.4s ease-in-out infinite;
}
.stButton>button:hover{ transform:scale(1.05); box-shadow:0 0 22px rgba(0,255,106,.6); }
@keyframes pulse{
  0%{ box-shadow:0 0 10px rgba(0,255,106,.35); }
  50%{ box-shadow:0 0 24px rgba(0,255,106,.75); }
  100%{ box-shadow:0 0 10px rgba(0,255,106,.35); }
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: rgba(230,255,240,.9);
  border-left: 3px solid var(--neon);
}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label {
  font-family: 'Chakra Petch', sans-serif;
  color: var(--ink-soft);
}

/* Área de texto resultado */
textarea{
  border-radius:12px !important; 
  border:2px solid rgba(0,255,106,.35) !important; 
  background:rgba(255,255,255,.9) !important;
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ====================================
# HERO (imagen + intro)
# ====================================
st.markdown("<div class='header-bar'></div>", unsafe_allow_html=True)
st.markdown("<h1>OCR Ferxxo Vision</h1>", unsafe_allow_html=True)
st.markdown("<div class='subhead'>Reconocimiento óptico de caracteres — flujo verde pro 💚</div>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

hero_left, hero_right = st.columns([1,1], vertical_alignment="center")
with hero_left:
    st.markdown("<div class='chip'>Portada</div>", unsafe_allow_html=True)
    try:
        hero_img = Image.open("ferquini3.jpg")  # ← tu foto
        st.image(hero_img, use_container_width=True, caption="Ferxxo vibes · portada", output_format="PNG")
    except Exception:
        st.info("Sube la imagen 'ferquini3.jpg' para mostrar la portada.")
with hero_right:
    st.markdown("<div class='chip'>Intro</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Captura · Procesa · Lee")
    st.write("Toma una foto, **aplica un filtro** si lo necesitas y extrae el texto con **OCR**. "
             "Estilo **Ferxxo**: neón verde, limpio y profesional.")
    st.write("Consejo: procura buena iluminación y enfoque para mejores resultados.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ====================================
# CÁMARA + CONTROLES
# ====================================
st.markdown("<div class='chip'>Captura</div>", unsafe_allow_html=True)
cam_col, opt_col = st.columns([2,1])

with cam_col:
    img_file_buffer = st.camera_input("📸 Toma una foto para analizar el texto")

with opt_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Opciones")
    filtro = st.radio("Filtro visual:", ('Sin Filtro', 'Invertir colores'))
    st.caption("Estética Ferxxo — verde neón con energía visual")
    st.markdown("</div>", unsafe_allow_html=True)

# ====================================
# PROCESAMIENTO
# ====================================
text = ""
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Invertir colores':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb).strip()

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    res_left, res_right = st.columns([1,1])
    with res_left:
        st.markdown("<div class='chip'>Vista previa</div>", unsafe_allow_html=True)
        st.image(img_rgb, caption="Imagen procesada", use_container_width=True)
    with res_right:
        st.markdown("<div class='chip'>Resultado OCR</div>", unsafe_allow_html=True)
        st.text_area("🧾 Texto detectado:", value=(text or "No se detectó texto. Intenta otra toma ✨"), height=220)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.caption("🌿 OCR Ferxxo Vision · Hecho con cariño · Estética CaFerxxo")
