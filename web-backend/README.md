# 🐭 Mausritter Web API (Backend)

FastAPI backend wrappující existující Python generátory pro web interface.

**Status:** ✅ ALL 17 Generators Implemented - Complete REST API

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

## 📋 Implementované Endpointy (17/17)

### Generátory

**Base URL:** `/api/v1/generate/`

#### MVP Generátory (5)
- ✅ `POST /character` - Generuj postavu
- ✅ `POST /npc` - Generuj NPC
- ✅ `POST /hex` - Generuj hex
- ✅ `POST /settlement` - Generuj osadu
- ✅ `POST /weather` - Generuj počasí

#### Rozšířené Generátory (12)
- ✅ `POST /hireling` - Generuj pomocníka
- ✅ `POST /reaction` - Generuj reakci NPC
- ✅ `POST /spell` - Generuj kouzlo
- ✅ `POST /treasure` - Generuj poklad
- ✅ `POST /adventure` - Generuj adventure seed
- ✅ `POST /hook` - Generuj adventure hook
- ✅ `POST /creature/{type}` - Generuj creature variantu (11 typů)
- ✅ `POST /tavern` - Generuj hospodu
- ✅ `POST /dungeon` - Generuj dungeon
- ✅ `POST /rumor` - Generuj zvěsti (6×)
- ⚠️ `POST /hexcrawl` - Generuj hexcrawl (encoding issue na Windows)

### Status

- ✅ `GET /api/v1/generate/status` - Seznam všech generátorů (vrací 17/17)

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

### ✅ Completed Features

- ✅ Všech 17 generátorů implementováno
- ✅ Pydantic Request models s validací
- ✅ Swagger UI dokumentace (`/docs`)
- ✅ Error handling pro všechny endpointy
- ✅ CORS middleware pro frontend komunikaci

### 🔜 Next Steps (V2)

- [ ] Supabase integrace (databáze)
- [ ] Authentication (JWT)
- [ ] Campaign CRUD endpoints
- [ ] WebSocket pro real-time dice
- [ ] Rate limiting
- [ ] Caching strategie

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
