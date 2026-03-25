import streamlit as st
import yt_dlp
import os
import qrcode
import string
import secrets
import pandas as pd
import base64
import time
from io import BytesIO
from pathlib import Path
from textblob import TextBlob
from PIL import Image, ImageOps

# ==========================================
# CONFIGURATION SYSTÈME & INTERFACE MOBILE
# ==========================================
st.set_page_config(
    page_title="OMNIS OS v5.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DESIGN GLASSMORPHISM (S'ADAPTE AUX ÉCRANS TACTILES)
st.markdown("""
<style>
    .stApp {
        background: #0d1117;
        color: #e6edf3;
    }
    /* Boutons larges pour pouces Android/iOS */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: #161b22;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
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
# DASHBOARD OMNIS (LES 16 FONCTIONS)
# ==========================================
st.markdown("<h1 style='text-align:center; color:#00d2ff; margin-bottom:0;'>⚡ OMNIS OS v5.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.6;'>MOBILE-READY MULTI-TOOLBOX</p>", unsafe_allow_html=True)

tabs = st.tabs(["📥 Media", "🎨 Studio", "🔐 Safe", "🧠 AI", "📊 Data", "🚀 Dev", "🌍 Life", "⚙️ Sys"])

# --- [F1] MEDIA DOWNLOADER ---
with tabs:
    st.subheader("📥 [F1] Media Extraction")
    url = st.text_input("Lien Vidéo/Audio", placeholder="Lien YouTube, TikTok...")
    fmt = st.selectbox("Format", ["MP4 Vidéo", "MP3 Audio"])
    if st.button("Lancer l'extraction"):
        if url:
            st.info(f"Recherche du flux pour {fmt}... (Simulé)")
            st.warning("Note: yt_dlp nécessite FFmpeg sur le serveur pour certaines conversions.")
        else:
            st.error("Veuillez entrer une URL.")

# --- [F2] STUDIO VISUEL ---
with tabs:
    st.subheader("🎨 [F2] Image Lab")
    up = st.file_uploader("Image", type=['jpg', 'jpeg', 'png'])
    if up:
        img = Image.open(up)
        st.image(img, caption="Original", use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("[F3] Noir & Blanc"): 
                st.image(img.convert('L'), caption="Grayscale")
        with c2:
            if st.button("[F4] Effet Miroir"): 
                st.image(ImageOps.mirror(img), caption="Miroir")
    
    st.divider()
    st.subheader("📷 [F5] QR Generator")
    qr_data = st.text_input("Donnée à encoder", "https://")
    if qr_data:
        qr = qrcode.make(qr_data)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.image(byte_im, width=200)
        st.download_button("Télécharger QR", byte_im, "qr_code.png", "image/png")

# --- [F6] CYBER-SÉCURITÉ ---
with tabs:
    st.subheader("🔐 [F6] Passphrase Master")
    length = st.slider("Longueur", 12, 64, 24)
    if st.button("Générer Passphrase"):
        st.code(secrets.token_urlsafe(length))
    
    st.divider()
    st.subheader("🔑 [F7] Encodeur Secret (Base64)")
    secret = st.text_input("Texte à cacher")
    if secret:
        encoded = base64.b64encode(secret.encode()).decode()
        st.code(encoded)
        if st.button("Décoder le texte ci-dessus"):
            st.write(base64.b64decode(encoded.encode()).decode())
    
    st.divider()
    if st.button("[F8] Simuler Scan Ports"):
        with st.spinner("Analyse réseau..."):
            time.sleep(1.5)
            st.warning("Port 80/TCP: Filtré | Port 443/TCP: Ouvert")

# --- [F9] AI TEXT ENGINE ---
with tabs:
    st.subheader("🧠 [F9] AI Analysis")
    txt = st.text_area("Analyse de Sentiment", placeholder="Écrivez quelque chose...")
    if txt:
        sentiment = TextBlob(txt).sentiment.polarity
        if sentiment > 0: st.success(f"Vibe Positive ({sentiment})")
        elif sentiment < 0: st.error(f"Vibe Négative ({sentiment})")
        else: st.info("Neutre")
    
    st.divider()
    if st.button("[F10] Stats de lecture"):
        if txt:
            w = len(txt.split())
            st.write(f"Mots: {w} | Temps de lecture estimé: {max(1, w//200)} min")
        else:
            st.error("Zone de texte vide.")

# --- [F11] DATA LAB ---
with tabs:
    st.subheader("📊 [F11] Data Visualizer")
    # Correction de l'erreur ID ici
    df = pd.DataFrame({
        'Composant': ['CPU', 'GPU', 'RAM'], 
        'Charge': [0.99, 0.85, 0.91]
    })
    st.table(df)
    st.bar_chart(df.set_index('Composant'))

# --- [F12] DEV LAB ---
with tabs:
    st.subheader("🚀 [F12] Syntax Checker")
    code = st.text_area("Snippet Python", "print('Hello World')", height=150)
    if st.button("Vérifier"):
        try:
            compile(code, '<string>', 'exec')
            st.success("Code Valide ✅")
        except Exception as e:
            st.error(f"Erreur : {e}")

# --- [F13] LIFE TOOLS ---
with tabs:
    st.subheader("🌍 [F13] Outils du Quotidien")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🪙 Pile ou Face"):
            st.subheader(secrets.choice(["PILE", "FACE"]))
    with c2:
        if st.button("🎲 Dé [F14]"):
            st.subheader(f"Résultat : {secrets.randbelow(6) + 1}")
    
    st.divider()
    st.subheader("📏 [F16] Quick Converter")
    val = st.number_input("Valeur en cm", value=1.0)
    st.write(f"En pouces : {val / 2.54:.2f} in")

# --- [F15] SYSTÈME ---
with tabs:
    st.subheader("⚙️ Maintenance")
    st.progress(98, text="System Stability")
    if st.button("PURGER CACHE"):
        st.cache_data.clear()
        st.toast("Mémoire libérée !")
    
    st.divider()
    st.info(f"OS Path: {os.getcwd()}")

# SIDEBAR (POUR MOBILE)
with st.sidebar:
    st.title("👤 ADMIN")
    st.write(f"Status: **En ligne**")
    if st.button("🔴 SHUTDOWN"):
        st.session_state.auth = False
        st.rerun()
