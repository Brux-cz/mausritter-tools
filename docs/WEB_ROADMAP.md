# 🗺️ Web Platform Roadmap

**Version:** 1.0
**Date:** 2025-11-03
**Status:** Planning fáze

---

## 🎯 Vision

Vytvořit **kompletní webovou platformu** pro Mausritter TTRPG komunitu poskytující:
- 🎲 Všech 17 generátorů (character, NPC, hex, dungeon, settlement, atd.)
- 🎭 Campaign management pro GM
- 👥 Character sheets pro hráče
- 🗺️ Interactive hexcrawl map viewer
- 🎲 Real-time dice roller
- 🤖 AI asistent (budoucnost)

**Target audience:** 100-500 aktivních uživatelů (škálovatelné do 50k)

**Budget:** $0-10/měsíc

---

## 📊 Development Phases

| Fáze | Časový odhad | Status | Klíčové features |
|------|--------------|--------|------------------|
| **MVP** | 4-5 týdnů | ⏳ Planned | Auth + 5 generátorů + Basic campaign |
| **V2** | +1 měsíc | 📅 Future | Všech 17 generátorů + Hexcrawl map |
| **V3** | +1 měsíc | 📅 Future | Real-time dice + Sessions + PDF export |
| **V4** | TBD | 💭 Maybe | AI asistent |

---

## 🚀 FÁZE 1: MVP (Minimum Viable Product)

**Cíl:** Funkční platforma pro 1 GM + 4 hráče, single campaign

**Časový odhad:** 4-5 týdnů (full-time vibe coding)

**Success Criteria:**
- ✅ Uživatel se může zaregistrovat a přihlásit
- ✅ GM může vytvořit kampaň
- ✅ Hráč může vygenerovat postavu
- ✅ Hráč může zobrazit character sheet
- ✅ GM může generovat NPC, hexy, osady, počasí
- ✅ Všechno se ukládá do DB a persists
- ✅ Deploynuté na Vercel + Railway + Supabase

---

### **Week 1: Setup & Infrastructure**

**Backend (2 dny):**
- [x] Setup Railway project
- [x] Create FastAPI boilerplate
  ```
  web-backend/
  ├── app/
  │   ├── main.py
  │   ├── routers/
  │   │   ├── generators.py
  │   │   └── campaigns.py
  │   ├── middleware/
  │   │   └── auth.py
  │   └── utils/
  │       └── supabase_client.py
  ├── requirements.txt
  ├── Dockerfile
  └── .env.example
  ```
- [x] Wrap 5 core generátorů:
  - Character (`POST /api/v1/generate/character`)
  - NPC (`POST /api/v1/generate/npc`)
  - Hex (`POST /api/v1/generate/hex`)
  - Settlement (`POST /api/v1/generate/settlement`)
  - Weather (`POST /api/v1/generate/weather`)
- [x] Setup Supabase client
- [x] Health check endpoint (`GET /health`)
- [x] Test all endpoints (Postman/Thunder Client)

**Database (1 den):**
- [x] Create Supabase project
- [x] Run `DATABASE_SCHEMA.sql`
- [x] Verify tables created
- [x] Test RLS policies (manually insert data)
- [x] Create test user (GM + Player)

**Frontend (2 dny):**
- [x] Setup Next.js project
  ```
  web-frontend/
  ├── app/
  │   ├── layout.tsx
  │   ├── page.tsx (landing)
  │   ├── auth/
  │   │   ├── login/page.tsx
  │   │   └── signup/page.tsx
  │   └── dashboard/
  │       └── page.tsx
  ├── components/
  │   └── ui/ (shadcn components)
  ├── lib/
  │   ├── supabase.ts
  │   └── api.ts
  └── .env.local.example
  ```
- [x] Install shadcn/ui + Tailwind
- [x] Setup Supabase Auth client
- [x] Landing page (public)
- [x] Auth pages (login, signup)

---

### **Week 2: Auth + Campaign Management**

**Backend (2 dny):**
- [x] Implement auth middleware (verify JWT from Supabase)
- [x] Campaign CRUD endpoints:
  - `GET /api/v1/campaigns` (list)
  - `POST /api/v1/campaigns` (create)
  - `GET /api/v1/campaigns/{id}` (detail)
  - `PUT /api/v1/campaigns/{id}` (update)
  - `DELETE /api/v1/campaigns/{id}` (delete)
- [x] Test RLS policies (GM vs Player access)

**Frontend (3 dny):**
- [x] Auth flow integration
  - Login page functional
  - Signup page functional
  - Protected routes middleware
  - User profile in header
