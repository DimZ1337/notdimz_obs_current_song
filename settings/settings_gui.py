import webview
import os
import json
import shutil
import sys

APP_FOLDER = os.path.join(os.getenv('APPDATA'), 'OBSCurrentSong')
CONFIG_FILE = os.path.join(APP_FOLDER, 'settings.json')

# Handle PyInstaller _MEIPASS path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Api:
    def save_settings(self, settings):
        os.makedirs(APP_FOLDER, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
        webview.windows[0].destroy()

if __name__ == '__main__':
    # Copy the HTML to a real accessible path
    os.makedirs(APP_FOLDER, exist_ok=True)
    src_html = resource_path('settings/settings_interface.html')
    dst_html = os.path.join(APP_FOLDER, 'settings_interface.html')
    shutil.copy(src_html, dst_html)

    api = Api()
    webview.create_window('OBS Current Song - Settings', dst_html, js_api=api)
    webview.start()
