# Mausritter Tools

## Tech Stack
- Backend: FastAPI, Python 3.12, Pydantic
- Frontend: Next.js 14 App Router, TypeScript, Tailwind CSS
- CLI: 17 Python generators v `src/generators/`

## Development Ports (FIXED - DO NOT CHANGE)
- Frontend: `localhost:3001`
- Backend: `localhost:8001`
- Swagger UI: `localhost:8001/docs`

## Commands
```bash
# Backend (z root)
cd web-backend
python -m uvicorn app.main:app --port 8001

# Frontend
cd web-frontend
npm run dev -- -p 3001
```