@echo off
echo Starting FastLoad...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import yt_dlp, tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error: Failed to install required packages
        pause
        exit /b 1
    )
)

REM Launch FastLoad
echo Launching FastLoad...
python fastload.py

if %errorlevel% neq 0 (
    echo.
    echo FastLoad encountered an error.
    pause
)