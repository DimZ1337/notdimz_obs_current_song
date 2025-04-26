
# 🎵 OBS Current Song Display

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)]()

A lightweight Windows tool that automatically detects the currently playing song on **Spotify** or **YouTube Music Desktop App**, and displays it in **OBS** using a simple Flask server!

> **Delivered as a standalone `.exe` file with a system tray icon and automatic song refresh.**

---

## 🚀 Features

- 🎧 Detects currently playing songs from Spotify or YouTube Music
- 🌐 Lightweight Flask web server to serve song info for OBS Browser Source
- 🖥️ Tray icon with a right-click menu
- 🔁 Auto-refresh every 2 seconds
- 🎨 Customizable interface (turquoise/red CSS theme)
- ❌ Clean exit by right-clicking the tray icon

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourrepo/obs-current-song.git
cd obs-current-song
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```
flask
pystray
pillow
pywin32
```

---

## 📦 Build the `.exe` (Windows)

You can use **PyInstaller** to package everything into a standalone executable:

```bash
pyinstaller --onefile --noconsole --add-data "assets/music_icon.ico;assets" current_song.py
```

Explanation of options:
- `--onefile`: Create a single `.exe` file
- `--noconsole`: No background console window
- `--add-data`: Include the `assets` folder and the icon

The final `.exe` will be in the `dist/` directory.

---

## 🎥 Use with OBS

1. Add a new **Browser Source** in OBS
2. URL: `http://127.0.0.1:5000/current-song`
3. Width: `300` — Height: `80`
4. Optionally check: "Refresh browser when scene becomes active"
5. Enjoy your stylish music display 🎶

---

## 🧹 System Tray Icon

- A small music note icon appears in the Windows tray bar.
- Right-click → **Quit** to close the application cleanly.

---

## 🔥 Upcoming Improvements

- Automatically detect artist info for YouTube Music
- Support for more music platforms
- More customization options (CSS, theme colors, animations)

---

## 📄 License

This project is licensed under the MIT License.  
Feel free to use, modify, and share it!

---

## 🎸 Screenshots

(To be added soon)

---
