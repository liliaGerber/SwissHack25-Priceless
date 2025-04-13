# 🎵 SwissHack25-Priceless

SwissHack25-Priceless is an AI-powered full-stack application developed during SwissHack25, aiming to transcribe, analyze, and semantically interpret audio input. It integrates **WhisperX** for efficient speech-to-text transcription and **Ollama** models (like LLaMA and Mistral) for advanced language processing, all wrapped within a scalable Dockerized microservice architecture.

---

## 🚀 Technologies Used

| Component   | Technology                                   | Purpose                                                                 |
|------------|-----------------------------------------------|-------------------------------------------------------------------------|
| Frontend   | [Vue 3](https://vuejs.org/)                  | User interface with modern JS framework                                |
| Backend    | [Flask](https://flask.palletsprojects.com/) | API server handling ML and DB logic                                    |
| AI/ML      | [WhisperX](https://github.com/m-bain/whisperx) | High-performance audio transcription and alignment                     |
| AI/ML      | [Ollama](https://ollama.com/)                | Local LLM server supporting Mistral and LLaMA                          |
| Database   | [MongoDB](https://www.mongodb.com/)          | NoSQL database for storing transcription data and semantic vectors     |
| Container  | [Docker](https://www.docker.com/)            | Environment and deployment management                                  |
| Orchestration | [Docker Compose](https://docs.docker.com/compose/) | Service linking, volume and port management                            |

---

## 📁 Project Structure

```plaintext
SwissHack25-Priceless/
├── backend/                 # Flask API with WhisperX + Ollama integration
│   ├── app/                 # Application modules
│   │   ├── whisperx_api.py  # WhisperX-based audio transcription
│   │   ├── llm_ollama.py    # Ollama-based semantic parsing
│   │   └── db.py            # MongoDB interaction layer
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # Vue 3 frontend
│   ├── src/
│   │   ├── components/      # UI components
│   │   └── views/           # App views (Home, Result etc.)
│   └── package.json         # JS dependencies and scripts
│
├── data/                    # Data volume and seed data
│
├── compose.dev.yml          # Docker Compose file for development
├── compose.prod.yml         # Docker Compose file for production
└── README.md                # Main documentation
```

---

## 🧠 Core Features

- **🎹 WhisperX Transcription**: Fast and aligned multi-language speech-to-text.
- **🧠 Semantic Search & Embedding**: LLM-generated vector embeddings and summarizations.
- **🔍 Searchability**: Indexed and retrievable audio insights stored in MongoDB.
- **📦 Modular Containers**: Easily scalable via Docker Compose for dev and prod.

---

## ⚙️ Local Development

### 1. Prerequisites

- Docker & Docker Compose
- Node.js (for frontend)
- `pyenv` (recommended for Python)

### 2. Clone the Repository

```bash
git clone https://github.com/liliaGerber/SwissHack25-Priceless.git
cd SwissHack25-Priceless
```

### 3. Development Setup (via Docker Compose)

```bash
docker compose -f compose.dev.yml up --build
```

- Frontend available at: http://localhost:5173
- Backend API on: http://localhost:5000
- MongoDB at: mongodb://localhost:27017

### 4. Stopping Services

```bash
docker compose -f compose.dev.yml down --volumes
```

---

## 🧪 Sub-Module Documentation

### 📁 `frontend/`

```markdown
# Frontend - Vue 3

This folder contains the Vue.ts frontend that serves the user interface for the SwissHack25-Priceless app.

## 📦 Setup

```bash
cd frontend
pnpm install
pnpm dev
```

## 🔨 Build for Production

```bash
pnpm build
```

## 🔧 File Structure

- `src/components/`: Reusable UI components
- `src/views/`: App views
- `main.js`: Entry file
- `vite.config.js`: Vite config
```

---

### 📁 `backend/`

```markdown
# Backend - Flask + AI Services

This folder contains the Flask-based backend which integrates WhisperX and Ollama APIs.

## 💡 Key APIs

- `/transcribe`: Uses WhisperX to transcribe audio
- `/semantic`: Sends data to Ollama for embedding/summarization

## ⚙️ Setup (Manual - Optional)

```bash
cd backend
pyenv install 3.13.1
pyenv virtualenv 3.13.1 venv
pyenv activate venv
pip install -r requirements.txt
```

## 📂 Files

- `whisperx_api.py`: Speech-to-text pipeline
- `llm_ollama.py`: Chat and embedding logic with Ollama
- `db.py`: MongoDB connection and queries
```

---

### 📁 `data/`

```markdown
# Data Folder

This directory holds volume mounts for MongoDB and example seed data for testing.

## 🧪 Usage

Used during container builds to initialize Mongo collections or persist across runs.
```

---

## 👥 Authors

- [Lilia Gerber](https://github.com/liliaGerber)
- [Arka Mitra](https://github.com/thearkamitra)
- [Kaja Vujic](https://github.com/kajavujic)
- [Olha Sirikova](https://github.com/olia110)
---


## 📨 Feedback & Issues

Open an [issue](https://github.com/liliaGerber/SwissHack25-Priceless/issues) or contact [@liliaGerber](https://github.com/liliaGerber).

