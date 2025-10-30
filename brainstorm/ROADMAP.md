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
