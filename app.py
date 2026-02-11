import streamlit as st
import yt_dlp
import os
import time
from pathlib import Path

# =========================
# CONFIGURATION PAGE
# =========================
st.set_page_config(
    page_title="Ultimate Downloader X",
    page_icon="🚀",
    layout="wide"
)

DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

# =========================
# STYLE CYBER FUTURISTE
# =========================
st.markdown("""
<style>

/* BODY: fond animé, gradient + étoiles */
body {
    margin:0;
    background: radial-gradient(circle at top, #0f2027, #141E30 70%);
    background-size: 400% 400%;
    animation: gradientBG 20s ease infinite;
    font-family: 'Arial', sans-serif;
    color: white;
}

@keyframes gradientBG {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

/* NOM DAVID EDWIN 3D NEON BLEU */
@keyframes neonGlow {
    0% {
        text-shadow: 0 0 5px #00c6ff,0 0 10px #00c6ff,0 0 20px #0072ff,0 0 40px #0072ff;
        transform: rotateY(0deg);
    }
    50% {
        text-shadow: 0 0 20px #00e0ff,0 0 40px #00e0ff,0 0 80px #0099ff,0 0 120px #0099ff;
        transform: rotateY(5deg);
    }
    100% {
        text-shadow: 0 0 5px #00c6ff,0 0 10px #00c6ff,0 0 20px #0072ff,0 0 40px #0072ff;
        transform: rotateY(0deg);
    }
}

.david-name {
    font-size: 8em;
    font-weight: 900;
    text-align: center;
    color: #00c6ff;
    animation: neonGlow 3s infinite alternate;
    letter-spacing: 8px;
    margin-bottom: 0;
}

/* Sous-titre futuriste */
.subtitle {
    text-align: center;
    font-size: 1.8em;
    color: #cccccc;
    letter-spacing: 4px;
    margin-bottom: 20px;
}

/* Carte centrale glass */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 30px;
    margin: auto;
    max-width: 800px;
    box-shadow: 0 0 50px rgba(0,198,255,0.6);
    border: 1px solid rgba(0,198,255,0.3);
}

/* Boutons futuristes */
.stButton>button {
    width: 100%;
    border-radius: 15px;
    height: 3.2em;
    font-weight: bold;
    font-size: 1em;
    background: linear-gradient(90deg,#0072ff,#00c6ff);
    color: white;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 30px #00c6ff;
}

.stDownloadButton>button {
    width: 100%;
    border-radius: 15px;
    height: 3.2em;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

/* Progress bar glow */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    box-shadow: 0 0 15px #00c6ff;
}

/* Footer futuriste */
.footer {
    text-align: center;
    font-size: 0.95em;
    opacity: 0.7;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER AVEC NOM + LOGO
# =========================
st.markdown('<p class="david-name">David Edwin</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ultimate Downloader X • Founder & Developer</p>', unsafe_allow_html=True)

# =========================
# CARTE CENTRALE POUR URL + FORMAT
# =========================
st.markdown('<div class="glass">', unsafe_allow_html=True)
url = st.text_input("🔗 Collez votre lien ici")
format_choice = st.radio("Choisissez le format :", ["MP4 🎥", "MP3 🎵"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TELECHARGEMENT AVEC PROGRESS BAR
# =========================
if url:
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        st.image(info.get("thumbnail"), use_container_width=True)
        st.subheader(info.get("title"))

        if st.button("🚀 Télécharger maintenant"):

            progress = st.progress(0)

            def hook(d):
                if d['status'] == 'downloading':
                    percent = d.get('_percent_str', '0%').replace('%','')
                    try:
                        progress.progress(int(float(percent)))
                    except:
                        pass

            filename = f"{DOWNLOAD_FOLDER}/file_{int(time.time())}.%(ext)s"

            if "MP4" in format_choice:
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
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

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            final_file = max(Path(DOWNLOAD_FOLDER).glob("file_*"), key=os.path.getctime)

            with open(final_file, "rb") as f:
                st.download_button("📥 Télécharger maintenant", f, file_name=final_file.name)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")

# =========================
# FOOTER FUTURISTE
# =========================
st.markdown("""
<div class="footer">
© 2026 David Edwin • Ultimate Downloader X  
Développé avec passion par David Edwin
</div>
""", unsafe_allow_html=True)
