from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# Template HTML avec CSS pour styliser l'affichage
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
            color: #1abc9c; /* Turquoise */
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
        }, 5000);  // Rafraîchit toutes les 5 secondes
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

# Route pour obtenir le titre de la chanson en cours
@app.route('/current-song', methods=['GET'])
def get_current_song():
    try:
        with open("current_song.txt", "r", encoding="utf-8") as f:
            song_title = f.read().strip()
        return render_template_string(HTML_TEMPLATE, song_title=song_title)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, song_title=None), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
