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

# DESIGN (ADAPTÉ MOBILE)
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
# SÉCURITÉ D'ACCÈS (Ligne 58 Corrigée)
# ==========================================
PASSWORD = "théo123"
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # CORRECTION : On précise 3 colonnes pour centrer le login
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
# DASHBOARD OMNIS (Structure corrigée)
# ==========================================
st.markdown("<h1 style='text-align:center; color:#00d2ff;'>⚡ OMNIS OS v5.0</h1>", unsafe_allow_html=True)

# Création des onglets
tabs = st.tabs(["📥 Media", "🎨 Studio", "🔐 Safe", "🧠 AI", "📊 Data", "🚀 Dev", "🌍 Life", "⚙️ Sys"])

# --- [F1] MEDIA ---
with tabs:
    st.subheader("📥 Extraction Média")
    url = st.text_input("Lien Vidéo/Audio", placeholder="Lien YouTube, TikTok...")
    if st.button("Lancer l'extraction"):
        st.info("Recherche du flux... (Simulé)")

# --- [F2-F5] STUDIO ---
with tabs:
    st.subheader("🎨 Image Lab & QR")
    up = st.file_uploader("Image", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        st.image(img, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Noir & Blanc"): st.image(img.convert('L'))
        with c2:
            if st.button("Effet Miroir"): st.image(ImageOps.mirror(img))
    
    st.divider()
    qr_data = st.text_input("QR Data", "https://")
    if qr_data:
        qr_img = qrcode.make(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=150)

# --- [F6-F8] SAFE ---
with tabs:
    st.subheader("🔐 Cyber-Sécurité")
    if st.button("Générer Passphrase"):
        st.code(secrets.token_urlsafe(20))
    st.divider()
    secret = st.text_input("Encoder en B64")
    if secret:
        st.code(base64.b64encode(secret.encode()).decode())

# --- [F9-F10] AI ---
with tabs:
    st.subheader("🧠 Intelligence")
    txt = st.text_area("Analyse Sentiment")
    if txt:
        st.write(f"Vibe Score: {TextBlob(txt).sentiment.polarity}")

# --- [F11] DATA (Correction erreur ID) ---
with tabs:
    st.subheader("📊 Performance")
    df = pd.DataFrame({
        'Composant': ['Système', 'Réseau', 'Kernel'],
        'Score': [99.9, 85.2, 91.0]
    })
    st.table(df)
    st.bar_chart(df.set_index('Composant'))

# --- [F12] DEV ---
with tabs:
    st.subheader("🚀 Dev Lab")
    code_input = st.text_area("Snippet Python", "print('Hello')")
    if st.button("Vérifier"):
        try: compile(code_input, '', 'exec'); st.success("Syntaxe OK")
        except Exception as e: st.error(f"Erreur: {e}")

# --- [F13-F14] LIFE ---
with tabs:
    st.subheader("🌍 Quotidien")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🪙 Pile/Face"): st.title(secrets.choice(["PILE", "FACE"]))
    with c2:
        if st.button("🎲 Dé"): st.title(f"Dés: {secrets.randbelow(6)+1}")

# --- [F15] SYSTÈME ---
with tabs:
    st.subheader("⚙️ Maintenance")
    st.progress(98, "Système Stable")
    if st.button("PURGER CACHE"):
        st.cache_data.clear()
        st.toast("Cache vidé !")

# SIDEBAR
with st.sidebar:
    st.title("👤 ADMIN")
    if st.button("🔴 SHUTDOWN"):
        st.session_state.auth = False
        st.rerun()
