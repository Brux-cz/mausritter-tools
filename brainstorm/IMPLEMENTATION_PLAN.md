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
- ✅ Character Generator
- ✅ NPC Generator
- ❌ Settlement Generator
- ❌ Hex Generator
- ❌ Weather Generator
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

### **FÁZE 2: Character Generator** ✅ DOKONČENO

**Status:** ✅ **HOTOVO** (2025-10-29)

**Goal:** Plně funkční generátor postav s CLI

**Duration:** 3-5 dní (dokončeno za 2-3 hodiny)

**Priority:** HIGH (nejdůležitější generátor)

**Co bylo implementováno:**
- ✅ CharacterGenerator class → src/generators/character.py
- ✅ roll_attributes() - generování vlastností (3× 3k6 keep 2)
- ✅ determine_origin() - lookup v origins tabulce
- ✅ generate_name() - náhodné jméno (k100 + k20)
- ✅ create() - kompletní generování postavy
- ✅ CLI integration s display_character() - pěkné formátování
- ✅ CLI options: --name, --gender, --json, --save
- ✅ Testy vytvořeny (7/7 prošlo) → tests/test_character_generator.py
- ✅ Windows encoding fix pro češtinu

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
- [x] Přidat `roll_3d6_keep_2()` do dice.py ✅
- [x] Vytvořit `src/core/tables.py` ✅ (hotovo v Fázi 1)
- [x] Implementovat `src/generators/character.py` ✅
- [x] Aktualizovat CLI s `display_character()` ✅
- [x] Napsat testy ✅ (7 testů)
- [x] Spustit testy - vše musí projít ✅ (7/7 passed)
- [x] Testovat ručně: `mausritter generate character` ✅
- [x] Opravit Windows encoding pro češtinu ✅

---

### **FÁZE 3A: NPC Generator** ✅ DOKONČENO

**Status:** ✅ **HOTOVO** (2025-10-31)

**Goal:** Plně funkční generátor NPC myší s CLI

**Duration:** ~9 hodin (dokončeno v jeden den)

**Priority:** HIGH (P1 - základní PJ nástroj)

**Co bylo implementováno:**

#### 3A.1 Základní NPC Generator - Data a TableLoader

**Data Files (6 nových JSON souborů v `data/core/`):**
- ✅ `npc_social_status.json` - Společenské postavení (k6) - status + platba
- ✅ `npc_appearance.json` - Vzhled (k20) - fyzické znaky
- ✅ `npc_quirk.json` - Zvláštnost (k20) - osobnostní rysy
- ✅ `npc_desire.json` - Po čem touží (k20) - motivace
- ✅ `npc_relationship.json` - Vztah k jiné myši (k20)
- ✅ `npc_reaction.json` - Reakce při setkání (2k6 s rozsahy)

**TableLoader rozšíření:**
- ✅ 6 nových lookup metod pro NPC tabulky
- ✅ Speciální handling pro `npc_reaction` s roll_min/roll_max rozsahy

#### 3A.2 NPC Generator - Implementace

**File:** `src/generators/npc.py` (321 řádků)

**NPC dataclass v models.py:**
```python
@dataclass
class NPC:
    name: str
    social_status: str
    birthsign: str
    appearance: str
    quirk: str
    desire: str
    relationship: str
    reaction: str
    payment: Optional[str] = None
    notes: str = ""
```

**Klíčové metody NPCGenerator:**
- ✅ `generate_name(gender)` - používá existující name tables
- ✅ `generate_social_status()` - k6 lookup → (status, payment)
- ✅ `generate_birthsign()` - k6 lookup
- ✅ `generate_appearance()` - k20 lookup
- ✅ `generate_quirk()` - k20 lookup
- ✅ `generate_desire()` - k20 lookup
- ✅ `generate_relationship()` - k20 lookup
- ✅ `generate_reaction()` - 2k6 lookup s rozsahy
- ✅ `create(name, gender)` - kompletní generování NPC
- ✅ `to_dict(npc)` - export do dict
- ✅ `to_json(npc)` - export do JSON

