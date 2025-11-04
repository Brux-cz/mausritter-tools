# 🐭 Mausritter Web Frontend

Next.js 14 frontend pro Mausritter Tools webovou platformu.

**Status:** ✅ Quick Prototype Complete - Landing page + 4 funkční generator pages + E2E testy

---

## 🚀 Quick Start

### 1. Instalace dependencies

```bash
cd web-frontend
npm install
```

### 2. Konfigurace

Zkopíruj `.env.local.example` do `.env.local`:
```bash
cp .env.local.example .env.local
```

**Nastav:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### 3. Spuštění development serveru

```bash
npm run dev -- -p 3001
```

Frontend běží na: **http://localhost:3001**

---

## 📋 Dostupné Stránky

### Public Pages (Quick Prototype - Implementováno)

- ✅ **/** - Landing page s Mausritter designem
- ✅ **/generators** - Generator hub (17 generátorů, filtrování, vyhledávání)
- ✅ **/generators/character** - Character Generator (plně funkční)
- ✅ **/generators/npc** - NPC Generator (plně funkční)
- ✅ **/generators/weather** - Weather Generator (plně funkční)
- ✅ **/generators/hexcrawl** - Hexcrawl Generator (plně funkční - 4 taby)

### Další Generator Pages (Připraveno k implementaci)

- ⏳ **/generators/hex** - Hex Generator
- ⏳ **/generators/settlement** - Settlement Generator
- ⏳ **/generators/hireling** - Hireling Generator
- ⏳ **/generators/reaction** - Reaction Generator
- ⏳ **/generators/spell** - Spell Generator
- ⏳ **/generators/treasure** - Treasure Generator
- ⏳ **/generators/adventure** - Adventure Generator
- ⏳ **/generators/hook** - Hook Generator
- ⏳ **/generators/tavern** - Tavern Generator
- ⏳ **/generators/dungeon** - Dungeon Generator
- ⏳ **/generators/rumor** - Rumor Generator
- ⏳ **/generators/creature/{type}** - Creature Variant Generator

### Authenticated Pages (V2)

- ⏳ **/auth/login** - Login page
- ⏳ **/auth/signup** - Signup page
- ⏳ **/dashboard** - Dashboard (GM/Player)
- ⏳ **/campaigns/{id}** - Campaign detail
- ⏳ **/characters/{id}** - Character sheet

---

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui ✅ (7 komponent: Button, Card, Input, Label, Select, Tabs, Toast)
- **API Client:** Custom fetch wrapper s TypeScript types ✅
- **Notifications:** Sonner (toast messages) ✅
- **Testing:** Playwright E2E ✅ (33 testů)
- **State Management:** React hooks (useState)
- **Data Fetching:** Native Fetch API
- **Auth:** Supabase Auth (V2 - připraveno)

---

## 📁 Struktura Projektu

```
web-frontend/
├── app/
│   ├── layout.tsx                      # Root layout + Toaster
│   ├── page.tsx                        # Landing page ✅
│   ├── globals.css                     # Global styles + Tailwind
│   └── generators/
│       ├── page.tsx                    # Generator hub ✅
│       ├── character/page.tsx          # Character Generator ✅
│       ├── npc/page.tsx                # NPC Generator ✅
│       ├── weather/page.tsx            # Weather Generator ✅
│       └── hexcrawl/page.tsx           # Hexcrawl Generator ✅
├── components/
│   └── ui/                             # shadcn/ui komponenty ✅
│       ├── button.tsx                  # Button component
│       ├── card.tsx                    # Card components
│       ├── input.tsx                   # Input component
│       ├── label.tsx                   # Label component
│       ├── select.tsx                  # Select dropdown
│       ├── tabs.tsx                    # Tabs component
│       └── sonner.tsx                  # Toast notifications
├── lib/
│   ├── api.ts                          # API client ✅ (17 generátorů)
│   └── utils.ts                        # cn() helper ✅
├── tests/
│   └── e2e/                            # Playwright E2E testy ✅
│       ├── homepage.spec.ts            # Landing page tests (5)
│       ├── generator-hub.spec.ts       # Hub tests (6)
│       ├── character-generator.spec.ts # Character tests (6)
│       ├── npc-generator.spec.ts       # NPC tests (5)
│       ├── weather-generator.spec.ts   # Weather tests (6)
│       └── api-health.spec.ts          # API tests (5)
├── public/                             # Static assets
├── playwright.config.ts                # Playwright config ✅
├── components.json                     # shadcn/ui config ✅
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

---

## 🎨 Design System

### Color Palette (Mausritter-themed)

- **Primary:** Earthy brown (#8B4513, #D2691E)
- **Secondary:** Forest green (#228B22, #6B8E23)
- **Accent:** Gold (#FFD700)
- **Background:** Beige (#F5F5DC)
- **Text:** Charcoal (#36454F)

### Typography

- **Headings:** Geist Sans (Next.js default)
- **Body:** Inter
- **Code:** Geist Mono

---

## 🧩 shadcn/ui Setup ✅

shadcn/ui je **nainstalováno a nakonfigurováno**. Dostupné komponenty:

- ✅ **Button** - Tlačítka s variantami (default, outline, ghost)
- ✅ **Card** - Karty pro zobrazení obsahu
- ✅ **Input** - Textové input fieldy
- ✅ **Label** - Labely pro formuláře
- ✅ **Select** - Dropdown selecty
- ✅ **Tabs** - Tabové rozhraní (Radix UI primitives)
- ✅ **Sonner** - Toast notifikace

### Přidání další komponenty

```bash
npx shadcn-ui@latest add [component-name]
# Např: npx shadcn-ui@latest add dialog
```

---

## 🔌 API Integration ✅

### API Client (lib/api.ts)

Plně funkční client s TypeScript types pro všech 17 generátorů:

```typescript
// Příklad použití
import { generateCharacter, generateNPC, generateWeather } from '@/lib/api'

