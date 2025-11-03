# 🐭 Mausritter Web Frontend

Next.js 14 frontend pro Mausritter Tools webovou platformu.

**Status:** ✅ MVP Week 1 Complete - Landing page s Mausritter designem

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
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Spuštění development serveru

```bash
npm run dev
```

Frontend běží na: **http://localhost:3000**

---

## 📋 Dostupné Stránky (MVP)

### Public Pages

- ✅ **/** - Landing page
- 🚧 **/auth/login** - Login (placeholder)
- 🚧 **/auth/signup** - Signup (placeholder)

### Authenticated Pages (V2)

- ⏳ **/dashboard** - Dashboard (GM/Player)
- ⏳ **/campaigns/{id}** - Campaign detail
- ⏳ **/generators** - Generator hub
- ⏳ **/characters/{id}** - Character sheet

---

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui (připraveno, ne installed)
- **State Management:** Zustand (připraveno)
- **Data Fetching:** TanStack Query (připraveno)
- **Auth:** Supabase Auth (V2)

---

## 📁 Struktura Projektu

```
web-frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing page
│   ├── globals.css          # Global styles + Tailwind
│   └── auth/                # Auth pages (V2)
├── components/              # React components
│   └── ui/                  # shadcn/ui components
├── lib/                     # Utility functions
│   ├── api.ts               # API client
│   └── supabase.ts          # Supabase client (V2)
├── public/                  # Static assets
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

## 🧩 shadcn/ui Setup (V2)

Pro přidání shadcn/ui komponent:

```bash
# Inicializace shadcn/ui
npx shadcn-ui@latest init

# Přidání komponent
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
# atd.
```

**Komponenty potřebné pro MVP:**
- Button, Card, Input, Select, Dialog, Toast

---

## 🔌 API Integration

### API Client (lib/api.ts)

Připravený client pro komunikaci s FastAPI backendem:

```typescript
// Příklad použití (V2)
import { api } from '@/lib/api'

const character = await api.post('/generate/character', {
  name: 'Pepřík',
  gender: 'male'
})
```

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

## 🔜 Next Steps (V2)

- [ ] Setup shadcn/ui
- [ ] Implement dashboard layout
- [ ] Connect API client
- [ ] Add generator pages
- [ ] Supabase Auth integration

---

**Last updated:** 2025-11-03