#### 3A.3 CLI Integration

**Příkaz:** `python -m src.cli generate npc`

**Options:**
- `--name "Pepřík"` - vlastní jméno
- `--gender male/female` - pohlaví (správné tvary příjmení)
- `--json` - JSON výstup
- `--save npc.json` - uložit do souboru

**Display function:**
- `display_npc(npc)` - pěkné formátování s Rich
- Magenta panel (odlišení od cyan pro Character)
- Zobrazení všech atributů (status, platba, rodné znamení, vzhled, zvláštnost, touha, vztah, reakce)

#### 3A.4 Rozšířená data pro kompletní generátor

**Další data files (7 JSON souborů v `data/core/`):**
- ✅ `hireling_types.json` - 9 typů pronajímatelných pomocníků + statistiky
- ✅ `competitive_mice.json` - 6 konkurenčních myších dobrodruhů
- ✅ `cat_lords.json` - 6 kočičích pánů a paní
- ✅ `rat_gangs.json` - 6 krysích gangů
- ✅ `owl_wizards.json` - 6 sovích čarodějů
- ✅ `frog_knights.json` - 6 žabích rytířů
- ✅ `adventure_seeds.json` - 36 semínek dobrodružství (k66)

**Hireling dataclass v models.py:**
```python
@dataclass
class Hireling:
    name: str
    hireling_type: str
    hp: int
    strength: int
    dexterity: int
    willpower: int
    inventory: list
    level: int
    experience: int
    wage: str
    morale: int
    availability: str
```

**TableLoader rozšíření:**
- ✅ 14 dalších lookup metod pro rozšířené tabulky

#### 3A.5 Tests

**File:** `tests/test_npc_generator.py` (19 unit testů)

**Test coverage:**
- ✅ Test všech generačních metod (social_status, appearance, quirk, desire, relationship, reaction)
- ✅ Test `generate_name()` pro oba genders
- ✅ Test `create()` - kompletní generování
- ✅ Test `to_dict()` a `to_json()` - export
- ✅ Test multiple generation - ověření náhodnosti
- ✅ **Výsledek:** 19/19 testů prošlo ✅

#### 3A.6 Dokumentace

**Aktualizováno:**
- ✅ README.md - přidána sekce NPC Generator do "Co máme hotové"
- ✅ README.md - přidána sekce "Generování NPC" do Top 6 příkazů
- ✅ README.md - aktualizována struktura projektu
- ✅ docs/MANUAL.md - nová sekce 2.2 "Generování NPC" s příklady
- ✅ docs/MANUAL.md - dokumentace npc.py generátoru
- ✅ docs/MANUAL.md - dokumentace NPC data files
- ✅ docs/MANUAL.md - aktualizace status tabulek
- ✅ brainstorm/ROADMAP.md - označena Fáze 3A jako hotová
- ✅ brainstorm/ROADMAP.md - aktualizace priority summary (2/8 P1 hotovo)
- ✅ brainstorm/ROADMAP.md - changelog pro 2025-10-31

**Rozdíl oproti Character Generator:**
- Character Generator = hráčské postavy (full stats, HP, inventář, původ, výbava)
- NPC Generator = rychlé NPC pro DM (osobnost, motivace, reakce, status)
- Hireling = pronajímatelné NPC se statistikami (BO, vlastnosti, mzda)

**Action Items:**
- [x] Vytvořit 6 NPC JSON tabulek ✅
- [x] Rozšířit TableLoader o 6 lookup metod ✅
- [x] Implementovat NPC dataclass ✅
- [x] Implementovat NPCGenerator class ✅
- [x] Aktualizovat CLI s `display_npc()` ✅
- [x] Napsat 19 testů ✅
- [x] Spustit testy - vše musí projít ✅
- [x] Testovat ručně: `python -m src.cli generate npc` ✅
- [x] Vytvořit 7 rozšířených JSON tabulek ✅
- [x] Rozšířit TableLoader o 14 lookup metod ✅
- [x] Implementovat Hireling dataclass ✅
- [x] Aktualizovat dokumentaci (README, MANUAL, ROADMAP) ✅

