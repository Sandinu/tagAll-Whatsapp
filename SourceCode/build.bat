@echo off
REM WhatsApp AutoTagger Build Script
REM Author: Sandinu Pinnawala

echo ========================================
echo WhatsApp AutoTagger - Build Script
echo Author: Sandinu Pinnawala
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python found!
echo.

REM Install required packages
echo [2/4] Installing required packages...
pip install pyautogui pyperclip keyboard pillow pygetwindow pystray pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo.

REM Check if script exists
if not exist tagall.py (
    echo ERROR: tagall.py not found in current directory
    pause
    exit /b 1
)

echo [3/4] Building EXE with PyInstaller...
echo.

REM Build with icon if available, otherwise without
if exist app_icon.ico (
    echo Building with custom icon and packaging icon file...
    pyinstaller --onefile --windowed --icon=app_icon.ico --add-data "app_icon.ico;." --name="TagAll" tagall.py
) else (
    echo Building without custom icon...
    pyinstaller --onefile --windowed --name="TagAll" tagall.py
)

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)
echo.

echo [4/4] Cleaning up...
REM Clean up build files
rmdir /s /q build 2>nul
del WhatsApp-AutoTagger.spec 2>nul
echo.

echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Your EXE is located at:
echo %cd%\dist\TagAll.exe
echo.
echo You can now:
echo - Run the EXE directly
echo - Copy it to any Windows PC
echo - Share it with others
echo.
echo To auto-start on boot:
echo 1. Press Win+R
echo 2. Type: shell:startup
echo 3. Copy the EXE to that folder
echo.
pause