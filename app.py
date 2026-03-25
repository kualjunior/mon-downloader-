import streamlit as st 
import yt_dlp 
import os 
import qrcode 
import secrets 
import pandas as pd 
import base64 
import time 
from io import BytesIO 
from PIL import Image, ImageOps 
from textblob import TextBlob 

# ========================================== 
# CONFIGURATION SYSTÈME
# ========================================== 
st.set_page_config(page_title="OMNIS OS v5.0", page_icon="⚡", layout="wide") 

st.markdown(""" 
<style> 
    .stApp { background: #0d1117; color: #e6edf3; } 
    div.stButton > button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); 
        color: white; border: none; font-weight: bold; 
    } 
    .stTabs [data-baseweb="tab-list"] { background-color: #161b22; border-radius: 10px; } 
</style> 
""", unsafe_allow_html=True) 

# ========================================== 
# SÉCURITÉ D'ACCÈS 
# ========================================== 
PASSWORD = "théo123" 
if "auth" not in st.session_state: 
    st.session_state.auth = False 

if not st.session_state.auth: 
    # Correction : st.columns(3) pour diviser l'écran en 3
    l, col, r = st.columns(3) 
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

# Initialisation de la LISTE des onglets
tabs = st.tabs(["📥 Media", "🎨 Studio", "🔐 Safe", "🧠 AI", "📊 Data", "🚀 Dev", "🌍 Life", "⚙️ Sys"]) 

# --- CORRECTION : ACCÈS PAR INDEX [0, 1, 2...] ---

with tabs: 
    st.subheader("📥 Media Extraction") 
    url = st.text_input("Lien Vidéo", placeholder="https://...", key="yt_url") 
    if st.button("Lancer l'extraction"): 
        st.info("Recherche du flux... (Simulé)") 

with tabs: 
    st.subheader("🎨 Image Lab") 
    up = st.file_uploader("Image", type=['jpg', 'png']) 
    if up: 
        img = Image.open(up) 
        st.image(img, use_container_width=True) 
        c1, c2 = st.columns(2) 
        with c1: 
            if st.button("Noir & Blanc"): st.image(img.convert('L')) 
        with c2: 
            if st.button("Effet Miroir"): st.image(ImageOps.mirror(img)) 

with tabs: 
    st.subheader("🔐 Security") 
    if st.button("Générer Passphrase"): st.code(secrets.token_urlsafe(20)) 
    sec_text = st.text_input("Texte à encoder", key="sec_text") 
    if sec_text: st.code(base64.b64encode(sec_text.encode()).decode()) 

with tabs: 
    st.subheader("🧠 AI Engine") 
    txt = st.text_area("Analyse", key="ai_area") 
    if txt: 
        st.write(f"Vibe Score: {TextBlob(txt).sentiment.polarity}") 

with tabs: 
    st.subheader("📊 Data") 
    df = pd.DataFrame({'ID': ['01', '02'], 'Value': ['99%', '85%']}) 
    st.table(df) 

with tabs: 
    st.subheader("🚀 Dev") 
    code_in = st.text_area("Python", "print('Hello')", key="code_in") 
    if st.button("Vérifier"): 
        try: compile(code_in, '', 'exec'); st.success("Valide") 
        except Exception as e: st.error(str(e)) 

with tabs: 
    st.subheader("🌍 Life") 
    if st.button("🪙 Pile ou Face"): st.title(secrets.choice(["PILE", "FACE"])) 

with tabs: 
    st.subheader("⚙️ Sys") 
    st.progress(98) 
    if st.button("🔴 LOGOUT"): 
        st.session_state.auth = False 
        st.rerun()
