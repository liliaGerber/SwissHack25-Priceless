# Real-Time Whisper Transcriber + WebSocket Viewer

This project uses `faster-whisper` for fast local transcription of microphone input, speaker detection, and streams the output via WebSocket to a minimal browser-based frontend.

---

## 🚀 Features

- Local real-time transcription (Whisper with `faster-whisper`)
- Lightweight pitch-based speaker identification
- WebSocket broadcast to a Vue + Tailwind frontend
- No build tools required – just open an HTML file

---

## 🧱 Requirements

- Python 3.9–3.13
- A working microphone
- Linux/macOS (or Windows with compatible audio drivers)

---

## 🛠 Setup

### 1. Clone & install dependencies
```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```
### 2. Start the transcriber
```bash
python real_time_transcriber_local_whisper.py
```

You should see:
```bash
WebSocket server started on ws://0.0.0.0:8765
Start speaking... (Press CTRL+C to stop)
```
### 3. Open the frontend
    Open index.html in any browser
    Transcribed text will appear in real time
ru this commands in backend/models
```bash
python3 -m http.server 8080
```