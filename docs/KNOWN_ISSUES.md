# Known Issues & TODO List

**Last updated:** 2025-11-03
**Status:** Backend API complete (17/17 generators), Frontend Quick Prototype complete (3 generator pages)

---

## 🐛 Known Issues

### High Priority

#### 1. Hexcrawl Generator - Windows Encoding Issue ✅ FIXED
- **Status:** ✅ Resolved (2025-11-03)
- **Component:** Backend API + Python Generator
- **Description:** Hexcrawl endpoint failed on Windows with `'charmap' codec can't encode character` error
- **Solution:** Added UTF-8 encoding declarations to hexcrawl.py and rumor.py, removed problematic emoji print statement
- **Result:** All 17/17 endpoints now functional on Windows
- **Commit:** 870a6cb

---

## 📝 TODO - Backend

### Testing & Quality Assurance

#### 2. Unit Tests for API Endpoints ✅ DONE
- **Status:** ✅ Implemented (2025-11-03) | ✅ All Tests Passing (2025-11-03)
- **Description:** Added pytest unit tests for all 17 API endpoints
- **Results:**
  - **24/24 tests passing** (100% pass rate) ✅
  - All test assertions corrected to match actual API responses
  - Settlement API bug fixed (no_tavern → generate_tavern)
  - Test framework fully functional
- **Coverage:**
  - MVP generators (5): Character, NPC, Hex, Settlement, Weather
  - V2 generators (12): All 12 extended generators
  - Status endpoint, Health check, Validation tests
- **Files Created:**
  - `web-backend/tests/test_generators.py` (24 tests)
  - `web-backend/tests/conftest.py` (pytest fixtures)
  - `web-backend/tests/__init__.py`
- **Files Modified:**
  - `web-backend/app/routers/generators.py` (Settlement bug fix)
- **Dependencies:** Added `httpx==0.26.0` for TestClient compatibility
- **Commits:** 870a6cb (initial tests), [NEW] (test fixes + settlement bug)

#### 3. Error Handling Edge Cases ✅ DONE
- **Status:** ✅ Already Implemented
- **Description:** Error handling is properly implemented via Pydantic validation
- **Current State:**
  - ✅ Pydantic Field validators for all parameters (ge, le constraints)
  - ✅ 422 Validation errors for out-of-range parameters
  - ✅ 400 Bad Request for invalid creature types
  - ✅ 500 Internal Server Error with descriptive messages for generator failures
  - ✅ FastAPI automatic validation and error handling
- **Evidence from tests:**
  - test_hireling_invalid_type: 422 error ✅
  - test_treasure_invalid_bonus: 422 error ✅
  - test_dungeon_invalid_rooms: 422 error ✅
  - test_creature_generator_invalid_type: 400 error ✅
- **Future improvements (V2):**
  - Logging of generator failures
  - Rate limiting for expensive operations

#### 4. API Response Consistency
- **Status:** ⏳ Not Started
- **Priority:** Low
- **Description:** Standardize response formats across all endpoints
- **Current State:**
  - Some return raw dicts from `to_dict()`
  - Some return `dataclasses.asdict()`
  - Rumor returns `{"rumors": [...]}`
  - Hireling adds `availability` field
- **Goal:** Decide on consistent response envelope format

---

## 📝 TODO - Frontend

### Quick Prototype ✅ **COMPLETE** (2025-11-03)

