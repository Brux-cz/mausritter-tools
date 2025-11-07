# 🎯 KDE JSEM SKONČIL - Quick Start Guide

**Poslední update:** 2025-11-07
**Branch:** `feature/game-page`
**Status:** Phase 1A ✅ HOTOVO → Phase 1B 🔄 PŘIPRAVENO

---

## ⚡ RYCHLÝ START (Jak pokračovat)

### 1️⃣ Přepni se na správnou branch:
```bash
git checkout feature/game-page
```

### 2️⃣ Spusť servery:
```bash
# Frontend (z root)
cd web-frontend
npm run dev -- -p 3001

# Backend (z root, nové okno)
cd web-backend
python -m uvicorn app.main:app --reload --port 8001
```

### 3️⃣ Otevři v prohlížeči:
```
http://localhost:3001/game
```

### 4️⃣ Co vidíš:
- ✅ Party Panel s 4 myšími (Pip, Rosa, Max, Lily)
- ✅ Time & Weather Panel (funguje Next Watch + Roll Weather)
- ✅ Click na myš → otevře sidebar s character sheet
- 🔄 Placeholder pro Hex Map (coming soon)

---

## 📁 CO BYLO VYTVOŘENO (Phase 1A)

### Hlavní soubory:
```
web-frontend/
├── app/game/page.tsx                    ← Hlavní stránka GM Dashboard
├── components/game/
│   ├── PartyPanel.tsx                   ← 4 myši s HP bary
│   ├── MouseDetailSidebar.tsx           ← Character sheet sidebar
│   └── TimeWeatherPanel.tsx             ← Time + Weather + Encounters
├── lib/types/campaign.ts                ← TypeScript interfaces (Mouse, Campaign, atd.)
└── docs/
    ├── game-dashboard-roadmap.md        ← KOMPLETNÍ roadmapa
    └── CURRENT_WORK.md                  ← Tento soubor
```

### Co funguje:
- ✅ Click na myš → Sidebar s detaily (HP, Grit, Pips, Background, Notes)
- ✅ Next Watch button → Posune čas (Morning → Afternoon → Evening → Night)
- ✅ Roll Weather → 2d6 podle Mausritter pravidel (Harsh/Normal/Favourable/Extreme)
- ✅ LocalStorage auto-save (campaign state persistuje mezi reloadama)
- ✅ Mock data (4 testovací myši načtené z `createMockCampaign()`)

---

## 🎯 CO DĚLAT PŘÍŠTĚ (Phase 1B)

### Priority:
1. **Tab System** (3 tabs: Hex Map | Tactical | Bestiary)
2. **Bestiary Panel** (static creatures + generate button)
3. **Tactical Canvas** (drawing + image upload)

### Konkrétní kroky:

#### 1. Tab System
```typescript
// Vytvořit: components/game/TabSystem.tsx
// 3 taby:
// - 🗺️ Hex Map (default)
// - 🎨 Tactical Map
// - 📚 Bestiary

// State:
type ActiveTab = 'hexmap' | 'tactical' | 'bestiary';
```

#### 2. Bestiary Panel
```typescript
// Vytvořit: components/game/BestiaryPanel.tsx
// Vytvořit: lib/data/creatures.json

// Funkce:
// - Zobrazit list creatures (Owl, Snake, Fox, Spider...)
// - Search/filter
// - Click creature → Detail view
// - Button "Generate Custom" → call backend /generate/creature
```

#### 3. Tactical Canvas
```typescript
// Vytvořit: components/game/TacticalCanvas.tsx

// Funkce:
// - HTML5 Canvas drawing
// - Tools: pen, eraser, shapes (circle, rectangle)
// - Image upload (drag & drop)
// - Save canvas do campaign.tacticalMaps.current
```

---

## 📚 DŮLEŽITÉ DOKUMENTY

### 1. **Kompletní Roadmapa:**
📄 `web-frontend/docs/game-dashboard-roadmap.md`
- Celý plán (Phase 1A-6)
- Data structures
- Backend endpoints
- Mausritter pravidla reference

### 2. **Hex Layout Fix:**
📄 `web-frontend/docs/hex-layout-fix.md`
- Jak opravit hex geometrii (pokud se rozbije)
- Backup commit: `a60885f`

