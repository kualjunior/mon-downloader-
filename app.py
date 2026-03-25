import streamlit as st

# 1. Titre de l'application
st.title("⚡ OMNIS OS v5.0")

# 2. Création des onglets (C'est une liste d'objets)
# On définit 3 onglets pour l'exemple
tabs = st.tabs(["📥 Media", "🎨 Studio", "⚙️ Sys"])

# 3. CORRECTION : On accède à chaque onglet par son numéro (index)
# = Premier onglet, = Deuxième, etc.

with tabs: 
    st.subheader("Media Downloader")
    url = st.text_input("Lien Vidéo", key="url_input")
    if st.button("Lancer"):
        st.write(f"Analyse de : {url}")

with tabs:
    st.subheader("Studio Photo")
    st.file_uploader("Charger une image", type=['png', 'jpg'])

with tabs:
    st.subheader("Système")
    st.write("Statut : Opérationnel")
    if st.button("Purger le cache"):
        st.success("Cache vidé !")
