import streamlit as st

# 1. Titre
st.title("⚡ OMNIS OS v5.0")

# 2. Création de la liste d'onglets
# On définit ici 3 onglets (tu peux en ajouter d'autres plus tard)
tabs = st.tabs(["📥 Media", "🎨 Studio", "⚙️ Sys"])

# 3. LA CORRECTION : Utiliser tabs, tabs, etc.
with tabs: 
    st.subheader("Section Media")
    url = st.text_input("Lien Vidéo", key="url_input")
    if st.button("Lancer"):
        st.write(f"Analyse de : {url}")

with tabs:
    st.subheader("Section Studio")
    st.file_uploader("Charger une image", type=['png', 'jpg'])

with tabs:
    st.subheader("Système")
    st.write("Statut : Opérationnel")
