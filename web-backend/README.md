# 🐭 Mausritter Web API (Backend)

FastAPI backend wrappující existující Python generátory pro web interface.

**Status:** ✅ MVP Week 1 Complete - 5 generátorů funkčních a otestovaných

---

## 🚀 Quick Start

### 1. Instalace dependencies

```bash
cd web-backend
pip install -r requirements.txt
```

### 2. Spuštění development serveru

```bash
# Spustit z root složky projektu (mausritter/)
cd web-backend
python -m uvicorn app.main:app --reload
```

Server běží na: **http://localhost:8000**

### 3. API dokumentace

- Swagger UI: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**
- Health check: **http://localhost:8000/health**

---

## 📋 Implementované Endpointy (MVP)

### Generátory

**Base URL:** `/api/v1/generate/`

- ✅ `POST /character` - Generuj postavu
- ✅ `POST /npc` - Generuj NPC
- ✅ `POST /hex` - Generuj hex
- ✅ `POST /settlement` - Generuj osadu
- ✅ `POST /weather` - Generuj počasí

### Status

- ✅ `GET /api/v1/generate/status` - Seznam všech generátorů

### Utility

- ✅ `GET /health` - Health check
- ✅ `GET /` - Root endpoint

---

## 🧪 Testování API

### cURL příklady

**Character Generator:**
```bash
curl -X POST http://localhost:8000/api/v1/generate/character \
  -H "Content-Type: application/json" \
  -d '{"name": "Pepřík", "gender": "male"}'
```

**Weather Generator:**
```bash
curl -X POST http://localhost:8000/api/v1/generate/weather \
  -H "Content-Type: application/json" \
  -d '{"season": "autumn", "with_event": true}'
```

---

## 📁 Struktura Projektu

```
web-backend/
├── app/
│   ├── main.py              # FastAPI aplikace
│   ├── routers/
│   │   ├── generators.py    # Generator endpoints
│   │   └── __init__.py
│   └── __init__.py
├── requirements.txt         # Python dependencies
├── Dockerfile              # Pro deployment
├── .env.example            # Environment variables template
└── README.md
```

---

## 🔧 Konfigurace

### Environment Variables

Zkopíruj `.env.example` do `.env`:
```bash
cp .env.example .env
```

**Proměnné:**
- `API_HOST` - Host adresa (default: 0.0.0.0)
- `API_PORT` - Port (default: 8000)
- `CORS_ORIGINS` - Povolené originy pro CORS (default: localhost:3000,3001)

---

## 🚢 Deployment

### Railway

1. Push projekt do GitHub
2. Connect repo v Railway
3. Railway automaticky detekuje `Dockerfile`
4. Nastav environment variables
5. Deploy!

### Docker

```bash
docker build -t mausritter-api .
docker run -p 8000:8000 mausritter-api
```

---

## 📝 Poznámky

### Závislosti na existujícím kódu

API wrappuje generátory z `src/generators/`:
- `src/generators/character.py`
- `src/generators/npc.py`
- `src/generators/hex.py`
- `src/generators/settlement.py`
- `src/generators/weather.py`

**Důležité:** Backend předpokládá, že má přístup k `src/` a `data/` složkám z root projektu.

### V2 Features (TODO)

- [ ] Zbývajících 12 generátorů
- [ ] Supabase integrace (databáze)
- [ ] Authentication (JWT)
- [ ] Campaign CRUD endpoints
- [ ] WebSocket pro real-time dice

---

## 🐛 Debugging

### Chyba: ModuleNotFoundError: No module named 'src'

**Řešení:** Ujisti se, že spouštíš server z root složky projektu (mausritter/), ne z web-backend/.

```bash
# ✅ Správně (z mausritter/)
cd web-backend
python -m uvicorn app.main:app --reload

# ❌ Špatně (src/ není accessible)
cd mausritter/web-backend
uvicorn app.main:app --reload
```

### Chyba: Address already in use

Port 8000 je obsazený. Zkus jiný port:
```bash
uvicorn app.main:app --reload --port 8001
```

---

## 📚 Další Dokumentace

- [API Endpoints Spec](../docs/API_ENDPOINTS.md)
- [Database Schema](../docs/DATABASE_SCHEMA.sql)
- [Web Roadmap](../docs/WEB_ROADMAP.md)
- [Architecture](../docs/WEB_ARCHITECTURE.md)

---

**Last updated:** 2025-11-03
