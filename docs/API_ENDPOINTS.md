# 🔌 API Endpoints Specification

**Version:** 1.0
**Date:** 2025-11-03
**Base URL:** `https://api.mausritter.com` (production)
**Base URL:** `http://localhost:8000` (development)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Generators](#generators)
3. [Campaigns](#campaigns)
4. [Characters](#characters)
5. [Hexes](#hexes)
6. [Settlements](#settlements)
7. [Dungeons](#dungeons)
8. [NPCs](#npcs)
9. [Rumors](#rumors)
10. [Sessions](#sessions)
11. [Dice Rolls](#dice-rolls)
12. [Utilities](#utilities)

---

## 🔐 Authentication

### Note
Authentication je handled přes **Supabase Auth**, ne FastAPI.
Frontend používá Supabase JS client pro login/signup.
FastAPI endpoints očekávají `Authorization: Bearer <jwt_token>` header.

**Supabase Auth Endpoints** (automatické):
- `POST /auth/v1/signup` - Register user
- `POST /auth/v1/token?grant_type=password` - Login
- `POST /auth/v1/logout` - Logout
- `GET /auth/v1/user` - Get current user
- `POST /auth/v1/recover` - Password reset

**FastAPI Middleware:**
- Všechny `/api/v1/*` endpointy vyžadují auth (kromě health check)
- JWT token validation přes Supabase
- User ID extraction z `auth.uid()`

---

## 🎲 Generators

### Overview
Wrapping existujících Python generátorů z `src/generators/`.
Všechny generator endpointy:
- **Method:** `POST`
- **Auth:** Required (JWT)
- **Response:** JSON object z generátoru
- **Status Codes:**
  - `200 OK` - Successful generation
  - `400 Bad Request` - Invalid parameters
  - `401 Unauthorized` - Missing/invalid token
  - `500 Internal Server Error` - Generator failed

---

### 1. Character Generator

**Endpoint:** `POST /api/v1/generate/character`

**Request Body:**
```json
{
  "name": "Pepřík",        // Optional, string
  "gender": "male"         // Optional, "male" | "female"
}
```

**Response:**
```json
{
  "name": "Pepřík Hrabal",
  "background": "Stěnolezec",
  "strength": 8,
  "dexterity": 11,
  "willpower": 12,
  "max_hp": 6,
  "current_hp": 6,
  "pips": 0,
  "pence": 4,
  "birthsign": "Kozoroh",
  "coat_color": "Šedá",
  "coat_pattern": "Pruhovaný",
  "distinctive_trait": "Velké uši",
  "inventory": [
    {"name": "Meč", "slots": 1, "damage": "k6"},
    {"name": "Štít", "slots": 1, "armor": "+1"},
    {"name": "Pochodně", "slots": 1, "uses": 3}
  ],
  "background_description": "Začal jako myš žijící v trámech...",
  "background_benefit": "Nikdo tě nepřekoná v šplhání."
}
```

**Testing with curl:**
```bash
# Basic example (random character)
curl -X POST http://localhost:8001/api/v1/generate/character \
  -H "Content-Type: application/json" \
  -d '{}'

# With custom name
curl -X POST http://localhost:8001/api/v1/generate/character \
  -H "Content-Type: application/json" \
  -d '{"name": "Pepřík"}'

# Female character with custom name
curl -X POST http://localhost:8001/api/v1/generate/character \
  -H "Content-Type: application/json" \
  -d '{"name": "Klárka", "gender": "female"}'

# Pretty-print JSON response (Windows)
curl -X POST http://localhost:8001/api/v1/generate/character \
  -H "Content-Type: application/json" \
  -d '{}' | python -m json.tool
```

---

### 2. NPC Generator

**Endpoint:** `POST /api/v1/generate/npc`

**Request Body:**
```json
{
  "name": null,           // Optional
  "gender": "female"      // Optional
}
```

**Response:**
```json
{
  "name": "Klárka Mlynářová",
  "social_status": "Chudák",
  "birthsign": "Blíženci",
  "appearance": "Špinavá srst",
  "quirk": "Otravně neustále kýchá",
  "desire": "Chce proslavit svůj rod",
  "relationship": "Spolupracující",
  "reaction": "Nejistá"
}
```

**Testing with curl:**
```bash
# Basic example (random NPC)
curl -X POST http://localhost:8001/api/v1/generate/npc \
  -H "Content-Type: application/json" \
  -d '{}'

# Female NPC with custom name
curl -X POST http://localhost:8001/api/v1/generate/npc \
  -H "Content-Type: application/json" \
  -d '{"name": "Klárka", "gender": "female"}'

# Male NPC
curl -X POST http://localhost:8001/api/v1/generate/npc \
  -H "Content-Type: application/json" \
  -d '{"gender": "male"}'
```

---

### 3. Hireling Generator

**Endpoint:** `POST /api/v1/generate/hireling`

**Request Body:**
```json
{
  "type": 6,              // Optional, 1-9 (see types below)
  "name": null,           // Optional
  "gender": "male"        // Optional
}
```

**Hireling Types:**
- 1: Světlonoš (1 ď/den)
- 2: Dělník (2 ď/den)
- 3: Kopáč chodeb (5 ď/den)
- 4: Zbrojíř/kovář (8 ď/den)
- 5: Místní průvodce (10 ď/den)
- 6: Zbrojmyš (10 ď/den)
- 7: Učenec (20 ď/den)
- 8: Rytíř (25 ď/den)
- 9: Tlumočník (30 ď/den)

**Response:**
```json
{
  "name": "Sir Pepřík",
  "type": "Zbrojmyš",
  "cost_per_day": 10,
  "strength": 10,
  "dexterity": 8,
  "willpower": 7,
  "hp": 5,
  "armor": 1,
  "attack": "+1",
  "equipment": ["Meč", "Zbroj"]
}
```

**Testing with curl:**
```bash
# Random hireling (any type)
curl -X POST http://localhost:8001/api/v1/generate/hireling \
  -H "Content-Type: application/json" \
  -d '{}'

# Specific type - Zbrojmyš (type 6)
curl -X POST http://localhost:8001/api/v1/generate/hireling \
  -H "Content-Type: application/json" \
  -d '{"type": 6}'

# Knight with custom name (type 8)
curl -X POST http://localhost:8001/api/v1/generate/hireling \
  -H "Content-Type: application/json" \
  -d '{"type": 8, "name": "Sir Pepřík", "gender": "male"}'

# Scholar (type 7)
curl -X POST http://localhost:8001/api/v1/generate/hireling \
  -H "Content-Type: application/json" \
  -d '{"type": 7}'
```

---

### 4. Weather Generator

**Endpoint:** `POST /api/v1/generate/weather`

**Request Body:**
```json
{
  "season": "autumn",     // Required: "spring" | "summer" | "autumn" | "winter"
  "with_event": true      // Optional, default false
}
```

**Response:**
```json
{
  "season": "Podzim",
  "weather": "Silný vítr",
  "effect": "Mise vyžadující sluch nebo dohled jsou obtížné.",
  "event": "Hejno migračních ptáků zamíří na jih.",
  "event_type": "Sezónní událost"
}
```

**Testing with curl:**
```bash
# Spring weather
curl -X POST http://localhost:8001/api/v1/generate/weather \
  -H "Content-Type: application/json" \
  -d '{"season": "spring"}'

# Summer weather with event
curl -X POST http://localhost:8001/api/v1/generate/weather \
  -H "Content-Type: application/json" \
  -d '{"season": "summer", "with_event": true}'

# Autumn weather with event
curl -X POST http://localhost:8001/api/v1/generate/weather \
  -H "Content-Type: application/json" \
  -d '{"season": "autumn", "with_event": true}'

# Winter weather (dangerous!)
curl -X POST http://localhost:8001/api/v1/generate/weather \
  -H "Content-Type: application/json" \
  -d '{"season": "winter"}'
```

---

### 5. Reaction Roll

**Endpoint:** `POST /api/v1/generate/reaction`

**Request Body:**
```json
{
  "modifier": 1          // Optional, default 0 (range: -6 to +6)
}
```

**Response:**
```json
{
  "roll": 9,
  "modifier": 1,
  "total": 10,
  "reaction": "Povídavá",
  "description": "Tvor je ochoten komunikovat a možná pomoci."
}
```

**Testing with curl:**
```bash
# Basic reaction roll
curl -X POST http://localhost:8001/api/v1/generate/reaction \
  -H "Content-Type: application/json" \
  -d '{}'

# With positive modifier (+2 from gift)
curl -X POST http://localhost:8001/api/v1/generate/reaction \
  -H "Content-Type: application/json" \
  -d '{"modifier": 2}'

# With negative modifier (-3 from aggression)
curl -X POST http://localhost:8001/api/v1/generate/reaction \
  -H "Content-Type: application/json" \
  -d '{"modifier": -3}'
```

---

### 6. Spell Generator

**Endpoint:** `POST /api/v1/generate/spell`

**Request Body:**
```json
{}  // No parameters
```

**Response:**
```json
{
  "name": "Ohnivá koule",
  "effect": "Vystřelíš ohnivou kouli, která způsobí [SOUČET] zranění...",
  "roll": [2, 5]
}
```

**Testing with curl:**
```bash
# Random spell
curl -X POST http://localhost:8001/api/v1/generate/spell \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### 7. Treasure Generator

**Endpoint:** `POST /api/v1/generate/treasure`

**Request Body:**
```json
{
  "bonus": 2            // Optional, 0-4, default 0
}
```

**Response:**
```json
{
  "items": [
    {
      "type": "pence",
      "amount": 50,
      "container": "Pytel",
      "slots": 1
    },
    {
      "type": "magic_sword",
      "name": "Vlčí zub",
      "damage": "k6",
      "cursed": false
    },
    {
      "type": "spell",
      "name": "Zahojení",
      "value": 300
    }
  ],
  "total_rolls": 4,
  "bonus_rolls": 2
}
```

**Testing with curl:**
```bash
# Basic treasure (2 rolls)
curl -X POST http://localhost:8001/api/v1/generate/treasure \
  -H "Content-Type: application/json" \
  -d '{}'

# Treasure with 2 bonus rolls
curl -X POST http://localhost:8001/api/v1/generate/treasure \
  -H "Content-Type: application/json" \
  -d '{"bonus": 2}'

# Maximum treasure (4 bonus rolls = 6 total)
curl -X POST http://localhost:8001/api/v1/generate/treasure \
  -H "Content-Type: application/json" \
  -d '{"bonus": 4}'
```

---

### 8. Adventure Seed Generator

**Endpoint:** `POST /api/v1/generate/adventure`

**Request Body:**
```json
{
  "custom": false       // Optional, default false (true = mix & match)
}
```

**Response:**
```json
{
  "creature": "Rybář",
  "problem": "Obviněn ze zločinu",
  "complication": "Může za to pomocník hráčské myši",
  "seed_number": 23,
  "inspiration": {
    "questions": ["Kde se to stalo?", "Proč rybář?", ...],
    "hooks": ["Rybář prosí o pomoc...", ...]
  }
}
```

**Testing with curl:**
```bash
# Standard adventure seed (one roll, whole row)
curl -X POST http://localhost:8001/api/v1/generate/adventure \
  -H "Content-Type: application/json" \
  -d '{}'

# Custom mode (three separate rolls, mix & match)
curl -X POST http://localhost:8001/api/v1/generate/adventure \
  -H "Content-Type: application/json" \
  -d '{"custom": true}'

# With inspiration text
curl -X POST http://localhost:8001/api/v1/generate/adventure \
  -H "Content-Type: application/json" \
  -d '{"with_inspiration": true}'
```

---

### 9. Adventure Hook Generator

**Endpoint:** `POST /api/v1/generate/hook`

**Request Body:**
```json
{}  // No parameters
```

**Response:**
```json
{
  "hook": "Hledání ztraceného člena rodiny",
  "category": "Osobní",
  "questions": [
    "Kdo zmizel?",
    "Kde byl naposledy viděn?",
    "Proč je důležité ho najít?"
  ]
}
```

**Testing with curl:**
```bash
# Random adventure hook
curl -X POST http://localhost:8001/api/v1/generate/hook \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### 10. Creature Variant Generator

**Endpoint:** `POST /api/v1/generate/creature/{type}`

**Path Parameters:**
- `type`: `ghost` | `snake` | `cat` | `rat` | `mouse` | `spider` | `owl` | `centipede` | `fairy` | `crow` | `frog`

**Request Body:**
```json
{}  // No parameters
```

**Response:**
```json
{
  "type": "Sova",
  "variant": "Bezalel",
  "description": "Vyrábí mechanické služebníky",
  "roll": 1
}
```

**Testing with curl:**
```bash
# Ghost variant
curl -X POST http://localhost:8001/api/v1/generate/creature/ghost \
  -H "Content-Type: application/json" \
  -d '{}'

# Cat variant
curl -X POST http://localhost:8001/api/v1/generate/creature/cat \
  -H "Content-Type: application/json" \
  -d '{}'

# Owl wizard variant
curl -X POST http://localhost:8001/api/v1/generate/creature/owl \
  -H "Content-Type: application/json" \
  -d '{}'

# Spider variant
curl -X POST http://localhost:8001/api/v1/generate/creature/spider \
  -H "Content-Type: application/json" \
  -d '{}'

# All 11 types: ghost, snake, cat, rat, mouse, spider, owl, centipede, fairy, crow, frog
```

---

### 11. Tavern Generator

**Endpoint:** `POST /api/v1/generate/tavern`

**Request Body:**
```json
{}  // No parameters
```

**Response:**
```json
{
  "name": "U Bílého Brouka",
  "specialty": "Pečená kořeněná mrkev"
}
```

**Testing with curl:**
```bash
# Random tavern
curl -X POST http://localhost:8001/api/v1/generate/tavern \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### 12. Settlement Generator

**Endpoint:** `POST /api/v1/generate/settlement`

**Request Body:**
```json
{
  "with_name": true,     // Optional, generate name from generator
  "no_tavern": false     // Optional, force no tavern even for large settlements
}
```

**Response:**
```json
{
  "size": "Víska",
  "size_description": "50-150 myší",
  "government": "Rada starších",
  "detail": "Postavená kolem jediného velkého stromu",
  "trades": ["Léčitel"],
  "features": ["Chrám nebo svatyně"],
  "event": "Svatba nebo pohřeb",
  "tavern": {
    "name": "U Černého Orla",
    "specialty": "Tlustý rybí řízek"
  }
}
```

**Testing with curl:**
```bash
# Basic settlement
curl -X POST http://localhost:8001/api/v1/generate/settlement \
  -H "Content-Type: application/json" \
  -d '{}'

# Settlement with generated name
curl -X POST http://localhost:8001/api/v1/generate/settlement \
  -H "Content-Type: application/json" \
  -d '{"with_name": true}'

# Settlement without tavern
curl -X POST http://localhost:8001/api/v1/generate/settlement \
  -H "Content-Type: application/json" \
  -d '{"no_tavern": true}'
```

---

### 13. Hex Generator

**Endpoint:** `POST /api/v1/generate/hex`

**Request Body:**
```json
{
  "with_settlement": false  // Optional, force settlement generation
}
```

**Response:**
```json
{
  "hex_type": "Les",
  "category": "Zvířecí a přírodní prvky",
  "detail": "Hnízdo zpěvného ptáka",
  "hook": "Jaké smutné příběhy pěje?",
  "settlement": null       // Populated if category=1 or with_settlement=true
}
```

**Testing with curl:**
```bash
# Random hex
curl -X POST http://localhost:8001/api/v1/generate/hex \
  -H "Content-Type: application/json" \
  -d '{}'

# Hex with forced settlement
curl -X POST http://localhost:8001/api/v1/generate/hex \
  -H "Content-Type: application/json" \
  -d '{"with_settlement": true}'
```

---

### 14. Dungeon Generator

**Endpoint:** `POST /api/v1/generate/dungeon`

**Request Body:**
```json
{
  "rooms": 6,                  // Optional, default 6 (1-20)
  "with_settlement": false     // Optional, force past=20 (Mouse settlement)
}
```

**Response:**
```json
{
  "past": "Starodávný chrám netopýřího kultu",
  "decay": "Magická nehoda",
  "inhabitants": "Přízrační duchové",
  "goal": "Zvláštní a mocné kouzlo",
  "secret": "Obelisk hučící mystickou energií",
  "rooms": [
    {
      "number": 1,
      "type": "Prázdná",
      "has_creature": false,
      "has_treasure": true,
      "feature": "Trs hub"
    },
    {
      "number": 2,
      "type": "Překážka",
      "has_creature": true,
      "has_treasure": false,
      "feature": "Zamčené dveře. Klíč se nachází v jiné místnosti."
    }
  ]
}
```

**Testing with curl:**
```bash
# Basic dungeon (6 rooms)
curl -X POST http://localhost:8001/api/v1/generate/dungeon \
  -H "Content-Type: application/json" \
  -d '{}'

# Small dungeon (3 rooms)
curl -X POST http://localhost:8001/api/v1/generate/dungeon \
  -H "Content-Type: application/json" \
  -d '{"rooms": 3}'

# Large dungeon (15 rooms)
curl -X POST http://localhost:8001/api/v1/generate/dungeon \
  -H "Content-Type: application/json" \
  -d '{"rooms": 15}'

# Dungeon with mouse settlement past
curl -X POST http://localhost:8001/api/v1/generate/dungeon \
  -H "Content-Type: application/json" \
  -d '{"rooms": 6, "with_settlement": true}'
```

---

### 15. Rumor Generator

**Endpoint:** `POST /api/v1/generate/rumor`

**Request Body:**
```json
{
  "count": 6,              // Optional, default 6 (k6 table)
  "category": null,        // Optional: "threat" | "npc" | "location" | "treasure" | "mystery"
  "core_only": true        // Optional, default true (no extended features)
}
```

**Response:**
```json
{
  "rumors": [
    {
      "rumor_text": "V bažině na severu se objevují podivná světla",
      "truthfulness": "true",
      "category": "mystery",
      "roll": 1
    },
    {
      "rumor_text": "Starý mlynář má ukrytý poklad",
      "truthfulness": "partial",
      "category": "treasure",
      "roll": 4
    }
  ]
}
```

**Testing with curl:**
```bash
# Basic rumors (6, core only)
curl -X POST http://localhost:8001/api/v1/generate/rumor \
  -H "Content-Type: application/json" \
  -d '{}'

# Core only rumors
curl -X POST http://localhost:8001/api/v1/generate/rumor \
  -H "Content-Type: application/json" \
  -d '{"core_only": true}'

# Advanced rumors (with extended features)
curl -X POST http://localhost:8001/api/v1/generate/rumor \
  -H "Content-Type: application/json" \
  -d '{"core_only": false, "advanced": true}'
```

---

### 16. Hexcrawl Generator (Bulk)

**Endpoint:** `POST /api/v1/generate/hexcrawl`

**Request Body:**
```json
{
  "size": 5,              // Optional, default 5 (5x5 grid = 25 hexes)
  "settlements": 3,       // Optional, default 3 (1-3)
  "dungeons": 3,          // Optional, default 3 (2-4)
  "rumors": 6            // Optional, default 6
}
```

**Response:**
```json
{
  "hexes": [
    {
      "col": 0,
      "row": 0,
      "hex_type": "Otevřená krajina",
      "detail": "Vílí kruh",
      ...
    },
    // ... 24 more hexes
  ],
  "settlements": [
    {
      "hex_position": {"col": 2, "row": 2},
      "size": "Víska",
      ...
    },
    // ... 2 more
  ],
  "dungeons": [
    {
      "hex_position": {"col": 1, "row": 3},
      "past": "Chrám",
      ...
    },
    // ... 2 more
  ],
  "rumors": [
    {"rumor_text": "...", "truthfulness": "true"},
    // ... 5 more
  ]
}
```

**Testing with curl:**
```bash
# Standard hexcrawl (25 hexes, 3 settlements, 3 dungeons, 6 rumors)
curl -X POST http://localhost:8001/api/v1/generate/hexcrawl \
  -H "Content-Type: application/json" \
  -d '{}'

# Standard preset (explicit)
curl -X POST http://localhost:8001/api/v1/generate/hexcrawl \
  -H "Content-Type: application/json" \
  -d '{"preset": "standard"}'

# Large hexcrawl preset
curl -X POST http://localhost:8001/api/v1/generate/hexcrawl \
  -H "Content-Type: application/json" \
  -d '{"preset": "large"}'

# Small hexcrawl preset
curl -X POST http://localhost:8001/api/v1/generate/hexcrawl \
  -H "Content-Type: application/json" \
  -d '{"preset": "small"}'

# Custom configuration
curl -X POST http://localhost:8001/api/v1/generate/hexcrawl \
  -H "Content-Type: application/json" \
  -d '{"settlements": 5, "dungeons": 4, "factions": 3}'

# Core-only mode (no advanced features)
curl -X POST http://localhost:8001/api/v1/generate/hexcrawl \
  -H "Content-Type: application/json" \
  -d '{"core_only": true}'
```

---

## 🏕️ Campaigns

### List Campaigns

**Endpoint:** `GET /api/v1/campaigns`

**Auth:** Required (GM or Player)

**Query Parameters:**
- `role`: Filter by role (`gm` or `player`)
- `active`: Filter by status (`true` or `false`)

**Response:**
```json
{
  "campaigns": [
    {
      "id": "uuid",
      "name": "Autumn Valley",
      "description": "A hexcrawl through...",
      "gm_id": "uuid",
      "gm_username": "GameMaster123",
      "is_active": true,
      "player_count": 4,
      "created_at": "2025-11-03T10:00:00Z"
    }
  ]
}
```

---

### Get Campaign

**Endpoint:** `GET /api/v1/campaigns/{id}`

**Auth:** Required (GM or campaign player)

**Response:**
```json
{
  "id": "uuid",
  "name": "Autumn Valley",
  "description": "...",
  "gm_id": "uuid",
  "gm_username": "GameMaster123",
  "current_season": "autumn",
  "current_weather": {...},
  "is_active": true,
  "players": [
    {"id": "uuid", "username": "Player1", "status": "active"}
  ],
  "stats": {
    "hexes_discovered": 8,
    "settlements_discovered": 2,
    "dungeons_cleared": 1,
    "sessions_played": 5
  },
  "created_at": "2025-11-03T10:00:00Z"
}
```

---

### Create Campaign

**Endpoint:** `POST /api/v1/campaigns`

**Auth:** Required (any user, becomes GM)

**Request Body:**
```json
{
  "name": "Autumn Valley",
  "description": "A hexcrawl adventure...",
  "current_season": "autumn"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Autumn Valley",
  "gm_id": "uuid",
  "created_at": "2025-11-03T10:00:00Z"
}
```

---

### Update Campaign

**Endpoint:** `PUT /api/v1/campaigns/{id}`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "name": "New Name",
  "description": "Updated description",
  "current_season": "winter",
  "current_weather": {...}
}
```

---

### Delete Campaign

**Endpoint:** `DELETE /api/v1/campaigns/{id}`

**Auth:** Required (GM only)

**Response:** `204 No Content`

---

### Add Player to Campaign

**Endpoint:** `POST /api/v1/campaigns/{id}/players`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "player_id": "uuid",    // Or "username": "Player1"
  "notes": "Friend from Discord"
}
```

---

### Remove Player from Campaign

**Endpoint:** `DELETE /api/v1/campaigns/{id}/players/{player_id}`

**Auth:** Required (GM only)

**Response:** `204 No Content`

---

## ⚔️ Characters

### List Characters

**Endpoint:** `GET /api/v1/campaigns/{campaign_id}/characters`

**Auth:** Required (GM or campaign player)

**Response:**
```json
{
  "characters": [
    {
      "id": "uuid",
      "name": "Pepřík Hrabal",
      "background": "Stěnolezec",
      "player_id": "uuid",
      "player_username": "Player1",
      "level": 1,
      "current_hp": 5,
      "max_hp": 6,
      "is_alive": true
    }
  ]
}
```

---

### Get Character

**Endpoint:** `GET /api/v1/characters/{id}`

**Auth:** Required (owner or GM)

**Response:**
```json
{
  "id": "uuid",
  "name": "Pepřík Hrabal",
  "background": "Stěnolezec",
  "strength": 8,
  "dexterity": 11,
  "willpower": 12,
  "current_hp": 5,
  "max_hp": 6,
  "level": 1,
  "xp": 150,
  "pips": 2,
  "pence": 25,
  "inventory": [...],
  "conditions": ["injured"],
  "created_at": "2025-11-03T10:00:00Z"
}
```

---

### Create Character

**Endpoint:** `POST /api/v1/campaigns/{campaign_id}/characters`

**Auth:** Required (player in campaign)

**Request Body:**
```json
{
  "generated_data": {...}  // Full output from character generator
}
```

---

### Update Character

**Endpoint:** `PUT /api/v1/characters/{id}`

**Auth:** Required (owner or GM)

**Request Body:**
```json
{
  "current_hp": 4,
  "pence": 30,
  "inventory": [...],
  "conditions": []
}
```

---

### Delete Character

**Endpoint:** `DELETE /api/v1/characters/{id}`

**Auth:** Required (owner or GM)

**Response:** `204 No Content`

---

## 🗺️ Hexes

### Get All Hexes (Grid)

**Endpoint:** `GET /api/v1/campaigns/{campaign_id}/hexes`

**Auth:** Required (GM or player)

**Query Parameters:**
- `discovered_only`: `true` (players see only discovered)

**Response:**
```json
{
  "hexes": [
    {
      "id": "uuid",
      "col": 0,
      "row": 0,
      "hex_type": "Les",
      "is_discovered": true,
      "detail": "Chýše myší čarodějnice"
    }
    // ... 24 more
  ]
}
```

---

### Get Hex

**Endpoint:** `GET /api/v1/hexes/{id}`

**Auth:** Required (GM or player if discovered)

**Response:**
```json
{
  "id": "uuid",
  "col": 2,
  "row": 3,
  "hex_type": "Otevřená krajina",
  "category": "Myší osada",
  "detail": "...",
  "hook": "...",
  "is_discovered": true,
  "discovered_at": "2025-11-03T15:00:00Z",
  "settlements": [...],
  "dungeons": [...],
  "npcs": [...]
}
```

---

### Bulk Create Hexes

**Endpoint:** `POST /api/v1/campaigns/{campaign_id}/hexes/bulk`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "hexes": [
    {
      "col": 0,
      "row": 0,
      "generated_data": {...}
    }
    // ... 24 more
  ]
}
```

---

### Update Hex

**Endpoint:** `PUT /api/v1/hexes/{id}`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "is_discovered": true,
  "discovered_by": "uuid",
  "notes": "Players found hidden cave"
}
```

---

## 🏘️ Settlements

### List Settlements

**Endpoint:** `GET /api/v1/campaigns/{campaign_id}/settlements`

**Auth:** Required (GM or player)

**Query Parameters:**
- `discovered_only`: `true`

**Response:**
```json
{
  "settlements": [
    {
      "id": "uuid",
      "name": "Mlýnov",
      "size": "Víska",
      "hex_id": "uuid",
      "is_discovered": true
    }
  ]
}
```

---

### Get Settlement

**Endpoint:** `GET /api/v1/settlements/{id}`

**Response:** Full settlement object

---

### Create Settlement

**Endpoint:** `POST /api/v1/campaigns/{campaign_id}/settlements`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "hex_id": "uuid",          // Optional
  "generated_data": {...}
}
```

---

### Update Settlement

**Endpoint:** `PUT /api/v1/settlements/{id}`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "attitude": "friendly",
  "notes": "Players saved the settlement from rats"
}
```

---

### Delete Settlement

**Endpoint:** `DELETE /api/v1/settlements/{id}`

**Auth:** Required (GM only)

---

## 🏛️ Dungeons

Similar structure to Settlements:

- `GET /api/v1/campaigns/{campaign_id}/dungeons`
- `GET /api/v1/dungeons/{id}`
- `POST /api/v1/campaigns/{campaign_id}/dungeons`
- `PUT /api/v1/dungeons/{id}`
- `DELETE /api/v1/dungeons/{id}`

**Additional Endpoints:**

### Mark Dungeon Room as Explored

**Endpoint:** `POST /api/v1/dungeons/{id}/explore`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "room_index": 2  // 0-based index
}
```

---

### Mark Dungeon as Cleared

**Endpoint:** `POST /api/v1/dungeons/{id}/clear`

**Auth:** Required (GM only)

---

## 👥 NPCs

Similar structure to Characters:

- `GET /api/v1/campaigns/{campaign_id}/npcs`
- `GET /api/v1/npcs/{id}`
- `POST /api/v1/campaigns/{campaign_id}/npcs`
- `PUT /api/v1/npcs/{id}`
- `DELETE /api/v1/npcs/{id}`

**Additional Endpoints:**

### Add NPC Interaction

**Endpoint:** `POST /api/v1/npcs/{id}/interactions`

**Auth:** Required (GM only)

**Request Body:**
```json
{
  "summary": "Players asked for directions",
  "reaction": "Povídavá"
}
```

---

## 📜 Rumors

Similar structure:

- `GET /api/v1/campaigns/{campaign_id}/rumors`
- `GET /api/v1/rumors/{id}`
- `POST /api/v1/campaigns/{campaign_id}/rumors`
- `PUT /api/v1/rumors/{id}`
- `DELETE /api/v1/rumors/{id}`

**Additional Endpoints:**

### Mark Rumor as Heard

**Endpoint:** `POST /api/v1/rumors/{id}/hear`

**Auth:** Required (GM or player)

**Request Body:**
```json
{
  "heard_by": "uuid"  // Player user ID
}
```

---

## 📖 Sessions

- `GET /api/v1/campaigns/{campaign_id}/sessions`
- `GET /api/v1/sessions/{id}`
- `POST /api/v1/campaigns/{campaign_id}/sessions`
- `PUT /api/v1/sessions/{id}`
- `DELETE /api/v1/sessions/{id}`

---

## 🎲 Dice Rolls

### Get Dice Roll History

**Endpoint:** `GET /api/v1/campaigns/{campaign_id}/dice-rolls`

**Auth:** Required (campaign member)

**Query Parameters:**
- `session_id`: Filter by session
- `limit`: Max results (default 50)

**Response:**
```json
{
  "rolls": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "username": "Player1",
      "dice_type": "d20",
      "result": 15,
      "reason": "STR test",
      "created_at": "2025-11-03T16:00:00Z"
    }
  ]
}
```

---

### Record Dice Roll

**Endpoint:** `POST /api/v1/campaigns/{campaign_id}/dice-rolls`

**Auth:** Required (campaign member)

**Request Body:**
```json
{
  "dice_type": "2d6",
  "result": 9,
  "reason": "Reaction roll",
  "character_id": "uuid"   // Optional
}
```

---

## 🔧 Utilities

### Health Check

**Endpoint:** `GET /health`

**Auth:** Not required

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T10:00:00Z",
  "version": "1.0.0"
}
```

**Testing with curl:**
```bash
# Check API health
curl http://localhost:8001/health

# With pretty-print
curl http://localhost:8001/health | python -m json.tool
```

---

### Generator Status

**Endpoint:** `GET /api/v1/generate/status`

**Auth:** Not required

**Response:**
```json
{
  "total_generators": 17,
  "implemented": 17,
  "status": "All generators operational",
  "generators": [...],
  "creature_types": ["ghost", "snake", "cat", "rat", "mouse", "spider", "owl", "centipede", "fairy", "crow", "frog"]
}
```

**Testing with curl:**
```bash
# Get generator status
curl http://localhost:8001/api/v1/generate/status

# With pretty-print
curl http://localhost:8001/api/v1/generate/status | python -m json.tool
```

---

### API Documentation

**Endpoint:** `GET /docs`

**Auth:** Not required

**Response:** Swagger UI (FastAPI auto-generated)

---

### OpenAPI Schema

**Endpoint:** `GET /openapi.json`

**Auth:** Not required

**Response:** OpenAPI 3.0 schema

---

## 📝 Error Responses

### Standard Error Format

All errors return:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Character name is required",
    "details": {
      "field": "name",
      "constraint": "required"
    }
  }
}
```

### Common Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| `UNAUTHORIZED` | 401 | Missing or invalid auth token |
| `FORBIDDEN` | 403 | Not allowed to access resource |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `INVALID_REQUEST` | 400 | Invalid request body/params |
| `CONFLICT` | 409 | Resource already exists |
| `INTERNAL_ERROR` | 500 | Server error |

---

## 🔄 Rate Limiting

**Free Tier Limits:**
- 100 requests/minute per user
- 1000 requests/hour per user

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699012800
```

---

## 📊 Pagination

For list endpoints (e.g., `/api/v1/campaigns`):

**Query Parameters:**
- `page`: Page number (default 1)
- `per_page`: Items per page (default 20, max 100)

**Response Headers:**
```
X-Total-Count: 150
X-Page: 1
X-Per-Page: 20
X-Total-Pages: 8
Link: <url?page=2>; rel="next", <url?page=8>; rel="last"
```

---

## 🔗 Related Documents

- [WEB_ARCHITECTURE.md](WEB_ARCHITECTURE.md) - Tech stack
- [DATABASE_SCHEMA.sql](DATABASE_SCHEMA.sql) - Database structure
- [WEB_ROADMAP.md](WEB_ROADMAP.md) - Implementation plan

---

**Last updated:** 2025-11-04
**Next review:** After MVP implementation
