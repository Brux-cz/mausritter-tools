# 🗺️ GM Dashboard - Kompletní Roadmapa

**Branch:** `feature/game-page`
**Stránka:** `/game`
**Účel:** Centrální hub pro vedení celé Mausritter kampaně

---

## 🎯 VIZE

Jeden unified dashboard, odkud GM řídí **celou kampaň**:
- ✅ Party tracker (myši s character sheety)
- ✅ Time & Weather systém
- 🔄 Hex mapa (interactive, propojená s generátory)
- 🔄 Tactical map (canvas pro kreslení)
- 🔄 Bestiary (creatures z pravidel + generované)
- 🔄 NPC systém (kontextový, rumors s truth/lie mechanikou)
- 🔄 Dungeon viewer
- 🔄 Encounter management
- 🔄 Dice roller (pro GM i hráče)

---

## 📋 PHASE 1A: Core Foundation ✅ **HOTOVO**

**Status:** ✅ Commitnuto (631355f)
**Datum:** 2025-11-07

### Co je hotové:
- ✅ `/game` page struktura
- ✅ Party Panel (4 myši: Pip, Rosa, Max, Lily)
  - Ikony 🐭, HP bary, conditions
  - Click → otevře sidebar
- ✅ Mouse Detail Sidebar (character sheet placeholder)
  - HP, Grit, Pips, Level
  - Background, Conditions
  - Notes textarea
  - Inventory placeholder
- ✅ Time & Weather Panel
  - Day counter + Watch tracking
  - Next Watch button (funguje!)
  - Weather roll (2d6) podle Mausritter pravidel
  - Encounter reminders
- ✅ TypeScript interfaces (`lib/types/campaign.ts`)
  - Mouse, Creature, HexData, Settlement, NPC, Weather, atd.
- ✅ LocalStorage persistence (auto-save)
- ✅ Mock data (4 testovací myši)

### Soubory vytvořené:
```
web-frontend/
├── app/game/page.tsx
├── components/game/
│   ├── PartyPanel.tsx
│   ├── MouseDetailSidebar.tsx
│   └── TimeWeatherPanel.tsx
├── lib/types/campaign.ts
└── docs/
    ├── hex-layout-fix.md
    └── game-dashboard-roadmap.md (tento soubor)
```

---

## 📋 PHASE 1B: Content Tabs 🔄 **PŘÍŠTĚ**

**Priorita:** Vysoká
**Odhad:** 2-3 hodiny

### Tasks:
- [ ] Tab System komponenta (3 tabs)
  - 🗺️ Hex Map (default)
  - 🎨 Tactical Map
  - 📚 Bestiary
- [ ] Bestiary komponenta
  - Static JSON s creatures z Mausritter rulebooku
  - Search/filter funkce
  - Detail view (HP, Attack, Wants, Special)
  - [Add to Encounter] button
- [ ] Tactical Canvas (základní verze)
  - HTML5 Canvas drawing
  - Drawing tools: pen, eraser, shapes
  - Image upload (drag & drop)
  - Save/load canvas state do LocalStorage
- [ ] Napojit Bestiary na `/generate/creature` backend
  - Button "Generate Custom Creature"
  - Add to bestiary + campaign state

### Soubory k vytvoření:
```
components/game/
├── TabSystem.tsx
├── BestiaryPanel.tsx
├── TacticalCanvas.tsx
└── HexMapViewer.tsx (placeholder)

lib/data/
└── creatures.json (static bestiary)
```

---

## 📋 PHASE 2: Hex Map Integration 🔄 **POZDĚJI**

**Priorita:** Vysoká
**Odhad:** 4-5 hodin

### Tasks:
- [ ] Hex Map Viewer
  - Použít existing `get19HexLayout()` z `lib/hexMath.ts`
  - Click hex → Sidebar s detaily
  - Zobrazit terrain, settlements, dungeons
