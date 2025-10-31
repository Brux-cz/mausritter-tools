# Mausritter Tools - Roadmap

Tento dokument obsahuje plán budoucího vývoje projektu Mausritter Tools.

## 📋 Legenda

- ✅ **Hotovo** - Implementováno a otestováno
- 🚧 **Probíhá** - Aktuálně se pracuje
- 📝 **Naplánováno** - Připraveno k implementaci
- 💡 **Nápad** - Zatím jen koncept

---

## ✅ Fáze 1: Data Extraction (HOTOVO)

**Stav:** Dokončeno ✅
**Datum:** 2025-01

### Co bylo vytvořeno:
- Extrakce dat z 21 markdown souborů v `docs/knowledge_base/`
- 13 JSON tabulek v `data/core/`
- TableLoader systém s LRU cache
- 0 chyb při kontrole

### Soubory:
- `src/core/tables.py` - TableLoader s lookup metodami
- `data/core/*.json` - 13 JSON tabulek (origins, names, birthsigns, atd.)

---

## ✅ Fáze 2: Character Generator (HOTOVO)

**Stav:** Dokončeno ✅
**Datum:** 2025-01

### Co bylo vytvořeno:
- Generátor náhodných myších postav
- CLI příkazy pro generování
- Podpora JSON exportu
- Rodná znamení a barvy srsti
- 16 testů (všechny prošly ✅)

### Příkazy:
```bash
python -m src.cli generate character
python -m src.cli generate character --name "Pepřík"
python -m src.cli generate character --gender female
python -m src.cli generate character --json
python -m src.cli generate character --save postava.json
```

### Soubory:
- `src/generators/character.py` - CharacterGenerator
- `src/cli.py` - CLI rozhraní s display_character()
- `tests/test_character_generator.py` - 16 testů

### Rozšíření v rámci Fáze 2A:
- ✅ Rodná znamení (k6 tabulka)
- ✅ Barvy srsti (k6 tabulka)
- ✅ Vzory srsti (k6 tabulka)
- ✅ Zobrazení v CLI
- ✅ Aktualizované testy

---

## 📖 Oficiální Mausritter Generátory z Pravidel

Tento přehled obsahuje **všechny náhodné generátory a tabulky** z oficiálních Mausritter pravidel (nalezeno v `docs/knowledge_base/`). Pomáhá identifikovat, co by mělo být v projektu implementováno, aby pokrýval celý systém.

### 🎯 Legenda priorit

- **P1 (Priorita 1):** 🔴 Základní nástroje pro PJ - používají se často během hry
- **P2 (Priorita 2):** 🟡 Důležité nástroje pro tvorbu světa - používají se při přípravě kampaně
- **P3 (Priorita 3):** 🟢 Volitelné varianty - přidávají rozmanitost a atmosféru

**Status:** ✅ Hotovo | 🚧 Probíhá | 📝 Naplánováno | 💡 Nápad

---

### P1: Základní PJ nástroje (8 generátorů) 🔴

Tyto generátory jsou **nejdůležitější** pro vedení hry. Používají se průběžně během herních sezení.

#### 1. ✅ Generátor myších postav
**Název:** Character Generator / Generátor myších dobrodruhů
**Popis:** Kompletní tvorba hráčských postav včetně vlastností, pozadí, vzhledu, vybavení
**Zdroj:** `02_CHARACTER_CREATION.md`
**Složitost:** ⭐⭐⭐ Střední
**Stav:** ✅ **HOTOVO** - Fáze 2 + 2A + 2B
**Tabulky:** origins, names, birthsigns, coat_colors/patterns, distinctive_traits, weapons

