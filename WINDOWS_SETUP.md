# CCTV Server - Windows Setup Guide

Run the CCTV Server on Windows (instead of Linux).

## Quick Start

### Prerequisites
- **Python 3.9+** installed
- **Git** installed

### Step 1: Install Python

1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **Check: "Add Python to PATH"**
4. Click **Install Now**

Verify:
```cmd
python --version
```

### Step 2: Clone Repository

```cmd
git clone https://github.com/noahtollysmells/CCTV-Server.git
cd CCTV-Server
```

### Step 3: Run Setup

**Option A: Batch File (Recommended)**
```cmd
start.bat
```

**Option B: Command Line**
```cmd
pip install -r requirements.txt
python app.py
```

---

## Interactive Setup (start.bat)

```cmd
start.bat
```

You'll be asked:
1. **Camera URLs** (paste each, press Enter twice when done)
2. **Recording folder** (or press Enter for `C:\cctv-recordings`)

---

## Manual Setup

### 1. Install Dependencies
```cmd
pip install Flask Flask-CORS opencv-python
```

### 2. Create config.json

Create file `config.json` in project folder:

```json
{
  "cameras": [
    {"id": 0, "name": "Front Door", "url": "rtsp://192.168.1.50:8554/stream"},
    {"id": 1, "name": "Hallway", "url": "http://192.168.1.51:8080/?action=stream"}
  ],
  "recordings": "C:/cctv-recordings"
}
```

### 3. Run App
```cmd
python app.py
```

---

## Access

Open browser:
```
http://localhost:5000
```

Or from another computer on your network:
```
http://your-windows-ip:5000
```

Find your IP:
```cmd
ipconfig
```

Look for "IPv4 Address" (usually `192.168.x.x`)

---

## Features

✅ Grid view of all cameras
✅ Click to fullscreen
✅ Record button (saves to your folder)
✅ Connection status indicator
✅ Works on any browser

---

## Get Camera URLs

### Android Phone (IP Webcam App)
1. Install [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam)
2. Start server
3. Copy RTSP URL: `rtsp://phone-ip:8554/stream`

### eBay Camera
```
rtsp://admin:admin@camera-ip:554/stream
```

### HTTP Camera
```
http://camera-ip:8080/?action=stream
```

---

## Troubleshooting

**Python not found:**
- Make sure you checked "Add Python to PATH" during install
- Restart Command Prompt

**Port 5000 already in use:**
- Edit `app.py`, change `port=5000` to `port=5001`

**Can't connect to camera:**
- Make sure camera is on same network
- Test URL in browser first

**Slow performance:**
- Reduce camera resolution
- Lower FPS in camera app settings

---

## Keep It Running

### As Startup Task

1. Press `Win + R`, type `taskschd.msc`
2. Right-click **Task Scheduler Library** → **Create Task**
3. **General** tab:
   - Name: `CCTV Server`
   - Check "Run with highest privileges"
4. **Triggers** tab → **New**:
   - Begin the task: **At startup**
5. **Actions** tab → **New**:
   - Program: `C:\path\to\CCTV-Server\start.bat`
6. Click **OK**

Now it starts automatically!

---

## Stop Server

Press `Ctrl + C` in the Command Prompt window.

---

That's it! Your CCTV server is running on Windows. 🎉
