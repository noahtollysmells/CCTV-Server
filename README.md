# 🎥 CCTV Server

**One command. Two questions. Done.**

## Run

```bash
git clone https://github.com/noahtollysmells/CCTV-Server.git
cd CCTV-Server
bash start.sh
```

## You'll be asked:

1. **Camera URLs** (one per line, press Enter twice)
2. **Where to save recordings** (press Enter for `/recordings`)

## Then:
- Open browser: `http://your-server-ip:5000`
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

**HTTP Camera:**
```
http://192.168.1.51:8080/?action=stream
```

---

**That's it.**