### 3. **Claude Instructions:**
📄 `.claude/CLAUDE.md`
- Tech stack
- Development workflow
- CORS setup
- Port configuration (3001 frontend, 8001 backend)

---

## 🔗 BACKEND ENDPOINTS (Existující)

### Zkontrolovat jestli backend běží:
```bash
curl http://localhost:8001/health
# Mělo by vrátit: {"status":"healthy"}
```

### Generators (pro Phase 1B+):
```bash
# Generate creature
POST http://localhost:8001/generate/creature

# Generate NPC
POST http://localhost:8001/generate/npc

# Generate hexcrawl
POST http://localhost:8001/generate/hexcrawl
```

---

## 🐛 Troubleshooting

### Port už používán (3001 nebo 8001):
```bash
# Najdi proces
netstat -ano | findstr :3001

# Ukonči proces (PowerShell)
powershell -Command "Stop-Process -Id <PID> -Force"
```

### Campaign state nefunguje:
```javascript
// V browser console:
localStorage.getItem('mausritter-campaign')

// Clear campaign:
localStorage.removeItem('mausritter-campaign')
// Pak reload page → vytvoří nový mock campaign
```

### Komponenta se neimportuje:
```typescript
// Zkontroluj path alias v tsconfig.json:
"@/components/*" → "web-frontend/components/*"
"@/lib/*" → "web-frontend/lib/*"
```

---

## 📦 DATA FLOW

```
User opens /game
     ↓
Load campaign from localStorage
     ↓
Render Party Panel + Time/Weather
     ↓
User clicks mouse → Open sidebar
     ↓
User clicks "Next Watch" → Update campaign state
     ↓
Auto-save to localStorage
```

---

## 🚀 GIT WORKFLOW

### Když chceš commitnout:
```bash
git add .
git status  # Zkontroluj co commituješ
git commit -m "Feat: Popis změny"
```

### Když chceš pushnout na GitHub:
```bash
git push origin feature/game-page
```

### ⚠️ DŮLEŽITÉ: Před merge do master:
**VŽDY SE ZEPTAT!** Push na master → auto-deploy na produkci!
```bash
# NEJDŘÍV ZEPTAT SE!
# Pak:
git checkout master
git merge feature/game-page
git push  # ← Deploy na Vercel + Render
```

---

## 📸 Screenshot

Poslední screenshot: `.playwright-mcp/game-page-mvp.png`

Ukazuje:
- Party Panel (4 myši)
- Time: Day 1, Afternoon Watch
- Weather: Normal (roll 8)
- Encounters: Active 0
- Hex Map placeholder

---

## 🎲 MAUSRITTER PRAVIDLA (Quick Reference)

### Watch System:
- 🌅 Morning (6am-12pm)
- ☀️ Afternoon (12pm-6pm)
- 🌆 Evening (6pm-12am)
- 🌙 Night (12am-6am)

### Weather Roll (2d6):
- **2-3**: ⛈️ Harsh Weather
- **4-9**: 🌤️ Normal
- **10-11**: ☀️ Favourable
- **12**: 🌪️ Extreme!

### Encounter Roll (d6):
- **Morning + Evening** watch only
- **1-2**: Nothing
- **3-4**: Sign of creature
- **5-6**: Encounter!

---

## 💡 TIPY

### Když nevíš kde začít:
1. Otevři tento soubor (`CURRENT_WORK.md`)
2. Projdi sekci "CO DĚLAT PŘÍŠTĚ"
3. Začni Task #1 (Tab System)

### Když něco nefunguje:
1. Zkontroluj console errors (F12)
2. Zkontroluj backend logs
3. Zkontroluj že oba servery běží (3001 + 8001)

### Když se ztratíš:
1. Otevři roadmapu: `docs/game-dashboard-roadmap.md`
2. Najdi aktuální Phase (1B)
3. Projdi tasks postupně

---

## 📞 KONTAKTY & RESOURCES

- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code
- **Mausritter Rules**: `docs/knowledge_base/*.md`
- **Next.js Docs**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

---

**🎯 NEXT ACTION: Začít Phase 1B - Tab System**

```bash
# 1. Checkout branch
git checkout feature/game-page

# 2. Spusť servery (3001 + 8001)

# 3. Vytvoř TabSystem.tsx komponentu

# 4. Test na localhost:3001/game

# 5. Commit když funguje
```

---

**Good luck! 🚀**
