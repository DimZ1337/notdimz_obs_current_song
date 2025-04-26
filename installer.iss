[Setup]
AppName=OBS Current Song Display
AppVersion=1.0
DefaultDirName={pf}\OBS Current Song Display
DefaultGroupName=OBS Current Song Display
OutputBaseFilename=obs-current-song-v0.1
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
WizardStyle=modern

[Files]
; Inclure tous les fichiers compilés
Source: "dist\current_song\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
; Créer un raccourci vers l'application
Name: "{group}\OBS Current Song"; Filename: "{app}\current_song.exe"; WorkingDir: "{app}"

[Run]
; Lancer l'application après installation (facultatif)
Filename: "{app}\current_song.exe"; Description: "Lancer OBS Current Song Display"; Flags: nowait postinstall skipifsilent