- [x] Dashboard layout
  - Sidebar navigation
  - Topbar (user menu)
  - Main content area
- [x] Campaign creation form
  - Name, description, season
  - Submit → create campaign
  - Redirect to campaign detail
- [x] Campaign list page
  - Display user's campaigns
  - GM vs Player role badge

---

### **Week 3: Character Creation & Generators**

**Backend (1 den):**
- [x] Character CRUD endpoints:
  - `POST /api/v1/campaigns/{id}/characters` (create)
  - `GET /api/v1/characters/{id}` (detail)
  - `GET /api/v1/campaigns/{id}/characters` (list)
- [x] Test character creation flow

**Frontend (4 dny):**
- [x] Character Generator page
  - Form: name (optional), gender radio
  - Generate button → call API
  - Display result (stats, equipment, background)
  - Save to campaign button
- [x] Character List page
  - Display all characters in campaign
  - Cards with avatar, name, background, HP
  - Click to view detail
- [x] Character Sheet page (read-only MVP)
  - Display full character data
  - Stats grid (STR/DEX/WIL)
  - HP hearts
  - Inventory grid (6 slots)
  - Background description
- [x] Generator pages for 4 other generators:
  - NPC Generator
  - Hex Generator
  - Settlement Generator
  - Weather Generator
- [x] Unified generator layout component
  - Options form (top)
  - Generate button
  - Result display (scrollable)
  - Actions (save, re-roll, export JSON)

---

### **Week 4: Campaign Detail & Polish**

**Backend (1 den):**
- [x] Campaign stats endpoint
  - Aggregate counts (characters, hexes, NPCs, sessions)
  - Recent activity feed
- [x] Simple save generated content endpoints:
  - `POST /api/v1/campaigns/{id}/npcs`
  - `POST /api/v1/campaigns/{id}/hexes`
  - `POST /api/v1/campaigns/{id}/settlements`

**Frontend (4 dny):**
- [x] Campaign Detail page
  - Stats dashboard (cards with counts)
  - Recent activity feed
  - Quick generate buttons
  - Player list (read-only for MVP)
- [x] Save generated content flow
  - Generate NPC → Save button → modal (assign to hex?) → save
  - Generate hex → Save button → auto-position in grid → save
- [x] NPC List page (simple table view)
- [x] Settlement List page (simple table view)
- [x] Hex List page (simple table view, NO map yet)
- [x] UI/UX polish
  - Consistent spacing, colors
  - Loading states
  - Error handling (toasts)
  - Empty states ("No characters yet")
- [x] Responsive design (mobile-friendly)

---

### **Week 5: Testing & Deployment**

**Testing (2 dny):**
- [x] Manual testing all flows
  - Signup → create campaign → generate character → save
  - Generate NPC → save → view list
  - GM vs Player permissions (use 2 browser windows)
- [x] Bug fixing
- [x] Edge cases (empty campaigns, no characters, etc.)

**Deployment (1 den):**
- [x] Deploy backend to Railway
  - Connect GitHub repo
  - Set environment variables
  - Test health check
- [x] Deploy frontend to Vercel
  - Connect GitHub repo
  - Set environment variables
  - Test production build
- [x] Connect frontend to production backend
- [x] Verify Supabase connection (production vs development)

**Documentation (1 den):**
- [x] README for web-frontend
- [x] README for web-backend
- [x] Environment variables documentation
- [x] Basic user guide (how to use platform)

**MVP Launch! 🎉**

---

## ✨ FÁZE 2: Enhanced Features

**Cíl:** Všech 17 generátorů + Interactive hexcrawl map

**Časový odhad:** 1 měsíc

**Success Criteria:**
- ✅ Všech 17 generátorů dostupných a funkčních
- ✅ Hexcrawl map viewer (5×5 interactive grid)
- ✅ Character sheet editing (HP, inventory)
- ✅ Campaign player management (add/remove players)
- ✅ Discovery state (mark hexes/NPCs as discovered)

---

### **Week 6-7: Remaining Generators**

**Backend (3 dny):**
- [ ] Wrap zbývajících 12 generátorů:
  - Hireling (`POST /api/v1/generate/hireling`)
  - Reaction (`POST /api/v1/generate/reaction`)
  - Spell (`POST /api/v1/generate/spell`)
  - Treasure (`POST /api/v1/generate/treasure`)
  - Adventure Seed (`POST /api/v1/generate/adventure`)
  - Adventure Hook (`POST /api/v1/generate/hook`)
  - Creature Variant (`POST /api/v1/generate/creature/{type}`)
  - Tavern (`POST /api/v1/generate/tavern`)
  - Dungeon (`POST /api/v1/generate/dungeon`)
  - Rumor (`POST /api/v1/generate/rumor`)
  - Hexcrawl (bulk) (`POST /api/v1/generate/hexcrawl`)
