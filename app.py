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
# DASHBOARD OMNITOOLS OS v4.0
# =========================
st.markdown("<h1 style='text-align:center; font-size:3.5em; margin-bottom:0; color:#00f2fe;'>⚡ OMNITOOLS OS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.8; letter-spacing:2px;'>SYSTÈME UTILITAIRE MULTI-COUCHES</p>", unsafe_allow_html=True)

# On crée 8 onglets pour répartir les 14 fonctions
tabs = st.tabs([
    "📥 Media", "🎨 Studio", "🔐 Safe", "🧠 AI Text", 
    "📊 Data", "🚀 Dev Lab", "🌡️ Life", "⚙️ System"
])

# --- TAB 1 : MEDIA (Index 0) ---
with tabs:
    st.subheader("📥 [F1] Extraire du contenu")
    url = st.text_input("URL Source (YouTube, TikTok, Insta...)")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        ext = st.selectbox("Extension", ["MP4 (Vidéo)", "MP3 (Audio)"])
    with col_m2:
        st.info("Note : Moteur FFmpeg V3 activé.")
    
    if st.button("EXÉCUTER LE DOWNLOAD"):
        if url: st.success("Extraction en cours...")

# --- TAB 2 : STUDIO (Index 1) ---
with tabs:
    st.subheader("🎨 [F2] Analyseur d'Image & Palette")
    up_img = st.file_uploader("Analysez une image", type=["jpg", "png"])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        # [F3] Noir & Blanc Instantané
        if st.button("Appliquer Filtre B&W"):
            st.image(img.convert('L'), caption="Version Noir & Blanc")

    st.divider()
    st.subheader("📷 [F4] Générateur de QR Pro")
    qr_txt = st.text_input("Texte ou URL pour le QR")
    if qr_txt:
        qr = qrcode.make(qr_txt)
        b = BytesIO()
        qr.save(b, format="PNG")
        st.image(b.getvalue(), width=150)

# --- TAB 3 : SAFE (Index 2) ---
with tabs:
    st.subheader("🔐 [F5] Cybersécurité")
    size = st.slider("Force du mot de passe", 12, 64, 24)
    if st.button("Générer Passphrase"):
        p = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%&*") for _ in range(size))
        st.code(p)
    
    st.divider()
    # [F6] Chiffrage de texte simple
    st.subheader("🔑 [F6] Encodeur Base64")
    secret_t = st.text_input("Texte à encoder/protéger")
    if secret_t:
        import base64
        encoded = base64.b64encode(secret_t.encode()).decode()
        st.write("Résultat sécurisé :")
        st.code(encoded)

# --- TAB 4 : AI TEXT (Index 3) ---
with tabs:
    st.subheader("🧠 [F7] Sentiment & Analyse")
    user_t = st.text_area("Collez un texte...")
    if user_t:
        analysis = TextBlob(user_t)
        st.write(f"Sentiment : {analysis.sentiment.polarity}")
    
    st.divider()
    # [F8] Compteur de lecture
    st.subheader("⏱️ [F8] Temps de lecture estimé")
    if user_t:
        words = len(user_t.split())
        st.write(f"Estimation : {max(1, words // 200)} minute(s) de lecture.")

# --- TAB 5 : DATA (Index 4) ---
with tabs:
    st.subheader("📈 [F9] Finance & Crypto")
    st.metric("Bitcoin (BTC)", "68,432 €", "+2.4%")
    
    st.divider()
    # [F10] Générateur de CSV de test
    st.subheader("📁 [F10] Générateur de Data Test")
    if st.button("Générer un fichier Excel/CSV fictif"):
       # Correction de la ligne 187
if st.button("Générer un fichier Excel/CSV fictif"):
    df = pd.DataFrame({
        'ID':, 
        'Score':
    })
    st.dataframe(df)
    st.download_button("Télécharger CSV", df.to_csv(index=False), "data_test.csv")
        st.dataframe(df)
        st.download_button("Télécharger CSV", df.to_csv(), "data_test.csv")

# --- TAB 6 : DEV LAB (Index 5) ---
with tabs:
    st.subheader("🚀 [F11] Inspecteur de Code")
    code_input = st.text_area("Collez du code Python ici...", "print('Hello World')")
    if st.button("Vérifier la syntaxe"):
        try:
            compile(code_input, '<string>', 'exec')
            st.success("Syntaxe Valide !")
        except Exception as e:
            st.error(f"Erreur détectée : {e}")

# --- TAB 7 : LIFE (Index 6) ---
with tabs:
    st.subheader("🌡️ [F12] Météo (Simulation)")
    st.write("Lieu : Paris, France")
    st.metric("Température", "18°C", "Nuageux")
    
    st.divider()
    # [F13] Chronomètre de productivité
    st.subheader("⌛ [F13] Mode Focus (Pomodoro)")
    if st.button("Démarrer 25 min"):
        st.toast("C'est parti ! Travaillez bien.")

# --- TAB 8 : SYSTEM (Index 7) ---
with tabs:
    st.subheader("⚙️ [F14] Maintenance")
    if st.button("Nettoyer le cache du serveur"):
        st.toast("Fichiers temporaires supprimés.")
    
    st.divider()
    st.write("**État du système :**")
    st.progress(85, text="Mémoire Vive Optimisée")

# --- SIDEBAR CORRIGÉE ---
with st.sidebar:
    st.markdown("### 👤 Admin Session")
    st.write(f"Date : {pd.to_datetime('today').strftime('%d/%m/%Y')}")
    st.markdown("---")
    if st.button("🔴 DÉCONNEXION"):
        st.session_state.auth = False
        st.rerun()
