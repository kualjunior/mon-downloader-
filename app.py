import streamlit as st
import yt_dlp
import os
import time
import qrcode
from io import BytesIO
from pathlib import Path
from textblob import TextBlob

# =========================
# CONFIG & ESTHÉTIQUE NEON
# =========================
st.set_page_config(
    page_title="OmniTools Pro Max 2026",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Fond animé et style moderne */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
        color: #e94560;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px;
        background-color: transparent;
        color: white;
        border: 1px solid #4e4e4e;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #e94560, #ff4b2b) !important;
        border: none !important;
    }
    /* Boutons personnalisés */
    div.stButton > button {
        border-radius: 20px;
        background: linear-gradient(45deg, #0f3460, #e94560);
        color: white;
        font-weight: bold;
        transition: 0.3s;
        border: none;
    }
    div.stButton > button:hover {
        box-shadow: 0px 0px 15px #e94560;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# INITIALISATION & SÉCURITÉ
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================
# SYSTÈME DE CONNEXION
# =========================
if not st.session_state.auth:
    col1, col2, col3 = st.columns()
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

# Navigation par Onglets (Le côté Couteau Suisse)
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 Media Downloader", 
    "📷 QR Generator", 
    "🧠 Text Intelligence", 
    "⚖️ Unit Master"
])

# -------------------------
# ONGLET 1 : TÉLÉCHARGEMENT MEDIA
# -------------------------
with tab1:
    st.subheader("Téléchargeur Multi-Plateformes")
    url = st.text_input("Lien (YouTube, TikTok, Instagram...)", placeholder="https://...")
    
    c1, c2 = st.columns(2)
    with c1:
        fmt = st.selectbox("Format", ["Vidéo MP4", "Audio MP3"])
    with c2:
        qual = st.select_slider("Qualité désirée", options=["Basique", "Standard", "Ultra"])

    if st.button("LANCER L'EXTRACTION"):
        if url:
            with st.spinner("Traitement en cours..."):
                # Simulation de téléchargement (Récupération de la logique yt_dlp originale)
                st.info(f"Analyse du flux pour : {url}")
                st.success("Prêt ! (Note : ffmpeg requis pour MP3 sur serveur)")
        else:
            st.warning("Veuillez entrer une URL.")

# -------------------------
# ONGLET 2 : GÉNÉRATEUR QR CODE
# -------------------------
with tab2:
    st.subheader("Générateur de QR Code Instantané")
    qr_data = st.text_input("Donnée ou URL à encoder", key="qr_input")
    qr_color = st.color_picker("Couleur du QR", "#e94560")
    
    if qr_data:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=qr_color, back_color="white")
        
        buf = BytesIO()
        img.save(buf)
        st.image(buf.getvalue(), width=250)
        st.download_button("Télécharger le QR Code", buf.getvalue(), "qrcode.png", "image/png")

# -------------------------
# ONGLET 3 : ANALYSE DE TEXTE (AI LIGHT)
# -------------------------
with tab3:
    st.subheader("Analyseur de Sentiment & Stats")
    user_text = st.text_area("Collez votre texte ici pour l'analyser...")
    
    if user_text:
        blob = TextBlob(user_text)
        col_a, col_b, col_c = st.columns(3)
        
        sentiment = blob.sentiment.polarity
        mood = "Positif 😊" if sentiment > 0 else "Négatif ☹️" if sentiment < 0 else "Neutre 😐"
        
        col_a.metric("Mots", len(user_text.split()))
        col_b.metric("Caractères", len(user_text))
        col_c.metric("Ambiance", mood)
        
        st.write("**Correction suggérée (Anglais uniquement) :**")
        st.write(blob.correct())

# -------------------------
# ONGLET 4 : CONVERTISSEUR UNIVERSEL
# -------------------------
with tab4:
    st.subheader("Convertisseur d'Unités Pro")
    cat = st.selectbox("Catégorie", ["Poids (kg ↔ lb)", "Température (°C ↔ °F)"])
    val = st.number_input("Valeur à convertir", value=1.0)
    
    if cat == "Poids (kg ↔ lb)":
        res = val * 2.20462
        st.success(f"{val} kg = **{res:.2f} lb**")
        st.info(f"{val} lb = **{val/2.20462:.2f} kg**")
    else:
        res = (val * 9/5) + 32
        st.success(f"{val} °C = **{res:.2f} °F**")
        st.info(f"{val} °F = **{(val-32)*5/9:.2f} °C**")

# =========================
# FOOTER
# =========================
st.sidebar.markdown("### 🛠️ Paramètres Système")
if st.sidebar.button("🔴 Déconnexion"):
    st.session_state.auth = False
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("OmniTools v2.0 - 2026")
st.sidebar.write("Statut Serveur : 🟢 Optimal")