- [ ] Test all endpoints
- [ ] Update OpenAPI docs

**Frontend (4 dny):**
- [ ] Create generator pages for all 12 remaining generators
- [ ] Reuse unified generator layout
- [ ] Custom result displays per generator:
  - Treasure: grouped by type (pence, magic sword, spell, etc.)
  - Dungeon: rooms table with creature/treasure indicators
  - Hexcrawl: preview grid (but not full interactive yet)
  - Creature: variant details with description
- [ ] Generator hub page (directory of all 17)
- [ ] Search/filter generators

---

### **Week 8-9: Hexcrawl Map Viewer**

**Backend (2 dny):**
- [ ] Hexcrawl bulk create endpoint
  - Accept 25 hexes + settlements + dungeons
  - Create all in transaction
  - Return campaign_id with all IDs
- [ ] Hex update endpoint (mark discovered)
  - `PUT /api/v1/hexes/{id}` with `is_discovered`
  - Trigger function to mark related entities

**Frontend (5 dny):**
- [ ] Hexcrawl Map component
  - 5×5 CSS Grid
  - Hex tiles (square tiles with emoji icons)
  - Hover effects
  - Click to open modal
- [ ] Hex detail modal
  - Display hex type, detail, hook
  - List settlements/dungeons/NPCs in hex
  - Mark discovered button (GM only)
  - Add notes field
- [ ] Discovery state visual
  - Undiscovered hexes: gray or "???"
  - Discovered hexes: full color + details
  - Players only see discovered hexes
- [ ] Hexcrawl generation flow
  - "Generate Hexcrawl" button in campaign
  - Generate 25 hexes + 3 settlements + 3 dungeons
  - Save all to DB
  - Redirect to map view
- [ ] Campaign hex map page
  - Embedded hex map component
  - Legend (hex types, discovered state)
  - Filter/search hexes

---

### **Week 10: Character Sheet Editing + Player Management**

**Backend (1 den):**
- [ ] Character update endpoint fields:
  - `current_hp`, `pence`, `inventory`, `conditions`
- [ ] Campaign player management:
  - `POST /api/v1/campaigns/{id}/players` (add player)
  - `DELETE /api/v1/campaigns/{id}/players/{player_id}` (remove)
  - Search users by username

**Frontend (4 dny):**
- [ ] Editable Character Sheet
  - HP editing:
    - Take damage modal (reduce HP, add conditions if 0 HP)
    - Heal button (increase HP up to max)
  - Inventory drag-and-drop
    - Use `react-beautiful-dnd`
    - Reorder items
    - Add/remove items
  - Pence editing (simple number input)
  - Conditions badges (add/remove)
- [ ] Campaign Settings page (GM only)
  - Player management section
  - Add player form (search by username)
  - Player list with remove button
  - Player notes field
- [ ] Attribute test buttons
  - Click STR/DEX/WIL → roll d20
  - Compare vs attribute value
  - Show success/fail
  - (No backend roll history yet, just UI)

---

## 🚀 FÁZE 3: Advanced Features

**Cíl:** Real-time dice + Session tracking + PDF export

**Časový odhad:** 1 měsíc

**Success Criteria:**
- ✅ Real-time shared dice roller (všichni v kampani vidí hody)
- ✅ Session creation & notes
- ✅ Session summary auto-generation
- ✅ PDF export (character sheets, hexcrawl map)
- ✅ File uploads (character avatars)

---

### **Week 11: Real-time Dice Roller**

**Backend (1 den):**
- [ ] Dice roll endpoints:
  - `POST /api/v1/campaigns/{id}/dice-rolls` (record roll)
  - `GET /api/v1/campaigns/{id}/dice-rolls` (history)
- [ ] Supabase Realtime setup
  - Enable realtime on `dice_rolls` table
  - Test subscriptions

**Frontend (4 dny):**
- [ ] Dice Roller page/modal
  - Dice buttons (d4, d6, d8, d10, d12, d20, 2d6, d66)
  - Reason input (optional)
  - Roll button
  - Record roll to DB
- [ ] Real-time roll feed
  - Subscribe to Supabase Realtime channel
  - Listen for new dice_rolls
  - Display in feed (live updates)
  - Roll animation (fade in)
  - User avatar + username + roll result
