# Implementation Plan - Mausritter Tools

**Verze:** 1.0
**Datum:** 2025-10-29
**Autor:** Claude & User
**Strategie:** Library-First, CLI, poté Web

---

## 📋 Obsah

1. [Current State](#current-state)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Implementation Phases](#implementation-phases)
5. [Timeline](#timeline)
6. [Success Metrics](#success-metrics)

---

## 🎯 Current State

### ✅ Co už máme

**Core Library (`src/core/`)**
- ✅ `dice.py` - Plně funkční dice roller
  - Všechny typy kostek (d4, d6, d8, d10, d12, d20, d66)
  - Advantage/Disadvantage mechaniky
  - Attribute tests (roll-under d20)
  - roll_3d6_keep_2() pro generování vlastností ✨ NOVÉ
- ✅ `models.py` - Datové třídy
  - Character, NPC, Item, Condition, Background, Location
- ✅ `tables.py` - TableLoader pro načítání JSON dat ✨ NOVÉ
  - Cachované načítání tabulek
  - Lookup funkce pro origins, names

**CLI Tool (`src/cli.py`)**
- ✅ Základní struktura s Click + Rich
- ✅ Fungující příkazy:
  - `mausritter roll <dice>` - hody kostkami
  - `mausritter test <attribute>` - testy vlastností
- ✅ Připravené skupiny:
  - `mausritter generate` (prázdná)
  - `mausritter tools` (prázdná)

**Infrastructure**
- ✅ pyproject.toml
- ✅ requirements.txt
- ✅ Projektová struktura
- ✅ Knowledge base (21 MD souborů s pravidly)

### ❌ Co chybí

**Generátory** (`src/generators/`)
- ❌ Character Generator
- ❌ Settlement Generator
- ❌ Hex Generator
- ❌ Weather Generator
- ❌ NPC Generator
- ❌ Dungeon Generator

**Data Files** (`data/`)
- ✅ Adresářová struktura vytvořena ✨ NOVÉ
- ✅ Origins table (36 položek) → data/core/origins.json ✨ NOVÉ
- ✅ Names table (100 jmen) → data/core/names_first.json ✨ NOVÉ
- ✅ Family names (20 příjmení) → data/core/names_family.json ✨ NOVÉ
- ❌ Birthsigns, coat colors/patterns (pro Fázi 2)
- ❌ Settlements tables
- ❌ Spells, Creatures, Equipment...

**Web Interface**
- ❌ FastAPI backend
- ❌ HTML frontend
- ❌ REST API

**Tests** (`tests/`)
- ✅ test_tableloader.py - Testy pro TableLoader ✨ NOVÉ
- ❌ Unit tests pro generátory
- ❌ Integration tests

---

## 🏗️ Architecture Overview

### Vrstvová architektura

```
┌─────────────────────────────────────────────────┐
│           USER INTERFACES                       │
├─────────────────────────────────────────────────┤
│  CLI Tool          │  Web Interface (Phase 4)   │
│  (Click + Rich)    │  (FastAPI + HTML)          │
├─────────────────────────────────────────────────┤
│           GENERATORS LAYER                      │
│  CharacterGen │ SettlementGen │ HexGen │ ...   │
├─────────────────────────────────────────────────┤
│           CORE LIBRARY                          │
│  Dice │ Models │ Tables │ Utils                 │
├─────────────────────────────────────────────────┤
│           DATA LAYER                            │
│  JSON tables loaded from data/                  │
└─────────────────────────────────────────────────┘
```

### Data Flow

```
1. User: mausritter generate character
           ↓
2. CLI: calls CharacterGenerator.create()
           ↓
3. Generator:
   - rolls 3d6 keep 2 for attributes (uses dice.py)
   - rolls d6 for HP
   - rolls d6 for pips
   - looks up origin in origins.json
   - selects starting equipment
           ↓
4. Returns: Character object (models.py)
           ↓
5. CLI: formats output with Rich
           ↓
6. User: sees beautiful formatted character
```

---

## 🔧 Technology Stack

### Confirmed (already in use)
- **Python**: 3.10+
- **Click**: CLI framework
- **Rich**: Terminal formatting
- **Dataclasses**: Data models

### Recommended additions
- **Pydantic**: Data validation (optional but recommended)
- **pytest**: Testing framework
- **FastAPI**: Web framework (Phase 4)
- **Jinja2**: HTML templates (Phase 4)
- **JSON**: Data storage format

### Not using
- ❌ Database (PostgreSQL/SQLite) - not needed, JSON is enough
- ❌ Frontend framework (React/Vue) - simple HTML + HTMX is enough
- ❌ Docker - not needed yet (maybe later)

---

## 🚀 Implementation Phases

---

### **FÁZE 1: Data Extraction** ✅ DOKONČENO

**Status:** ✅ **HOTOVO** (2025-10-29)

**Goal:** Převést všechny tabulky z knowledge_base/*.md do JSON formátu

**Duration:** 1-2 dny (dokončeno za 1 den)

**Priority:** HIGH (blokuje všechny generátory)

**Co bylo implementováno:**
- ✅ Vytvořena data/ struktura (core, creatures, magic, settlements)
- ✅ Extrahována Origins tabulka (36 původů) → data/core/origins.json
- ✅ Extrahována Names tabulka (100 jmen) → data/core/names_first.json
- ✅ Extrahována Family Names tabulka (20 příjmení) → data/core/names_family.json
- ✅ Vytvořena TableLoader třída → src/core/tables.py
- ✅ Přidána roll_3d6_keep_2() → src/core/dice.py
- ✅ Vytvořeny testy → test_tableloader.py (všechny prošly)

#### 1.1 Vytvoř data/ strukturu

```
data/
├── core/
│   ├── origins.json          # 36 původů (BO × Ďobky)
│   ├── names_first.json      # 100 jmen (k100)
│   ├── names_family.json     # 20 příjmení (k20)
│   ├── birthsigns.json       # 6 znamení (k6)
│   ├── coat_colors.json      # 6 barev (k6)
│   └── coat_patterns.json    # 6 vzorů (k6)
│
├── creatures/
│   └── creatures.json        # 12 tvorů + varianty
│
├── magic/
│   └── spells.json           # 16 kouzel (2k8)
│
├── settlements/
│   ├── sizes.json            # 6 velikostí
│   ├── governance.json       # Společenské zřízení
│   ├── details.json          # k20 podrobnosti
│   ├── trades.json           # k20 živností
│   ├── features.json         # k20 výrazných prvků
│   └── events.json           # k20 událostí
│
├── hexcrawl/
│   ├── hex_types.json        # k6 typů hexů
│   ├── details.json          # k6/k8 detailů
│   └── hooks.json            # k6 háčků
│
├── weather/
│   ├── spring.json           # 2k6 počasí + k6 události
│   ├── summer.json
│   ├── autumn.json
│   └── winter.json
│
└── equipment/
    ├── weapons.json
    ├── armor.json
    └── items.json
```

#### 1.2 Příklad Origins Table

**Source:** `docs/knowledge_base/02_CHARACTER_CREATION.md` (řádky 79-116)

**Target:** `data/core/origins.json`

```json
{
  "table_name": "Tabulka původů",
  "lookup_by": ["hp", "pips"],
  "entries": [
    {
      "hp": 1,
      "pips": 1,
      "origin": "Pokusná myš",
      "item_a": {
        "type": "spell",
        "name": "Kouzelná střela"
      },
      "item_b": {
        "type": "armor",
        "name": "Olověný plášť",
        "subtype": "heavy",
        "slots": 2
      }
    },
    {
      "hp": 1,
      "pips": 2,
      "origin": "Kuchyňský slídil",
      "item_a": {
        "type": "armor_and_shield",
        "name": "Štít a kabátec",
        "subtype": "light"
      },
      "item_b": {
        "type": "item",
        "name": "Hrnce"
      }
    }
    // ... všech 36 kombinací
  ]
}
```

#### 1.3 Script pro extrakci

**Vytvoř:** `scripts/extract_tables.py`

```python
"""
Script pro extrakci tabulek z knowledge base do JSON formátu
"""
import json
import re
from pathlib import Path

def extract_origins_table():
    """Extrahuje tabulku původů z 02_CHARACTER_CREATION.md"""
    kb_path = Path("docs/knowledge_base/02_CHARACTER_CREATION.md")

    # Parse markdown table (řádky 79-116)
    # ... logika parsování ...

    origins = {
        "table_name": "Tabulka původů",
        "lookup_by": ["hp", "pips"],
        "entries": []
    }

    # ... extract logic ...

    # Save
    output_path = Path("data/core/origins.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(origins, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_origins_table()
    # ... další tabulky ...
```

**Action Items:**
- [x] Vytvoř `data/` strukturu ✅
- [x] Extrahuj origins.json ✅
- [x] Extrahuj names_first.json ✅
- [x] Extrahuj names_family.json ✅
- [x] Vytvoř TableLoader class ✅
- [x] Validuj JSON (správný formát) ✅
- [ ] Vytvoř `scripts/extract_tables.py` (volitelné - můžeme udělat manuálně)
- [ ] Extrahuj ostatní core tables (birthsigns, coat colors/patterns) - pro Fázi 2
- [ ] Extrahuj creatures, spells, equipment tables - pro Fázi 3

---

### **FÁZE 2: Character Generator**

**Goal:** Plně funkční generátor postav s CLI

**Duration:** 3-5 dní

**Priority:** HIGH (nejdůležitější generátor)

#### 2.1 Vytvoř TableLoader

**File:** `src/core/tables.py`

```python
"""
Načítání a práce s JSON tabulkami
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from functools import lru_cache

class TableLoader:
    """Singleton pro načítání tabulek"""

    _instance = None
    _tables_cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    @lru_cache(maxsize=50)
    def load_table(table_path: str) -> Dict[str, Any]:
        """
        Načte JSON tabulku

        Args:
            table_path: Cesta relativní k data/ složce
                       např. "core/origins.json"
        """
        full_path = Path("data") / table_path
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_origins() -> Dict:
        """Načte tabulku původů"""
        return TableLoader.load_table("core/origins.json")

    @staticmethod
    def get_names() -> Dict:
        """Načte tabulku jmen"""
        first = TableLoader.load_table("core/names_first.json")
        family = TableLoader.load_table("core/names_family.json")
        return {"first": first, "family": family}

    # ... další helper metody ...
```

#### 2.2 Implementuj CharacterGenerator

**File:** `src/generators/character.py`

```python
"""
Generator myších postav
"""
from dataclasses import asdict
from typing import Optional, Dict, Any
from src.core.dice import roll_d6, roll_3d6_keep_2  # potřeba doplnit
from src.core.models import Character
from src.core.tables import TableLoader

class CharacterGenerator:
    """
    Generátor náhodných myších postav podle pravidel Mausritter
    """

    @staticmethod
    def roll_attributes() -> tuple[int, int, int]:
        """
        Hoď vlastnosti (3d6 keep highest 2, třikrát)

        Returns:
            (strength, dexterity, willpower)
        """
        # TODO: přidat roll_3d6_keep_2 do dice.py
        strength = roll_3d6_keep_2()
        dexterity = roll_3d6_keep_2()
        willpower = roll_3d6_keep_2()

        return strength, dexterity, willpower

    @staticmethod
    def determine_origin(hp: int, pips: int) -> Dict[str, Any]:
        """
        Najdi původ podle BO a ďobků

        Args:
            hp: Body ochrany (1-6)
            pips: Ďobky (1-6)

        Returns:
            Dictionary s informacemi o původu
        """
        origins_table = TableLoader.get_origins()

        # Najdi matching entry
        for entry in origins_table["entries"]:
            if entry["hp"] == hp and entry["pips"] == pips:
                return entry

        raise ValueError(f"Nenalezen původ pro HP={hp}, Pips={pips}")

    @staticmethod
    def generate_name() -> str:
        """
        Vygeneruj náhodné myší jméno

        Returns:
            "Jméno Příjmení" (např. "Pepřík Hrabal")
        """
        names = TableLoader.get_names()

        # Hoď k100 pro jméno
        first_roll = random.randint(1, 100)
        first_name = names["first"]["entries"][first_roll - 1]

        # Hoď k20 pro příjmení
        family_roll = random.randint(1, 20)
        family_name = names["family"]["entries"][family_roll - 1]

        return f"{first_name} {family_name}"

    @classmethod
    def create(cls,
               name: Optional[str] = None,
               swap_attributes: bool = False) -> Character:
        """
        Vytvoř kompletní náhodnou postavu

        Args:
            name: Volitelné vlastní jméno (jinak náhodné)
            swap_attributes: Povolit prohození dvou vlastností

        Returns:
            Vygenerovaná Character instance
        """
        # 1. Roll vlastnosti
        strength, dexterity, willpower = cls.roll_attributes()

        # 2. Roll HP a Pips
        hp = roll_d6()
        pips = roll_d6()

        # 3. Určit původ
        origin_data = cls.determine_origin(hp, pips)

        # 4. Generovat/použít jméno
        if name is None:
            name = cls.generate_name()

        # 5. Sestavit postavu
        character = Character(
            name=name,
            background=origin_data["origin"],
            strength=strength,
            dexterity=dexterity,
            willpower=willpower,
            max_hp=hp,
            current_hp=hp,
            # TODO: přidat starting equipment z origin_data
        )

        return character

    @staticmethod
    def to_dict(character: Character) -> Dict[str, Any]:
        """Konvertuj Character do dictionary"""
        return asdict(character)

    @staticmethod
    def to_json(character: Character) -> str:
        """Konvertuj Character do JSON"""
        import json
        return json.dumps(
            CharacterGenerator.to_dict(character),
            ensure_ascii=False,
            indent=2
        )
```

#### 2.3 Aktualizuj CLI

**File:** `src/cli.py`

```python
# ... existing imports ...
from src.generators.character import CharacterGenerator
from rich.panel import Panel
from rich.text import Text

@generate.command()
@click.option("--name", "-n", help="Vlastní jméno postavy")
@click.option("--json", "-j", is_flag=True, help="Výstup jako JSON")
@click.option("--save", "-s", type=click.Path(), help="Uložit do souboru")
def character(name: str, json: bool, save: str):
    """
    Vygeneruj náhodnou myší postavu

    Příklady:
        mausritter generate character
        mausritter generate character --name "Pepřík"
        mausritter generate character --json
        mausritter generate character --save postava.json
    """
    try:
        # Generuj postavu
        char = CharacterGenerator.create(name=name)

        if json:
            # JSON výstup
            output = CharacterGenerator.to_json(char)
            console.print(output)
        else:
            # Pěkný formátovaný výstup
            display_character(char)

        # Uložení do souboru
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(CharacterGenerator.to_json(char))
            console.print(f"\n[green]✓[/green] Uloženo do {save}")

    except Exception as e:
        console.print(f"[bold red]Chyba:[/bold red] {e}", style="red")
        import traceback
        traceback.print_exc()


def display_character(char: Character):
    """Zobraz postavu v pěkném formátu"""

    # Header
    title = Text(char.name, style="bold cyan", justify="center")
    subtitle = Text(f"⭐ {char.background}", style="dim", justify="center")

    # Vlastnosti s progress bary
    attrs = f"""
[bold]Vlastnosti:[/bold]
  Síla:      {char.strength:2d}  [{'█' * char.strength}{'░' * (20-char.strength)}]
  Mrštnost:  {char.dexterity:2d}  [{'█' * char.dexterity}{'░' * (20-char.dexterity)}]
  Vůle:      {char.willpower:2d}  [{'█' * char.willpower}{'░' * (20-char.willpower)}]

[bold]Zdraví:[/bold]
  BO: {char.current_hp}/{char.max_hp}

[bold]Původ:[/bold]
  {char.background}
"""

    panel = Panel(
        attrs,
        title=title,
        subtitle=subtitle,
        border_style="cyan",
        padding=(1, 2)
    )

    console.print(panel)
```

#### 2.4 Tests

**File:** `tests/test_character_generator.py`

```python
"""
Testy pro CharacterGenerator
"""
import pytest
from src.generators.character import CharacterGenerator
from src.core.models import Character

def test_roll_attributes():
    """Test že vlastnosti jsou v rozsahu 2-12"""
    str, dex, wil = CharacterGenerator.roll_attributes()

    assert 2 <= str <= 12
    assert 2 <= dex <= 12
    assert 2 <= wil <= 12

def test_determine_origin():
    """Test lookup v origins table"""
    origin = CharacterGenerator.determine_origin(hp=1, pips=1)

    assert origin["origin"] == "Pokusná myš"
    assert "item_a" in origin
    assert "item_b" in origin

def test_generate_name():
    """Test generování jména"""
    name = CharacterGenerator.generate_name()

    assert isinstance(name, str)
    assert " " in name  # Musí obsahovat mezeru (jméno + příjmení)

def test_create_character():
    """Test kompletní generování postavy"""
    char = CharacterGenerator.create()

    assert isinstance(char, Character)
    assert char.name
    assert char.background
    assert 2 <= char.strength <= 12
    assert 1 <= char.max_hp <= 6

def test_create_with_custom_name():
    """Test s vlastním jménem"""
    char = CharacterGenerator.create(name="Testovací Myš")

    assert char.name == "Testovací Myš"
```

**Action Items:**
- [ ] Přidat `roll_3d6_keep_2()` do dice.py
- [ ] Vytvořit `src/core/tables.py`
- [ ] Implementovat `src/generators/character.py`
- [ ] Aktualizovat CLI s `display_character()`
- [ ] Napsat testy
- [ ] Spustit `pytest` - vše musí projít
- [ ] Testovat ručně: `mausritter generate character`

---

### **FÁZE 3: Další Generátory**

**Duration:** 1-2 týdny (postupně)

**Priority:** MEDIUM

#### 3.1 Settlement Generator

**File:** `src/generators/settlement.py`

```python
class SettlementGenerator:
    """Generátor myších osad"""

    @staticmethod
    def determine_size() -> Dict:
        """Hoď 2k6, vezmi nižší"""
        # Implementace...

    @staticmethod
    def determine_governance(size_modifier: int) -> str:
        """k6 + velikost osady"""
        # Implementace...

    @classmethod
    def create(cls) -> Dict:
        """Vygeneruj kompletní osadu"""
        # Implementace...
```

**CLI:**
```bash
mausritter generate settlement
mausritter generate settlement --size village
```

#### 3.2 Hex Generator

**File:** `src/generators/hex.py`

```python
class HexGenerator:
    """Generátor hexů pro hexcrawl"""

    @staticmethod
    def generate_hex() -> Dict:
        """Vygeneruj náhodný hex"""
        # Typ hexu (k6)
        # Výrazný prvek (k6/k8)
        # Detail

    @staticmethod
    def generate_hexcrawl(width: int, height: int) -> List[List[Dict]]:
        """Vygeneruj celou mapu hexcrawlu"""
        # Implementace...
```

**CLI:**
```bash
mausritter generate hex
mausritter generate hexcrawl --size 5x5
```

#### 3.3 Weather Generator

**File:** `src/generators/weather.py`

```python
class WeatherGenerator:
    """Generátor počasí podle ročního období"""

    @staticmethod
    def roll_weather(season: str) -> Dict:
        """
        Hoď 2k6 pro počasí a k6 pro událost

        Args:
            season: "spring", "summer", "autumn", "winter"
        """
        # Implementace...
```

**CLI:**
```bash
mausritter generate weather --season spring
mausritter generate weather --season winter
```

#### 3.4 NPC Generator

**File:** `src/generators/npc.py`

```python
class NPCGenerator:
    """Generátor NPC myší"""

    @staticmethod
    def generate_npc() -> NPC:
        """Vygeneruj náhodnou NPC myš"""
        # Jméno
        # Znamení
        # Vzhled (k20)
        # Zvláštnost (k20)
        # Po čem touží (k20)
```

**Action Items (postupně):**
- [ ] Settlement generator + CLI + tests
- [ ] Hex generator + CLI + tests
- [ ] Weather generator + CLI + tests
- [ ] NPC generator + CLI + tests

---

### **FÁZE 4: Web Interface**

**Duration:** 1-2 týdny

**Priority:** LOW (bonus, není nutné)

#### 4.1 FastAPI Backend

**File:** `src/web/api.py`

```python
"""
REST API pro Mausritter Tools
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.generators.character import CharacterGenerator
from src.generators.settlement import SettlementGenerator

app = FastAPI(title="Mausritter Tools API")

@app.get("/")
async def root():
    """Homepage"""
    return HTMLResponse(content=open("src/web/templates/index.html").read())

@app.post("/api/character/generate")
async def generate_character(name: str | None = None):
    """
    Endpoint pro generování postav

    POST /api/character/generate?name=Pepřík
    """
    try:
        char = CharacterGenerator.create(name=name)
        return CharacterGenerator.to_dict(char)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/settlement/generate")
async def generate_settlement():
    """Endpoint pro generování osad"""
    settlement = SettlementGenerator.create()
    return settlement

# ... další endpoints ...
```

#### 4.2 Simple HTML Frontend

**File:** `src/web/templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mausritter Tools</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        #result {
            margin-top: 20px;
            padding: 20px;
            border: 2px solid #333;
            border-radius: 5px;
            background: #f9f9f9;
        }
    </style>
</head>
<body>
    <h1>🐭 Mausritter Tools</h1>

    <h2>Generátor Postav</h2>
    <input type="text" id="charName" placeholder="Jméno (volitelné)">
    <button onclick="generateCharacter()">Generuj Postavu</button>

    <h2>Generátor Osad</h2>
    <button onclick="generateSettlement()">Generuj Osadu</button>

    <div id="result"></div>

    <script>
        async function generateCharacter() {
            const name = document.getElementById('charName').value;
            const url = `/api/character/generate${name ? '?name=' + name : ''}`;

            const response = await fetch(url, { method: 'POST' });
            const data = await response.json();

            document.getElementById('result').innerHTML = `
                <h3>${data.name}</h3>
                <p><strong>Původ:</strong> ${data.background}</p>
                <p><strong>Síla:</strong> ${data.strength} |
                   <strong>Mrštnost:</strong> ${data.dexterity} |
                   <strong>Vůle:</strong> ${data.willpower}</p>
                <p><strong>BO:</strong> ${data.max_hp}</p>
            `;
        }

        async function generateSettlement() {
            const response = await fetch('/api/settlement/generate', { method: 'POST' });
            const data = await response.json();

            document.getElementById('result').innerHTML = `
                <h3>${data.name}</h3>
                <p><strong>Velikost:</strong> ${data.size}</p>
                <p><strong>Obyvatelé:</strong> ${data.population}</p>
                <!-- ... další data ... -->
            `;
        }
    </script>
</body>
</html>
```

#### 4.3 Spuštění

**File:** `src/web/run.py`

```python
"""
Spustí web server
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.web.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload při změnách
    )
```

**Usage:**
```bash
python src/web/run.py
# Otevři http://localhost:8000
```

**Action Items:**
- [ ] Implementovat FastAPI endpoints
- [ ] Vytvořit základní HTML frontend
- [ ] Testovat v prohlížeči
- [ ] (Volitelné) Nasadit na Render/Railway/Heroku

---

## 📅 Timeline

### Realistic Timeline (Full-time work)

| Fáze | Trvání | Kumulativní |
|------|--------|-------------|
| **Fáze 1: Data Extraction** | 1-2 dny | 2 dny |
| **Fáze 2: Character Generator** | 3-5 dní | 7 dní |
| **Fáze 3.1: Settlement Generator** | 2-3 dny | 10 dní |
| **Fáze 3.2: Hex Generator** | 2-3 dny | 13 dní |
| **Fáze 3.3: Weather Generator** | 1 den | 14 dní |
| **Fáze 3.4: NPC Generator** | 2 dny | 16 dní |
| **Fáze 4: Web Interface** | 3-5 dní | 21 dní |

**Total:** ~3 týdny (full-time)

### Part-time Timeline (2-3h/den)

| Fáze | Trvání |
|------|--------|
| **Fáze 1** | 3-4 dny |
| **Fáze 2** | 1-2 týdny |
| **Fáze 3** | 2-3 týdny |
| **Fáze 4** | 1 týden |

**Total:** ~6-8 týdnů

### Milestones

✅ **Milestone 1:** Data Extraction dokončena
- Všechny tabulky v JSON
- Validace formátu

✅ **Milestone 2:** Character Generator funkční
- `mausritter generate character` funguje
- Pěkný výstup v CLI
- Všechny testy projdou

✅ **Milestone 3:** Všechny CLI generátory hotové
- Character, Settlement, Hex, Weather, NPC
- Kompletní CLI nástroj použitelný u stolu

✅ **Milestone 4:** Web interface live
- Běžící web na localhost
- API funkční
- (Volitelně) Nasazeno online

---

## 🎯 Success Metrics

### Minimum Viable Product (MVP)
- ✅ Character Generator funguje v CLI
- ✅ Data v JSON formátu
- ✅ Testy projdou
- ✅ Dokumentace k použití

### Complete CLI Tool
- ✅ Všechny generátory (Character, Settlement, Hex, Weather, NPC)
- ✅ Pěkný výstup s Rich
- ✅ Export do JSON
- ✅ 80%+ test coverage

### Full Solution (s webem)
- ✅ Funkční web interface
- ✅ REST API
- ✅ Dokumentace API
- ✅ (Volitelně) Deployment online

---

## 🔄 Next Steps

### Immediate (co udělat teď)

1. **Začni s Fází 1:**
   ```bash
   mkdir -p data/core
   mkdir -p scripts
   ```

2. **Vytvoř první tabulku:**
   - Extrahuj Origins table do JSON
   - Validuj formát

3. **Test načtení:**
   - Vytvoř TableLoader
   - Test že dokáže načíst origins.json

4. **Implementuj roll_3d6_keep_2:**
   - Přidej do dice.py
   - Napsat test

### This Week
- [ ] Dokončit Fázi 1 (všechny JSON tabulky)
- [ ] Začít Fázi 2 (Character Generator)
- [ ] Mít funkční `mausritter generate character`

### This Month
- [ ] Dokončit všechny CLI generátory
- [ ] Testovat u stolu při hraní
- [ ] Získat feedback od hráčů

### Future Ideas
- Discord bot integration
- PDF export postav
- Virtual dice roller s animací
- Spell/Item search tool
- Session tracker
- Campaign manager

---

## 📚 Resources

### Documentation
- Knowledge Base: `docs/knowledge_base/`
- Brainstorm: `brainstorm/`
- This plan: `brainstorm/IMPLEMENTATION_PLAN.md`

### Code References
- Dice mechanics: `src/core/dice.py`
- Data models: `src/core/models.py`
- CLI: `src/cli.py`

### External Docs
- Click docs: https://click.palletsprojects.com/
- Rich docs: https://rich.readthedocs.io/
- FastAPI docs: https://fastapi.tiangolo.com/
- Mausritter rules: `docs/knowledge_base/`

---

## 📝 Notes

### Design Decisions

**Proč JSON místo databáze?**
- Tabulky jsou statické (nemění se za běhu)
- Jednoduchá validace
- Snadný version control (git)
- Rychlé načítání
- Žádné dependencies navíc

**Proč CLI first?**
- Rychleji implementovatelné
- Okamžitě použitelné
- Testování logiky bez UI
- Web je jen "hezká obálka" nad funkčním jádrem

**Proč FastAPI pro web?**
- Moderní Python framework
- Automatická API dokumentace
- Rychlé
- Type hints support
- Snadná integrace s našimi dataclasses

---

## ✅ Checklist

### Before Starting
- [x] Přečíst celý implementation plan
- [x] Pochopit architekturu
- [x] Mít jasno v timeline
- [ ] Nainstalovat dependencies: `pip install -r requirements.txt`
- [ ] Spustit existující CLI: `python -m src.cli`

### During Development
- [ ] Commit často (po každé funkční feature)
- [ ] Psát testy průběžně
- [ ] Udržovat dokumentaci aktuální
- [ ] Testovat na reálných use cases

### Before Release
- [ ] Všechny testy projdou
- [ ] README aktuální
- [ ] CLI help texty správně
- [ ] Otestováno na Windows i Linux/Mac

---

**Konec dokumentu**

*Tento plán je living document - aktualizuj ho jak postupuješ!*
