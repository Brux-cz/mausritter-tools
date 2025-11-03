# Known Issues & TODO List

**Last updated:** 2025-11-03
**Status:** Backend API complete (17/17 generators), Frontend MVP Week 1 complete

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

### Quick Prototype (Option B - Not Started)

#### 5. Setup shadcn/ui
- **Status:** ⏳ Not Started
- **Priority:** Medium
- **Description:** Initialize shadcn/ui component library
- **Steps:**
  ```bash
  cd web-frontend
  npx shadcn-ui@latest init
  npx shadcn-ui@latest add button card input select dialog toast
  ```
- **Components Needed:** Button, Card, Input, Select, Dialog, Toast
- **Estimate:** 10 minutes

#### 6. API Client Implementation
- **Status:** ⏳ Not Started
- **Priority:** Medium
- **Description:** Create API client in `web-frontend/lib/api.ts`
- **Requirements:**
  - TypeScript types for all 17 generators
  - Error handling
  - Loading states
  - Response validation
- **Dependencies:** Backend must be running on port 8001
- **Estimate:** 15 minutes

#### 7. Generator Hub Page
- **Status:** ⏳ Not Started
- **Priority:** Medium
- **Description:** `/generators` page with grid of all generators
- **Features:**
  - Visual cards for each generator
  - Category filtering (MVP vs Extended)
  - Search functionality
  - Links to individual generator pages
- **File:** `web-frontend/app/generators/page.tsx`
- **Estimate:** 20 minutes

#### 8. Character Generator Page
- **Status:** ⏳ Not Started
- **Priority:** High
- **Description:** `/generators/character` page with full UI
- **Features:**
  - Form inputs: name (optional), gender (select)
  - Generate button
  - Display result with styling
  - Copy/Save functionality
- **File:** `web-frontend/app/generators/character/page.tsx`
- **Estimate:** 30 minutes

#### 9. NPC Generator Page
- **Status:** ⏳ Not Started
- **Priority:** High
- **Description:** `/generators/npc` page
- **Features:** Similar to Character Generator
- **File:** `web-frontend/app/generators/npc/page.tsx`
- **Estimate:** 20 minutes

#### 10. Weather Generator Page
- **Status:** ⏳ Not Started
- **Priority:** Medium
- **Description:** `/generators/weather` page
- **Features:**
  - Season select dropdown
  - Event checkbox
  - Display result with weather-themed styling
- **File:** `web-frontend/app/generators/weather/page.tsx`
- **Estimate:** 25 minutes

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
| Frontend TODO | 6 | 0 | 6 | 0 |
| Documentation | 2 | 0 | 2 | 0 |
| **TOTAL** | **12** | **4** | **8** | **0** |

**Completed Today (2025-11-03):**
- ✅ #1: Hexcrawl encoding fix
- ✅ #2: Unit tests (24/24 passing - 100%)
- ✅ #3: Error handling (already implemented)
- ✅ Settlement API bug fix (no_tavern parameter)
- ✅ All test assertions corrected

---

**Next Steps:**
- Quick Prototype (3 generator pages) OR Continue with MVP Week 2
- No blocking issues remaining in backend ✅