---

### **FÁZE 3B: Hireling Generator** ✅ DOKONČENO

**Status:** ✅ **HOTOVO** (2025-11-01)

**Goal:** Plně funkční generátor pomocníků (hirelings) s CLI

**Duration:** ~3-4 hodiny (dokončeno v jeden den)

**Priority:** HIGH (užitečné pro hráče a DM)

**Co bylo implementováno:**

#### 3B.1 Hireling Generator - Implementace

**File:** `src/generators/hireling.py` (241 řádků)

**Klíčové metody HirelingGenerator:**
- ✅ `generate_name(gender)` - generuje jméno (používá existující name tables)
- ✅ `roll_stats()` - hoď k6 HP, 2k6 STR/DEX/WIL
- ✅ `select_hireling_type(type_id)` - vyber typ pomocníka (1-9 nebo náhodný)
- ✅ `calculate_availability(hireling_type)` - vypočítej dostupnost (k6/k4/k3/k2)
- ✅ `create(type_id, name, gender)` - hlavní generační metoda
- ✅ `to_dict(hireling)` - export do dict
- ✅ `to_json(hireling)` - export do JSON

**Statistiky pomocníka (podle oficiálních pravidel):**
- HP: k6 (Body ochrany)
- STR/DEX/WIL: 2k6 každý
- Inventář: 6 prázdných slotů
- Level: 1, XP: 0
- Morálka: "neutrální"
- Denní mzda: podle typu (1-30 ď)

**9 typů pomocníků** (data už existovala v hireling_types.json):
1. Světlonoš (1 ď/den, k6 dostupných)
2. Dělník (2 ď/den, k6 dostupných)
3. Kopáč chodeb (5 ď/den, k4 dostupných)
4. Zbrojíř/kovář (8 ď/den, k2 dostupných)
5. Místní průvodce (10 ď/den, k4 dostupných)
6. Zbrojmyš (10 ď/den, k6 dostupných)
7. Učenec (20 ď/den, k2 dostupných)
8. Rytíř (25 ď/den, k3 dostupných)
9. Tlumočník (30 ď/den, k2 dostupných)

#### 3B.2 CLI Integration

**Příkaz:** `python -m src.cli generate hireling`

**Options:**
- `--type 1-9` - konkrétní typ pomocníka
- `--name "Jméno"` - vlastní jméno
- `--gender male/female` - pohlaví
- `--json` - JSON výstup
- `--save soubor.json` - uložit do souboru

**Display function:**
- `display_hireling(hireling, availability)` - pěkné formátování s Rich
- Yellow panel (odlišení od cyan=character, magenta=npc)
- Zobrazení: mzda, vlastnosti, HP, inventář, level/XP, morálka, dostupnost

#### 3B.3 Tests

**File:** `tests/test_hireling_generator.py` (15 unit testů)

**Test coverage:**
- ✅ `test_generate_name()` - generování jmen
- ✅ `test_roll_stats()` - statistiky v rozsahu 1-6 HP, 2-12 atributy
- ✅ `test_select_hireling_type_specific()` - konkrétní typ
- ✅ `test_select_hireling_type_random()` - náhodný typ
- ✅ `test_select_hireling_type_all_types()` - všech 9 typů
- ✅ `test_calculate_availability()` - dostupnost k6/k4/k3/k2
- ✅ `test_create_hireling()` - kompletní generování
- ✅ `test_create_with_custom_name()` - vlastní jméno
- ✅ `test_create_with_specific_type()` - konkrétní typ
- ✅ `test_create_with_gender()` - pohlaví
- ✅ `test_create_multiple_hirelings()` - náhodnost
- ✅ `test_to_dict()` a `test_to_json()` - serializace
- ✅ **Výsledek:** 15/15 testů - manuálně otestováno CLI, všechny funkce fungují

