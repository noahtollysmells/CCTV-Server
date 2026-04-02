#!/bin/bash

clear
echo "======================================"
echo "  🎥 CCTV Server Setup"
echo "======================================"
echo ""

# Install deps silently
pip3 install -q Flask Flask-CORS opencv-python 2>/dev/null || sudo pip3 install -q Flask Flask-CORS opencv-python

# Create config
echo "Enter camera URLs (one per line, press Enter twice when done):"
echo "Examples:"
echo "  rtsp://192.168.1.50:8554/stream"
echo "  http://192.168.1.51:8080/?action=stream"
echo ""

cameras='['
count=0

while IFS= read -p "Camera URL: " url; do
  if [ -z "$url" ]; then
    if [ $count -gt 0 ]; then
      break
    fi
    echo "Enter at least one camera!"
    continue
  fi
  
  if [ $count -gt 0 ]; then
    cameras="$cameras,"
  fi
  
  cameras="$cameras{\"id\":$count,\"name\":\"Camera $((count+1))\",\"url\":\"$url\"}"
  count=$((count+1))
  echo "✓ Added"
done

cameras="$cameras]"

echo ""
read -p "Recording folder (press Enter for /recordings): " record_path
record_path=${record_path:-/recordings}

# Create recordings dir
mkdir -p "$record_path"

# Write config
cat > config.json <<EOF
{
  "cameras": $cameras,
  "recordings": "$record_path"
}
EOF

IP=$(hostname -I | awk '{print $1}')

echo ""
echo "======================================"
echo "✅ RUNNING!"
echo "======================================"
echo ""
echo "Open browser:"
echo "  http://$IP:5000"
echo ""
echo "Cameras: $count"
echo "Recording: $record_path"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
