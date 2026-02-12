import streamlit as st
import yt_dlp
import os
import time
from pathlib import Path

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Ultimate Downloader X PRO MAX",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.block-container {
    padding-top: 1.5rem;
    max-width: 800px;
}
h1, h2, h3 { text-align: center; }
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
</style>
""", unsafe_allow_html=True)

# =========================
# CONSTANTS
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# =========================
# CLEAN OLD FILES (>1h)
# =========================
for file in Path(DOWNLOAD_FOLDER).glob("*"):
    try:
        if file.is_file() and time.time() - file.stat().st_mtime > 3600:
            file.unlink()
    except:
        pass

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
    st.markdown("<h1>🔒 Connexion sécurisée</h1>", unsafe_allow_html=True)
    password_input = st.text_input("Mot de passe", type="password")

    if st.button("Connexion"):
        if password_input == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect")

# =========================
# MAIN APP
# =========================
if st.session_state.auth:

    st.markdown("<h1>🚀 Ultimate Downloader X PRO MAX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Télécharge tes vidéos et audios facilement ⚡</p>", unsafe_allow_html=True)
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

    col1, col2 = st.columns(2)

    with col1:
        format_choice = st.radio("Format", ["Vidéo MP4", "Audio MP3"])

    with col2:
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
        elif d['status'] == 'finished':
            progress.progress(100)

    if st.button("🚀 Télécharger") and url:

        try:
            status.info("Analyse de la vidéo...")

            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)

            st.subheader(info.get("title", "Vidéo"))
            if info.get("thumbnail"):
                st.image(info.get("thumbnail"), use_container_width=True)

            duration = info.get("duration")
            if duration:
                st.write("⏱ Durée :", round(duration / 60, 2), "minutes")

            filename = custom_name.strip() if custom_name else f"file_{int(time.time())}"
            output_template = f"{DOWNLOAD_FOLDER}/{filename}.%(ext)s"

            # FORMAT FIX
            if format_choice == "Vidéo MP4":
                if quality == "best":
                    fmt = "bestvideo+bestaudio/best"
                else:
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

            files = list(Path(DOWNLOAD_FOLDER).glob(f"{filename}*"))
            if files:
                latest_file = max(files, key=os.path.getctime)

                with open(latest_file, "rb") as f:
                    st.download_button(
                        "📥 Télécharger le fichier",
                        f,
                        file_name=latest_file.name
                    )

                st.success("Téléchargement terminé ✅")
                st.session_state.history.append(info.get("title", "Vidéo"))

            else:
                st.error("Fichier introuvable après téléchargement.")

        except Exception as e:
            st.error(f"Erreur : {e}")

    st.divider()
    st.caption("© 2026 DAVID EDWIN • Ultimate Downloader X PRO MAX")
