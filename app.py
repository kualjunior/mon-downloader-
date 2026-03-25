import streamlit as st
import yt_dlp
import os
import qrcode
import secrets
import pandas as pd
import base64
import time
from io import BytesIO
from textblob import TextBlob
from PIL import Image, ImageOps

# ==========================================
# CONFIGURATION SYSTÈME
# ==========================================
st.set_page_config(
    page_title="OMNIS OS v5.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DESIGN GLASSMORPHISM
st.markdown("""
<style>
    .stApp { background: #0d1117; color: #e6edf3; }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SÉCURITÉ D'ACCÈS (CORRECTION LIGNE 54)
# ==========================================
PASSWORD = "théo123"
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # CRITIQUE : Ajout de pour définir la structure des colonnes
    left, col, right = st.columns()
    with col:
        st.markdown("<h2 style='text-align:center;'>🔒 KERNEL LOCKED</h2>", unsafe_allow_html=True)
        pwd = st.text_input("PASSWORD", type="password")
        if st.button("BOOT UP"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("ACCESS DENIED")
    st.stop()

# ==========================================
# DASHBOARD OMNIS
# ==========================================
st.markdown("<h1 style='text-align:center; color:#00d2ff;'>⚡ OMNIS OS v5.0</h1>", unsafe_allow_html=True)

# Définition des onglets
tabs = st.tabs(["📥 Media", "🎨 Studio", "🔐 Safe", "🧠 AI", "📊 Data", "🚀 Dev", "🌍 Life", "⚙️ Sys"])

# --- [F1] MEDIA ---
with tabs:
    st.subheader("📥 Extraction Média")
    url = st.text_input("Lien Vidéo/Audio", placeholder="URL YouTube, TikTok...")
    if st.button("Lancer l'analyse"):
        if url:
            st.info("Analyse du flux en cours...")
        else:
            st.warning("Veuillez entrer une URL valide.")

# --- [F2] STUDIO ---
with tabs:
    st.subheader("🎨 Image Lab & QR")
    up = st.file_uploader("Charger une image", type=['jpg', 'png', 'jpeg'])
    if up:
        img = Image.open(up)
        st.image(img, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Noir & Blanc"): st.image(img.convert('L'))
        with c2:
            if st.button("Effet Miroir"): st.image(ImageOps.mirror(img))
    
    st.divider()
    qr_data = st.text_input("Générer QR Code", "https://")
    if qr_data:
        qr_img = qrcode.make(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=200)

# --- [F3] SAFE ---
with tabs:
    st.subheader("🔐 Sécurité & Chiffrement")
    if st.button("Générer Passphrase"):
        st.code(secrets.token_urlsafe(24))
    
    st.divider()
    secret_txt = st.text_input("Texte à encoder (Base64)")
    if secret_txt:
        st.code(base64.b64encode(secret_txt.encode()).decode())

# --- [F4] AI ---
with tabs:
    st.subheader("🧠 Analyse Textuelle")
    user_txt = st.text_area("Analyse de Sentiment", placeholder="Écrivez ici...")
    if user_txt:
        blob = TextBlob(user_txt)
        st.write(f"Vibe Score : {blob.sentiment.polarity}")

# --- [F5] DATA ---
with tabs:
    st.subheader("📊 Métriques Système")
    # Correction de l'erreur d'ID dictionnaire
    df = pd.DataFrame({
        'Composant': ['Kernel', 'Network', 'Uptime'],
        'Status': [99.8, 87.5, 95.0]
    })
    st.table(df)
    st.bar_chart(df.set_index('Composant'))

# --- [F6] DEV ---
with tabs:
    st.subheader("🚀 Code Sandbox")
    snippet = st.text_area("Vérificateur de Syntaxe Python", "print('Hello World')")
    if st.button("Compiler"):
        try:
            compile(snippet, '<string>', 'exec')
            st.success("Syntaxe Valide")
        except Exception as e:
            st.error(f"Erreur détectée : {e}")

# --- [F7] LIFE ---
with tabs:
    st.subheader("🌍 Utilitaires")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🪙 Pile ou Face"):
            st.title(secrets.choice(["PILE", "FACE"]))
    with col2:
        if st.button("🎲 Lancer un Dé"):
            st.title(f"Score : {secrets.randbelow(6) + 1}")

# --- [F8] SYSTEM ---
with tabs:
    st.subheader("⚙️ Maintenance")
    st.progress(98, "Stabilité OS")
    if st.button("PURGER LE CACHE"):
        st.cache_data.clear()
        st.toast("Mémoire système libérée")

# SIDEBAR
with st.sidebar:
    st.title("👤 ADMIN")
    if st.button("🔴 SHUTDOWN"):
        st.session_state.auth = False
        st.rerun()
        
