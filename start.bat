@echo off
setlocal enabledelayedexpansion

cls
echo ======================================
echo   CCTV Server Setup
echo ======================================
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q Flask Flask-CORS opencv-python 2>nul || (
    echo Installing with admin...
    python -m pip install --upgrade pip >nul 2>&1
    pip install Flask Flask-CORS opencv-python
)

REM Check if config.json exists
if exist config.json (
    cls
    echo ======================================
    echo   CCTV Server Running
    echo ======================================
    echo.
    echo Open browser: http://localhost:5000
    echo.
    echo Press Ctrl+C to stop
    echo.
    python app.py
) else (
    cls
    echo ======================================
    echo   First Time Setup
    echo ======================================
    echo.
    echo Create config.json with your cameras:
    echo.
    echo Example URL^(s^):
    echo   rtsp://192.168.1.50:8554/stream
    echo   http://192.168.1.51:8080/?action=stream
    echo.
    echo Open config.json in a text editor and add your camera URLs.
    echo.
    echo Then run this file again.
    echo.
    
    REM Create template config
    (
        echo {
        echo   "cameras": [
        echo     {"id": 0, "name": "Camera 1", "url": "rtsp://192.168.1.50:8554/stream"}
        echo   ],
        echo   "recordings": "C:/cctv-recordings"
        echo }
    ) > config.json
    
    echo Created config.json - edit it now!
    echo.
    timeout /t 3
    start config.json
)

pause
