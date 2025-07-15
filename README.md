# Fullstack Web Template (FastAPI + React + TypeScript)

This is a minimal fullstack web template using:

- 🧠 **FastAPI** (Python backend)
- ⚛️ **React + TypeScript** (frontend via Vite)
- 🎨 **Tailwind CSS** (optional, for styling)
- 🐳 **Docker Compose** for local dev

---

## 📦 Project Structure

.
├── backend/       # FastAPI backend (API, models, schemas)
├── frontend/      # React + TS frontend (Vite-based)
├── docker-compose.yml
├── requirements.txt / Pipfile
└── .env

---

## 🚀 Getting Started

### 1. Clone and Setup

```bash
git clone https://github.com/yourname/fullstack-web-template.git
cd fullstack-web-template

2. Environment Variables

Create a .env in the root with:

DATABASE_URL=sqlite:///./test.db
API_BASE_URL=http://localhost:8000


⸻

🧪 Run Locally (with Docker)

docker-compose up --build

	•	Frontend: http://localhost:5173
	•	Backend: http://localhost:8000

⸻

🧰 Dev Tools
	•	Backend: FastAPI, Pydantic, Uvicorn, CORS
	•	Frontend: React, TypeScript, Vite
	•	Styling: Tailwind CSS (optional)
	•	Auth: Not included, but easy to add
	•	Database: SQLite (starter), ready for PostgreSQL

⸻

📂 Backend Folder Overview
	•	api/: Route handlers
	•	schemas/: Request/response models (Pydantic)
	•	models/: Database models (if using ORM)
	•	seeds/: Seeding scripts for test/dev data
	•	main.py: FastAPI entrypoint
	•	config.py: App settings, CORS, etc.

⸻

📂 Frontend Folder Overview
	•	src/pages: Page-level routes
	•	src/components: Reusable components
	•	index.tsx: App entry
	•	vite.config.ts: Config (make sure server.host = "0.0.0.0" for Docker)

⸻

🧱 Build Goals

This template is ideal for:
	•	Client dashboards
	•	Admin portals
	•	Inventory/resale websites
	•	Custom CRMs
	•	Any app needing a Python backend + modern frontend

⸻

📜 License

MIT License — free to use, modify, and adapt.
# webpageTemp
# webpageTemp
# webTemp
# webTemp
# webTemp
# webTemp
# webTemp
# surfaceClean
