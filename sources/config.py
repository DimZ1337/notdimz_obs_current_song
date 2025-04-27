import os
import json

def get_app_folder():
    """Retourne le chemin vers le dossier AppData de l'application."""
    appdata = os.getenv('APPDATA')
    save_folder = os.path.join(appdata, 'OBSCurrentSong')
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    return save_folder

def get_save_path():
    """Retourne le chemin complet vers le fichier current_song.txt"""
    return os.path.join(get_app_folder(), 'current_song.txt')

def get_log_path():
    """Retourne le chemin complet vers le fichier de log"""
    return os.path.join(get_app_folder(), 'current_song.log')

def load_colors():
    """Charge les couleurs personnalisées depuis settings.json ou valeurs par défaut."""
    settings_path = os.path.join(get_app_folder(), 'settings.json')
    default_colors = {
        "background": "#121212",
        "container": "#2c2c2c",
        "icon_background": "#1a1a1a",
        "text": "#1abc9c",
        "border": "#1abc9c",
        "error_text": "#e74c3c",
    }
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default_colors
    return default_colors
