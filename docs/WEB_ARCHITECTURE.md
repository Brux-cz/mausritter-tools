# 🏗️ Web Platform Architecture

**Dokument verze:** 1.0
**Datum:** 2025-11-03
**Status:** Design fáze

---

## 🎯 Přehled

Webová platforma pro Mausritter TTRPG poskytující:
- 🎲 **17 generátorů** (character, NPC, hex, dungeon, settlement, atd.)
- 🎭 **Campaign management** pro GM
- 👥 **Character sheets** pro hráče
- 🗺️ **Hexcrawl map viewer** (5×5 interactive grid)
- 🎲 **Real-time dice roller**
- 🤖 **AI asistent** (budoucnost)

**Cílová skupina:**
- GM (Game Masters) - příprava kampaní, session management
- Hráči - character creation, tracking, collaboration
- Komunita - 100-500 aktivních uživatelů (škálovatelné do 50k)

**Budget:** $0/měsíc (využití free tiers)

---

## 📚 Tech Stack

### **Frontend**

**Framework: Next.js 14 (App Router)**
- **Verze:** 14.x
- **Důvod výběru:**
  - Server Components (menší JS bundle)
  - Built-in API routes (pro proxy calls)
  - Vynikající developer experience
  - Perfektní pro vibe coding (V0.dev, Cursor, Claude)
  - Image optimization z krabice
  - SEO friendly
- **Hosting:** Vercel (free tier: 100GB bandwidth)

**UI Library: shadcn/ui + Tailwind CSS**
- **shadcn/ui:** Copy-paste komponenty (ne NPM dependency)
  - Radix UI primitives (accessibility)
  - Fully customizable
  - TypeScript native
- **Tailwind CSS 3.x:** Utility-first CSS
  - Rapid prototyping
  - Konzistentní design system
  - Purge unused styles (malý bundle)

**State Management:**
- **TanStack Query (React Query):** Server state cache
  - Automatic refetching
  - Optimistic updates
  - Error handling
- **Zustand:** Client state (lightweight, simple)
  - Dice roller state
  - UI preferences
  - User settings

**Real-time:** Supabase Realtime
- WebSocket pod kapotou
- Subscribe to DB changes
- Broadcast messages (pro dice rolls)

**Fonts:** Geist Sans + Geist Mono (Vercel default)

---

### **Backend**

