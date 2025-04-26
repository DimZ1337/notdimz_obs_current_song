import sys
import time
import threading
from flask import Flask, render_template_string
import os

# Import des modules pour récupérer les chansons
from sources import youtube
from sources import spotify
from sources import config

# --- Ajouts pour le tray ---
import pystray
from PIL import Image, ImageDraw

def set_working_directory():
    """Force le working directory au dossier du programme"""
    if hasattr(sys, '_MEIPASS'):
        # Mode PyInstaller (exécutable)
        os.chdir(sys._MEIPASS)
    else:
        # Mode normal (Python)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

set_working_directory()

# Paramètres
OUTPUT_FILE = config.get_save_path()
REFRESH_INTERVAL = 2  # secondes

# Flask app
app = Flask(__name__)

# Template HTML avec CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Current Song</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #121212;
            font-family: Arial, sans-serif;
        }
        .container {
            width: 300px;
            height: 80px;
            display: flex;
            background-color: #2c2c2c;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        .icon-section {
            width: 60px;
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 28px;
            color: #1abc9c;
            border-right: 2px solid #1abc9c;
        }
        .text-section {
            flex: 1;
            padding: 10px;
            display: flex;
            align-items: center;
            color: #1abc9c;
            font-size: 14px;
            text-align: left;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        .error {
            font-size: 16px;
            color: #e74c3c;
            text-align: center;
        }
    </style>
</head>
<body>
    <script>
        setInterval(function() {
            location.reload();
        }, 5000);
    </script>
<div class="container">
    <div class="icon-section">🎵</div>
    <div class="text-section">
        {% if song_title %}
            {{ song_title }}
        {% else %}
            Aucune chanson en cours
        {% endif %}
    </div>
</div>
</body>
</html>
"""

def resource_path(relative_path):
    """ Trouve le bon chemin que ce soit en dev ou en exe compilé """
    if hasattr(sys, '_MEIPASS'):
        # Quand exécuté via PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # En mode développement normal
        return os.path.join(os.path.abspath("."), relative_path)

# Fonction pour écrire dans le fichier
def write_to_file(text):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

# Fonction qui récupère et met à jour la chanson
def song_updater():
    last_song = ""
    while True:
        youtube_song = youtube.get_current_song()
        spotify_song = spotify.get_spotify_window_title()

        if youtube_song != "No Song" and spotify_song == "No Song":
            current_song = youtube_song
        elif spotify_song != "No Song" and youtube_song == "No Song":
            current_song = spotify_song
        elif spotify_song == "No Song" and youtube_song == "No Song":
            current_song = "No Song"
        else:
            current_song = "Erreur : Conflit de sources"

        if current_song != last_song:
            write_to_file(current_song)
            print(f"[INFO] Chanson mise à jour : {current_song}")
            last_song = current_song

        time.sleep(REFRESH_INTERVAL)

# Route Flask
@app.route('/current-song', methods=['GET'])
def get_current_song():
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            song_title = f.read().strip()
        return render_template_string(HTML_TEMPLATE, song_title=song_title)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, song_title=None), 500

# Fonctions Tray
def create_image():
    """Crée une icône simple pour la tray"""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (30, 30, 30))
    dc = ImageDraw.Draw(image)
    dc.text((18, 18), "NCS", fill=(26, 188, 156))
    return image

def on_quit(icon, item):
    print("[INFO] Fermeture de l'application.")
    icon.stop()
    os.remove(OUTPUT_FILE) 
    os._exit(0)  # Force la fermeture proprement

def run_tray():
    #ico_path = resource_path("assets/current_song.ico")
    icon = pystray.Icon(
        "current_song",
        Image.open("assets/current_song.ico"),  # ← On charge un vrai .ico ici
        menu=pystray.Menu(
            pystray.MenuItem("Quitter", on_quit)
        )
    )
    icon.run()

def start_server():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Lancement des deux parties ensemble
if __name__ == "__main__":
    # Lancer la récupération de chanson en parallèle
    threading.Thread(target=song_updater, daemon=True).start()

    # Lancer le serveur Flask
    threading.Thread(target=start_server, daemon=True).start()

    # Lancer l'icône tray en principal
    run_tray()