#!/usr/bin/env python3
"""CCTV Server - Simple Camera Viewer with Recording"""

from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS
import json
import cv2
import threading
import time
import os
from urllib.parse import urlsplit, urlunsplit

app = Flask(__name__)
CORS(app)

cameras = {}
config = {}
recordings = {}


def get_default_recordings_path():
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    if not os.path.isdir(desktop):
        desktop = os.path.expanduser('~')
    return os.path.join(desktop, 'CCTV-Recordings')


DEFAULT_RECORDINGS_PATH = get_default_recordings_path()


def save_config():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)


def normalize_camera_url(url):
    raw = (url or '').strip()
    if not raw:
        return raw

    # Allow entering only host/path and assume RTSP with default credentials.
    if '://' not in raw:
        return f"rtsp://admin:admin@{raw.lstrip('/')}"

    parsed = urlsplit(raw)
    if parsed.scheme.lower() == 'rtsp' and '@' not in parsed.netloc:
        return urlunsplit((parsed.scheme, f"admin:admin@{parsed.netloc}", parsed.path, parsed.query, parsed.fragment))

    return raw


class CameraStream:
    def __init__(self, cam_id, name, url, record_path=None):
        self.id = cam_id
        self.name = name
        self.url = normalize_camera_url(url)
        self.record_path = record_path
        self.cap = None
        self.last_frame = None
        self.is_connected = False
        self.is_recording = False
        self.writer = None
        self.record_filename = None
        self.record_fps = 20
        self.connect()
    
    def connect(self):
        try:
            self.cap = cv2.VideoCapture(self.url)
            self.is_connected = self.cap.isOpened()
            if self.is_connected:
                threading.Thread(target=self._read_frames, daemon=True).start()
                print(f"✅ {self.name}")
        except Exception as e:
            print(f"❌ {self.name}: {e}")
    
    def _read_frames(self):
        while True:
            try:
                if not self.is_connected or not self.cap:
                    time.sleep(1)
                    continue
                
                ret, frame = self.cap.read()
                if ret:
                    self.last_frame = frame.copy()
                    if self.is_recording and self.writer is None:
                        self._create_writer_from_frame(frame)
                    if self.is_recording and self.writer:
                        self.writer.write(frame)
                else:
                    self.is_connected = False
                    self.connect()
                    time.sleep(2)
            except Exception as e:
                print(f"Error {self.name}: {e}")
                self.is_connected = False
                time.sleep(2)
    
    def get_frame_bytes(self):
        if self.last_frame is None:
            return None
        try:
            ret, buffer = cv2.imencode('.jpg', self.last_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            return buffer.tobytes() if ret else None
        except:
            return None
    
    def start_recording(self):
        if self.is_recording:
            return False
        try:
            self.record_path = DEFAULT_RECORDINGS_PATH
            os.makedirs(self.record_path, exist_ok=True)
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            safe_name = ''.join(ch if ch.isalnum() or ch in ('-', '_', ' ') else '_' for ch in self.name).strip().replace(' ', '_')
            self.record_filename = os.path.join(self.record_path, f"{safe_name}_{timestamp}.mp4")
            try:
                cap_fps = float(self.cap.get(cv2.CAP_PROP_FPS)) if self.cap else 0
            except Exception:
                cap_fps = 0
            self.record_fps = cap_fps if cap_fps and cap_fps > 1 else 20
            self.is_recording = True
            if self.last_frame is not None:
                self._create_writer_from_frame(self.last_frame)
            print(f"⏺️ Recording {self.name} to {self.record_filename}")
            return True
        except Exception as e:
            print(f"Record error {self.name}: {e}")
            return False

    def _create_writer_from_frame(self, frame):
        if self.writer is not None:
            return
        if frame is None or self.record_filename is None:
            return
        h, w = frame.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.record_filename, fourcc, self.record_fps, (w, h))
        if not self.writer or not self.writer.isOpened():
            self.writer = None
            self.is_recording = False
            print(f"❌ Failed to open writer for {self.name}")
    
    def stop_recording(self):
        if self.writer:
            self.writer.release()
            self.writer = None
        self.is_recording = False
        self.record_filename = None
        print(f"⏹️ Stopped recording {self.name}")

    def release(self):
        if self.writer:
            self.writer.release()
            self.writer = None
        if self.cap:
            self.cap.release()
            self.cap = None
        self.is_connected = False


