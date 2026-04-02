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
  "recordings": ""
}
EOF
fi

IP=$(hostname -I | awk '{print $1}')

echo ""
echo "======================================"
echo "✅ RUNNING!"
echo "======================================"
echo ""
echo "Open browser:"
echo "  http://$IP:5000"
echo ""
echo "Recording: Desktop/CCTV-Recordings"
echo "Add cameras in the web page."
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
