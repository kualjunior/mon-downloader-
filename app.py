import streamlit as st
import yt_dlp
import os
import time
import requests
from pathlib import Path
from streamlit_lottie import st_lottie
from PIL import Image, ImageFilter, ImageEnhance

# =========================
# CONFIGURATION PRO
# =========================
st.set_page_config(
    page_title="UltraStream X - Ultimate OS",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_rocket = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_96bovdur.json")
lottie_loading = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_raiw2hsc.json")

# =========================
# STYLE CYBERPUNK AMÉLIORÉ
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');

    .stApp { background: #08080a; font-family: 'Rajdhani', sans-serif; }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem !important;
        background: linear-gradient(90deg, #00f2fe, #7000ff, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: shine 3s linear infinite;
    }

    @keyframes shine { to { background-position: 200% center; } }

    /* Glassmorphism Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px 10px 0 0 !important;
        color: white !important;
        padding: 10px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIQUE SÉCURITÉ
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st_lottie(lottie_rocket, height=200)
        st.markdown("<h1 style='text-align:center; color:white;'>ACCÈS RESTREINT</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Clé d'accès", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ Code erroné.")
    st.stop()

# =========================
# DASHBOARD MULTI-FONCTIONS
# =========================
st.markdown("<h1 class='main-title'>ULTRASTREAM X</h1>", unsafe_allow_html=True)

# Barre latérale avec historique
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3502/3502688.png", width=60)
    st.header("💎 Session")
    if st.session_state.history:
        for item in st.session_state.history[-5:]:
            st.caption(f"✅ {item}")

# CRÉATION DES ONGLETS (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Downloader", "🎨 Image Lab", "⏱️ Productivity", "📝 Notepad"])

# --- ONGLET 1 : DOWNLOADER ---
with tab1:
    col_u, col_o = st.columns() # FIX: Ajout de la liste de ratios
    with col_u:
        url = st.text_input("🔗 URL de la source", placeholder="YouTube, Twitch, TikTok...")
    with col_o:
        format_type = st.selectbox("Format", ["Vidéo (MP4)", "Audio (MP3)"])

    if st.button("LANCER L'EXTRACTION 🚀"):
        if not url:
            st.warning("URL vide.")
        else:
            try:
                with st.status("🛸 Extraction...", expanded=True) as status:
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                    title = "".join([c for c in info.get('title', 'file') if c.isalnum() or c==' ']).strip()
                    
                    ydl_opts = {'outtmpl': f"{DOWNLOAD_FOLDER}/{title}.%(ext)s"}
                    if "Audio" in format_type:
                        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
                    
                    ydl.download([url])
                    status.update(label="✅ Succès !", state="complete")
                    
                st.balloons()
                ext = "mp3" if "Audio" in format_type else "mp4"
                final_path = Path(DOWNLOAD_FOLDER) / f"{title}.{ext}"
                
                c1, c2 = st.columns() # FIX: Ajout de liste
                with c1: st.image(info.get('thumbnail'), use_container_width=True)
                with c2:
                    with open(final_path, "rb") as f:
                        st.download_button("📥 RÉCUPÉRER LE FICHIER", f, file_name=f"{title}.{ext}")
                    st.session_state.history.append(title)
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- ONGLET 2 : IMAGE LAB (OFFLINE) ---
with tab2:
    st.subheader("🎨 Studio de Retouche (Fonctionne sans lien)")
    img_file = st.file_uploader("Importer une photo", type=['png', 'jpg', 'jpeg'])
    if img_file:
        image = Image.open(img_file)
        col_img1, col_img2 = st.columns()
        
        with col_img1:
            st.image(image, caption="Original", use_container_width=True)
            effect = st.selectbox("Effet Spécial", ["Aucun", "Noir & Blanc", "Flou Artistique", "Contraste Néon"])
        
        # Traitement Image
        processed = image.copy()
        if effect == "Noir & Blanc": processed = processed.convert("L")
        elif effect == "Flou Artistique": processed = processed.filter(ImageFilter.BLUR)
        elif effect == "Contraste Néon": processed = ImageEnhance.Contrast(processed).enhance(2.5)
        
        with col_img2:
            st.image(processed, caption="Résultat", use_container_width=True)

# --- ONGLET 3 : PRODUCTIVITY (TIMER) ---
with tab3:
    st.subheader("⏱️ Mode Focus (Pomodoro)")
    t_col1, t_col2 = st.columns()
    with t_col1:
        minutes = st.number_input("Durée du focus (min)", 1, 120, 25)
        if st.button("DÉMARRER FOCUS"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            for percent_complete in range(100):
                time.sleep((minutes * 60) / 100)
                progress_bar.progress(percent_complete + 1)
                status_text.text(f"Concentration... {percent_complete + 1}%")
            st.success("Session terminée ! Prends une pause.")
    with t_col2:
        st.info("Utilise ce mode pour rester productif sans être distrait par les réseaux sociaux.")

# --- ONGLET 4 : NOTEPAD ---
with tab4:
    st.subheader("📝 Quick Notes")
    user_note = st.text_area("Prends tes notes ici (Listes de vidéos, idées, rappels...)", height=250)
    if st.button("💾 Sauvegarder en texte"):
        st.download_button("Télécharger ma note", user_note, file_name="notes_ultrastream.txt")

st.markdown("<br><hr><p style='text-align:center; opacity:0.5;'>© 2026 DAVID EDWIN • UltraStream X Multi-Tool</p>", unsafe_allow_html=True)import streamlit as st
import yt_dlp
import os
import time
import requests
from pathlib import Path
from streamlit_lottie import st_lottie
from PIL import Image, ImageFilter, ImageEnhance

# =========================
# CONFIGURATION PRO
# =========================
st.set_page_config(
    page_title="UltraStream X - Ultimate OS",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_rocket = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_96bovdur.json")
lottie_loading = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_raiw2hsc.json")

# =========================
# STYLE CYBERPUNK AMÉLIORÉ
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');

    .stApp { background: #08080a; font-family: 'Rajdhani', sans-serif; }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem !important;
        background: linear-gradient(90deg, #00f2fe, #7000ff, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: shine 3s linear infinite;
    }

    @keyframes shine { to { background-position: 200% center; } }

    /* Glassmorphism Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px 10px 0 0 !important;
        color: white !important;
        padding: 10px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIQUE SÉCURITÉ
# =========================
PASSWORD = "théo123"
DOWNLOAD_FOLDER = "downloads"
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

if "auth" not in st.session_state: st.session_state.auth = False
if "history" not in st.session_state: st.session_state.history = []

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st_lottie(lottie_rocket, height=200)
        st.markdown("<h1 style='text-align:center; color:white;'>ACCÈS RESTREINT</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Clé d'accès", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else: st.error("❌ Code erroné.")
    st.stop()

# =========================
# DASHBOARD MULTI-FONCTIONS
# =========================
st.markdown("<h1 class='main-title'>ULTRASTREAM X</h1>", unsafe_allow_html=True)

# Barre latérale avec historique
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3502/3502688.png", width=60)
    st.header("💎 Session")
    if st.session_state.history:
        for item in st.session_state.history[-5:]:
            st.caption(f"✅ {item}")

# CRÉATION DES ONGLETS (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Downloader", "🎨 Image Lab", "⏱️ Productivity", "📝 Notepad"])

# --- ONGLET 1 : DOWNLOADER ---
with tab1:
    col_u, col_o = st.columns() # FIX: Ajout de la liste de ratios
    with col_u:
        url = st.text_input("🔗 URL de la source", placeholder="YouTube, Twitch, TikTok...")
    with col_o:
        format_type = st.selectbox("Format", ["Vidéo (MP4)", "Audio (MP3)"])

    if st.button("LANCER L'EXTRACTION 🚀"):
        if not url:
            st.warning("URL vide.")
        else:
            try:
                with st.status("🛸 Extraction...", expanded=True) as status:
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                    title = "".join([c for c in info.get('title', 'file') if c.isalnum() or c==' ']).strip()
                    
                    ydl_opts = {'outtmpl': f"{DOWNLOAD_FOLDER}/{title}.%(ext)s"}
                    if "Audio" in format_type:
                        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
                    
                    ydl.download([url])
                    status.update(label="✅ Succès !", state="complete")
                    
                st.balloons()
                ext = "mp3" if "Audio" in format_type else "mp4"
                final_path = Path(DOWNLOAD_FOLDER) / f"{title}.{ext}"
                
                c1, c2 = st.columns() # FIX: Ajout de liste
                with c1: st.image(info.get('thumbnail'), use_container_width=True)
                with c2:
                    with open(final_path, "rb") as f:
                        st.download_button("📥 RÉCUPÉRER LE FICHIER", f, file_name=f"{title}.{ext}")
                    st.session_state.history.append(title)
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- ONGLET 2 : IMAGE LAB (OFFLINE) ---
with tab2:
    st.subheader("🎨 Studio de Retouche (Fonctionne sans lien)")
    img_file = st.file_uploader("Importer une photo", type=['png', 'jpg', 'jpeg'])
    if img_file:
        image = Image.open(img_file)
        col_img1, col_img2 = st.columns()
        
        with col_img1:
            st.image(image, caption="Original", use_container_width=True)
            effect = st.selectbox("Effet Spécial", ["Aucun", "Noir & Blanc", "Flou Artistique", "Contraste Néon"])
        
        # Traitement Image
        processed = image.copy()
        if effect == "Noir & Blanc": processed = processed.convert("L")
        elif effect == "Flou Artistique": processed = processed.filter(ImageFilter.BLUR)
        elif effect == "Contraste Néon": processed = ImageEnhance.Contrast(processed).enhance(2.5)
        
        with col_img2:
            st.image(processed, caption="Résultat", use_container_width=True)

# --- ONGLET 3 : PRODUCTIVITY (TIMER) ---
with tab3:
    st.subheader("⏱️ Mode Focus (Pomodoro)")
    t_col1, t_col2 = st.columns()
    with t_col1:
        minutes = st.number_input("Durée du focus (min)", 1, 120, 25)
        if st.button("DÉMARRER FOCUS"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            for percent_complete in range(100):
                time.sleep((minutes * 60) / 100)
                progress_bar.progress(percent_complete + 1)
                status_text.text(f"Concentration... {percent_complete + 1}%")
            st.success("Session terminée ! Prends une pause.")
    with t_col2:
        st.info("Utilise ce mode pour rester productif sans être distrait par les réseaux sociaux.")

# --- ONGLET 4 : NOTEPAD ---
with tab4:
    st.subheader("📝 Quick Notes")
    user_note = st.text_area("Prends tes notes ici (Listes de vidéos, idées, rappels...)", height=250)
    if st.button("💾 Sauvegarder en texte"):
        st.download_button("Télécharger ma note", user_note, file_name="notes_ultrastream.txt")

st.markdown("<br><hr><p style='text-align:center; opacity:0.5;'>© 2026 DAVID EDWIN • UltraStream X Multi-Tool</p>", unsafe_allow_html=True)