#### 2. 📝 Generátor NPC myší
**Název:** NPC Generator / Generátor nehráčských myší
**Popis:** Rychlé vytváření NPC - společenské postavení, vzhled, zvláštnosti, touhy, vztahy
**Zdroj:** `16_RANDOM_TABLES.md` (řádky 15-140)
**Složitost:** ⭐⭐ Jednoduchá
**Tabulky:** Společenské postavení (k6), Rodné znamení (k6), Vzhled (k20), Zvláštnost (k20), Po čem touží (k20), Vztah (k20)
**Priorita:** Vysoká - podobné Character Generatoru, ale rychlejší

#### 3. 📝 Generátor počasí
**Název:** Weather Generator / Generátor počasí a sezónních událostí
**Popis:** Určení počasí (2k6) podle ročního období + sezónní události (k6)
**Zdroj:** `16_RANDOM_TABLES.md` (řádky 194-293)
**Složitost:** ⭐ Velmi jednoduchá
**Tabulky:** Jaro/Léto/Podzim/Zima - každé má počasí (2k6) + události (k6)
**Priorita:** Střední - rychlá implementace, používá se denně v hexcrawl

#### 4. 📝 Tabulka reakcí
**Název:** Reaction Roll / Tabulka reakcí tvorů
**Popis:** Určení nálady tvora při setkání (2k6)
**Zdroj:** `08_GM_GUIDE.md` (řádky 213-224)
**Složitost:** ⭐ Velmi jednoduchá
**Tabulka:** 2k6 - Agresivní (2), Nepřátelská (3-5), Nejistá (6-8), Povídavá (9-11), Nápomocná (12)
**Priorita:** Vysoká - používá se v každém setkání

#### 5. 📝 Generátor pokladů
**Název:** Treasure Generator / Generátor pokladů
**Popis:** Určení obsahu pokladu - ďobky, předměty, kouzelné meče, kouzla
**Zdroj:** `15_TREASURE.md` (řádky 17-115)
**Složitost:** ⭐⭐⭐ Střední až složitá
**Tabulky:** Hlavní (k20), Drobnosti (k6), Cenný (k6), Objemný (k6), Neobvyklý (k6), Užitečný (k6), Meče + Kouzla
**Priorita:** Vysoká - důležité pro odměňování hráčů

#### 6. 📝 Generátor kouzelných mečů
**Název:** Magic Sword Generator / Generátor kouzelných mečů
**Popis:** Typ zbraně (k6), schopnost (k10), šance na prokletí (1/6), typ kletby (k6)
**Zdroj:** `15_TREASURE.md` (řádky 118-216)
**Složitost:** ⭐⭐ Střední
**Tabulky:** Typ (k6), 10 druhů mečů, Prokletí (k6)
**Priorita:** Střední - součást Treasure Generatoru

#### 7. 📝 Generátor semínek dobrodružství
**Název:** Adventure Seeds / Generátor semínek dobrodružství
**Popis:** Kombinace Tvor + Problém + Komplikace (k66 tabulka)
**Zdroj:** `16_RANDOM_TABLES.md` (řádky 143-191)
**Složitost:** ⭐⭐ Střední
**Tabulka:** k66 (36 kombinací)
**Priorita:** Střední - inspirace pro PJ při tvorbě questů

#### 8. 📝 Generátor kouzel
**Název:** Spell Generator / Generátor náhodných kouzel
**Popis:** Náhodné kouzlo z tabulky (2k8 na 16 kouzel)
**Zdroj:** `06_MAGIC.md` (řádky 83-107)
**Složitost:** ⭐ Velmi jednoduchá
**Tabulka:** 2k8 - 16 kouzel
**Priorita:** Střední - náhodné nalezení kouzel

---

### P2: Nástroje pro tvorbu světa (6 generátorů) 🟡

Tyto generátory se používají **při přípravě kampaně** a tvorby hexcrawl mapy.

#### 9. 📝 Generátor myších osad
**Název:** Settlement Generator / Generátor myších osad
**Popis:** Velikost, společenské zřízení, podrobnosti, živnost, výrazné prvky, události, název
**Zdroj:** `12_SETTLEMENTS.md` (řádky 22-237)
**Složitost:** ⭐⭐⭐ Střední
**Tabulky:** Velikost (2k6 nižší), Zřízení (k6+velikost), Podrobnosti (k20), Živnost (k20), Prvky (k20), Události (k20), Název (4×k12)
**Priorita:** Vysoká - klíčové pro hexcrawl

