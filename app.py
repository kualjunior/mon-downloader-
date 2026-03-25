import streamlit as st
import yt_dlp
import os
import time
import requests
from pathlib import Path
from streamlit_lottie import st_lottie
from PIL import Image, ImageFilter, ImageEnhance

# =========================
# CONFIGURATION ET THÈME
# =========================
st.set_page_config(
    page_title="UltraStream X - Master OS",
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
        text-align: center; padding: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SÉCURITÉ ET DOSSIERS
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []

# =========================
# ÉCRAN DE CONNEXION
# =========================
if not st.session_state.auth:
    col_l, col_m, col_r = st.columns([1, 1.5, 1]) # Correction : Ratios définis
    with col_m:
        if lottie_rocket: st_lottie(lottie_rocket, height=200)
        st.markdown("<h2 style='text-align:center; color:white;'>ACCÈS SÉCURISÉ</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Clé d'accès", type="password", key="login_pwd")
        if st.button("DÉVERROUILLER LE SYSTÈME", key="login_btn"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ Code incorrect")
    st.stop()

# =========================
# DASHBOARD MULTIMÉDIA
# =========================
st.markdown("<h1 class='main-title'>ULTRASTREAM X PRO</h1>", unsafe_allow_html=True)

# Barre latérale
with st.sidebar:
    st.markdown("### 📊 État du Système")
    st.success("Serveurs : Online")
    st.divider()
    if st.session_state.history:
        st.markdown("### 📜 Récents")
        for h in st.session_state.history[-5:]:
            st.caption(f"• {h}")

# Onglets
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Downloader", "🎨 Image Lab", "⏱️ Focus Timer", "📝 Notepad"])

# --- ONGLET 1 : DOWNLOADER ---
with tab1:
    col_input1, col_input2 = st.columns() # Correction : Ratios définis
    with col_input1:
        url = st.text_input("🔗 URL de la source", placeholder="Lien vidéo ici...", key="main_url")
    with col_input2:
        ftype = st.selectbox("Format", ["Vidéo (MP4)", "Audio (MP3)"], key="main_fmt")

    if st.button("LANCER L'EXTRACTION 🚀", key="exec_btn"):
        if not url:
            st.warning("⚠️ L'URL est manquante.")
        else:
            try:
                with st.status("🛸 Traitement...", expanded=True) as status:
                    ydl_opts = {'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s", 'quiet': True}
                    if "Audio" in ftype:
                        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        f_name = ydl.prepare_filename(info)
                        if "Audio" in ftype: f_name = f_name.rsplit('.', 1) + ".mp3"

                st.balloons()
                c_res1, c_res2 = st.columns() # Correction : Ratios définis
                with c_res1:
                    st.image(info.get('thumbnail'), use_container_width=True)
                with c_res2:
                    st.success("Fichier prêt !")
                    with open(f_name, "rb") as f:
                        st.download_button("📥 TÉLÉCHARGER", f, file_name=os.path.basename(f_name), key="dl_btn")
                    st.session_state.history.append(info.get('title'))
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- ONGLET 2 : IMAGE LAB (OFFLINE) ---
with tab2:
    st.subheader("🎨 Studio Photo")
    up_img = st.file_uploader("Charge une image", type=['png', 'jpg', 'jpeg'], key="img_up")
    if up_img:
        img = Image.open(up_img)
        ci1, ci2 = st.columns() # Correction : Ratios définis
        with ci1:
            st.image(img, caption="Original", use_container_width=True)
            effect = st.radio("Appliquer un filtre", ["Aucun", "Noir & Blanc", "Flou", "Néon"], key="filter_choice")
        
        # Logique de traitement
        out = img.copy()
        if effect == "Noir & Blanc": out = out.convert("L")
        elif effect == "Flou": out = out.filter(ImageFilter.BLUR)
        elif effect == "Néon": out = ImageEnhance.Contrast(out).enhance(3)
        
        with ci2:
            st.image(out, caption="Résultat", use_container_width=True)

# --- ONGLET 3 : TIMER ---
with tab3:
    st.subheader("⏱️ Chrono de Productivité")
    ct1, ct2 = st.columns() # Correction : Ratios définis
    with ct1:
        m = st.number_input("Minutes de focus", 1, 60, 25, key="timer_input")
        if st.button("DÉMARRER", key="timer_btn"):
            st.info(f"C'est parti pour {m} minutes !")
    with ct2:
        st.write("Le secret des pros : travaillez par blocs de 25 minutes.")

# --- ONGLET 4 : NOTEPAD ---
with tab4:
    st.subheader("📝 Quick Notes")
    text = st.text_area("Notez vos idées ici...", height=200, key="note_area")
    st.download_button("💾 EXPORTER (.txt)", text, file_name="notes_ultrastream.txt", key="export_btn")

st.markdown("<br><hr><p style='text-align:center; opacity:0.4;'>UltraStream X v3.5 | © 2026 David Edwin</p>", unsafe_allow_html=True)
