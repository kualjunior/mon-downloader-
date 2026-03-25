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
    .stTextInput>div>div>input {
        background-color: #0d1117;
        color: #00ffcc;
        border: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SÉCURITÉ D'ACCÈS
# ==========================================
PASSWORD = "théo123"
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns()
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

tabs = st.tabs(["📥 Media", "🎨 Studio", "🔐 Safe", "🧠 AI", "📊 Data", "🚀 Dev", "🌍 Life", "⚙️ Sys"])

# --- [F1] MEDIA ---
with tabs:
    st.subheader("📥 Extraction Média")
    url = st.text_input("Lien Vidéo/Audio", placeholder="URL YouTube...")
    if st.button("Lancer l'analyse"):
        st.info("Recherche du flux en cours...")

# --- [F2-F5] STUDIO ---
with tabs:
    st.subheader("🎨 Image Lab & QR")
    up = st.file_uploader("Charger une image", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        st.image(img, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Noir & Blanc"): st.image(img.convert('L'))
        with c2:
            if st.button("Effet Miroir"): st.image(ImageOps.mirror(img))
    
    st.divider()
    qr_data = st.text_input("QR Code Data", "https://")
    if qr_data:
        qr = qrcode.make(qr_data)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=150)

# --- [F6-F8] SAFE ---
with tabs:
    st.subheader("🔐 Sécurité")
    if st.button("Générer Mot de Passe"):
        st.code(secrets.token_urlsafe(20))
    
    st.divider()
    secret_txt = st.text_input("Encoder en Base64")
    if secret_txt:
        st.code(base64.b64encode(secret_txt.encode()).decode())

# --- [F9-F10] AI ---
with tabs:
    st.subheader("🧠 Analyse AI")
    user_txt = st.text_area("Texte à analyser")
    if user_txt:
        blob = TextBlob(user_txt)
        st.write(f"Polarité (Sentiment) : {blob.sentiment.polarity}")
        if st.button("Stats de lecture"):
            mots = len(user_txt.split())
            st.write(f"Mots : {mots} | Temps estimé : {max(1, mots//200)} min")

# --- [F11] DATA ---
with tabs:
    st.subheader("📊 Performance Système")
    df = pd.DataFrame({
        'Composant': ['Système', 'Réseau', 'Kernel'],
        'Valeur': [99.9, 85.2, 91.0]
    })
    st.table(df)
    st.bar_chart(df.set_index('Composant'))

# --- [F12] DEV ---
with tabs:
    st.subheader("🚀 Dev Check")
    code_input = st.text_area("Snippet Python", "print('Hello')")
    if st.button("Check Syntax"):
        try:
            compile(code_input, '<string>', 'exec')
            st.success("Syntaxe OK")
        except Exception as e:
            st.error(f"Erreur : {e}")

# --- [F13-F14] LIFE ---
with tabs:
    st.subheader("🌍 Utilitaires")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🪙 Pile ou Face"): st.title(secrets.choice(["PILE", "FACE"]))
    with col_b:
        if st.button("🎲 Dé"): st.title(f"Score : {secrets.randbelow(6) + 1}")

# --- [F15] SYSTEM ---
with tabs:
    st.subheader("⚙️ Maintenance")
    st.progress(98, "Stabilité")
    if st.button("PURGER CACHE"):
        st.cache_data.clear()
        st.toast("Cache vidé avec succès !")

# SIDEBAR
with st.sidebar:
    st.title("👤 ADMIN")
    if st.button("🔴 SHUTDOWN"):
        st.session_state.auth = False
        st.rerun()
