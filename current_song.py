import sys
import os
import threading
import time
import logging
from flask import Flask, render_template_string
import pystray
from PIL import Image

# --- Imports projet ---
from sources import youtube
from sources import spotify
from sources import config

# ========== CONFIGURATION ==========

REFRESH_INTERVAL = 2  # secondes
APP_FOLDER = os.path.join(os.getenv('APPDATA'), 'OBSCurrentSong')

# Crée le dossier si nécessaire
os.makedirs(APP_FOLDER, exist_ok=True)

OUTPUT_FILE = os.path.join(APP_FOLDER, "current_song.txt")
LOG_FILE = os.path.join(APP_FOLDER, "current_song.log")

# Nettoyer le log à chaque démarrage
if os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()  # Ouvre le fichier et l'efface immédiatement
    
# Configuration du logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)

# Flask app
app = Flask(__name__)

HTML_TEMPLATE = """ 
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Current Song</title>
<style>
    body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #121212; font-family: Arial, sans-serif; }
    .container { width: 300px; height: 80px; display: flex; background-color: #2c2c2c; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); }
    .icon-section { width: 60px; background-color: #1a1a1a; display: flex; justify-content: center; align-items: center; font-size: 28px; color: #1abc9c; border-right: 2px solid #1abc9c; }
    .text-section { flex: 1; padding: 10px; display: flex; align-items: center; color: #1abc9c; font-size: 14px; text-align: left; word-wrap: break-word; overflow-wrap: break-word; }
    .error { font-size: 16px; color: #e74c3c; text-align: center; }
</style>
</head>
<body>
<script>
    setInterval(function() { location.reload(); }, 5000);
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

# ========== UTILITAIRES ==========

def resource_path(relative_path):
    """Trouve le bon chemin pour PyInstaller ou en dev"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

ICON_PATH = resource_path("assets/current_song.ico")

def write_to_file(text):
    """Écrit la chanson actuelle dans le fichier OUTPUT_FILE"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def get_current_song():
    """Détermine la chanson en cours"""
    youtube_song = youtube.get_current_song()
    spotify_song = spotify.get_spotify_window_title()

    if youtube_song != "No Song" and spotify_song == "No Song":
        return youtube_song
    elif spotify_song != "No Song" and youtube_song == "No Song":
        return spotify_song
    elif spotify_song == "No Song" and youtube_song == "No Song":
        return "No Song"
    else:
        return "Erreur : Conflit de sources"

# ========== TÂCHES DE FOND ==========

def song_updater():
    last_song = ""
    while True:
        current_song = get_current_song()

        if current_song != last_song:
            write_to_file(current_song)
            logging.info(f"Song updated: {current_song}")
            last_song = current_song

        time.sleep(REFRESH_INTERVAL)

def start_server():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# ========== FLASK ROUTES ==========

@app.route('/current-song', methods=['GET'])
def current_song_route():
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            song_title = f.read().strip()
        return render_template_string(HTML_TEMPLATE, song_title=song_title)
    except Exception as e:
        logging.error(f"Error reading song title: {e}")
        return render_template_string(HTML_TEMPLATE, song_title=None), 500

# ========== TRAY ICON ==========

def on_quit(icon, item):
    logging.info("Quitting application.")
    try:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    except Exception as e:
        logging.error(f"Error removing output file: {e}")
    icon.stop()
    sys.exit(0)

def run_tray():
    try:
        icon = pystray.Icon(
            "current_song",
            Image.open(ICON_PATH),
            menu=pystray.Menu(
                pystray.MenuItem("Quit", on_quit)
            )
        )
        icon.run()
    except Exception as e:
        logging.error(f"Error loading tray icon: {e}")

# ========== MAIN ==========

if __name__ == "__main__":
    logging.info("Starting OBS Current Song Display")
    threading.Thread(target=song_updater, daemon=True).start()
    threading.Thread(target=start_server, daemon=True).start()
    run_tray()
