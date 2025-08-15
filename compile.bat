@echo off
echo AI-Powered Sudoku Solver - Compilation Script
echo ============================================

echo Installing dependencies...
pip install -r requirements.txt

echo Creating app icon...
python create_icon.py

echo Compiling to executable...
pyinstaller --onefile --windowed --icon=icon.ico --name="AI-Sudoku-Solver" main_gui.py

echo.
echo Compilation complete!
echo Executable can be found in the 'dist' folder.
echo.
pause
