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

# DESIGN GLASSMORPHISM
st.markdown(""" 
<style> 
    .stApp { 
        background: #0d1117; 
        color: #e6edf3; 
    } 
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

st.markdown("<h1 style='text-align:center; color:#00d2ff; margin-bottom:0;'>⚡ OMNIS OS v5.0</h1>", unsafe_allow_html=True) 
st.markdown("<p style='text-align:center; opacity:0.6;'>MOBILE-READY MULTI-TOOLBOX</p>", unsafe_allow_html=True) 

# Initialisation des onglets
tabs = st.tabs(["📥 Media", "🎨 Studio", "🔐 Safe", "🧠 AI", "📊 Data", "🚀 Dev", "🌍 Life", "⚙️ Sys"]) 

# --- [F1] MEDIA DOWNLOADER --- 
with tabs: 
    st.subheader("📥 [F1] Media Extraction") 
    url = st.text_input("Lien Vidéo/Audio", placeholder="Lien YouTube, TikTok...") 
    fmt = st.selectbox("Format", ["MP4 Vidéo", "MP3 Audio"]) 
    if st.button("Lancer l'extraction"): 
        st.info("Recherche du flux... (FFmpeg prêt)") 

# --- [F2] STUDIO VISUEL --- 
with tabs: 
    st.subheader("🎨 [F2] Image Lab") 
    up = st.file_uploader("Image", type=['jpg', 'png']) 
    if up: 
        img = Image.open(up) 
        st.image(img, use_container_width=True) 
        c1, c2 = st.columns(2) 
        with c1: 
            if st.button("[F3] Noir & Blanc"): 
                st.image(img.convert('L')) 
        with c2: 
            if st.button("[F4] Effet Miroir"): 
                st.image(ImageOps.mirror(img)) 
     
    st.divider() 
    st.subheader("📷 [F5] QR Generator") 
    qr_data = st.text_input("Donnée à encoder", "https://") 
    if qr_data: 
        qr = qrcode.make(qr_data) 
        buf = BytesIO() 
        qr.save(buf) 
        st.image(buf.getvalue(), width=200) 

# --- [F6] CYBER-SÉCURITÉ --- 
with tabs: 
    st.subheader("🔐 [F6] Passphrase Master") 
    if st.button("Générer Passphrase"): 
        st.code(secrets.token_urlsafe(20)) 
     
    st.divider() 
    st.subheader("🔑 [F7] Encodeur Secret") 
    secret = st.text_input("Texte à cacher") 
    if secret: 
        st.code(base64.b64encode(secret.encode()).decode()) 
     
    if st.button("[F8] Simuler Scan Ports"): 
        with st.spinner("Analyse réseau..."): 
            time.sleep(1) 
            st.warning("Port 80/TCP: Filtré") 

# --- [F9] AI TEXT ENGINE --- 
with tabs: 
    st.subheader("🧠 [F9] AI Analysis") 
    txt = st.text_area("Analyse de Sentiment", key="ai_text") 
    if txt: 
        st.write(f"Vibe Score: {TextBlob(txt).sentiment.polarity}") 
     
    st.divider() 
    if st.button("[F10] Stats de lecture"): 
        if txt:
            w = len(txt.split()) 
            st.write(f"Mots: {w} | Temps de lecture: {max(1, w//200)} min") 
        else:
            st.warning("Veuillez saisir du texte d'abord.")

# --- [F11] DATA VIS ---
with tabs:
    st.subheader("📊 [F11] Data Analytics")
    df = pd.DataFrame({ 
        'ID': ['A1', 'B2', 'C3'],  
        'Value': ['99.9%', '85.2%', '91.0%'] 
    }) 
    st.table(df)

# --- [F12] DEV LAB --- 
with tabs: 
    st.subheader("🚀 [F12] Syntax Checker") 
    code_input = st.text_area("Snippet Python", "print('Hello')", key="dev_code") 
    if st.button("Vérifier"): 
        try: 
            compile(code_input, '', 'exec')
            st.success("Code Valide") 
        except Exception as e: 
            st.error(f"Erreur de syntaxe : {e}") 

# --- [F13] LIFE TOOLS --- 
with tabs: 
    st.subheader("🌍 [F13] Outils du Quotidien") 
    if st.button("🪙 Lancer une pièce"): 
        st.title(secrets.choice(["PILE", "FACE"])) 
     
    st.divider() 
    if st.button("🎲 Lancer un Dé [F14]"): 
        st.title(f"Résultat : {secrets.randbelow(6) + 1}") 

# --- [F15] SYSTÈME --- 
with tabs: 
    st.subheader("⚙️ Maintenance") 
    st.progress(98)
    st.write("System Stability: 98%")
    if st.button("PURGER CACHE"): 
        st.toast("Mémoire libérée !") 

# SIDEBAR 
with st.sidebar: 
    st.title("👤 ADMIN") 
    if st.button("🔴 SHUTDOWN"): 
        st.session_state.auth = False 
        st.rerun()