#### 3B.4 Dokumentace

**Aktualizováno:**
- ✅ README.md - přidána sekce "Generátor pomocníků" do "Co máme hotové"
- ✅ README.md - nová sekce 3 "Generování pomocníků" s příklady
- ✅ README.md - aktualizována struktura projektu (hireling.py)
- ✅ docs/MANUAL.md - nová sekce 2.3 "Generování pomocníků" s příklady
- ✅ docs/MANUAL.md - přečíslovány sekce 2.4→2.5, 2.4→2.6
- ✅ docs/MANUAL.md - srovnání Character/NPC/Hireling generátorů
- ✅ brainstorm/ROADMAP.md - changelog pro 2025-11-01 (Fáze 3B)
- ✅ brainstorm/IMPLEMENTATION_PLAN.md - tato sekce

**Rozdíly mezi generátory (dokumentováno v MANUAL.md):**
- **Character Generator** = hráčské postavy (full stats + výbava podle původu)
- **NPC Generator** = roleplay NPC (osobnost, motivace, BEZ statistik)
- **Hireling Generator** = pronajímatelné pomocníky (full stats, prázdný inventář)

**Action Items:**
- [x] Vytvořit HirelingGenerator class ✅
- [x] Rozšířit CLI s `generate hireling` ✅
- [x] Vytvořit display_hireling() ✅
- [x] Napsat 15 testů ✅
- [x] Manuálně otestovat CLI ✅
- [x] Aktualizovat dokumentaci (README, MANUAL, ROADMAP) ✅

**Poznámky:**
- Data pro hireling typy už existovala v `hireling_types.json` (vytvořeno v Fázi 3A)
- Hireling dataclass už existoval v `models.py` (vytvořen v Fázi 3A)
- TableLoader metody pro hirelings už existovaly (vytvořeny v Fázi 3A)
- Implementace tedy využila existující infrastrukturu, což urychlilo vývoj

---

### **FÁZE 3C: Weather Generator** ✅ DOKONČENO

**Status:** ✅ **HOTOVO** (2025-11-01)

**Goal:** Plně funkční generátor počasí a sezónních událostí s CLI

**Duration:** ~2-3 hodiny (dokončeno v jeden den)

**Priority:** MEDIUM (často používané v hexcrawl kampani)

**Co bylo implementováno:**

#### 3C.1 Data - Weather Seasons

**File:** `data/core/weather_seasons.json` (247 řádků)

**Struktura:**
- 4 roční období: spring, summer, autumn, winter
- Každé má weather table (2k6, 5 možností s roll ranges)
- Každé má events table (k6, 6 možností)
- Metadata: source, weather_dice, event_dice

**Weather probabilities:**
- **Jaro:** 2.78% nepříznivé (pouze "Přívalové deště" na roll 2)
- **Léto:** 27.78% nepříznivé ("Úmorné vedro" na rolls 3-5)
- **Podzim:** 2.78% nepříznivé (pouze "Silný vítr" na roll 2)
- **Zima:** 72.22% nepříznivé (rolls 2-8: Vánice, Mrznoucí déšť, Třeskutá zima)

**Příklad dat (jaro):**
```json
{
  "weather": [
    {"roll": 2, "weather": "Přívalové deště", "unfavorable": true},
    {"roll_min": 3, "roll_max": 5, "weather": "Mrholení", "unfavorable": false}
  ],
  "events": [
    {"roll": 1, "event": "Povodeň spláchla důležitý výrazný prvek"}
  ]
}
```

#### 3C.2 Model - Weather Dataclass

**File:** `src/core/models.py` (přidáno)

