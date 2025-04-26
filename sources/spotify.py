import win32gui
import win32process
import psutil

def get_spotify_window_title():
    spotify_title = None

    def enum_handler(hwnd, ctx):
        nonlocal spotify_title
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                proc = psutil.Process(pid)
                if proc.name().lower() == "spotify.exe":
                    title = win32gui.GetWindowText(hwnd)
                    if title and title.lower() != "spotify":
                        spotify_title = title
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    win32gui.EnumWindows(enum_handler, None)
    if "Spotify" in spotify_title:
        return "No Song"
    else:
        return spotify_title