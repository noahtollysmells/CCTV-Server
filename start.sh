#!/bin/bash

clear
echo "======================================"
echo "  🎥 CCTV Server Setup"
echo "======================================"
echo ""

# Install deps silently
pip3 install -q Flask Flask-CORS opencv-python 2>/dev/null || sudo pip3 install -q Flask Flask-CORS opencv-python

# Create initial config if missing
if [ ! -f config.json ]; then
  cat > config.json <<EOF
{
  "cameras": [],
  "recordings": "/recordings"
}
EOF
fi

read -p "Recording folder (press Enter for /recordings): " record_path
record_path=${record_path:-/recordings}
mkdir -p "$record_path"

# Keep existing cameras, only update recordings path
python3 - <<PY
import json
with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
cfg.setdefault('cameras', [])
cfg['recordings'] = "$record_path"
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(cfg, f, indent=2)
PY

IP=$(hostname -I | awk '{print $1}')

echo ""
echo "======================================"
echo "✅ RUNNING!"
echo "======================================"
echo ""
echo "Open browser:"
echo "  http://$IP:5000"
echo ""
echo "Recording: $record_path"
echo "Add cameras in the web page."
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
