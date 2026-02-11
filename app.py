import yt_dlp
import os

# Chemin du Bureau
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Lien vidéo
url = input("Entrez le lien de la vidéo à télécharger : ")

ydl_opts = {
    # Sortie
    "outtmpl": os.path.join(desktop, "%(title)s.%(ext)s"),
    "format": "best",  # format pré-fusionné (le plus stable)
    "merge_output_format": "mp4",

    # Cookies (OBLIGATOIRE dans ton cas)
    "cookiefile": r"C:\Users\david\Downloads\youtube_cookies.txt",

    # Client YouTube (contournement SABR / 403)
    "extractor_args": {
        "youtube": {
            "player_client": ["android"]
        }
    },

    # Sécurité / stabilité
    "noplaylist": True,
    "retries": 10,
    "fragment_retries": 10,
    "socket_timeout": 30,

    # Logs utiles
    "quiet": False,
    "no_warnings": False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("✅ Téléchargement terminé ! Vérifie ton Bureau.")
except Exception as e:
    print(f"❌ Une erreur est survenue : {e}")