- [ ] Hexcrawl Generator Integration
  - Button "Generate World"
  - Call backend `/generate/hexcrawl`
  - Uložit do campaign state
  - Render na mapě
- [ ] Hex Detail Page
  - Route: `/game/hex/[id]`
  - Full detail view (terrain, weather, encounters, NPCs)
  - "Generate More Content" buttons
- [ ] Hex Editor (basic)
  - Edit terrain type
  - Add custom notes
  - Mark as explored/unexplored

---

## 📋 PHASE 3: NPC & Rumor System 🔄 **POZDĚJI**

**Priorita:** Střední
**Odhad:** 3-4 hodiny

### Tasks:
- [ ] NPC Generator Integration
  - Context-aware (ví o hexu, settlementu, počasí)
  - Call backend `/generate/npc`
- [ ] Rumor System
  - Roll 2d6 pro truth level:
    - 2-5: Lie
    - 6-8: Partial Truth
    - 9-12: Full Truth
  - Nebo fixed 33% probability každý
  - NPC zobrazí rumor based on Reaction roll
- [ ] NPC Tracker
  - Seznam všech NPCs v kampani
  - Filter by location (hex/settlement)
  - Click → Detail view
  - Show conversation history
- [ ] NPC Detail Page
  - Route: `/game/npc/[id]`
  - Personality, rumors, notes
  - Relationship status s party

---

## 📋 PHASE 4: Encounter System 🔄 **POZDĚJI**

**Priorita:** Střední
**Odhad:** 3-4 hodiny

### Tasks:
- [ ] Encounter Roll Mechanika
  - Auto-reminder při Morning/Evening watch
  - Roll d6:
    - 1-2: No encounter
    - 3-4: Sign of creature
    - 5-6: Encounter!
- [ ] Reaction Roll
  - 2d6: Hostile, Cautious, Curious, Friendly
  - Vliv na NPC dialogue a rumor truthfulness
- [ ] Encounter Tracker
  - Active encounters list
  - Initiative tracker (optional)
  - HP tracking for enemies
  - Quick actions (Attack, Flee, Parley)
- [ ] Encounter Log
  - Historie všech encounters
  - Výsledky (fled, killed, befriended)
  - Link to hex kde se stalo

---

## 📋 PHASE 5: Dungeon System 🔄 **POZDĚJI**

**Priorita:** Nízká
**Odhad:** 4-5 hodin

### Tasks:
- [ ] Dungeon Viewer
  - Click settlement/location → Otevře dungeon
  - Room-by-room exploration
- [ ] Dungeon Generator Integration
  - Call backend `/generate/dungeon`
  - Procedural rooms, monsters, treasures
- [ ] Dungeon Detail Page
  - Route: `/game/dungeon/[id]`
  - Map view (if available)
  - Room list s descriptions
  - Track explored/unexplored rooms
- [ ] Dungeon Notes
  - GM notes per room
  - Monster HP tracking
  - Treasure looted status

---

## 📋 PHASE 6: Advanced Features 🔄 **BUDOUCNOST**

**Priorita:** Nízká
**Odhad:** Týdny

### Tasks:
- [ ] Full Character Sheets
  - Inventory management (drag & drop)
  - Equipment slots
  - Spell tracking
  - Conditions management
- [ ] Combat Tracker
  - Initiative order
  - HP/Grit tracking
  - Status effects
  - Attack rolls
- [ ] Session Logger
  - Auto-log důležitých events
  - Manual notes
  - Export session summary
- [ ] Shared Dice Roller
  - Real-time pro multiplayer
  - Roll visibility (GM vs Players)
  - Roll history
- [ ] Export/Import
  - Download campaign JSON
  - Share campaign s jinými GMs
  - Backup/restore
- [ ] Database Backend
  - Replace LocalStorage
  - Cloud persistence
  - Multi-device sync
- [ ] Mobile Responsive
  - Touch-friendly UI
  - Collapsible panels
- [ ] Dark Mode
  - Toggle theme
  - Persist preference

