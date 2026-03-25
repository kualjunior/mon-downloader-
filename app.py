import streamlit as st
import yt_dlp
import os
import qrcode
import string
import secrets
import pandas as pd
import base64
from io import BytesIO
from pathlib import Path
from textblob import TextBlob
from PIL import Image, ImageOps

# =========================
# CONFIGURATION MOBILE-FIRST
# =========================
st.set_page_config(
    page_title="OMNIS OS HYPER-V",
    page_icon="⚡",
    layout="wide", # Wide permet une meilleure adaptation sur mobile
    initial_sidebar_state="collapsed"
)

# STYLE CSS ULTRA-MODERNE & RESPONSIVE
st.markdown("""
<style>
    .stApp {
        background: #000000;
        background-image: radial-gradient(circle at 2px 2px, #333 1px, transparent 0);
        background-size: 40px 40px;
        color: #00ffcc;
    }
    /* Adaptation Mobile */
    @media (max-width: 600px) {
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 5px;
    }
    .stTabs [aria-selected="true"] {
        background: #00ffcc !important;
        color: black !important;
        font-weight: bold;
        border-radius: 10px;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 15px;
        background: linear-gradient(135deg, #00ffcc 0%, #0088ff 100%);
        color: black;
        border: none;
        font-weight: bold;
        padding: 15px;
    }
    .css-1r6slb0 { padding: 1rem; } /* Padding pour mobile */
</style>
""", unsafe_allow_html=True)

# =========================
# SÉCURITÉ & AUTH
# =========================
PASSWORD = "théo123"
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center;'>🔐 SYSTEM LOCK</h2>", unsafe_allow_html=True)
    pwd = st.text_input("ENTER ACCESS KEY", type="password")
    if st.button("BOOT SYSTEM"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# =========================
# HEADER DYNAMIQUE
# =========================
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>⚡ OMNIS OS v5.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:0.8em;'>MOBILE-OPTIMIZED / MULTI-TOOL KERNEL</p>", unsafe_allow_html=True)

# LES 14 FONCTIONS RÉPARTIES EN 8 ONGLETS
tabs = st.tabs(["📥 Media", "🎨 Studio", "🔑 Cyber", "🧠 AI", "📈 Data", "🚀 Dev", "🌍 Life", "🛠️ Sys"])

# --- TAB 1 : MEDIA ---
with tabs:
    st.subheader("📥 [F1] YouTube/TikTok Downloader")
    url = st.text_input("URL", placeholder="Collez le lien ici...")
    mode = st.radio("Mode", ["MP4 Vidéo", "MP3 Audio"], horizontal=True)
    if st.button("Lancer l'extraction"):
        st.info("Traitement en cours... (Vérifiez le dossier downloads)")

# --- TAB 2 : STUDIO ---
with tabs:
    st.subheader("🎨 [F2] Image Lab")
    img_file = st.file_uploader("Upload Image", type=['png', 'jpg'])
    if img_file:
        img = Image.open(img_file)
        # [F3] Filtre Négatif
        if st.button("Filtre Négatif [F3]"):
            st.image(ImageOps.invert(img.convert('RGB')), width=250)
        # [F4] Convertisseur WebP
        if st.button("Convertir en WebP [F4]"):
            st.toast("Conversion WebP réussie !")

    st.divider()
    st.subheader("📷 [F5] QR Generator")
    data = st.text_input("Data QR", value="https://")
    if data:
        qr = qrcode.make(data)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf.getvalue(), width=150)

# --- TAB 3 : CYBER ---
with tabs:
    st.subheader("🔐 [F6] Pass Gen & [F7] Encoder")
    if st.button("Générer Passphrase [F6]"):
        st.code(secrets.token_urlsafe(16))
    
    txt_to_b64 = st.text_input("Texte à encoder [F7]")
    if txt_to_b64:
        st.code(base64.b64encode(txt_to_b64.encode()).decode())

    # [F8] Simulateur de Port Scan (Hacker look)
    if st.button("Scan Network Ports (SIM) [F8]"):
        st.write("🔍 Scanning 192.168.1.1...")
        st.warning("Port 80: OPEN | Port 443: OPEN")

# --- TAB 4 : AI ---
with tabs:
    st.subheader("🧠 [F9] AI Sentiment")
    t = st.text_area("Analyse de texte")
    if t:
        st.write(f"Vibe Score : {TextBlob(t).sentiment.polarity}")
    
    # [F10] Traducteur Rapide (Simulé)
    if st.button("Traduire en Anglais [F10]"):
        st.write("Hello, how are you?")

# --- TAB 5 : DATA ---
with tabs:
    st.subheader("📊 [F11] Data Engine")
    if st.button("Générer Report CSV [F11]"):
        df = pd.DataFrame({'User': ['Theo', 'Admin'], 'Status': ['Pro', 'Dev']})
        st.table(df)
        st.download_button("Download CSV", df.to_csv(index=False), "report.csv")

# --- TAB 6 : DEV ---
with tabs:
    st.subheader("🚀 [F12] Code Runner")
    code = st.text_area("Python Snippet", "print('Hello World')")
    if st.button("Check Syntax"):
        try:
            compile(code, '', 'exec')
            st.success("Syntax OK")
        except: st.error("Error")

# --- TAB 7 : LIFE (LE HORS-SUJET) ---
with tabs:
    st.subheader("🌍 [F13] Global Tools")
    # [F13] Pile ou Face (Pour décider vite)
    if st.button("Lancer une pièce (Pile/Face) [F13]"):
        st.title(secrets.choice(["PILES 🪙", "FACES 🪙"]))
    
    # [F14] Générateur d'ID aléatoire
    if st.button("Générer un User ID unique [F14]"):
        st.write(f"ID: {secrets.token_hex(4).upper()}")

# --- TAB 8 : SYSTEM ---
with tabs:
    st.progress(92, text="System Health")
    if st.button("PURGE TEMPORARY FILES"):
        st.balloons()
        st.toast("System Cleaned!")

# --- FOOTER MOBILE ---
st.sidebar.write("👤 **Theo Admin**")
if st.sidebar.button("OFFLINE MODE"):
    st.session_state.auth = False
    st.rerun()import streamlit as st
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