#### 10. 📝 Generátor hospod a hostinců
**Název:** Tavern Generator / Generátor hospod
**Popis:** Název hospody (2×k12), specialita hostince (k12)
**Zdroj:** `12_SETTLEMENTS.md` (řádky 240-296)
**Složitost:** ⭐ Velmi jednoduchá
**Tabulky:** Část 1 (k12), Část 2 (k12), Specialita (k12)
**Priorita:** Nízká - doplněk Settlement Generatoru

#### 11. 📝 Generátor hexů
**Název:** Hex Generator / Generátor obsahu hexů
**Popis:** Typ hexu (k6), výrazný prvek, detaily (k6+k8)
**Zdroj:** `11_HEXCRAWL_SETUP.md` (řádky 93-160)
**Složitost:** ⭐⭐⭐ Střední
**Tabulky:** Typ hexu (k6), Detaily výrazných prvků (k6 pak k8 - 48 možností)
**Priorita:** Střední - důležité pro hexcrawl kampaně

#### 12. 📝 Generátor dobrodružných míst (Dungeon)
**Název:** Dungeon/Adventure Site Generator / Generátor dobrodružných míst
**Popis:** Téma místa (minulost + chátrání), obyvatelé, tajemství, místnosti
**Zdroj:** `14_DUNGEON_CREATION.md` (řádky 69-268)
**Složitost:** ⭐⭐⭐⭐ Složitá
**Tabulky:** Minulost budovy (k20), Chátrání (k12), Obyvatelé-bytosti (k10), Obyvatelé-co hledají (k8), Tajemství (k6), Místnosti (3×k6), Prázdné (k20), Překážky (k8), Pasti (k8), Hlavolamy (k6), Doupata (k6)
**Priorita:** Vysoká - klíčové pro tvorbu dungeonů

#### 13. 📝 Generátor háčků dobrodružství
**Název:** Adventure Hook Generator / Generátor háčků
**Popis:** Důvod, proč se myši vydají na dobrodružství (k6)
**Zdroj:** `11_HEXCRAWL_SETUP.md` (řádky 66-75)
**Složitost:** ⭐ Velmi jednoduchá
**Tabulka (k6):** Ztracený člen rodiny, Vyšetřování, Přísada, Doupě, Mapa, Útočiště
**Priorita:** Nízká - doplněk pro první sezení

#### 14. 📝 Framework zvěstí
**Název:** Rumor Generator / Framework pro tvorbu zvěstí
**Popis:** Návod na tvorbu tabulky k6 zvěstí (pravdivé 1-3, částečně 4-5, nepravdivé 6)
**Zdroj:** `11_HEXCRAWL_SETUP.md` (řádky 43-50)
**Složitost:** ⭐⭐ Střední
**Priorita:** Nízká - spíš framework než konkrétní generátor

---

### P3: Varianty tvorů (14 generátorů) 🟢

Tyto generátory **přidávají rozmanitost** do setkání s tvory. Jsou volitelné, ale zvyšují atmosféru.

#### 15-28. 💡 Creature Variant Generators
**Popis:** Varianty pro různé typy tvorů - každý má tabulku k6
**Zdroj:** `09_CREATURES.md` (různé sekce)
**Složitost:** ⭐ Velmi jednoduchá (každý)
**Priorita:** Nízká - flavor pro jednotlivé tvory

