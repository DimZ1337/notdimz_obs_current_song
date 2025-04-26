import win32gui

def get_current_song():
    """
    Récupère le titre de la chanson en cours depuis l'application
    YouTube Music Desktop App en détectant la fenêtre active.
    """
    song_title = "No Song"

    def enum_handler(hwnd, ctx):
        nonlocal song_title
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            # La fenêtre a généralement un titre comme : "Artiste - Titre · YouTube Music"
            if "YouTube Music" in window_title:
                song_title = window_title.strip()

    win32gui.EnumWindows(enum_handler, None)
    if "- YouTube Music" in song_title:
        song_title = song_title.split(" - ")[0]
        return song_title
    else:
        return "No Song"