# OBS Current Song Display

A lightweight Windows application that displays your currently playing song (from Spotify or YouTube Music) into OBS via a dynamic Flask server.

Features real-time color customization with a live preview using a full HTML5/CSS3 WebView GUI.

---

## Features

- 🎵 Detect current song from **Spotify** or **YouTube Music Desktop App**
- 🖌️ **Fully customizable** colors for the display (background, text, border, etc.)
- 🌐 **Real-time live preview** of your settings inside the config interface
- 🖥️ **Web server (Flask)** providing the song title as a browser source for OBS
- 🛎️ **System Tray integration** (Reload configuration / Open settings / Quit)
- 💾 Settings are automatically saved in `%APPDATA%/OBSCurrentSong`
- 🧹 Lightweight executable with no installation required (simple `.exe`)

---

## Project Structure

```
notdimz_obs_current_song/
│
├── assets/            # Icons and static resources
│   └── current_song.ico
│
├── sources/           # Source detection modules
│   ├── youtube.py
│   ├── spotify.py
│   ├── config.py
│
├── settings/          # GUI and HTML interface for settings
│   ├── settings_gui.py
│   ├── settings_interface.html
│
├── current_song.py    # Main server and tray launcher
├── build.bat          # Batch file to automate compilation
├── README.md          # Project documentation
```

---

## Installation & Usage

### 1. Requirements

Install required Python packages:

```bash
pip install flask pystray pillow pywebview
```

### 2. Compilation

Compile both the settings GUI and the main server using PyInstaller:

```bash
cd notdimz_obs_current_song

REM Compile settings GUI
pyinstaller --onefile --noconsole --add-data "settings\\settings_interface.html;settings" --distpath . --workpath build --specpath build settings/settings_gui.py

REM Compile main server
pyinstaller --onefile --noconsole --add-data "assets\\*;assets" --distpath . --workpath build --specpath build current_song.py
```

(You can also simply double-click on `build.bat`)

### 3. Run the Program

After compilation:

- Launch `current_song.exe`
- A system tray icon will appear
- Right-click to:
  - Open settings and customize the colors
  - Reload configuration
  - Quit the application

### 4. Add a Browser Source in OBS

- URL: `http://127.0.0.1:5000/current-song`
- Refresh interval: 5 seconds (auto-refresh embedded)

---

## Next Planned Features

- 🎨 Allow direct font size and font style selection inside settings
- 📄 Multi-line preview if the song title is too long (auto-wrap)
- 🖼️ Show artist thumbnails if available (future integration)
- 📻 Radio station and streaming support detection
- 🚀 Build a full installer (`.exe` via InnoSetup) for user-friendly setup
- 🔔 Tray notifications when a new song is detected
- 🌙 Auto Dark/Light theme mode detection
- 🔄 Automatic refresh without full page reload (via AJAX or WebSocket)

---

## Credits

Developed with ❤️ for the OBS streaming community.

Special thanks for PyWebView, Flask, and the open-source Python community!

---

## License

MIT License - free for personal and commercial use.

---

## Author

**notdimz** 🎸 - 2025

Feel free to fork, suggest improvements, or star the project if you like it!