**Seznam:**
- Přízračné schopnosti duchů (k6) - Ghost Abilities
- Zvláštní hadi (k6) - Snake Types
- Kočičí pánové (k6) - Cat Lords
- Krysí gangy (k6) - Rat Gangs
- Konkurenční myši (k6) - Rival Mice
- Druhy pavouků (k6) - Spider Types
- Soví čarodějové (k6) - Owl Wizards
- Zevlující stonožky (k6) - Centipede Types
- Vílí plány (k6) - Fairy Schemes
- Vraní písně (k6) - Crow Songs
- Žabí rytíři (k6) - Frog Knights
- Pomocníci dostupnost (různé) - Hireling Availability
- (+další creature specifics)

---

## 📊 Souhrn: Oficiální generátory

### Celkem identifikováno: **28 generátorů** z oficiálních pravidel

| Priorita | Počet | Hotovo | Zbývá | Popis |
|----------|-------|--------|-------|-------|
| **P1 🔴** | 8 | 1 ✅ | 7 📝 | Základní PJ nástroje - nutné pro hru |
| **P2 🟡** | 6 | 0 ✅ | 6 📝 | Nástroje pro tvorbu světa - důležité pro kampaň |
| **P3 🟢** | 14 | 0 ✅ | 14 💡 | Varianty tvorů - volitelné, ale atmosférické |
| **CELKEM** | **28** | **1** | **27** | |

### 🎯 Doporučené pořadí implementace (podle priorit z pravidel)

**Fáze 3 - Základní PJ nástroje (P1):**
1. ✅ Character Generator (HOTOVO)
2. 📝 NPC Generator - podobný Character Gen, rychlá implementace
3. 📝 Treasure Generator - důležité pro odměny
4. 📝 Weather Generator - velmi jednoduché, denní použití
5. 📝 Reaction Roll - velmi jednoduché, časté použití
6. 📝 Magic Sword Generator - součást Treasure Gen
7. 📝 Adventure Seeds - inspirace pro PJ
8. 📝 Spell Generator - velmi jednoduché

**Fáze 4 - Tvorba světa (P2):**
9. 📝 Settlement Generator - klíčové pro hexcrawl
10. 📝 Hex Generator - pro hexcrawl kampaně
11. 📝 Dungeon Generator - složitější, ale důležité
12. 📝 Tavern Generator - doplněk Settlement Gen
13. 📝 Adventure Hooks - jednoduché, session starters
14. 📝 Rumor Framework - framework pro zvěsti

**Fáze 5 - Flavor & Rozmanitost (P3):**
15-28. 💡 Creature Variants - všechny varianty tvorů

---

## 📝 Budoucí vývoj

### B: Settlement Generator (Generátor sídel)

**Priorita:** 🔴 Vysoká
**Čas:** ~4 hodiny
**Stav:** 💡 Nápad

**Popis:**
Generátor náhodných myších osad/vesnic podle Mausritter pravidel.

**Co implementovat:**
1. **Data a tabulky** (1 hod)
   - `data/settlements/settlement_types.json` - Typy sídel (vesnice, měřič, předsunutá základna)
   - `data/settlements/settlement_features.json` - Rysy sídel
   - `data/settlements/settlement_problems.json` - Problémy sídla
   - Rozšířit `TableLoader` o settlement lookup metody

2. **Generátor** (2 hod)
   - `src/generators/settlement.py` - SettlementGenerator
   - Metody: `generate_type()`, `generate_features()`, `generate_population()`, `create()`
   - Model: `src/core/models.py` - Settlement dataclass

3. **CLI příkaz** (30 min)
   - `python -m src.cli generate settlement`
   - `--json` a `--save` podpora
   - Pěkné zobrazení s Rich formátováním

4. **Testy** (30 min)
   - `tests/test_settlement_generator.py`
   - Test všech lookup metod
   - Test create() s validací

**Zdroje dat:**
- `docs/knowledge_base/05_SETTLEMENTS.md` - pokud existuje
- Oficiální Mausritter pravidla