**API Framework: FastAPI**
- **Verze:** 0.110+
- **Jazyk:** Python 3.11+
- **Důvod výběru:**
  - **Reuse existujících generátorů** (src/generators/*.py)
  - Modern async/await podpora
  - Auto-generated OpenAPI docs
  - Type hints + Pydantic validation
  - Rychlé (comparable to Node.js)
- **Hosting:** Railway (free tier: $5 credit trial)
  - **Alternativa:** Render.com (free tier s spin-down)

**Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `supabase-py` - Supabase Python client
- `pydantic` - Data validation
- `python-multipart` - File uploads
- Existing: `src/` moduly (dice, generators, models)

**Architecture:**
```
FastAPI
  ├── /api/v1/generate/*  → Wrap existing Python generators
  ├── /api/v1/campaigns/* → CRUD + RLS validation
  ├── /api/v1/characters/* → CRUD + RLS validation
  └── /health             → Health check
```

**API Pattern:**
- RESTful endpoints
- JWT auth (Supabase tokens)
- RLS validation (check Supabase policies)
- JSON responses (from generators)
- Error handling (FastAPI exceptions)

---

### **Database**

**PostgreSQL via Supabase**
- **Verze:** PostgreSQL 15
- **Důvod výběru:**
  - All-in-one (DB + Auth + Storage + Realtime)
  - Generous free tier (500MB DB, 50k MAU)
  - Auto-generated REST API
  - Row Level Security (RLS) z krabice
  - Python SDK existuje
  - Real-time subscriptions

**Schema:**
- 12 tabulek (viz DATABASE_SCHEMA.sql)
- RLS policies pro security
- Indexes pro performance
- JSONB columns pro generated data

**Alternativy zvažované:**
- ❌ Firebase - NoSQL, horší pro relational data
- ❌ PocketBase - Go backend, nutný selfhosting
- ❌ Neon - Postgres serverless, ale méně features než Supabase

---

### **Authentication**

**Supabase Auth**
- **Metody:**
  - Email + Password (primary)
  - Magic Links (passwordless, budoucnost)
  - OAuth (Google, Discord - budoucnost)
- **Token:** JWT (auto-handled)
- **Session:** Cookie-based (Next.js middleware)
- **User roles:** `gm` nebo `player` (v profiles tabulce)

**Security:**
- Password hashing (bcrypt)
- Email verification
- Password reset flow
- Rate limiting (Supabase built-in)

**RLS Integration:**
- `auth.uid()` v policies
- Automatic user context v queries

---

### **File Storage**

**Supabase Storage**
- **Free tier:** 2GB storage, 2GB bandwidth
- **Use cases:**
  - Character avatary (1MB/image → 2000 avatarů)
  - Campaign banners
  - PDF exports
  - Custom hex images (budoucnost)
- **Buckets:**
  - `avatars` - Public read, user write-only
  - `exports` - Private, user read-only
  - `campaign-assets` - Private, campaign members read

**CDN:** Supabase Edge (global)

**Alternativa zvažovaná:**
- ❌ Cloudflare R2 - Více práce, nutná separátní konfigurace

---

## 🌐 Deployment

### **Architektura**

```
┌────────────────┐
│   Cloudflare   │ (DNS only, free)
│   DNS          │
└───────┬────────┘
        │
        ▼
┌────────────────┐      ┌─────────────────┐
│    Vercel      │◀────▶│   Supabase      │
│  (Frontend)    │      │  (DB+Auth+Files)│
│  Next.js App   │      │   PostgreSQL    │
└───────┬────────┘      └─────────────────┘
        │
        │ API Proxy
        ▼
┌────────────────┐
│   Railway      │
│   (Backend)    │
│   FastAPI      │
└────────────────┘
```

**Data Flow:**
1. User → Vercel (Next.js)
2. Next.js → Supabase (auth, data queries)
3. Next.js → Railway FastAPI (generators)
4. FastAPI → Supabase (save generated data)

---

### **Frontend Deployment (Vercel)**

**Free Tier Limits:**
- ✅ 100GB bandwidth/měsíc
- ✅ Unlimited builds
- ✅ Automatic HTTPS
- ✅ Edge network (global CDN)
- ✅ Serverless Functions (100GB-hours)

**Deployment Process:**
1. Push to GitHub → Auto-deploy
2. Preview deployments (každý commit)
3. Production deploy (merge to main)

**Environment Variables:**
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
RAILWAY_API_URL=https://mausritter-api.railway.app
```

**Estimate pro 100-500 users:**
- Page views: 10k-50k/měsíc
- Bandwidth usage: 10-30GB/měsíc
- **Status:** Bezpečně v free tier ✅

---

### **Backend Deployment (Railway)**

**Free Tier (Trial):**
- ✅ $5 trial credit (jednorázový)
- ✅ 500 execution hours/měsíc
- ✅ 8GB RAM, 8GB storage

**Po trial ($5 credit vyčerpán):**
- **Cost:** $0.000463/GB-hour
- **24/7 server (1GB RAM):** ~$10/měsíc
- **Alternativa:** Render.com (spin-down po 15 min, zdarma)

**Deployment Process:**
1. Connect GitHub repo
2. Railway detekuje Python (Dockerfile)
3. Auto-build + deploy

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Environment Variables:**
```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJxxx...
DATABASE_URL=postgresql://xxx
```

**Estimate:**
- API calls: 1k-5k/měsíc (většina přes Supabase direct)
- Runtime: 24/7 needed (generators)
- **Status:** Trial OK, pak $10/měsíc nebo migrate to Render

---

### **Database Deployment (Supabase)**

**Free Tier Limits:**
- ✅ 500MB database
- ✅ 50k monthly active users (MAU)
- ✅ 2GB file storage
- ✅ 2GB bandwidth
- ✅ Unlimited API requests
- ✅ 200 concurrent realtime connections

**Setup Process:**
1. Create Supabase project
2. Run DATABASE_SCHEMA.sql (create tables)
3. Enable RLS on all tables
4. Create RLS policies
5. Setup Storage buckets

**Estimate pro 100-500 users:**
- DB size: 50-100MB (20% of limit)
- MAU: 100-500 (1% of limit)
- API requests: 10k-50k/měsíc (unlimited)
- **Status:** Velmi bezpečně v free tier ✅

**Paid tier trigger:**
- 50k+ MAU → Supabase Pro ($25/měsíc)
- 500MB+ DB → Supabase Pro ($25/měsíc)

---

## 💰 Cost Breakdown

### **Free Tier Capacity**

| Service | Free Limit | Usage (100-500 users) | Headroom |
|---------|------------|----------------------|----------|
| Vercel | 100GB bandwidth | 10-30GB/měsíc | 70-90GB |
| Railway | $5 trial | Trial exhausted | Need paid |
| Supabase | 50k MAU, 500MB DB | 100-500 MAU, 50MB | 49.5k MAU, 450MB |

**Total monthly cost:**
- **MVP phase (trial):** $0/měsíc ✅
- **Post-trial:** $10/měsíc (Railway) nebo $0 (Render spin-down)
- **At scale (50k+ users):** $25 (Supabase) + $10 (Railway) + $20 (Vercel) = **$55/měsíc**

---

## 🔒 Security

### **Authentication**
- Supabase Auth (JWT tokens)
- Password hashing (bcrypt)
- Email verification
- Rate limiting

### **Authorization**
- Row Level Security (RLS)
- Role-based (`gm` vs `player`)
- Campaign membership checks
- Discovery state (`is_discovered`)

### **Data Protection**
- HTTPS everywhere (TLS 1.3)
- Secure cookies (httpOnly, sameSite)
- CORS configuration
- Input validation (Pydantic)

### **RLS Policies Example:**
```sql
-- Players can only read their own characters
CREATE POLICY "Players read own characters"
  ON characters FOR SELECT
  USING (auth.uid() = player_id);

-- GMs can read all characters in their campaigns
CREATE POLICY "GMs read campaign characters"
  ON characters FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );
```

---

## 📊 Monitoring & Observability

### **MVP Phase**
- Vercel Analytics (free, basic)
- Railway logs (free)
- Supabase dashboard (queries, errors)

### **Future**
- Sentry (error tracking)
- PostHog (analytics, free tier)
- LogTail (log aggregation)

---

## 🔄 CI/CD

### **Automated Deployment**
- GitHub → Vercel (auto-deploy on push)
- GitHub → Railway (auto-deploy on push)
- Supabase migrations (manual for now)

### **Testing**
- Pytest (backend unit tests)
- Jest + React Testing Library (frontend)
- Playwright (E2E, budoucnost)

### **Quality Gates**
- TypeScript check (Next.js)
- Linting (ESLint, Ruff for Python)
- Formatting (Prettier, Black)

---

## 🚀 Performance

### **Frontend Optimizations**
- Next.js Server Components (less client JS)
- Image optimization (Next/Image)
- Code splitting (automatic)
- Edge caching (Vercel CDN)

### **Backend Optimizations**
- FastAPI async endpoints
- DB connection pooling (Supabase)
- Response caching (future)
- Lazy loading generators

### **Database Optimizations**
- Indexes na foreign keys
- JSONB indexes (GIN)
- Query optimization (avoid N+1)
- Connection pooling

**Target Performance:**
- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- API response time: <200ms (generators <500ms)

---

## 🔧 Development Workflow

### **Local Development**

**Prerequisites:**
- Node.js 18+
- Python 3.11+
- Git

**Setup:**
```bash
# Frontend
cd web-frontend
npm install
npm run dev  # http://localhost:3000

# Backend
cd web-backend
pip install -r requirements.txt
uvicorn app.main:app --reload  # http://localhost:8000

# Supabase (local)
npx supabase init
npx supabase start  # Local Postgres + dashboard
```

**Environment Variables:**
```env
# .env.local (frontend)
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_API_URL=http://localhost:8000

# .env (backend)
SUPABASE_URL=http://localhost:54321
SUPABASE_SERVICE_KEY=xxx
```

---

## 📝 Additional Notes

### **Why NOT serverless for backend?**
- Python cold starts jsou pomalé (500ms-2s)
- Generátory loadují JSON data (warm cache je lepší)
- 24/7 server je acceptable pro $10/měsíc

### **Why NOT rewrite generators to JS?**
- Zbytečná práce (17 generátorů, 100% tested)
- Python ecosystem pro game tools je silný
- FastAPI wrapping je rychlé (1 den práce)

### **Scalability Considerations**
- Supabase connection pooling (pgBouncer)
- Railway horizontal scaling (budoucnost)
- Vercel Edge Functions (future)
- Read replicas (Supabase Pro feature)

---

## 🔗 Related Documents

- [DATABASE_SCHEMA.sql](DATABASE_SCHEMA.sql) - Database structure
- [API_ENDPOINTS.md](API_ENDPOINTS.md) - API specification
- [WEB_ROADMAP.md](WEB_ROADMAP.md) - Implementation plan
- [UI_WIREFRAMES.md](UI_WIREFRAMES.md) - UI/UX design

---

**Last updated:** 2025-11-03
**Next review:** After MVP deployment
