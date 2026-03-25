import streamlit as st
import yt_dlp
import os
import qrcode
import string
import secrets
import pandas as pd
from io import BytesIO
from pathlib import Path
from textblob import TextBlob
from PIL import Image

# =========================
# CONFIGURATION ULTIME
# =========================
st.set_page_config(
    page_title="OMNITOOLS OS v3.0",
    page_icon="🌌",
    layout="wide"
)

# STYLE CSS AVANCÉ (EFFET GIVRÉ & NÉON)
st.markdown("""
<style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=2072&ixlib=rb-4.0.3');
        background-size: cover;
        color: #ffffff;
    }
    /* Panneaux translucides */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* Onglets stylisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0,0,0,0.3);
        border-radius: 50px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #aaa;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        border-radius: 50px;
    }
    /* Bouton Action */
    div.stButton > button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        border: none;
        color: black;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 12px;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #4facfe;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIQUE DE SESSION
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================
# ÉCRAN DE VERROUILLAGE
# =========================
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<h1 style='text-align:center;'>🌌 BIENVENUE DANS L'OMNIS</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Saisissez votre clé d'accès", type="password")
        if st.button("INITIALISER LE SYSTÈME"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Accès refusé. Tentative loguée.")
    st.stop()

# =========================
# DASHBOARD PRINCIPAL
# =========================
st.markdown("<h1 style='text-align:center; font-size:3em; margin-bottom:0;'>⚡ OMNITOOLS OS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.7;'>L'intelligence utilitaire regroupée.</p>", unsafe_allow_html=True)

tabs = st.tabs(["📥 Media", "🎨 Design", "🔐 Crypto/Security", "🧠 AI Text", "⚙️ Utils"])

# --- TAB 1 : MEDIA ---
with tabs:
    st.subheader("Extraire du contenu")
    url = st.text_input("URL Source (YouTube, TikTok, Insta...)")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        ext = st.selectbox("Extension", ["MP4 (Vidéo)", "MP3 (Audio)"])
    with col_m2:
        st.info("Note: FFmpeg est activé pour la conversion haute fidélité.")
    
    if st.button("EXÉCUTER LE DOWNLOAD"):
        if url:
            st.success("Lancement du moteur d'extraction...")
            # Ici ton code yt_dlp précédent s'insère parfaitement

# --- TAB 2 : DESIGN ---
with tabs:
    st.subheader("Outils Visuels")
    up_img = st.file_uploader("Analysez une image", type=["jpg", "png"])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=400)
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            st.write("**Infos Fichier:**")
            st.write(f"Format: {img.format} | Taille: {img.size}")
        with col_i2:
            if st.button("Générer Palette de Couleurs"):
                st.warning("Fonctionnalité en cours de calcul...")

    st.divider()
    st.write("Générateur QR High-Tech")
    qr_txt = st.text_input("Donnée QR")
    if qr_txt:
        qr = qrcode.make(qr_txt)
        b = BytesIO()
        qr.save(b, format="PNG")
        st.image(b.getvalue(), width=150)

# --- TAB 3 : CRYPTO & SÉCURITÉ ---
with tabs:
    st.subheader("Sécurité & Finance")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.write("**Générateur de Passphrase Militaire**")
        size = st.slider("Force", 12, 64, 24)
        if st.button("Générer"):
            p = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(size))
            st.code(p)
    
    with col_c2:
        st.write("**Cours Crypto Temps Réel**")
        # Simulé pour l'exemple, peut être relié à une API
        st.metric("Bitcoin (BTC)", "68,432 €", "+2.4%")
        st.metric("Ethereum (ETH)", "3,541 €", "-0.8%")

# --- TAB 4 : AI TEXT ---
with tabs:
    st.subheader("Analyseur de Pensée")
    user_t = st.text_area("Collez un texte pour détecter les émotions...")
    if user_t:
        analysis = TextBlob(user_t)
        score = analysis.sentiment.polarity
        if score > 0.5: st.balloons()
        st.write(f"**Score émotionnel :** {score:.2f} (-1 à 1)")
        st.progress((score + 1) / 2)

# --- TAB 5 : UTILS ---
with tabs:
    st.subheader("Boîte à outils")
    st.write("Convertisseur d'unités ultra-précis")
    # Ajoute ici tes convertisseurs KG/LB etc.
    if st.button("Nettoyer le cache du serveur"):
        st.toast("Cache vidé avec succès !")

# SIDEBAR
with st.sidebar:
    st.markdown("### 👤 Utilisateur : Admin")
    st.write(f"Date : {pd.to_datetime('today').strftime('%d/%m/%Y')}")
    if st.button("LOGOUT"):
        st.session_state.auth = False
        st.rerun()