**Příklad výstupu:**
```
┌─────────── Mlýnská Víska ───────────┐
│  Typ: Vesnice                       │
│  Populace: 45 myší                  │
│  Rysy:                              │
│    - Mlýn na vodní kolo             │
│    - Tržiště                        │
│  Problém:                           │
│    - Krysy z lesa obtěžují osadníky│
└─────────────────────────────────────┘
```

---

### C: Hex Generator (Generátor hexů)

**Priorita:** 🟡 Střední
**Čas:** ~6 hodin
**Stav:** 💡 Nápad

**Popis:**
Generátor náhodných hexů pro hex-crawl mapy podle Mausritter pravidel.

**Co implementovat:**
1. **Data a tabulky** (1.5 hod)
   - `data/hexes/terrain_types.json` - Typy terénu (les, louka, bažina, atd.)
   - `data/hexes/hex_features.json` - Zajímavé prvky hexu
   - `data/hexes/encounters.json` - Možná setkání v hexu
   - `data/hexes/weather.json` - Základní počasí

2. **Generátor** (3 hod)
   - `src/generators/hex.py` - HexGenerator
   - Metody: `generate_terrain()`, `generate_features()`, `generate_encounter()`, `create()`
   - Model: `src/core/models.py` - Hex dataclass
   - Podpora hex souřadnic (column, row)

3. **CLI příkaz** (1 hod)
   - `python -m src.cli generate hex`
   - `python -m src.cli generate hex --coords 0501` (column 05, row 01)
   - `--count 10` - Vygeneruj 10 hexů najednou
   - `--json` export

4. **Testy** (30 min)
   - `tests/test_hex_generator.py`

**Rozšíření (budoucnost):**
- Generování celých map (např. 10×10 hexů)
- Export do SVG/PNG
- Integrace s Settlement Generatorem

**Zdroje dat:**
- `docs/knowledge_base/` - hledej hex-related pravidla
- Mausritter Adventure Site kit

---

### D: Weather Generator (Generátor počasí)

**Priorita:** 🟢 Nízká
**Čas:** ~2 hodiny
**Stav:** 💡 Nápad

**Popis:**
Generátor náhodného počasí pro herní sezení.

**Co implementovat:**
1. **Data** (30 min)
   - `data/weather/conditions.json` - Podmínky (slunečno, déšť, vítr, sníh)
   - `data/weather/seasons.json` - Roční období (jaro, léto, podzim, zima)
   - `data/weather/events.json` - Speciální události (bouře, mlha, atd.)

2. **Generátor** (1 hod)
   - `src/generators/weather.py` - WeatherGenerator
   - Metody: `generate_condition()`, `generate_event()`, `create()`
   - Seasonal modifiers (jiné pravděpodobnosti v zimě vs. létě)

3. **CLI** (20 min)
   - `python -m src.cli generate weather`
   - `--season spring/summer/autumn/winter`

4. **Testy** (10 min)
   - `tests/test_weather_generator.py`

**Možná integrace:**
- Hex Generator může volat Weather Generator

---

### E: NPC Quick Generator (Rychlý NPC generátor)

**Priorita:** 🔴 Vysoká
**Čas:** ~3 hodiny
**Stav:** 💡 Nápad

**Popis:**
Rychlý generátor NPC myší (non-player characters) pro DM.

**Co implementovat:**
1. **Data** (1 hod)
   - `data/npcs/npc_traits.json` - Povahové rysy (k66 tabulka)
   - `data/npcs/npc_quirks.json` - Zvláštnosti (k20 tabulka)
   - `data/npcs/npc_goals.json` - Cíle NPC (k20 tabulka)
   - `data/npcs/npc_occupations.json` - Povolání (k100 tabulka?)

2. **Generátor** (1.5 hod)
   - `src/generators/npc.py` - NPCGenerator
   - **Rychlý režim:** Jen jméno + 1 rys + 1 cíl (pro náhodná setkání)
   - **Detailní režim:** Jméno + vlastnosti + rys + cíl + povolání + majetek
   - Model: `src/core/models.py` - NPC dataclass

