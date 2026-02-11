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

DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# HEADER
# =========================
st.title("🚀 Ultimate Downloader X - PRO Edition")
st.caption("Founder & Developer : DAVID EDWIN")

st.divider()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📜 Historique")

if st.session_state.history:
    for item in st.session_state.history:
        st.sidebar.write("•", item)
else:
    st.sidebar.info("Aucun téléchargement pour le moment.")

st.sidebar.divider()
st.sidebar.success("✔ Compatible YouTube, TikTok, Facebook, Instagram")

# =========================
# INPUT
# =========================
urls = st.text_area("🔗 Collez un ou plusieurs liens (1 par ligne)")

format_choice = st.radio(
    "Format :",
    ["MP4 🎥 (Vidéo)", "MP3 🎵 (Audio)"],
    horizontal=True
)

quality = st.selectbox(
    "🎞️ Qualité vidéo",
    ["Best", "1080p", "720p", "480p", "360p"]
)

st.divider()

# =========================
# TELECHARGEMENT
# =========================
if urls:
    url_list = [u.strip() for u in urls.split("\n") if u.strip()]

    if st.button("🚀 Lancer le téléchargement PRO"):

        progress = st.progress(0)
        status_text = st.empty()

        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = int(downloaded / total * 100)
                    progress.progress(percent)

        try:
            for url in url_list:

                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)

                st.subheader(info.get("title"))
                st.image(info.get("thumbnail"), width=400)

                duration = info.get("duration", 0)
                views = info.get("view_count", 0)
                uploader = info.get("uploader", "Unknown")

                st.write(f"👤 Chaîne : {uploader}")
                st.write(f"⏱️ Durée : {duration//60} min")
                st.write(f"👁️ Vues : {views}")

                # Choix qualité
                if quality == "1080p":
                    format_string = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
                elif quality == "720p":
                    format_string = "bestvideo[height<=720]+bestaudio/best[height<=720]"
                elif quality == "480p":
                    format_string = "bestvideo[height<=480]+bestaudio/best[height<=480]"
                elif quality == "360p":
                    format_string = "bestvideo[height<=360]+bestaudio/best[height<=360]"
                else:
                    format_string = "best"

                filename = f"{DOWNLOAD_FOLDER}/file_{int(time.time())}.%(ext)s"

                if "MP4" in format_choice:
                    ydl_opts = {
                        'format': format_string,
                        'merge_output_format': 'mp4',
                        'outtmpl': filename,
                        'progress_hooks': [hook],
                    }
                else:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': filename,
                        'progress_hooks': [hook],
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }

                status_text.info("⏳ Téléchargement en cours...")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                final_file = max(Path(DOWNLOAD_FOLDER).glob("file_*"), key=os.path.getctime)

                with open(final_file, "rb") as f:
                    st.download_button(
                        "📥 Télécharger maintenant",
                        f,
                        file_name=final_file.name
                    )

                st.success("✅ Téléchargement terminé avec succès !")
                st.session_state.history.append(info.get("title"))

            progress.empty()
            status_text.empty()
            st.balloons()

        except Exception as e:
            st.error(f"❌ Erreur : {e}")
