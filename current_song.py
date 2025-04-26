import time
import threading
from flask import Flask, render_template_string
import os

# Import des modules pour récupérer les chansons
from sources import youtube
from sources import spotify

# Paramètres
OUTPUT_FILE = "current_song.txt"
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

# Lancement des deux parties ensemble
if __name__ == "__main__":
    # Lancer la récupération de chanson en parallèle
    threading.Thread(target=song_updater, daemon=True).start()

    # Lancer le serveur Flask
    app.run(host="0.0.0.0", port=5000)