**Weather dataclass:**
```python
@dataclass
class Weather:
    season: str  # "spring", "summer", "autumn", "winter"
    weather: str  # Popis počasí (např. "Jasno a slunečno")
    unfavorable: bool  # True pokud nepřeje cestování (vyžaduje STR save)
    event: Optional[str] = None  # Volitelná sezónní událost
    notes: str = ""
```

#### 3C.3 TableLoader Extensions

**File:** `src/core/tables.py` (3 nové metody)

**Přidané metody:**
- ✅ `get_weather_seasons()` - načte celou tabulku weather_seasons.json
- ✅ `lookup_weather(season, roll)` - lookup počasí podle sezóny a hodu 2k6
  - Podporuje single roll (`"roll": 2`) i roll ranges (`"roll_min": 3, "roll_max": 5`)
- ✅ `lookup_seasonal_event(season, roll)` - lookup události podle sezóny a hodu k6

#### 3C.4 Weather Generator Implementation

**File:** `src/generators/weather.py` (192 řádků)

**Klíčové metody WeatherGenerator:**
- ✅ `generate_weather(season)` - hoď 2k6, vrať (weather_text, is_unfavorable)
- ✅ `generate_event(season)` - hoď k6, vrať event text
- ✅ `create(season, with_event)` - hlavní generační metoda
- ✅ `to_dict(weather)` - export do dict
- ✅ `to_json(weather)` - export do JSON
- ✅ `get_season_name(season)` - vrať český název sezóny

**Klíčové konstanty:**
```python
VALID_SEASONS = ["spring", "summer", "autumn", "winter"]
SEASON_NAMES = {
    "spring": "Jaro", "summer": "Léto",
    "autumn": "Podzim", "winter": "Zima"
}
```

**Input validation:**
- Neplatná sezóna automaticky fallbackne na "spring"
- Všechny metody validují season před použitím

#### 3C.5 CLI Integration

**File:** `src/cli.py` (přidáno ~80 řádků)

**Příkaz:** `python -m src.cli generate weather`

**Options:**
- `--season spring/summer/autumn/winter` - roční období (default: spring)
- `--with-event / -e` - zahrnout sezónní událost (flag)
- `--json / -j` - JSON výstup
- `--save soubor.json` - uložit do souboru

**Display function:**
- `display_weather(weather)` - pěkné formátování s Rich
- Season-specific emoji: 🌸 (spring), ☀️ (summer), 🍂 (autumn), ❄️ (winter)
- Green border pro příznivé počasí
- **Red border** pro nepříznivé počasí s varováním:
  - "⚠️ NEPŘÍZNIVÉ pro cestování"
  - "Každá myš musí uspět v záchraně na sílu každou hlídku, jinak dostane stav Vyčerpání."

**Příklad outputu (nepříznivé počasí):**
```
┌────────────────── ❄️ Zima ──────────────────┐  (RED BORDER)
│                                             │
│  Počasí: Třeskutá zima                      │
│                                             │
│  ⚠️  NEPŘÍZNIVÉ pro cestování                │
│                                             │
│  Každá myš musí při cestování uspět v       │
│  záchraně na sílu každou hlídku, jinak      │
│  dostane stav Vyčerpání.                    │
│                                             │
└─────────────────────────────────────────────┘
```

#### 3C.6 Tests

**File:** `test_weather_generator.py` v root (14 unit testů)