- [ ] Dice roller widget
  - Embeddable in multiple pages (character sheet, campaign detail)
  - Floating action button (FAB) → open modal
- [ ] Sound effects (optional toggle)
  - Dice roll sound on roll
  - Use Howler.js
- [ ] Roll history page
  - Filterable by user, session, dice type
  - Statistics (average roll, distribution chart)

---

### **Week 12: Session Tracking**

**Backend (1 den):**
- [ ] Session CRUD endpoints:
  - `POST /api/v1/campaigns/{id}/sessions` (create)
  - `GET /api/v1/sessions/{id}` (detail)
  - `PUT /api/v1/sessions/{id}` (update notes, summary)
  - `DELETE /api/v1/sessions/{id}` (delete)
- [ ] Session stats aggregation
  - Hexes explored, NPCs met, combat encounters

**Frontend (4 dny):**
- [ ] Session List page
  - Display all sessions for campaign
  - Timeline view (sorted by date)
  - Session cards (number, date, title, summary)
- [ ] Session Detail page
  - Session metadata (date, duration, players)
  - Notes editor (WYSIWYG - use TipTap or Quill)
  - Summary field
  - Highlights list (add/remove)
  - XP awarded tracker
- [ ] Session Creation wizard (GM)
  - Create session form (date, players present)
  - Auto-increment session number
  - During session: track hexes explored, NPCs met
  - End session: auto-generate summary draft (template)
- [ ] Session Prep page (GM)
  - Checklist (generate weather, rumors, NPCs)
  - Quick generators embedded
  - Link to session notes

---

### **Week 13: PDF Export**

**Backend (2 dny):**
- [ ] PDF generation endpoints:
  - `GET /api/v1/characters/{id}/pdf` (character sheet)
  - `GET /api/v1/campaigns/{id}/hexcrawl-pdf` (hexcrawl map)
  - `GET /api/v1/sessions/{id}/pdf` (session summary)
- [ ] Use WeasyPrint or Puppeteer
  - Render HTML templates → PDF
  - Store in Supabase Storage
  - Return download URL

**Frontend (3 dny):**
- [ ] PDF export buttons
  - Character sheet: "Export PDF" button
  - Hexcrawl map: "Export PDF" button (map + legend)
  - Session: "Export PDF" button (notes + summary)
- [ ] PDF templates design
  - Match Mausritter aesthetic
  - Use HTML/CSS (printable layouts)
- [ ] Download flow
  - Click export → loading state
  - Backend generates PDF
  - Auto-download file
  - Toast notification

---

### **Week 14: File Storage & Polish**

**Backend (1 den):**
- [ ] Supabase Storage setup
  - Create buckets: `avatars`, `exports`, `campaign-assets`
  - RLS policies (users can upload own avatars)
  - File upload endpoint: `POST /api/v1/upload/avatar`

**Frontend (4 dny):**
- [ ] Character avatar upload
  - File picker
  - Image crop/resize (use `react-easy-crop`)
  - Upload to Supabase Storage
  - Display avatar in character sheet + list
- [ ] Profile page
  - Edit username, bio
  - Upload profile avatar
  - Change password (Supabase Auth)
- [ ] Campaign banner upload (optional)
  - Custom image for campaign
  - Display on campaign detail page
- [ ] UI/UX polish V3
  - Animation improvements (Framer Motion)
  - Loading skeletons
  - Better error messages
  - Accessibility improvements (ARIA labels)

---

## 🤖 FÁZE 4: AI Asistent (Future)

**Cíl:** AI-powered rules assistant + content generation

**Časový odhad:** TBD (závisí na AI API costs)

**Prerequisite:** AI API free tier nebo low-cost (OpenAI/Claude)

**Možné features:**
- [ ] Rules chatbot
  - Answer questions about Mausritter rules
  - Knowledge base from `docs/knowledge_base/*.md`
  - Embeddings + RAG (Retrieval-Augmented Generation)
- [ ] AI content generation
  - Custom NPC backgrounds (based on prompts)
  - Session summary auto-generation (from notes)
  - Rumor network expansion
  - Description enhancer (short text → flavor text)
- [ ] GM improvisation assistant
  - "What if players go to hex (3,2)?" → suggest encounter
  - Random name generator (beyond 100 names)
  - Plot thread tracker (AI suggests connections)

**Implementation:**
- Backend: AI API calls (OpenAI/Claude)
- Frontend: Chat interface component
- Database: conversation history (optional)

