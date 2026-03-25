import streamlit as st
import yt_dlp
import os
import time
import qrcode
import string
import secrets
from io import BytesIO
from pathlib import Path
from textblob import TextBlob

# =========================
# CONFIG & ESTHÉTIQUE
# =========================
st.set_page_config(
    page_title="OmniTools Pro Max 2026",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #e94560, #ff4b2b) !important;
        border: none !important;
    }
    div.stButton > button {
        border-radius: 20px;
        background: linear-gradient(45deg, #0f3460, #e94560);
        color: white;
        border: none;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# INITIALISATION
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================
# CONNEXION
# =========================
if not st.session_state.auth:
  _, col2, _ = st.columns()
    with col2:
        st.markdown("<h1 style='text-align:center;'>🔐 ACCÈS OMNITOOLS</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Clé d'accès", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Accès refusé.")
    st.stop()

# =========================
# INTERFACE PRINCIPALE
# =========================
st.markdown("<h1 style='text-align:center; color:#e94560;'>🚀 OMNITOOLS PRO MAX</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Media Downloader", 
    "📷 QR Generator", 
    "🧠 Text Intelligence", 
    "⚖️ Unit Master",
    "🔐 Password Gen"
])

# -------------------------
# ONGLET 1 : TÉLÉCHARGEMENT REEL
# -------------------------
with tab1:
    st.subheader("Téléchargeur Multi-Plateformes")
    url = st.text_input("Lien (YouTube, TikTok, Instagram...)", placeholder="https://...")
    c1, c2 = st.columns(2)
    with c1:
        fmt_choice = st.selectbox("Format", ["Vidéo MP4", "Audio MP3"])
    with c2:
        qual = st.select_slider("Qualité", options=["Basse", "Standard", "Haute"])

    if st.button("LANCER L'EXTRACTION"):
        if url:
            with st.spinner("Téléchargement et conversion en cours..."):
                try:
                    # Configuration yt_dlp
                    ydl_opts = {
                        'format': 'bestvideo+bestaudio/best' if fmt_choice == "Vidéo MP4" else 'bestaudio/best',
                        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                        'quiet': True,
                    }
                    if fmt_choice == "Audio MP3":
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        temp_file = ydl.prepare_filename(info)
                        # Ajustement de l'extension pour le MP3
                        final_file = temp_file.rsplit('.', 1) + ".mp3" if fmt_choice == "Audio MP3" else temp_file

                    with open(final_file, "rb") as f:
                        st.download_button("💾 Télécharger le fichier final", f, file_name=os.path.basename(final_file))
                    st.success("Prêt !")
                except Exception as e:
                    st.error(f"Erreur : {e}")
        else:
            st.warning("Entrez une URL.")

# -------------------------
# ONGLET 2 : QR CODE
# -------------------------
with tab2:
    st.subheader("Générateur de QR Code")
    qr_data = st.text_input("Donnée à encoder", key="qr_in")
    if qr_data:
        qr = qrcode.make(qr_data)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=200)
        st.download_button("Télécharger QR", buf.getvalue(), "code.png")

# -------------------------
# ONGLET 3 : TEXTE
# -------------------------
with tab3:
    st.subheader("Analyseur de Texte")
    txt = st.text_area("Texte à analyser")
    if txt:
        blob = TextBlob(txt)
        st.write(f"Mots : {len(txt.split())} | Sentiment : {'😊' if blob.sentiment.polarity > 0 else '😐'}")

# -------------------------
# ONGLET 4 : UNITÉS
# -------------------------
with tab4:
    st.subheader("Convertisseur")
    v = st.number_input("Valeur (KG)", value=1.0)
    st.write(f"{v} KG = {v * 2.20462:.2f} Lbs")

# -------------------------
# ONGLET 5 : PASSWORD GEN (NOUVEAU)
# -------------------------
with tab5:
    st.subheader("Générateur de Sécurité")
    length = st.slider("Longueur", 8, 32, 16)
    if st.button("Générer un mot de passe"):
        chars = string.ascii_letters + string.digits + string.punctuation
        pwd_gen = ''.join(secrets.choice(chars) for _ in range(length))
        st.code(pwd_gen)
        st.warning("Copiez-le en lieu sûr !")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.markdown("### 🛠️ Système")
if st.sidebar.button("🔴 Déconnexion"):
    st.session_state.auth = False
    st.rerun()
st.sidebar.divider()
st.sidebar.caption("OmniTools v2.0 - 2026")
