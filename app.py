import streamlit as st
import yt_dlp
import os
import time
from pathlib import Path
from datetime import datetime

# =========================
# CONFIG PRO VERSION
# =========================
st.set_page_config(
    page_title="Ultimate Downloader X PRO MAX",
    page_icon="🚀",
    layout="centered",  # mieux pour mobile
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS (Modern + Mobile)
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Main container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 800px;
}

/* Titles */
h1, h2, h3 {
    text-align: center;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    height: 3.5em;
    font-size: 18px;
    border-radius: 12px;
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    border: none;
}

div.stButton > button:hover {
    transform: scale(1.02);
    transition: 0.2s;
}

/* Inputs */
div[data-baseweb="input"] > div {
    height: 3em;
    border-radius: 10px;
}

/* Mobile adjustments */
@media (max-width: 768px) {
    .block-container {
        padding: 0.5rem;
    }

    h1 {
        font-size: 22px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<h1>🚀 Ultimate Downloader X PRO MAX</h1>
<p style='text-align:center; font-size:18px;'>
Télécharge tes vidéos et audios facilement ⚡
</p>
""", unsafe_allow_html=True)

PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# =========================
# CLEAN OLD FILES (auto cleanup > 1h)
# =========================
for file in Path(DOWNLOAD_FOLDER).glob("*"):
    if time.time() - file.stat().st_mtime > 3600:
        file.unlink()

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    st.title("🔒 Connexion sécurisée")
    password_input = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if password_input == PASSWORD:
            st.session_state.auth = True
            st.success("Accès autorisé")
        else:
            st.error("Mot de passe incorrect")

# =========================
# MAIN APP
# =========================
if st.session_state.auth:

    st.title("🚀 Ultimate Downloader X PRO MAX")
    st.divider()

    # SIDEBAR
    st.sidebar.title("📜 Historique")
    if st.session_state.history:
        for item in st.session_state.history:
            st.sidebar.write("•", item)
        if st.sidebar.button("🗑 Supprimer historique"):
            st.session_state.history = []
    else:
        st.sidebar.info("Aucun téléchargement.")

    st.sidebar.divider()
    st.sidebar.success("Compatible avec les plateformes supportées par yt_dlp")

    # INPUTS
    url = st.text_input("🔗 URL de la vidéo")
    custom_name = st.text_input("✏ Nom personnalisé (optionnel)")
    format_choice = st.radio("Format", ["Vidéo MP4", "Audio MP3"])
    quality = st.selectbox("Qualité vidéo", ["best", "1080", "720", "480", "360"])
    bitrate = st.selectbox("Qualité audio (kbps)", ["128", "192", "256", "320"])
    download_playlist = st.checkbox("Télécharger playlist complète")

    progress = st.progress(0)
    status = st.empty()

    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded / total * 100)
                progress.progress(percent)
        if d['status'] == 'finished':
            progress.progress(100)

    if st.button("🚀 Télécharger") and url:

        try:
            status.info("Analyse de la vidéo...")

            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)

            st.subheader(info.get("title"))
            st.image(info.get("thumbnail"), width=400)
            st.write("👤 Uploader :", info.get("uploader"))
            st.write("⏱ Durée :", round(info.get("duration", 0) / 60, 2), "minutes")
            st.write("👁 Vues :", info.get("view_count"))
            st.write("🎞 Résolution :", info.get("resolution"))
            st.write("🎬 FPS :", info.get("fps"))

            filename = custom_name if custom_name else f"file_{int(time.time())}"
            output_template = f"{DOWNLOAD_FOLDER}/{filename}.%(ext)s"

            if format_choice == "Vidéo MP4":
                fmt = f"bestvideo[height<={quality}]+bestaudio/best"
                ydl_opts = {
                    'format': fmt,
                    'merge_output_format': 'mp4',
                    'outtmpl': output_template,
                    'progress_hooks': [hook],
                    'noplaylist': not download_playlist
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': output_template,
                    'progress_hooks': [hook],
                    'noplaylist': not download_playlist,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': bitrate,
                    }],
                }

            status.info("Téléchargement en cours...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            latest_file = max(Path(DOWNLOAD_FOLDER).glob(f"{filename}*"), key=os.path.getctime)

            with open(latest_file, "rb") as f:
                st.download_button("📥 Télécharger le fichier", f, file_name=latest_file.name)

            st.success("Téléchargement terminé !")
            st.session_state.history.append(info.get("title"))

        except Exception as e:
            st.error(f"Erreur : {e}")

    st.divider()
    st.caption("© 2026 DAVID EDWIN • Ultimate Downloader X PRO MAX")