// Character Generator
const character = await generateCharacter({
  name: 'Pepřík',
  gender: 'male'
})

// NPC Generator
const npc = await generateNPC({ gender: 'female' })

// Weather Generator
const weather = await generateWeather({
  season: 'winter',
  with_event: true
})
```

**Dostupné generátory:**
- `generateCharacter()` - Character Generator
- `generateNPC()` - NPC Generator
- `generateHex()` - Hex Generator
- `generateSettlement()` - Settlement Generator
- `generateWeather()` - Weather Generator
- `generateHireling()` - Hireling Generator
- `generateReaction()` - Reaction Generator
- `generateSpell()` - Spell Generator
- `generateTreasure()` - Treasure Generator
- `generateAdventure()` - Adventure Generator
- `generateHook()` - Hook Generator
- `generateTavern()` - Tavern Generator
- `generateDungeon()` - Dungeon Generator
- `generateRumor()` - Rumor Generator
- `generateHexcrawl()` - Hexcrawl Generator
- `generateCreature(type)` - Creature Variant Generator
- `getGeneratorStatus()` - Status endpoint
- `healthCheck()` - Health check

**Error Handling:**

```typescript
try {
  const character = await generateCharacter({ name: 'Test' })
} catch (error) {
  if (error instanceof APIError) {
    console.error(`API Error ${error.status}: ${error.message}`)
  }
}
```

---

## 🧪 Testing

### Playwright E2E Tests ✅

Projekt obsahuje **33 E2E testů** rozdělených do 6 test suites:

| Test Suite | Testy | Popis |
|------------|-------|-------|
| `homepage.spec.ts` | 5 | Landing page, CTA buttons, feature boxes |
| `generator-hub.spec.ts` | 6 | 17 generátorů, filtrování, vyhledávání |
| `character-generator.spec.ts` | 6 | Generování, custom name, inventory, JSON copy |
| `npc-generator.spec.ts` | 5 | Generování NPC, custom name, reaction info |
| `weather-generator.spec.ts` | 6 | Season select, event checkbox, info panel |
| `api-health.spec.ts` | 5 | Backend health, status, API calls |

### Spuštění testů

```bash
# Headless mode (CI)
npm run test:e2e

# UI mode (interaktivní)
npm run test:e2e:ui

# Headed mode (s viditelným browserem)
npm run test:e2e:headed
```

**Konfigurace:** [playwright.config.ts](./playwright.config.ts)

---

## 🚢 Deployment

### Vercel (Doporučeno)

1. Push projekt do GitHub
2. Import repo ve Vercel
3. Nastav environment variables:
   - `NEXT_PUBLIC_API_URL=https://your-api.railway.app`
4. Deploy!

**Vercel automaticky:**
- Detekuje Next.js
- Buildne produkční verzi
- Nastaví CDN
- Poskytne HTTPS

---

## 📝 Development Workflow

### Přidání nové stránky

1. Vytvoř `app/your-page/page.tsx`
2. Export default React component
3. Page je automaticky routovaná na `/your-page`

### Přidání API endpointu

1. V Next.js: `app/api/your-endpoint/route.ts`
2. Nebo use FastAPI backend (doporučeno)

### Styling

Používej Tailwind utility classes:
```tsx
<div className="bg-primary text-primary-foreground p-4 rounded-lg">
  Obsah
</div>
```

---

## 🐛 Debugging

### Chyba: Cannot connect to API

**Řešení:** Ujisti se, že FastAPI backend běží:
```bash
cd web-backend
python -m uvicorn app.main:app --reload
```

### Chyba: Port 3000 already in use

Zkus jiný port:
```bash
npm run dev -- -p 3001
```

### TypeScript errors

Přebuilduј types:
```bash
npm run build
```

---

## 📚 Další Dokumentace

- [UI Wireframes](../docs/UI_WIREFRAMES.md)
- [Web Roadmap](../docs/WEB_ROADMAP.md)
- [Architecture](../docs/WEB_ARCHITECTURE.md)

---

## 🔜 Next Steps

### Quick Prototype ✅ COMPLETE

- ✅ Setup shadcn/ui (7 komponent: Button, Card, Input, Label, Select, Tabs, Toast)
- ✅ Connect API client (17 generátorů)
- ✅ Add generator hub page
- ✅ Implement 4 generator pages (Character, NPC, Weather, Hexcrawl)
- ✅ Create Playwright E2E tests (33 testů)

### Další možné kroky

**Implementace dalších generator pages (13 zbývajících):**
- [ ] Hex, Settlement, Hireling, Reaction, Spell
- [ ] Treasure, Adventure, Hook, Tavern, Dungeon
- [ ] Rumor, Creature Variants

**Vylepšení UX:**
- [ ] Loading states (skeletons)
- [ ] Error boundaries
- [ ] Responsive mobile design improvements
- [ ] Dark mode support

**Autentizace a persistence (V2):**
- [ ] Supabase Auth integration
- [ ] Campaign management
- [ ] Character persistence
- [ ] Shared campaigns

---

**Last updated:** 2025-11-04
