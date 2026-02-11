import streamlit as st
import yt_dlp
import os
import time
from pathlib import Path

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Ultimate Downloader X PRO",
    page_icon="🚀",
    layout="wide"
)

# =========================
# CONSTANTES
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# =========================
# STYLE GLOBAL
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0f172a, #111827);
    color: #f1f5f9;
    font-family: 'Segoe UI', sans-serif;
}

.david-signature {
    font-size: 4em;
    font-weight: 800;
    text-align: center;
    color: #38bdf8;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-size: 1.2em;
    color: #94a3b8;
    margin-top: -5px;
}

.stButton>button, .stDownloadButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: 600;
    border: none;
    transition: 0.2s ease-in-out;
}

.stButton>button {
    background: #38bdf8;
    color: black;
}

.stButton>button:hover {
    background: #0ea5e9;
    transform: translateY(-2px);
}

.stDownloadButton>button {
    background: #22c55e;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# AUTHENTIFICATION
# =========================
if not st.session_state.auth:
    st.title("🔒 Connexion requise")
    password_input = st.text_input("Entrez le mot de passe :", type="password")
    if st.button("Se connecter"):
        if password_input == PASSWORD:
            st.session_state.auth = True
            st.success("✅ Authentification réussie !")
        else:
            st.error("❌ Mot de passe incorrect")

# =========================
# APPLICATION PRINCIPALE
# =========================
if st.session_state.auth:
    # HEADER
    st.markdown('<p class="david-signature">DAVID EDWIN</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Ultimate Downloader X • Founder & Developer</p>', unsafe_allow_html=True)
    st.divider()

    # SIDEBAR - Historique
    st.sidebar.title("📜 Historique")
    if st.session_state.history:
        for item in st.session_state.history:
            st.sidebar.write("•", item)
    else:
        st.sidebar.info("Aucun téléchargement pour le moment.")
    st.sidebar.divider()
    st.sidebar.success("✔ Compatible YouTube, TikTok, Facebook, Instagram")

    # INPUT URLS
    urls = st.text_area("🔗 Collez un ou plusieurs liens (1 par ligne)")
    format_choice = st.radio("Format :", ["MP4 🎥 (Vidéo)", "MP3 🎵 (Audio)"], horizontal=True)
    quality = st.selectbox("🎞️ Qualité vidéo", ["Best", "1080p", "720p", "480p", "360p"])
    st.divider()

    # FONCTION DE TÉLÉCHARGEMENT
    def download_video(url, format_choice, quality):
        # Détermination du format
        if format_choice == "MP4 🎥 (Vidéo)":
            if quality == "1080p":
                fmt = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
            elif quality == "720p":
                fmt = "bestvideo[height<=720]+bestaudio/best[height<=720]"
            elif quality == "480p":
                fmt = "bestvideo[height<=480]+bestaudio/best[height<=480]"
            elif quality == "360p":
                fmt = "bestvideo[height<=360]+bestaudio/best[height<=360]"
            else:
                fmt = "best"
            ydl_opts = {
                'format': fmt,
                'merge_output_format': 'mp4',
                'outtmpl': f'{DOWNLOAD_FOLDER}/file_%(id)s.%(ext)s',
                'progress_hooks': [progress_hook]
            }
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/file_%(id)s.%(ext)s',
                'progress_hooks': [progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        st.session_state.history.append(info.get("title"))
        return info

    # PROGRESS HOOK
    progress_bar = st.empty()
    status_text = st.empty()
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded / total * 100)
                progress_bar.progress(percent)
        elif d['status'] == 'finished':
            progress_bar.empty()
            status_text.success("✅ Téléchargement terminé !")

    # LANCER LE TÉLÉCHARGEMENT
    if urls:
        url_list = [u.strip() for u in urls.split("\n") if u.strip()]
        if st.button("🚀 Lancer le téléchargement PRO"):
            for url in url_list:
                try:
                    status_text.info("⏳ Téléchargement en cours...")
                    info = download_video(url, format_choice, quality)

                    # Affichage info vidéo
                    st.subheader(info.get("title"))
                    st.image(info.get("thumbnail"), width=400)
                    st.write(f"👤 Chaîne : {info.get('uploader', 'Unknown')}")
                    st.write(f"⏱️ Durée : {info.get('duration', 0)//60} min")
                    st.write(f"👁️ Vues : {info.get('view_count', 0)}")

                    # Bouton de téléchargement
                    final_file = max(Path(DOWNLOAD_FOLDER).glob(f"file_*"), key=os.path.getctime)
                    with open(final_file, "rb") as f:
                        st.download_button("📥 Télécharger maintenant", f, file_name=final_file.name)

                except Exception as e:
                    st.error(f"❌ Erreur : {e}")

    # FOOTER
    st.divider()
    st.markdown("<div style='text-align:center; opacity:0.6;'>© 2026 DAVID EDWIN • Ultimate Downloader X PRO</div>", unsafe_allow_html=True)
