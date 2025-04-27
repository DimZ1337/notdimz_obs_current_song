@echo off

REM Create build folder if not exists
if not exist build mkdir build

REM Compile settings GUI with HTML embedded
pyinstaller --onefile --noconsole --add-data "..\\settings\\settings_interface.html;settings" --distpath . --workpath build --specpath build settings/settings_gui.py

REM Compile current_song server
pyinstaller --onefile --noconsole --add-data "..\\assets\\*;assets" --distpath . --workpath build --specpath build current_song.py

echo.
echo Build complete!
pause
