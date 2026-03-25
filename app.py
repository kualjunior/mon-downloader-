import streamlit as st
import yt_dlp
import os
import time
import requests
from pathlib import Path
from streamlit_lottie import st_lottie
from PIL import Image, ImageFilter, ImageEnhance

# =========================
# CONFIGURATION PRO
# =========================
st.set_page_config(
    page_title="UltraStream X - Ultimate OS",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_rocket = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_96bovdur.json")

# =========================
# STYLE CYBERPUNK
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');
    .stApp { background: #08080a; font-family: 'Rajdhani', sans-serif; }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem !important;
        background: linear-gradient(90deg, #00f2fe, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIQUE SÉCURITÉ
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    c_left, c_mid, c_right = st.columns([1, 1.5, 1]) # FIX 1: Specifier les ratios
    with c_mid:
        if lottie_rocket: st_lottie(lottie_rocket, height=200)
        st.markdown("<h2 style='text-align:center; color:white;'>ACCÈS SÉCURISÉ</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Clé d'accès", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ Code incorrect")
    st.stop()

# =========================
# DASHBOARD
# =========================
st.markdown("<h1 class='main-title'>ULTRASTREAM X PRO</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🚀 Downloader", "🎨 Image Lab", "⏱️ Productivity", "📝 Notepad"])

# --- TAB 1 : DOWNLOADER ---
with tab1:
    # C'EST ICI QUE ÇA PLANTAIT (Ligne 106 dans ton log)
    col_u, col_o = st.columns() # FIX 2: Ratios obligatoires
    with col_u:
        url = st.text_input("🔗 URL de la source", placeholder="YouTube, TikTok, etc...")
    with col_o:
        format_type = st.selectbox("Format", ["Vidéo (MP4)", "Audio (MP3)"])

    if st.button("LANCER L'EXTRACTION 🚀"):
        if not url:
            st.warning("Veuillez entrer une URL.")
        else:
            try:
                with st.status("🛸 Extraction en cours...", expanded=True) as status:
                    ydl_opts = {'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s", 'quiet': True}
                    if "Audio" in format_type:
                        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        if "Audio" in format_type: filename = filename.rsplit('.', 1) + ".mp3"

                st.balloons()
                res_col1, res_col2 = st.columns() # FIX 3: Ratios
                with res_col1:
                    st.image(info.get('thumbnail'), use_container_width=True)
                with res_col2:
                    with open(filename, "rb") as f:
                        st.download_button("📥 TÉLÉCHARGER MAINTENANT", f, file_name=os.path.basename(filename))
                    st.session_state.history.append(info.get('title'))
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- TAB 2 : IMAGE LAB ---
with tab2:
    st.subheader("🎨 Retouche Photo Rapide")
    img_file = st.file_uploader("Choisir une image", type=['png', 'jpg', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        # On définit 2 colonnes égales
        ci1, ci2 = st.columns() # FIX 4: Ratios
        with ci1:
            st.image(img, caption="Original", use_container_width=True)
            effect = st.selectbox("Effet", ["Aucun", "Noir & Blanc", "Flou", "Contraste"])
        
        # Traitement simple
        out = img.copy()
        if effect == "Noir & Blanc": out = out.convert("L")
        elif effect == "Flou": out = out.filter(ImageFilter.BLUR)
        elif effect == "Contraste": out = ImageEnhance.Contrast(out).enhance(2)
        
        with ci2:
            st.image(out, caption="Résultat", use_container_width=True)

# --- TAB 3 : PRODUCTIVITY ---
with tab3:
    st.subheader("⏱️ Timer Focus")
    t1, t2 = st.columns() # FIX 5: Ratios
    with t1:
        mins = st.number_input("Minutes", 1, 60, 25)
        if st.button("Démarrer le chrono"):
            st.info(f"Focus activé pour {mins} minutes !")
    with t2:
        st.write("Idéal pour travailler sans distractions.")

# --- TAB 4 : NOTEPAD ---
with tab4:
    st.subheader("📝 Bloc-notes")
    note = st.text_area("Vos notes ici...", height=200)
    st.download_button("💾 Sauvegarder la note", note, file_name="note.txt")

st.markdown("<br><hr><p style='text-align:center; opacity:0.5;'>© 2026 David Edwin</p>", unsafe_allow_html=True)