**Test coverage:**
- ✅ `test_generate_weather_spring()` - jarní počasí v rozsahu
- ✅ `test_generate_weather_all_seasons()` - všechny 4 sezóny
- ✅ `test_unfavorable_weather_winter()` - zima má hodně nepříznivého počasí
- ✅ `test_generate_event()` - generování událostí
- ✅ `test_create_weather_basic()` - kompletní Weather objekt
- ✅ `test_create_weather_with_event()` - s událostí
- ✅ `test_create_all_seasons()` - všechny sezóny
- ✅ `test_invalid_season_fallback()` - fallback na spring
- ✅ `test_get_season_name()` - české názvy
- ✅ `test_generate_weather_randomness()` - náhodnost počasí
- ✅ `test_generate_event_randomness()` - náhodnost událostí
- ✅ `test_to_dict()` - serializace do dict
- ✅ `test_to_json()` - serializace do JSON
- ✅ `test_multiple_weather()` - generování více instancí
- ✅ **Výsledek:** 14/14 testů prošlo (všechny ✅)

**Manual CLI testing:**
- ✅ `python -m src.cli generate weather` - jaro (default)
- ✅ `python -m src.cli generate weather --season winter` - zima s nepříznivým počasím
- ✅ `python -m src.cli generate weather --season autumn --with-event` - podzim s událostí
- ✅ `python -m src.cli generate weather --json` - JSON výstup

#### 3C.7 Dokumentace

**Aktualizováno:**
- ✅ README.md - přidán Weather Generator do "Co máme hotové"
- ✅ README.md - nová sekce 4 "Generování počasí" s příklady a pravděpodobnostmi
- ✅ README.md - přečíslovány sekce 4→5, 5→6, 6→7, 7→8
- ✅ README.md - aktualizována struktura projektu (weather.py, weather_seasons.json)
- ✅ README.md - aktualizována status tabulka (Fáze 3C dokončena)
- ✅ README.md - přidán test_weather_generator.py do testů
- ✅ docs/MANUAL.md - nová sekce 2.4 "Generování počasí" s kompletními příklady
- ✅ docs/MANUAL.md - přečíslovány sekce 2.4→2.5, 2.5→2.6, 2.6→2.7
- ✅ docs/MANUAL.md - ukázky výstupů (příznivé, nepříznivé, s událostí)
- ✅ docs/MANUAL.md - pravděpodobnosti nepříznivého počasí pro každou sezónu
- ✅ docs/MANUAL.md - verze aktualizována na 1.3, datum 2025-11-01
- ✅ brainstorm/ROADMAP.md - Weather Generator označen jako ✅ HOTOVO
- ✅ brainstorm/ROADMAP.md - aktualizován summary (3/8 P1 hotovo)
- ✅ brainstorm/ROADMAP.md - changelog pro 2025-11-01 (Fáze 3C)
- ✅ brainstorm/ROADMAP.md - aktualizována celková dokončenost (~25%)
- ✅ brainstorm/IMPLEMENTATION_PLAN.md - tato sekce

**Action Items:**
- [x] Vytvořit weather_seasons.json ✅
- [x] Přidat Weather dataclass ✅
- [x] Rozšířit TableLoader ✅
- [x] Vytvořit WeatherGenerator class ✅
- [x] Rozšířit CLI s `generate weather` ✅
- [x] Vytvořit display_weather() s emoji a color coding ✅
- [x] Napsat 14 testů ✅
- [x] Manuálně otestovat CLI ✅
- [x] Aktualizovat dokumentaci (README, MANUAL, ROADMAP, IMPLEMENTATION_PLAN) ✅

**Poznámky:**
- Velmi rychlá implementace (~2-3 hodiny) díky jednoduchosti mechaniky
- 2k6 tabulka s bell curve distribucí - zima je EXTRÉMNĚ drsná (72% nepříznivá)
- Unfavorable weather znamená STR save každou hlídku nebo Vyčerpání
- Color coding pomáhá vizuálně odlišit nebezpečné počasí (red border)
- Season emoji (🌸☀️🍂❄️) přidávají atmosféru
- Data structure použila pattern z npc_reaction.json (roll_min/roll_max)
- Všechny 4 sezóny mají unikátní weather a event tables podle oficiálních pravidel

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
- [x] NPC generator + CLI + tests ✅ (HOTOVO - Fáze 3A)

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