**Blocker:** Cost (OpenAI/Claude není free). Skip pokud budget je $0.

---

## 📅 Timeline Summary

| Week | Phase | Focus | Estimated Hours |
|------|-------|-------|----------------|
| 1 | MVP | Setup + Infrastructure | 40h |
| 2 | MVP | Auth + Campaign Management | 40h |
| 3 | MVP | Character + Generators | 40h |
| 4 | MVP | Campaign Detail + Polish | 40h |
| 5 | MVP | Testing + Deployment | 40h |
| **Total MVP** | | | **200h (5 týdnů)** |
| 6-7 | V2 | Remaining Generators | 56h |
| 8-9 | V2 | Hexcrawl Map Viewer | 56h |
| 10 | V2 | Character Editing + Players | 40h |
| **Total V2** | | | **152h (4 týdny)** |
| 11 | V3 | Real-time Dice Roller | 40h |
| 12 | V3 | Session Tracking | 40h |
| 13 | V3 | PDF Export | 40h |
| 14 | V3 | File Storage + Polish | 40h |
| **Total V3** | | | **160h (4 týdny)** |
| **TOTAL** | | | **512h (13 týdnů / 3 měsíce)** |

**Note:** Odhady předpokládají full-time vibe coding (40h/týden). Part-time (10h/týden) = 4× delší čas.

---

## 🎯 Success Metrics

### MVP Success Metrics:
- [ ] 5+ test users (GM + players)
- [ ] 3+ active campaigns created
- [ ] 20+ characters generated
- [ ] 100+ generator API calls
- [ ] Zero critical bugs
- [ ] <2s page load time

### V2 Success Metrics:
- [ ] Všech 17 generátorů used at least once
- [ ] 10+ hexcrawl maps created
- [ ] 50+ hexes discovered
- [ ] Players can successfully navigate hexcrawl map

### V3 Success Metrics:
- [ ] 100+ dice rolls recorded
- [ ] 10+ sessions tracked
- [ ] 5+ PDFs exported
- [ ] Real-time updates work reliably

---

## 🚧 Known Risks & Mitigations

### Risk 1: Railway free tier exhaustion
**Mitigation:** Migrate to Render.com (spin-down) nebo pay $10/měsíc

### Risk 2: Supabase 500MB DB limit
**Mitigation:**
- JSONB compression
- Archivace starých kampaní
- Upgrade to Pro ($25/měsíc) if needed

### Risk 3: Vibe coding complexity (no prior web dev experience)
**Mitigation:**
- Start with MVP (simple features)
- Use AI heavily (V0.dev, Cursor, Claude)
- Follow tutorials closely
- Ask for help in Discord communities

### Risk 4: Real-time dice roller technical challenges
**Mitigation:**
- Use Supabase Realtime (easier than raw WebSockets)
- Test thoroughly with multiple clients
- Fallback: polling (if realtime fails)

### Risk 5: PDF generation performance issues
**Mitigation:**
- Generate PDFs async (job queue)
- Cache generated PDFs (1 hour TTL)
- Limit PDF generation to 5/user/hour

---

## 📦 Deliverables

### MVP Deliverables:
- [ ] `web-frontend/` repository (Next.js)
- [ ] `web-backend/` repository (FastAPI)
- [ ] Deployed production URLs:
  - Frontend: `https://mausritter.vercel.app`
  - Backend: `https://api.mausritter.com`
- [ ] User documentation (README)
- [ ] API documentation (Swagger)

### V2 Deliverables:
- [ ] All 17 generators integrated
- [ ] Hexcrawl map feature complete
- [ ] Player management complete

### V3 Deliverables:
- [ ] Real-time features working
- [ ] Session tracking complete
- [ ] PDF exports functional

---

## 🔄 Iteration Plan

Po každé fázi:
1. **User testing** (5-10 users)
2. **Feedback collection** (surveys, Discord)
3. **Bug fixes** (prioritize critical bugs)
4. **Feature refinement** (UX improvements)
5. **Performance optimization** (if needed)

---

## 🔗 Related Documents

- [WEB_ARCHITECTURE.md](WEB_ARCHITECTURE.md) - Tech stack
- [DATABASE_SCHEMA.sql](DATABASE_SCHEMA.sql) - Database structure
- [API_ENDPOINTS.md](API_ENDPOINTS.md) - API specification
- [UI_WIREFRAMES.md](UI_WIREFRAMES.md) - UI/UX design

---

**Last updated:** 2025-11-03
**Next review:** After MVP launch
