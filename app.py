import streamlit as st
import yt_dlp
import os
import time
import requests
from pathlib import Path
from streamlit_lottie import st_lottie
from streamlit_js_eval import streamlit_js_eval

# =========================
# CONFIGURATION PRO
# =========================
st.set_page_config(
    page_title="UltraStream X - PRO MAX",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger les animations Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_rocket = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_96bovdur.json")
lottie_loading = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_raiw2hsc.json")

# =========================
# STYLE & JAVASCRIPT (PARTICULES)
# =========================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    .stApp {
        background: #050505;
        font-family: 'Inter', sans-serif;
    }

    /* Titre Cyberpunk */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem !important;
        font-weight: 700;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 3px;
        margin-top: -50px;
    }

    /* Cartes Glassmorphism */
    div.stSelectbox, div.stTextInput, div.stNumberInput {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(0, 242, 254, 0.2);
        padding: 5px;
    }

    /* Bouton Rayonnant */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #00f2fe, #7000ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-family: 'Orbitron', sans-serif;
        padding: 1rem !important;
        font-size: 1.2rem !important;
        transition: 0.4s;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    }
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 30px rgba(112, 0, 255, 0.6);
    }
</style>

<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<div id="particles-js" style="position: fixed; width: 100%; height: 100%; top: 0; left: 0; z-index: -1;"></div>
<script>
    particlesJS("particles-js", {
        "particles": {
            "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
            "color": {"value": "#00f2fe"},
            "shape": {"type": "circle"},
            "opacity": {"value": 0.5, "random": false},
            "size": {"value": 3, "random": true},
            "line_linked": {"enable": true, "distance": 150, "color": "#7000ff", "opacity": 0.4, "width": 1},
            "move": {"enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out"}
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {"onhover": {"enable": true, "mode": "repulse"}, "onclick": {"enable": true, "mode": "push"}}
        }
    });
</script>
""", unsafe_allow_html=True)

# =========================
# LOGIQUE & SÉCURITÉ
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []

# =========================
# LOGIN (ÉLÉGANT)
# =========================
if not st.session_state.auth:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st_lottie(lottie_rocket, height=200)
        st.markdown("<h1 style='text-align:center; color:white;'>SYSTÈME SÉCURISÉ</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Clé d'accès", type="password", placeholder="Entrez le code...")
        if st.button("DÉVERROUILLER LE PANEL"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ Code erroné.")
    st.stop()

# =========================
# DASHBOARD PRINCIPAL
# =========================
st.markdown("<h1 class='main-title'>ULTRASTREAM X</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3502/3502688.png", width=80)
    st.header("⚡ Settings")
    theme = st.toggle("Activer mode Turbo", value=True)
    st.divider()
    
    st.subheader("📜 Historique de session")
    for item in st.session_state.history:
        st.caption(f"✨ {item}")

# --- ZONE DE SAISIE ---
container = st.container()
with container:
    col_u, col_o = st.columns()
    with col_u:
        url = st.text_input("🔗 URL de la source", placeholder="Collez votre lien YouTube, Twitch, Facebook...")
    with col_o:
        format_type = st.selectbox("Format", ["Vidéo (MP4)", "Audio (MP3)", "Full HD+ (MKV)"])

    expander = st.expander("🛠 Options Avancées")
    with expander:
        c1, c2, c3 = st.columns(3)
        with c1: custom_name = st.text_input("Nom personnalisé")
        with c2: quality = st.select_slider("Qualité Max", options=["360p", "720p", "1080p", "4K"])
        with c3: st.checkbox("Ignorer Playlist", value=True)

# --- ACTION ---
if st.button("LANCER L'EXTRACTION 🚀"):
    if not url:
        st.warning("⚠️ L'URL est vide.")
    else:
        try:
            with st.status("🛸 En orbite... Extraction en cours", expanded=True) as status:
                # 1. Analyse
                st_lottie(lottie_loading, height=100)
                st.write("🔍 Analyse des serveurs...")
                
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                
                title = custom_name if custom_name else info.get('title', 'file')
                title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip()
                
                # 2. Config technique
                ydl_opts = {
                    'outtmpl': f"{DOWNLOAD_FOLDER}/{title}.%(ext)s",
                    'noplaylist': True,
                }

                if "Audio" in format_type:
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}]
                    })
                else:
                    q_val = quality.replace('p', '')
                    ydl_opts['format'] = f'bestvideo[height<={q_val}]+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4' if "MP4" in format_type else 'mkv'

                # 3. Download
                ydl.download([url])
                status.update(label="✅ Terminé avec succès !", state="complete")

            # --- AFFICHAGE RÉSULTAT ---
            st.balloons()
            ext = "mp3" if "Audio" in format_type else ("mp4" if "MP4" in format_type else "mkv")
            final_file = Path(DOWNLOAD_FOLDER) / f"{title}.{ext}"

            res_col1, res_col2 = st.columns()
            with res_col1:
                st.image(info.get('thumbnail'), caption=info.get('title'), use_container_width=True)
            
            with res_col2:
                st.success(f"Prêt : {title}.{ext}")
                with open(final_file, "rb") as f:
                    st.download_button(
                        f"📥 TÉLÉCHARGER LE FICHIER",
                        data=f,
                        file_name=f"{title}.{ext}",
                        mime="application/octet-stream"
                    )
                if "Audio" in format_type:
                    st.audio(final_file)
                
                st.session_state.history.append(title)

        except Exception as e:
            st.error(f"💥 Crash système : {e}")

st.markdown("<br><br><p style='text-align:center; opacity:0.5;'>Version 2.0-PRO | © 2026 David Edwin</p>", unsafe_allow_html=True)
