import streamlit as st
import yt_dlp
import os
import time

# Configuration de la page
st.set_page_config(page_title="Ultimate Downloader", page_icon="🚀", layout="wide")

# Style personnalisé pour le look "Magnifique"
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF4B4B; color: white; border: none; }
    .stDownloadButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #00c853; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Ultimate Video Downloader")
st.write("Téléchargez vos contenus préférés en un clic, directement sur votre téléphone.")

# 1. Entrée du lien
url = st.text_input("🔗 Collez votre lien ici :", placeholder="YouTube, TikTok, Instagram...")

if url:
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            
        # 2. Affichage des infos (Fonctionnalité Info)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info.get('thumbnail', ''), use_container_width=True)
        with col2:
            st.subheader(info.get('title', 'Vidéo sans titre'))
            st.write(f"👤 **Auteur :** {info.get('uploader', 'Inconnu')}")
            st.write(f"⏱️ **Durée :** {info.get('duration_string', 'N/A')}")

        # 3. Choix des options (Onglets)
        tab1, tab2 = st.tabs(["🎥 Vidéo", "🎵 Audio MP3"])

        with tab1:
            # 4. Choix de la qualité
            quality = st.radio("Qualité :", ["Haute Qualité (HD)", "Économie de données (LQ)"], horizontal=True)
            if st.button("🚀 Préparer la Vidéo"):
                with st.spinner("Traitement en cours..."):
                    fmt = 'best' if "HD" in quality else 'worst'
                    filename = f"video_{int(time.time())}.mp4"
                    
                    ydl_opts = {'format': fmt, 'outtmpl': filename, 'noplaylist': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    # 5. Bouton de téléchargement final
                    with open(filename, "rb") as f:
                        st.download_button("📥 Enregistrer la vidéo", f, file_name=filename)
                    os.remove(filename)

        with tab2:
            if st.button("🎵 Extraire le MP3"):
                with st.spinner("Conversion audio..."):
                    filename = f"audio_{int(time.time())}.mp3"
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': filename,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    with open(filename, "rb") as f:
                        st.download_button("📥 Enregistrer le MP3", f, file_name=filename)
                    os.remove(filename)

    except Exception as e:
        st.error(f"❌ Désolé, cette vidéo est protégée ou le lien est mort. Erreur : {e}")

# Bas de page
st.divider()
st.caption("Application hébergée dans le Cloud - Votre ordinateur peut rester éteint.")
