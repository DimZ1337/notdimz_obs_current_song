import sys
import os
import threading
import time
import logging
import subprocess
from flask import Flask, render_template_string
import pystray
from PIL import Image
from sources import youtube
from sources import spotify
from sources import config

# ========== CONFIGURATION ==========

REFRESH_INTERVAL = 2  # seconds
APP_FOLDER = config.get_app_folder()

OUTPUT_FILE = config.get_save_path()
LOG_FILE = config.get_log_path()

# Clean the log file on each startup
if os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)

# Flask app initialization
app = Flask(__name__)

# Load colors
colors = config.load_colors()

# Generate the HTML template based on current colors
def generate_html_template():
    return f"""
    <!DOCTYPE html>
    <html lang=\"fr\">
    <head>
        <meta charset=\"UTF-8\">
        <title>Current Song</title>
        <style>
            body {{
                background-color: {colors['background']};
                font-family: Arial, sans-serif;
                height: 100vh;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                width: 300px;
                height: 80px;
                background-color: {colors['container']};
                border-radius: 15px;
                display: flex;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
                overflow: hidden;
            }}
            .icon-section {{
                width: 60px;
                background-color: {colors['icon_background']};
                display: flex;
                justify-content: center;
                align-items: center;
                color: {colors['text']};
                font-size: 28px;
                border-right: 2px solid {colors['border']};
            }}
            .text-section {{
                flex: 1;
                padding: 10px;
                display: flex;
                align-items: center;
                color: {colors['text']};
                font-size: 18px;
                font-weight: bold;
                text-align: left;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}
            .error {{
                font-size: 16px;
                color: {colors['error_text']};
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <script>
            setInterval(function() {{ location.reload(); }}, 5000);
        </script>
        <div class=\"container\">
            <div class=\"icon-section\">&#127925;</div>
            <div class=\"text-section\">
                {{% if song_title %}}
                    {{{{ song_title }}}}
                {{% else %}}
                    Aucune chanson en cours
                {{% endif %}}
            </div>
        </div>
    </body>
    </html>
    """

# Initial HTML template
HTML_TEMPLATE = generate_html_template()

# Utility function for resource path (for PyInstaller or dev)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

ICON_PATH = resource_path("assets/current_song.ico")

# Write current song title to file
def write_to_file(text):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

# Detect current song
def get_current_song():
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

# Background task: Update song info
def song_updater():
    last_song = ""
    while True:
        current_song = get_current_song()

        if current_song != last_song:
            write_to_file(current_song)
            logging.info(f"Song updated: {current_song}")
            last_song = current_song

        time.sleep(REFRESH_INTERVAL)

# Background task: Flask server
def start_server():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Flask route for browser source
@app.route('/current-song', methods=['GET'])
def current_song_route():
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            song_title = f.read().strip()
        return render_template_string(HTML_TEMPLATE, song_title=song_title)
    except Exception as e:
        logging.error(f"Error reading song title: {e}")
        return render_template_string(HTML_TEMPLATE, song_title=None), 500

# Action: Open settings_gui.py to edit color
def open_settings(icon, item):
    logging.info("Opening settings interface...")
    try:
        # Use the .exe version
        subprocess.Popen(["settings_gui.exe"], shell=True)
    except Exception as e:
        logging.error(f"Error opening settings_gui: {e}")

# Action: Reload configuration dynamically
def reload_configuration(icon, item):
    global colors, HTML_TEMPLATE
    logging.info("Reloading configuration...")
    colors = config.load_colors()
    HTML_TEMPLATE = generate_html_template()
    logging.info("Configuration reloaded successfully.")

# Action: Quit application
def on_quit(icon, item):
    logging.info("Quitting application.")
    try:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    except Exception as e:
        logging.error(f"Error removing output file: {e}")
    icon.stop()
    sys.exit(0)

# System Tray icon runner
def run_tray():
    try:
        icon = pystray.Icon(
            "current_song",
            Image.open(ICON_PATH),
            menu=pystray.Menu(
                pystray.MenuItem("Reload Configuration", reload_configuration),
                pystray.MenuItem("Open Settings", open_settings),
                pystray.MenuItem("Quit", on_quit)
            )
        )
        icon.run()
    except Exception as e:
        logging.error(f"Error loading tray icon: {e}")

# ========== MAIN ENTRY POINT ==========

if __name__ == "__main__":
    logging.info("Starting OBS Current Song Display")
    threading.Thread(target=song_updater, daemon=True).start()
    threading.Thread(target=start_server, daemon=True).start()
    run_tray()