3. **CLI** (30 min)
   - `python -m src.cli generate npc` - rychlý režim
   - `python -m src.cli generate npc --detailed` - detailní
   - `python -m src.cli generate npc --count 5` - 5 NPC najednou (pro DM prep)

**Rozdíl oproti Character Generator:**
- Character Generator = hráčské postavy (full stats, HP, inventář)
- NPC Generator = rychlé NPC pro DM (jen potřebné info)

---

### F: Documentation & Quality of Life

**Priorita:** 🟡 Střední
**Čas:** Průběžně
**Stav:** 📝 Naplánováno

**Co zlepšit:**

1. **README rozšíření** (30 min)
   - Animované GIF s demo použití
   - Screenshoty CLI výstupů
   - FAQ sekce
   - "Jak přispět" sekce

2. **Manuál rozšíření** (1 hod)
   - `docs/MANUAL.md` - Přidat sekci "Příklady workflow"
   - Přidat sekci "Jak fungují tabulky"
   - Tutorial: "Jak přidat vlastní tabulku"

3. **Vývojářská dokumentace** (1 hod)
   - `docs/DEVELOPMENT.md` - Architektura projektu
   - `docs/CONTRIBUTING.md` - Contributing guide
   - Diagramy architektury (Python modules dependencies)

4. **Automatizace** (2 hod)
   - GitHub Actions CI/CD pipeline
   - Automatické spouštění testů
   - Automatické formátování (black, isort)
   - Linting (ruff)

5. **Package distribution** (2 hod)
   - Vytvořit `pyproject.toml` pro Poetry/setuptools
   - Publikovat na PyPI
   - Umožnit instalaci: `pip install mausritter-tools`
   - Přejmenovat CLI: `mausritter` místo `python -m src.cli`

---

### G: Web Interface (Webové rozhraní)

**Priorita:** 🟢 Nízká
**Čas:** ~15 hodin
**Stav:** 💡 Nápad

**Popis:**
Webová aplikace pro generování postav a dalších věcí bez nutnosti CLI.

**Technologie:**
- **Backend:** FastAPI (Python) - využít existující kód z `src/`
- **Frontend:** HTML + CSS + Vanilla JS (nebo HTMX pro jednoduchost)
- **Styling:** Tailwind CSS nebo custom CSS s myším motivem

**Co implementovat:**

1. **Backend API** (6 hod)
   - `src/web/app.py` - FastAPI aplikace
   - Endpoints:
     - `GET /` - Homepage
     - `POST /api/character/generate` - Generuj postavu (JSON response)
     - `POST /api/settlement/generate` - Generuj sídlo
     - `POST /api/hex/generate` - Generuj hex
     - `POST /api/npc/generate` - Generuj NPC
   - Swagger UI dokumentace (`/docs`)

2. **Frontend** (8 hod)
   - `src/web/static/` - HTML/CSS/JS
   - Stránky:
     - Homepage - výběr generátoru
     - Character Generator page - formulář + preview
     - Settlement Generator page
     - Hex Generator page
     - NPC Generator page
   - Features:
     - Live preview výsledků
     - Export do JSON
     - Export do PDF (pomocí WeasyPrint?)
     - Možnost "re-roll" jednotlivých částí (jméno, vlastnosti, atd.)
     - Uložení do localStorage (bez DB)

3. **Deploy** (1 hod)
   - Docker containerizace
   - Deploy na Render.com nebo Railway.app (free tier)
   - Nebo Vercel/Netlify pro frontend + Cloudflare Workers pro API

**Mockup UI:**
```
┌─────────────────────────────────────────┐
│  MAUSRITTER TOOLS                       │
│  [Character] [Settlement] [Hex] [NPC]   │
├─────────────────────────────────────────┤
│  Character Generator                    │
│                                         │
│  Name: [          ] [Random]            │
│  Gender: (•) Male ( ) Female            │
│                                         │
│  [Generate Character]                   │
│                                         │
│  ┌────── Result ──────┐                 │
│  │ Pepřík Hrabal      │                 │
│  │ ⭐ Stěnolezec      │                 │
│  │ STR: 8 DEX: 11...  │                 │
│  └────────────────────┘                 │
│  [Download JSON] [Re-roll]              │
└─────────────────────────────────────────┘
```