---

## 🗂️ DATA STRUCTURE

### Campaign State
```typescript
interface CampaignState {
  id: string;
  name: string;
  created: Date;
  lastModified: Date;

  // Time
  currentDay: number;
  currentWatch: 'morning' | 'afternoon' | 'evening' | 'night';

  // Party
  party: Mouse[];

  // World
  hexMap: HexData[];
  settlements: Settlement[];
  npcs: NPC[];

  // Game State
  weather: WeatherState;
  encounters: Encounter[];
  bestiary: Creature[];

  // Tactical Maps
  tacticalMaps: {
    current: CanvasState | null;
    saved: CanvasState[];
  };

  // History
  weatherLog: WeatherState[];
  rollHistory: DiceRoll[];

  // Notes
  gmNotes: string;
  sessionLog: string[];
}
```

### Mouse (Character)
```typescript
interface Mouse {
  id: string;
  name: string;
  hp: number;
  maxHp: number;
  grit: number;
  maxGrit: number;
  pips: number;
  level: number;
  background?: string;
  disposition?: string;
  birthsign?: string;
  coat?: string;
  inventory?: InventoryItem[];
  conditions?: string[];
  notes?: string;
}
```

### Creature (Bestiary)
```typescript
interface Creature {
  id: string;
  name: string;
  hp: number;
  attack: string;
  wants: string;
  special?: string[];
  description?: string;
  source: 'rulebook' | 'generated' | 'custom';
}
```

---

## 🔗 BACKEND ENDPOINTS (Existing)

### Generators:
- `POST /generate/hexcrawl` - Vygeneruje hex world
- `POST /generate/npc` - Vygeneruje NPC
- `POST /generate/creature` - Vygeneruje creature
- `POST /generate/dungeon` - Vygeneruje dungeon
- `POST /generate/settlement` - Vygeneruje settlement
- `POST /generate/adventure_site` - Vygeneruje adventure site

### Health:
- `GET /health` - Backend health check

---

## 🚀 DEPLOYMENT WORKFLOW

### Development (Branch: feature/game-page):
1. Pracuj na `feature/game-page` branch
2. Test lokálně: `localhost:3001/game`
3. Commit po každé feature
4. **NEPUSHUJ NA MASTER** bez potvrzení!

### Testing:
```bash
# Frontend
cd web-frontend
npm run dev -- -p 3001

# Backend
cd web-backend
python -m uvicorn app.main:app --reload --port 8001
```

### Production (až bude ready):
1. Zeptat se na merge do master
2. Push → Auto-deploy na:
   - Vercel: https://mausritter-tools.vercel.app
   - Render: https://mausritter-tools.onrender.com

---

## 📚 MAUSRITTER PRAVIDLA (Reference)

### Hexcrawl Mechaniky:
- **Watch** = 6 hodin (4 watches za den)
- **Day** = Morning → Afternoon → Evening → Night
- **Movement**: 1 hex za watch

### Weather (2d6):
- **2-3**: Harsh Weather (stop movement, seek shelter)
- **4-9**: Normal
- **10-11**: Favourable
- **12**: Extreme (roll seasonal table)

### Encounters (d6):
- **Morning + Evening watch**: Roll d6
  - 1-2: No encounter
  - 3-4: Sign of creature
  - 5-6: Encounter!

### Reaction Roll (2d6):
- **2-3**: Hostile
- **4-6**: Cautious
- **7-9**: Curious
- **10-12**: Friendly

---

## 🐛 Known Issues

Zatím žádné! Phase 1A funguje perfektně.

---

## 📝 Notes

- LocalStorage key: `mausritter-campaign`
- Auto-save při každé změně campaign state
- Mock campaign: "Thornwood Vale"
- 4 testovací myši: Pip, Rosa, Max, Lily

---

**Poslední update:** 2025-11-07
**Current Phase:** Phase 1A ✅ → Phase 1B 🔄
