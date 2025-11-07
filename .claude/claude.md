# Mausritter Tools

mluv se mnou českým jazykem

## 🎯 AKTUÁLNÍ PRÁCE
**Branch:** `feature/game-page` | **Stránka:** `/game` (GM Dashboard)
**Stav:** Phase 1A ✅ hotovo (Party Panel, Time/Weather) → Phase 1B 🔄 připraveno (Tab System, Bestiary, Canvas)
📖 Dokumentace: [CURRENT_WORK.md](../web-frontend/docs/CURRENT_WORK.md) | [Roadmapa](../web-frontend/docs/game-dashboard-roadmap.md)

## 🌐 Production (OVĚŘENO)
- **Frontend**: https://mausritter-tools.vercel.app (Vercel)
- **Backend**: https://mausritter-tools.onrender.com (Render)
- **Health check**: `/health` endpoint vrací `{"status":"healthy"}`

## 🔧 Tech Stack
- **Backend**: FastAPI, Python 3.12, Pydantic, Docker
- **Frontend**: Next.js 14 App Router, TypeScript, Tailwind CSS, Radix UI
- **CLI**: 17 Python generátorů v `src/generators/`
- **Hosting**: Vercel (frontend), Render (backend)

## 🚀 Development

### Ports (FIXED - DO NOT CHANGE)
- **Frontend**: `localhost:3001` (Next.js)
- **Backend**: `localhost:8001` (FastAPI)
- **Swagger UI**: `localhost:8001/docs`

### Start Servers
```bash
# Backend (z root)
cd web-backend
python -m uvicorn app.main:app --reload --port 8001

# Frontend (z root)
cd web-frontend
npm run dev -- -p 3001
```

## ⚙️ Configuration

### Environment Variables
- **Vercel Production**: `NEXT_PUBLIC_API_URL=https://mausritter-tools.onrender.com`
- **Local Development**: Fallback v `next.config.js:7` → `http://localhost:8001`

### CORS Setup (KRITICKÉ!)
Backend `web-backend/app/main.py:23-28` **MUSÍ** obsahovat:
```python
allow_origins=[
    "http://localhost:3001",  # Next.js dev server
    "https://mausritter-tools.vercel.app",  # Production
    "https://mausritter-tools-git-master-bruxs-projects.vercel.app",  # Git branch
    "https://*.vercel.app",  # Preview URLs
]
```

⚠️ **Pokud generátory nefungují online → zkontroluj CORS!**

## 🤝 Workflow s uživatelem (KRITICKÉ!)

### VŽDY na začátku každé úlohy se ZEPTAT:
```
❓ "Na jaké git branch chceš pracovat?"

   Možnosti:
   a) Vytvořit novou branch: feature/nazev (DOPORUČENO)
   b) Pracovat na existující branch
   c) Master (změny jdou PŘÍMO na produkci!)
```

### Bezpečný development workflow:
```bash
# 1. Vytvoř feature branch
git checkout -b feature/nazev-funkce

# 2. Pracuj lokálně a commituj
git add .
git commit -m "Popis změny"
git push origin feature/nazev-funkce

# 3. Testuj na localhostu (3001 + 8001)
# Web na produkci zůstává beze změny!

# 4. ⚠️ VŽDY SE ZEPTAT před mergem:
# "Mám mergovat do masteru? Tím se změny DEPLOYNY na web!"

# 5. Po schválení uživatele:
git checkout master
git merge feature/nazev-funkce
git push  # ← Auto-deploy na produkci
```

### PRAVIDLA:
- ✅ VŽDY nabídnout vytvoření feature branch
- ✅ VŽDY vysvětlit dopad (branch = bezpečné, master = produkce)
- ✅ VŽDY se zeptat před mergem do masteru
- ❌ NIKDY nedělat změny přímo na master bez dotazu
- ❌ NIKDY nepushovat na master bez potvrzení

## 🚢 Deployment

### Auto-Deploy z `master` branch
- **Render**: Docker build (~1-2 min) → `https://mausritter-tools.onrender.com`
- **Vercel**: Next.js build (~55s) → `https://mausritter-tools.vercel.app`
- Push na `master` → obě platformy se automaticky redeployují
- **Push na jinou branch = ŽÁDNÝ deploy na produkci**

### Vercel Build Settings
- **Framework Preset**: Next.js (NE "Other"!)
- **Root Directory**: `web-frontend`
- **Build Command**: Auto-detect (`npm run build`)
- **Output Directory**: Auto-detect (`.next`)

## 🐛 Troubleshooting

### Generátory nefungují online
1. Zkontroluj CORS v `main.py` - musí obsahovat Vercel domény
2. Ověř `NEXT_PUBLIC_API_URL` v Vercel Settings → Environment Variables
3. Zkontroluj backend health: `https://mausritter-tools.onrender.com/health`

### Port už používán (3001 nebo 8001)
```bash
# Najdi proces
netstat -ano | findstr :3001

# Ukonči proces (PowerShell)
powershell -Command "Stop-Process -Id <PID> -Force"
```

### Vercel vrací 404
- Framework Preset **musí být Next.js** (ne "Other")
- Root Directory **musí být web-frontend**
- Zkontroluj build logs - build musí trvat ~55s (ne 4-5s)

### Backend nemá CORS
Symptom: Console error `Access to fetch at '...' has been blocked by CORS policy`
→ Přidej Vercel URL do `allow_origins` v `main.py` a redeploy na Render
