import streamlit as st
import yt_dlp
import os
import time
from pathlib import Path
import streamlit_lottie as st_lottie
import requests

# =========================
# CONFIG & ASSETS
# =========================
st.set_page_config(
    page_title="UltraStream X - Pro Max",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_download = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ai9m8way.json") # Radar
lottie_success = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_7W9rAL.json") # Check

# =========================
# STYLE "NEON DARK"
# =========================
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }
    
    /* Glassmorphism Cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Custom Titles */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        transition: 0.3s all ease;
        border-radius: 10px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.6);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIC & FOLDERS
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []

# =========================
# LOGIN SCREEN
# =========================
if not st.session_state.auth:
    cols = st.columns()
    with cols:
        st.markdown("<h1 class='main-title'>ACCESS GRANTED</h1>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 Entrez votre clé d'accès", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("Accès refusé.")
    st.stop()

# =========================
# MAIN INTERFACE
# =========================
st.markdown("<h1 class='main-title'>⚡ UltraStream X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.7;'>Vitesse maximale • Qualité Premium • Sans publicité</p>", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.header("💎 Premium Hub")
    if st.session_state.history:
        st.subheader("Récents")
        for h in st.session_state.history[-5:]:
            st.caption(f"✅ {h}")
        if st.button("Vider le cache"):
            st.session_state.history = []
    
    st.divider()
    st.info("💡 Astuce : Le format MP3 extrait la meilleure piste audio disponible.")

# Layout Principal
c1, c2 = st.columns()

with c1:
    url = st.text_input("🔗 Lien de la vidéo (YouTube, Twitch, etc.)", placeholder="https://...")
    name = st.text_input("✏️ Nommer le fichier (laisser vide pour l'original)")

with c2:
    mode = st.selectbox("📺 Format", ["Vidéo (MP4)", "Audio (MP3)"])
    if "Vidéo" in mode:
        res = st.select_slider("Résolution", options=["360p", "480p", "720p", "1080p", "Best"])
    else:
        res = st.selectbox("Bitrate", ["128kbps", "192kbps", "320kbps"])

# Bouton de lancement
if st.button("🚀 ANALYSER ET GÉNÉRER"):
    if not url:
        st.warning("Veuillez entrer une URL.")
    else:
        try:
            with st.status("🛠 Traitement en cours...", expanded=True) as status_box:
                # 1. Analyse
                st.write("Analyse des métadonnées...")
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                
                # Affichage des infos
                st.image(info.get('thumbnail'), width=300)
                st.write(f"**Titre :** {info.get('title')}")
                
                # 2. Configuration du téléchargement
                filename = name if name else info.get('title', 'video')
                # Nettoyage du nom pour éviter les erreurs de caractères spéciaux
                filename = "".join([c for c in filename if c.isalnum() or c in (' ', '.', '_')]).rstrip()
                
                out_path = f"{DOWNLOAD_FOLDER}/{filename}.%(ext)s"
                
                ydl_opts = {
                    'outtmpl': out_path,
                    'noplaylist': True,
                }

                if "Audio" in mode:
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': res.replace('kbps', ''),
                        }],
                    })
                else:
                    quality_map = {"360p": "360", "480p": "480", "720p": "720", "1080p": "1080", "Best": "9999"}
                    q = quality_map[res]
                    ydl_opts['format'] = f'bestvideo[height<={q}]+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4'

                # 3. Exécution
                st.write("Téléchargement des paquets...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                status_box.update(label="✅ Fichier prêt !", state="complete", expanded=False)

            # 4. Bouton de téléchargement final
            # On cherche le fichier créé
            ext = "mp3" if "Audio" in mode else "mp4"
            final_file = Path(DOWNLOAD_FOLDER) / f"{filename}.{ext}"
            
            if final_file.exists():
                with open(final_file, "rb") as f:
                    st.download_button(
                        label=f"📥 TÉLÉCHARGER {ext.upper()}",
                        data=f,
                        file_name=f"{filename}.{ext}",
                        mime=f"video/{ext}" if ext == "mp4" else "audio/mpeg"
                    )
                st.session_state.history.append(info.get('title'))
                if "Audio" in mode:
                    st.audio(final_file)
            else:
                st.error("Erreur lors de la récupération du fichier final.")

        except Exception as e:
            st.error(f"Détails de l'erreur : {str(e)}")

st.markdown("---")
st.caption("⚡ Powered by yt-dlp | Design by David Edwin | 2026 Edition")
