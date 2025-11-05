# 🐭 Mausritter Tools

**Webová platforma pro generátory a campaign management pro Mausritter TTRPG**

[![Frontend](https://img.shields.io/badge/Frontend-Next.js%2014-black?logo=next.js)](https://nextjs.org/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🎯 Co to je?

Mausritter Tools je neoficiální fan nástroj pro TTRPG hru [Mausritter](https://mausritter.com) od Games Omnivorous. Poskytuje:

- **17 generátorů** - Character, NPC, Weather, Hex, Settlement, Hireling, Spell, Treasure, Adventure, Hook, Creature Variants, Tavern, Dungeon, Rumor, Hexcrawl a další
- **Web interface** - Moderní Next.js 14 frontend s 16 funkčními generátorovými stránkami
- **REST API** - FastAPI backend s auto-generated dokumentací
- **Campaign Management** - Správa kampaní, persistentní postavy (V2 - připravujeme)

**Status:** 🎉 **MVP COMPLETE** - Backend (17/17) + Frontend (16/16) + E2E testy (33) 🎉

---

## ✨ Features

### ✅ **MVP (Hotovo - 2025-11-04)**
- 🎲 **17 plně funkčních generátorů** s REST API
- 🌐 **Next.js frontend** s 16 generator pages
- 🧪 **57 testů celkem** - 24 pytest + 33 Playwright E2E
- 📖 **Auto-generated API docs** (FastAPI Swagger)
- 🎨 **Mausritter design theme** (earthy colors, myší atmosféra)

### ⏳ **V2 (Připravujeme)**
- 🔐 Accounts & Authentication (Supabase Auth)
- 📊 Campaign Management
- 💾 Persistent Characters
- 🗺️ Interactive Hexcrawl Map (5×5 grid)
- 👥 Party & Player Management

### 🔮 **V3+ (Roadmap)**
- 🎲 Real-time Dice Roller
- 📝 Session Notes & Tracker
- 📄 PDF Export
- 🤖 AI Adventure Assistant

Pro detailní roadmap viz [/roadmap](web-frontend/app/roadmap/page.tsx) nebo [WEB_ROADMAP.md](docs/WEB_ROADMAP.md)

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **UI:** shadcn/ui + Tailwind CSS
- **State:** React hooks (useState)
- **Testing:** Playwright E2E (33 tests)
- **Deployment:** Vercel (free tier)

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Generators:** 17 Python modules (src/generators/)
- **Testing:** Pytest (24/24 tests passing)
- **Deployment:** Render (free tier)

### Database (V2+)
- **DB:** PostgreSQL via Supabase
- **Auth:** Supabase Auth
- **Storage:** Supabase Storage

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/your-username/mausritter.git
cd mausritter
```

### 2. Backend Setup

```bash
cd web-backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn app.main:app --port 8001 --reload
```

Backend běží na: **http://localhost:8001**
API Docs: **http://localhost:8001/docs**

### 3. Frontend Setup

```bash
cd web-frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local - set:
# NEXT_PUBLIC_API_URL=http://localhost:8001

# Run development server
npm run dev -- -p 3001
```

Frontend běží na: **http://localhost:3001**

### 4. Test

```bash
# Backend tests
cd web-backend
pytest  # 24/24 tests

# Frontend E2E tests
cd web-frontend
npm run test:e2e  # 33/33 tests
```

---

## 📦 Deployment

### Option A: Cloud Deployment (Doporučeno - FREE)

#### Backend → Render

1. **Vytvoř Render účet** na [render.com](https://render.com)
2. **New Web Service** → Connect GitHub repo
3. **Build Settings:**
   - Root Directory: `web-backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8001`
4. **Environment Variables:**
   ```
   API_PORT=8001
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
5. **Deploy** → Dostaneš URL: `https://mausritter-api.onrender.com`

**Free Tier Limity:**
- ✅ Zdarma navždy
- ⚠️ Spin-down po 15 min (první request pak trvá 30-60s)

#### Frontend → Vercel

1. **Vytvoř Vercel účet** na [vercel.com](https://vercel.com)
2. **Import GitHub repo**
3. **Project Settings:**
   - Framework Preset: Next.js
   - Root Directory: `web-frontend`
4. **Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://mausritter-api.onrender.com
   ```
5. **Deploy** → Dostaneš URL: `https://mausritter-tools.vercel.app`

**Free Tier Limity:**
- ✅ 100GB bandwidth/měsíc
- ✅ Unlimited builds
- ✅ Edge network (global CDN)

### Option B: Docker Deployment

```bash
# Build & Run s Docker Compose
docker-compose up --build

# Frontend: http://localhost:3001
# Backend: http://localhost:8001
```

---

## 📚 Dokumentace

- **[WEB_ARCHITECTURE.md](docs/WEB_ARCHITECTURE.md)** - Tech stack a deployment strategie
- **[WEB_ROADMAP.md](docs/WEB_ROADMAP.md)** - Development roadmap (Week 1-5)
- **[API_ENDPOINTS.md](docs/API_ENDPOINTS.md)** - API dokumentace (17 generátorů)
- **[DATABASE_SCHEMA.sql](docs/DATABASE_SCHEMA.sql)** - Database schema (V2+)
- **[UI_WIREFRAMES.md](docs/UI_WIREFRAMES.md)** - UI/UX design
- **[KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md)** - Bug tracking (29/29 fixed ✅)

---

## 🧪 Testing

### Backend Tests (Pytest)

```bash
cd web-backend
pytest -v  # 24 tests, all passing

# Specific test
pytest tests/test_generators.py::test_character_generator -v
```

### Frontend Tests (Playwright E2E)

```bash
cd web-frontend

# Headless mode
npm run test:e2e

# UI mode (interactive)
npm run test:e2e:ui

# Headed mode (browser visible)
npm run test:e2e:headed
```

**Test Coverage:** 33 tests across 6 suites
- Homepage (5 tests)
- Generator Hub (6 tests)
- Character Generator (6 tests)
- NPC Generator (5 tests)
- Weather Generator (6 tests)
- API Health (5 tests)

---

## 🎲 17 Dostupných Generátorů

### MVP Generators (5/5)
1. **Character Generator** - Kompletní myší postavy (stats, HP, inventory, background)
2. **NPC Generator** - Rychlé NPC (jméno, vzhled, touha, reakce)
3. **Weather Generator** - Počasí a události (4 roční období)
4. **Hex Generator** - Hexy pro hexcrawl (4 terény, 48 detailů)
5. **Settlement Generator** - Myší osady (velikost, vláda, detaily)

### Extended Generators (11/11)
6. **Hireling Generator** - Najatí pomocníci (9 typů se statistikami)
7. **Reaction Roll** - Reakce NPC/tvorů (2k6 mechanika)
8. **Spell Generator** - Náhodná kouzla (16 kouzel)
9. **Treasure Generator** - Poklady (ďobky, meče, kouzla)
10. **Adventure Seeds** - Semínka dobrodružství (tvor + problém + komplikace)
11. **Adventure Hooks** - Háčky pro začátek (6 typů motivací)
12. **Creature Variants** - Varianty stvoření (11 typů: ghost, snake, cat, atd.)
13. **Tavern Generator** - Hospody (názvy + speciality)
14. **Dungeon Generator** - Dobrodružná místa (past, obyvatelé, místnosti)
15. **Rumor Generator** - Zvěsti (6 zvěstí s pravdivostním systémem)
16. **Hexcrawl Generator** - Celý hexcrawl (25 hexů + osady + dungeony)

**Bonus:** Weather Creature Generator (17. - internal použití)

---

## 🤝 Contributing

Contributions are welcome! Toto je fan projekt pro komunitu.

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Guidelines:**
- Následuj existing code style (TypeScript + Python type hints)
- Přidej testy pro nové features
- Aktualizuj dokumentaci

---

## 📖 API Usage

### Character Generator

```bash
curl -X POST http://localhost:8001/api/v1/generate/character \
  -H "Content-Type: application/json" \
  -d '{"name": "Pepřík", "gender": "male"}'
```

### Weather Generator

```bash
curl -X POST http://localhost:8001/api/v1/generate/weather \
  -H "Content-Type: application/json" \
  -d '{"season": "winter", "with_event": true}'
```

Pro všechny endpointy viz [API_ENDPOINTS.md](docs/API_ENDPOINTS.md) nebo Swagger UI na `/docs`.

---

## 📜 License

MIT License - viz [LICENSE](LICENSE)

**Disclaimer:** Toto je neoficiální fan tool. Mausritter je © Games Omnivorous.

---

## 🙏 Credits

- **Mausritter TTRPG** - [Games Omnivorous](https://mausritter.com)
- **Development** - Community project
- **Powered by** - Next.js, FastAPI, Vercel, Render, Supabase

---

## 🐭 Roadmap Overview

| Phase | Status | Features | Timeline |
|-------|--------|----------|----------|
| **MVP (Week 1)** | ✅ Complete | 17 Generators + Frontend + Tests | Done |
| **V2 (Week 2-5)** | ⏳ Planning | Auth + Campaigns + Hexmap | 4 weeks |
| **V3** | 🔮 Future | Dice Roller + Sessions + PDF | TBD |
| **V4** | 🔮 Future | AI Assistant | TBD |

---

**🐭 Happy adventuring in the mouse kingdoms!**

Pro otázky nebo bug reports: [GitHub Issues](https://github.com/your-username/mausritter/issues)
