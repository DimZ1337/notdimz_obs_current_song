# OBS Current Song Display

Display your current playing song (Spotify or YouTube Music) inside OBS via a dynamic Flask server and Webview GUI.

## Features
- Dynamic HTML/CSS song preview
- Full color customization
- System tray integration
- Fast reload of settings
- Lightweight .exe compilation

## Project Structure

assets/ # Icons sources/ # Song detection modules settings/ # GUI and Webview for configuration current_song.py # Main server and tray launcher


## How to Build
1. Install dependencies:
```bash
pip install flask pystray pillow pywebview
```
2. Compile the GUI:
```bash
pyinstaller --onefile --noconsole settings/settings_gui.py
```
3. Compile the main server:
```bash
pyinstaller --onefile --noconsole --add-data "assets;assets" current_song.py
```
4. Bundle everything into a release folder!