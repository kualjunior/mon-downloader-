import streamlit as st

# 1. Configuration de la page
st.set_page_config(page_title="OMNIS OS", layout="wide")

# 2. Sécurité (Correction des colonnes)
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # On précise '3' pour créer 3 colonnes
    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("🔒 Login")
        pwd = st.text_input("PASSWORD", type="password")
        if st.button("BOOT UP"):
            if pwd == "théo123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Accès refusé")
    st.stop()

# 3. Dashboard (Correction des Onglets)
st.title("⚡ OMNIS OS v5.0")

# On crée la liste des onglets
tabs = st.tabs(["📥 Media", "🎨 Studio", "⚙️ Sys"])

# ON UTILISE L'INDEX,, POUR CHAQUE ONGLET
with tabs: 
    st.subheader("Media Downloader")
    st.text_input("Lien URL", key="url_media")
    if st.button("Extraire"):
        st.info("Traitement en cours...")

with tabs:
    st.subheader("Studio Photo")
    st.file_uploader("Charger une image", type=['png', 'jpg'])

with tabs:
    st.subheader("Système")
    if st.button("DÉCONNEXION"):
        st.session_state.auth = False
        st.rerun()
