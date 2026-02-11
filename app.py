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
# STYLE ULTRA PREMIUM + SIGNATURE
# =========================
st.markdown("""
<style>

/* Background animé */
body {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #141E30);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass effect */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255,255,255,0.18);
}

/* Boutons premium */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    background: linear-gradient(90deg,#ff416c,#ff4b2b);
    color: white;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #ff4b2b;
}

.stDownloadButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(90deg,#00c853,#64dd17);
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stDownloadButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00e676;
}

/* DAVID EDWIN Glow */
@keyframes glow {
    0% { text-shadow: 0 0 5px #ff416c, 0 0 10px #ff4b2b; }
    50% { text-shadow: 0 0 25px #ff416c, 0 0 40px #ff4b2b; }
    100% { text-shadow: 0 0 5px #ff416c, 0 0 10px #ff4b2b; }
}

.david-name {
    font-size: 3.5em;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#ff416c,#ff4b2b,#ff416c);
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    animation: glow 2s infinite alternate;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-size: 1.2em;
    color: #cccccc;
    letter-spacing: 2px;
}

.badge {
    display: inline-block;
    padding: 8px 20px;
    border-radius: 30px;
    background: linear-gradient(90deg,#00c853,#64dd17);
    color: black;
    font-weight: bold;
    font-size: 0.9em;
    margin-top: 10px;
}

.footer-signature {
    text-align: center;
    font-size: 0.9em;
    opacity: 0.6;
    margin-top: 50px;
}

section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER SIGNATURE
# =========================
st.markdown('<p class="david-name">DAVID EDWIN</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ultimate Downloader X</p>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center;'><span class='badge'>Founder & Developer</span></div>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# =========================
# SIDEBAR SIGNATURE
# =========================
st.sidebar.markdown("## 👑 DAVID EDWIN")
st.sidebar.markdown("Founder & Developer")
st.sidebar.markdown("---")

# =========================
# INPUT URL
# =========================
st.markdown('<div class="glass">', unsafe_allow_html=True)
url = st.text_input("🔗 Collez votre lien ici")
st.markdown('</div>', unsafe_allow_html=True)

if url:
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,2])

        with col1:
            st.image(info.get("thumbnail"), use_container_width=True)

        with col2:
            st.markdown(f"""
            <div class="glass">
                <h3>{info.get("title")}</h3>
                👤 {info.get("uploader")} <br>
                ⏱️ {info.get("duration_string")} <br>
                👀 {info.get("view_count")} vues
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🎥 Télécharger Vidéo", "🎵 Télécharger Audio"])

        # VIDEO
        with tab1:
            st.markdown('<div class="glass">', unsafe_allow_html=True)

            quality = st.selectbox("Qualité :", ["1080", "720", "480", "360"])
            format_video = st.selectbox("Format :", ["mp4", "mkv", "webm"])

            if st.button("🚀 Télécharger la Vidéo"):
                progress = st.progress(0)

                def hook(d):
                    if d['status'] == 'downloading':
                        percent = d.get('_percent_str', '0%').replace('%','')
                        try:
                            progress.progress(int(float(percent)))
                        except:
                            pass

                filename = f"{DOWNLOAD_FOLDER}/video_{int(time.time())}.%(ext)s"

                ydl_opts = {
                    'format': f'bestvideo[height<={quality}]+bestaudio/best',
                    'merge_output_format': format_video,
                    'outtmpl': filename,
                    'progress_hooks': [hook],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                final_file = max(Path(DOWNLOAD_FOLDER).glob("video_*"), key=os.path.getctime)

                with open(final_file, "rb") as f:
                    st.download_button("📥 Télécharger maintenant", f, file_name=final_file.name)

            st.markdown('</div>', unsafe_allow_html=True)

        # AUDIO
        with tab2:
            st.markdown('<div class="glass">', unsafe_allow_html=True)

            audio_format = st.selectbox("Format audio :", ["mp3", "wav", "m4a"])
            bitrate = st.selectbox("Qualité :", ["128", "192", "256", "320"])

            if st.button("🎵 Télécharger Audio"):
                progress = st.progress(0)

                def hook(d):
                    if d['status'] == 'downloading':
                        percent = d.get('_percent_str', '0%').replace('%','')
                        try:
                            progress.progress(int(float(percent)))
                        except:
                            pass

                filename = f"{DOWNLOAD_FOLDER}/audio_{int(time.time())}.%(ext)s"

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': filename,
                    'progress_hooks': [hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': audio_format,
                        'preferredquality': bitrate,
                    }],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                final_file = max(Path(DOWNLOAD_FOLDER).glob("audio_*"), key=os.path.getctime)

                with open(final_file, "rb") as f:
                    st.download_button("📥 Télécharger maintenant", f, file_name=final_file.name)

            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer-signature">
© 2026 DAVID EDWIN • Ultimate Downloader X • All Rights Reserved  
Développé avec passion 🔥
</div>
""", unsafe_allow_html=True)
