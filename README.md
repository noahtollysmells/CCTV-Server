# 🎥 CCTV Server

**One command. Open browser. Add cameras there. Done.**

## Run

```bash
git clone https://github.com/noahtollysmells/CCTV-Server.git
cd CCTV-Server
bash start.sh
```

## Recording

- Recordings always save to your local Desktop folder: `Desktop/CCTV-Recordings`

## Then:
- Open browser: `http://your-server-ip:5000`
- Add camera name + URL in the **Add Camera** box
- For RTSP cameras, `admin/admin` is auto-added if credentials are missing
- Recording badge flashes `REC` in the top-right while recording
- Click any camera to expand
- Click **REC** to record
- Done

---

## Get Your Camera URLs

**Android Phone (IP Webcam app):**
```
rtsp://192.168.1.50:8554/stream
```

**eBay Camera:**
```
rtsp://admin:admin@192.168.1.52:554/stream
```

You can also enter without credentials and it will use `admin/admin` automatically:
```
rtsp://192.168.1.52:554/stream
```

**HTTP Camera:**
```
http://192.168.1.51:8080/?action=stream
```

---

---

## 🪟 Windows Setup?

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for Windows instructions.

**That's it.**
