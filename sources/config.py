import os

def get_save_path():
    """ Retourne le chemin sûr pour écrire current_song.txt """
    appdata = os.getenv('APPDATA')
    save_folder = os.path.join(appdata, 'OBSCurrentSong')
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    return os.path.join(save_folder, 'current_song.txt')