---

## 🎯 Doporučené pořadí implementace

Pokud chceš pokračovat efektivně:

1. **Krátkodobě (příštích pár týdnů):**
   - ✅ Fáze 2A: Rozšířit Character Generator (HOTOVO!)
   - 📝 **E: NPC Quick Generator** - užitečné pro DM, podobné Character Generatoru
   - 📝 **B: Settlement Generator** - často potřebné v kampani

2. **Střednědobě (1-2 měsíce):**
   - 📝 **C: Hex Generator** - užitečné pro hex-crawl kampaně
   - 📝 **D: Weather Generator** - rychlá doplňková feature
   - 📝 **F: Documentation & QoL** - zlepšit UX, připravit pro publikaci

3. **Dlouhodobě (3+ měsíce):**
   - 📝 **G: Web Interface** - velký projekt, ale dá se ukázat ostatním hráčům
   - 📝 Další generátory dle potřeby (Treasures, Spells, Adventures, atd.)

---

## 💡 Další nápady (backlog)

Nápady, které zatím nejsou v hlavním roadmap:

- **Treasure Generator** - Generování pokladů a předmětů
- **Spell Generator** - Náhodné kouzla (pokud má Mausritter magie)
- **Encounter Generator** - Generování soubojových encounter
- **Adventure Generator** - Celá mini-dobrodružství
- **Faction Generator** - Generování frakcí a organizací
- **Dungeon Generator** - Generování podzemí/dutin
- **Name Generator (standalone)** - Jen rychlé generování jmen
- **Dice Bot Discord/Telegram** - Bot pro hraní přes Discord
- **Character Sheet PDF Export** - Export do official character sheet PDF
- **Campaign Manager** - Sledování kampaně, postav, sídel, atd.
- **Interactive Maps** - Hex mapy s klikáním a zoom

---

## 📊 Aktuální stav projektu

**Celková dokončenost:** ~20%

| Feature               | Status | Progress |
|-----------------------|--------|----------|
| Data Extraction       | ✅     | 100%     |
| Character Generator   | ✅     | 100%     |
| Settlement Generator  | 💡     | 0%       |
| Hex Generator         | 💡     | 0%       |
| Weather Generator     | 💡     | 0%       |
| NPC Generator         | 💡     | 0%       |
| Documentation         | 🚧     | 60%      |
| Web Interface         | 💡     | 0%       |

---

## 🤝 Jak přispět

Pokud chceš přidat novou feature:

1. Zkontroluj tento roadmap - možná už je naplánovaná
2. Otevři issue na GitHubu s popisem
3. Diskutuj implementaci
4. Vytvoř pull request

---

**Poslední aktualizace:** 2025-01
**Autor:** Claude Code + uživatel

---

## 📝 Changelog

### 2025-01-XX - Fáze 2A dokončena
- ✅ Přidána rodná znamení (birthsigns)
- ✅ Přidány barvy srsti (coat colors)
- ✅ Přidány vzory srsti (coat patterns)
- ✅ Aktualizovány testy (16 testů, všechny prošly)
- ✅ Vytvořen ROADMAP.md

### 2025-01-XX - Fáze 2 dokončena
- ✅ Implementován CharacterGenerator
- ✅ CLI příkazy pro generování postav
- ✅ JSON export
- ✅ 12 testů (všechny prošly)
- ✅ README.md a MANUAL.md dokumentace

### 2025-01-XX - Fáze 1 dokončena
- ✅ Extrakce dat z 21 markdown souborů
- ✅ 13 JSON tabulek
- ✅ TableLoader systém
- ✅ 0 chyb