def load_config():
    global cameras, config
    try:
        with open('config.json') as f:
            config = json.load(f)

        config['recordings'] = DEFAULT_RECORDINGS_PATH
        save_config()
        record_path = DEFAULT_RECORDINGS_PATH
        
        for cam in config.get('cameras', []):
            cam_id = cam['id']
            cameras[cam_id] = CameraStream(cam_id, cam['name'], cam['url'], record_path)
    except Exception as e:
        print(f"Config error: {e}")


@app.route('/')
def index():
    return render_template('simple.html')


@app.route('/api/cameras')
def get_cameras():
    cam_list = []
    for cam_id in sorted(cameras.keys()):
        cam = cameras[cam_id]
        cam_list.append({
            'id': cam_id,
            'name': cam.name,
            'connected': cam.is_connected,
            'recording': cam.is_recording
        })
    return jsonify(cam_list)


@app.route('/api/cameras', methods=['POST'])
def add_camera():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    url = (data.get('url') or '').strip()

    if not name or not url:
        return jsonify({'error': 'Name and URL are required'}), 400

    existing_ids = set(cameras.keys())
    new_id = 0
    while new_id in existing_ids:
        new_id += 1

    record_path = DEFAULT_RECORDINGS_PATH
    cameras[new_id] = CameraStream(new_id, name, url, record_path)

    config.setdefault('cameras', []).append({
        'id': new_id,
        'name': name,
        'url': url
    })
    save_config()

    return jsonify({'id': new_id, 'name': name, 'url': url})


@app.route('/api/cameras/<int:cam_id>', methods=['DELETE'])
def delete_camera(cam_id):
    camera = cameras.pop(cam_id, None)
    if not camera:
        return jsonify({'error': 'Camera not found'}), 404

    camera.stop_recording()
    camera.release()

    config['cameras'] = [cam for cam in config.get('cameras', []) if cam.get('id') != cam_id]
    save_config()
    return jsonify({'ok': True})


@app.route('/api/settings/recordings', methods=['POST'])
def set_recordings_path():
    os.makedirs(DEFAULT_RECORDINGS_PATH, exist_ok=True)
    config['recordings'] = DEFAULT_RECORDINGS_PATH

    for camera in cameras.values():
        camera.record_path = DEFAULT_RECORDINGS_PATH

    save_config()
    return jsonify({'recordings': DEFAULT_RECORDINGS_PATH})


@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify({'recordings': DEFAULT_RECORDINGS_PATH})


@app.route('/api/stream/<int:cam_id>')
def stream(cam_id):
    def generate():
        while True:
            camera = cameras.get(cam_id)
            if not camera:
                break
            
            frame_bytes = camera.get_frame_bytes()
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n'
                       b'Content-Length: ' + str(len(frame_bytes)).encode() + b'\r\n\r\n'
                       + frame_bytes + b'\r\n')
            else:
                time.sleep(0.1)
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/record/<int:cam_id>', methods=['POST'])
def toggle_record(cam_id):
    camera = cameras.get(cam_id)
    if not camera:
        return jsonify({'error': 'Camera not found'}), 404
    
    action = request.json.get('action', 'start')
    
    if action == 'start':
        success = camera.start_recording()
        return jsonify({'recording': success})
    elif action == 'stop':
        camera.stop_recording()
        return jsonify({'recording': False})
    
    return jsonify({'error': 'Invalid action'}), 400


if __name__ == '__main__':
    load_config()
    print("\n🚀 CCTV Server running\n")
    app.run(host='0.0.0.0', port=5000, threaded=True)
