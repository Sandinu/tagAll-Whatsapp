@echo off
echo ========================================
echo Installing WhatsApp Tag All Tool
echo ========================================
echo.
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)
echo.
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo You can now run the tool using: python tagall.py
echo Or simply double-click run.bat
echo.
pause
