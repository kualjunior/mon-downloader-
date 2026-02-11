import streamlit as st
import yt_dlp
import os
import time
from pathlib import Path

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Ultimate Downloader X",
    page_icon="🚀",
    layout="wide"
)

DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# =========================
# STYLE ULTRA PREMIUM BLEU
# =========================
st.markdown("""
<style>

/* Background sombre premium */
body {
    background: linear-gradient(135deg,#0f2027,#1c2b36,#141E30);
}

/* DAVID EDWIN énorme bleu néon */
@keyframes blueGlow {
    0% { text-shadow: 0 0 10px #00c6ff, 0 0 20px #0072ff; }
    50% { text-shadow: 0 0 40px #00c6ff, 0 0 80px #0072ff; }
    100% { text-shadow: 0 0 10px #00c6ff, 0 0 20px #0072ff; }
}

.david-name {
    font-size: 5.5em;
    font-weight: 900;
    text-align: center;
    color: #00c6ff;
    animation: blueGlow 2s infinite alternate;
    margin-bottom: 0;
    letter-spacing: 5px;
}

.subtitle {
    text-align: center;
    font-size: 1.5em;
    color: #cccccc;
    letter-spacing: 3px;
}

/* Boutons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    background: linear-gradient(90deg,#0072ff,#00c6ff);
    color: white;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px #00c6ff;
}

.stDownloadButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    font-weight: bold;
    border: none;
}

/* Card style */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    margin-top: 20px;
}

/* Footer */
.footer {
    text-align: center;
    opacity: 0.6;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER SIGNATURE
# =========================
st.markdown('<p class="david-name">DAVID EDWIN</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ultimate Downloader X • Founder & Developer</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# INPUT URL
# =========================
st.markdown('<div class="glass">', unsafe_allow_html=True)
url = st.text_input("🔗 Collez votre lien ici")
format_choice = st.radio("Choisissez le format :", ["MP4 🎥 (Vidéo)", "MP3 🎵 (Audio)"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TELECHARGEMENT
# =========================
if url:
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        st.image(info.get("thumbnail"), use_container_width=True)
        st.subheader(info.get("title"))

        if st.button("🚀 Lancer le téléchargement"):

            progress = st.progress(0)

            def hook(d):
                if d['status'] == 'downloading':
                    percent = d.get('_percent_str', '0%').replace('%','')
                    try:
                        progress.progress(int(float(percent)))
                    except:
                        pass

            filename = f"{DOWNLOAD_FOLDER}/file_{int(time.time())}.%(ext)s"

            # MP4
            if "MP4" in format_choice:
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                    'outtmpl': filename,
                    'progress_hooks': [hook],
                }

            # MP3
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

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            final_file = max(Path(DOWNLOAD_FOLDER).glob("file_*"), key=os.path.getctime)

            with open(final_file, "rb") as f:
                st.download_button("📥 Télécharger maintenant", f, file_name=final_file.name)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
© 2026 DAVID EDWIN • Ultimate Downloader X  
Application officielle développée par DAVID EDWIN
</div>
""", unsafe_allow_html=True)