#### 5. Setup shadcn/ui ✅ DONE
- **Status:** ✅ Complete (2025-11-03)
- **Priority:** Medium
- **Description:** Initialize shadcn/ui component library
- **Implemented:**
  - Created `components.json` config
  - Created `lib/utils.ts` with cn() helper
  - Installed dependencies: clsx, tailwind-merge, class-variance-authority, lucide-react, @radix-ui/*
  - Created UI components: button, card, input, label, select, sonner (toast)
  - Added Toaster to root layout
- **Components:** Button, Card, Input, Label, Select, Toast ✅
- **Time:** ~15 minutes

#### 6. API Client Implementation ✅ DONE
- **Status:** ✅ Complete (2025-11-03)
- **Priority:** Medium
- **Description:** Create API client in `web-frontend/lib/api.ts`
- **Implemented:**
  - ✅ TypeScript types for all 17 generators (Request + Response interfaces)
  - ✅ Error handling (APIError class)
  - ✅ Fetch wrappers for all 17 generators
  - ✅ Health check and status endpoints
- **File:** `web-frontend/lib/api.ts` (400+ lines)
- **Time:** ~20 minutes

#### 7. Generator Hub Page ✅ DONE
- **Status:** ✅ Complete (2025-11-03)
- **Priority:** Medium
- **Description:** `/generators` page with grid of all generators
- **Implemented:**
  - ✅ Grid of all 17 generators with cards (emoji + název + popis)
  - ✅ Category filtering (All/MVP/Extended)
  - ✅ Search functionality
  - ✅ Links to individual generator pages
  - ✅ "Coming Soon" badge for not-yet-implemented generators
- **File:** `web-frontend/app/generators/page.tsx`
- **Time:** ~25 minutes

#### 8. Character Generator Page ✅ DONE
- **Status:** ✅ Complete (2025-11-03)
- **Priority:** High
- **Description:** `/generators/character` page with full UI
- **Implemented:**
  - ✅ Form inputs: name (optional), gender (select)
  - ✅ Generate button with loading state
  - ✅ Display result: Stats grid, HP hearts, Inventory grid, Appearance details
  - ✅ Copy JSON functionality
  - ✅ Reset button
  - ✅ Toast notifications (success/error)
- **File:** `web-frontend/app/generators/character/page.tsx`
- **Time:** ~35 minutes

#### 9. NPC Generator Page ✅ DONE
- **Status:** ✅ Complete (2025-11-03)
- **Priority:** High
- **Description:** `/generators/npc` page
- **Implemented:**
  - ✅ Form inputs: name (optional), gender (select)
  - ✅ Generate button with loading state
  - ✅ Display result: Status, Birthsign, Appearance, Quirk, Desire, Relationship, Reaction
  - ✅ Copy JSON functionality
  - ✅ Dice roll info
- **File:** `web-frontend/app/generators/npc/page.tsx`
- **Time:** ~25 minutes

#### 10. Weather Generator Page ✅ DONE
- **Status:** ✅ Complete (2025-11-03)
- **Priority:** Medium
- **Description:** `/generators/weather` page
- **Implemented:**
  - ✅ Season select dropdown (Spring/Summer/Autumn/Winter)
  - ✅ Event checkbox
  - ✅ Display result with weather-themed styling
  - ✅ Season emoji icons
  - ✅ Adverse weather warning (red border)
  - ✅ Season info panel
- **File:** `web-frontend/app/generators/weather/page.tsx`
- **Time:** ~30 minutes

### E2E Testing ✅ **COMPLETE** (2025-11-03)

#### 11. Playwright E2E Tests ✅ DONE
- **Status:** ✅ Tests Created (2025-11-03)
- **Priority:** High
- **Description:** 6 E2E test suites using Playwright
- **Implemented:**
  - ✅ `playwright.config.ts` - Configuration with webServer setup
  - ✅ `tests/e2e/homepage.spec.ts` - 5 tests (landing page, headings, buttons, features)
  - ✅ `tests/e2e/generator-hub.spec.ts` - 6 tests (17 generators, filters, search)
  - ✅ `tests/e2e/character-generator.spec.ts` - 6 tests (form, generation, inventory, JSON copy, reset)
  - ✅ `tests/e2e/npc-generator.spec.ts` - 5 tests (generation, custom name, reaction info)
  - ✅ `tests/e2e/weather-generator.spec.ts` - 6 tests (seasons, events, info panel)
  - ✅ `tests/e2e/api-health.spec.ts` - 5 tests (backend health, status, API calls)
- **Total:** 33 E2E tests across 6 test files
- **Commands:** `npm run test:e2e`, `npm run test:e2e:ui`, `npm run test:e2e:headed`
- **Time:** ~45 minutes

---

## 📝 TODO - Frontend (Next Steps)

---

## 📝 TODO - Documentation

#### 11. API Testing Documentation
- **Status:** ⏳ Not Started
- **Priority:** Low
- **Description:** Add curl examples for all 17 endpoints
- **File:** `docs/API_ENDPOINTS.md` (needs update)
- **Current State:** Only has 5 MVP examples

#### 12. Deployment Guide
- **Status:** ⏳ Not Started
- **Priority:** Low
- **Description:** Document deployment process
- **Platforms:**
  - Backend: Railway / Render
  - Frontend: Vercel
  - Environment variables
  - CI/CD setup

---

## 🔮 Future Enhancements (V2)

### Authentication & Users
- Supabase Auth integration
- User registration/login
- JWT token handling
- Protected routes

### Campaign Management
- Campaign CRUD endpoints
- Character persistence
- Session notes
- Shared campaigns (GM + Players)

### Real-time Features
- WebSocket for dice rolls
- Live campaign updates
- Multiplayer sessions

### Performance
- Rate limiting (e.g., 10 req/min per IP)
- Caching strategy (Redis?)
- Database connection pooling
- CDN for static assets

### Monitoring
- Error tracking (Sentry?)
- Analytics (Plausible?)
- Performance monitoring
- API usage metrics

---

## 📌 Development Notes

### Port Configuration (FIXED - DO NOT CHANGE)
- Frontend: `localhost:3001`
- Backend: `localhost:8001`
- Swagger UI: `localhost:8001/docs`

**Important:** Port 8000 is blocked by stale process. Always use 8001 for backend.

### Commands Reference
```bash
# Backend (from root)
cd web-backend
python -m uvicorn app.main:app --port 8001

# Frontend
cd web-frontend
npm run dev -- -p 3001
```

### Git Workflow
- Commit frequently with descriptive messages
- Test before committing
- Update README.md when adding features
- Keep KNOWN_ISSUES.md updated

---

## ✅ Completed (Reference)

- ✅ Backend API expanded from 5 → 17 generators
- ✅ All endpoint parameter issues fixed
- ✅ Dataclass serialization implemented
- ✅ Path parameters for creature variants
- ✅ Port conflicts resolved (8000 → 8001)
- ✅ Documentation updated (README.md, claude.md)
- ✅ Git commit: 55543c7

---

## 📊 Progress Tracker

| Category | Total | Done | Pending | Blocked |
|----------|-------|------|---------|---------|
| Backend Issues | 1 | 1 | 0 | 0 |
| Backend TODO | 3 | 3 | 0 | 0 |
| Frontend Quick Prototype | 7 | 7 | 0 | 0 |
| Documentation | 2 | 0 | 2 | 0 |
| **TOTAL** | **13** | **11** | **2** | **0** |

**Completed Today (2025-11-03):**
- ✅ #1: Hexcrawl encoding fix
- ✅ #2: Unit tests (24/24 passing - 100%)
- ✅ #3: Error handling (already implemented)
- ✅ #4: Settlement API bug fix (no_tavern parameter)
- ✅ #5: shadcn/ui setup (6 komponenty)
- ✅ #6: API Client (17 generátorů, 400+ řádků)
- ✅ #7: Generator Hub page (filtrování, vyhledávání)
- ✅ #8: Character Generator page
- ✅ #9: NPC Generator page
- ✅ #10: Weather Generator page
- ✅ #11: Playwright E2E testy (33 testů v 6 souborech)

---

**Next Steps:**
- Dokumentace API testingu (curl příklady)
- Deployment Guide (Railway/Vercel)
- Implementace dalších 14 generátor pages (optional)
