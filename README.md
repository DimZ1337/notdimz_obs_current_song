
# 🎵 OBS Current Song Display

Un petit outil Windows qui détecte automatiquement la chanson en cours sur **Spotify** ou **YouTube Music Desktop App** et l'affiche dans **OBS** via un serveur Flask !

> **Fonctionne sous forme d'un exécutable `.exe` avec une icône tray et rafraîchissement automatique.**

---

## 🚀 Fonctionnalités

- 🎧 Détection de la chanson en cours sur Spotify ou YouTube Music
- 🌐 Petit serveur web Flask pour affichage dans OBS via une Source Navigateurs
- 🖥️ Icône dans la zone de notification (tray bar)
- 🔁 Actualisation automatique toutes les 2 secondes
- 🎨 Interface personnalisée (CSS turquoise/rouge)
- ❌ Possibilité de quitter proprement avec clic droit sur l'icône

---

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/tonrepo/obs-current-song.git
cd obs-current-song
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt` :**

```
flask
pystray
pillow
pywin32
```

---

## 📦 Compilation en `.exe` (Windows)

Tu peux utiliser **PyInstaller** pour packager tout en un exécutable :

```bash
pyinstaller --onefile --noconsole --add-data "assets/music_icon.ico;assets" main.py
```

Explication des options :
- `--onefile` : Un seul `.exe`
- `--noconsole` : Pas de fenêtre noire en arrière-plan
- `--add-data` : Ajoute l'icône `.ico`

Le `.exe` sera dans le dossier `dist/`.

---

## 🎥 Utilisation avec OBS

1. **Ajouter une Source Navigateurs** dans OBS
2. URL : `http://127.0.0.1:5000/current-song`
3. Largeur : `300` — Hauteur : `80`
4. Cocher : "Actualiser la page si la source devient active" (optionnel)
5. Profitez de votre affichage musical stylé 🎶

---

## 🧹 Icône Tray

- L'icône de musique apparaît en bas à droite (zone de notification Windows).
- Clic droit → **Quitter** pour fermer proprement l'application.

---

## 🔥 À venir

- Récupérer automatiquement l'artiste pour YouTube Music
- Support de plus de plateformes musicales
- Options de personnalisation plus poussées (CSS, couleurs, etc.)

---

## 📄 Licence

Projet personnel.  
Tu peux l'utiliser, le modifier et le partager librement !

---

## 🎸 Screenshots

(à ajouter plus tard si besoin)

---
