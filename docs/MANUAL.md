# 📚 Mausritter Tools - Uživatelská příručka

Kompletní česká příručka pro práci s Mausritter Tools.

**Verze:** 1.0
**Datum:** 2025-10-29
**Status:** Fáze 1 a 2 dokončeny

---

## 📖 Obsah

1. [Quick Start](#1-quick-start)
2. [CLI Příkazy (Tools)](#2-cli-příkazy-tools)
3. [Struktura projektu (Python moduly)](#3-struktura-projektu-python-moduly)
4. [Příklady použití](#4-příklady-použití)
5. [Status projektu](#5-status-projektu)
6. [Testování](#6-testování)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Quick Start

### 1.1 Jak otevřít terminál

**Ve VS Code:**
1. Stiskni **Ctrl + `** (zpětný apostrof, vlevo nahoře pod Esc)
2. Nebo klikni na **Terminal** → **New Terminal** v horním menu
3. Dole se otevře okno s příkazovým řádkem

**Alternativně (Windows PowerShell):**
1. Stiskni **Windows + R**
2. Napiš `powershell` a Enter
3. Objeví se modré okno

### 1.2 Přejdi do složky projektu

V terminálu napiš:

```bash
cd c:\Users\user\Projekty\ttrpg\mausritter
```

**Zkontroluj že jsi na správném místě:**
```bash
dir
```

Měl bys vidět složky: `src`, `data`, `docs`, `brainstorm`, `tests`

### 1.3 Tvůj první příkaz

Vygeneruj náhodnou myší postavu:

```bash
python -m src.cli generate character
```

Měl bys vidět pěkně naformátovanou postavu s jménem, vlastnostmi, HP a výbavou! 🎉

---

## 2. CLI Příkazy (Tools)

**Co jsou CLI příkazy?** Příkazy které spouštíš v terminálu pro práci s Mausritter Tools.

**Základní formát:**
```bash
python -m src.cli <příkaz> [možnosti]
```

**Proč `-m`?** Říká Pythonu aby spustil modul s jeho importy.

---

### 2.1 Generování postav

**Hlavní příkaz:**
```bash
python -m src.cli generate character
```

**Co to dělá:**
Vygeneruje kompletní náhodnou myší postavu podle pravidel Mausritter:
- Hoď 3× vlastnosti (3k6 keep 2) → Síla, Mrštnost, Vůle
- Hoď k6 pro Body ochrany (HP)
- Hoď k6 pro počáteční ďobky (Pips)
- Najdi původ v tabulce podle HP a Pips
- Vygeneruj náhodné jméno (k100 + k20)
- Přiřaď počáteční výbavu (Pochodně, Zásoby + 2 předměty z původu)

#### 2.1.1 Možnosti příkazu

**`--name` / `-n` - Vlastní jméno**
```bash
python -m src.cli generate character --name "Pepřík"
python -m src.cli generate character -n "Sedmikráska"
```
Použije zadané jméno místo náhodného.

**`--gender` / `-g` - Pohlaví (pro správný tvar příjmení)**
```bash
python -m src.cli generate character --gender female
python -m src.cli generate character -g male
```
Možnosti: `male` (výchozí), `female`
Určuje tvar příjmení (Hrabal vs. Hrabalová)

**`--json` / `-j` - JSON výstup**
```bash
python -m src.cli generate character --json
```
Zobrazí postavu jako JSON místo pěkného formátování.

**`--save` / `-s` - Uložit do souboru**
```bash
python -m src.cli generate character --save postava.json
python -m src.cli generate character -s moje_postavy/prvni.json
```
Uloží postavu do JSON souboru.

#### 2.1.2 Příklady použití

**Náhodná mužská postava:**
```bash
python -m src.cli generate character
```

**Náhodná ženská postava:**
```bash
python -m src.cli generate character --gender female
```

**Postava s vlastním jménem:**
```bash
python -m src.cli generate character --name "Testovací Myš"
```

**Kombinace možností:**
```bash
python -m src.cli generate character --name "Pepřík" --gender male --save peprik.json
```

**5 postav za sebou:**
```bash
python -m src.cli generate character
python -m src.cli generate character
python -m src.cli generate character
python -m src.cli generate character
python -m src.cli generate character
```

#### 2.1.3 Ukázka výstupu

```
┌────────────────── Pepřík Hrabal ──────────────────┐
│  Vlastnosti:                                      │
│    Síla:       4  [███░░░░░░░]                    │
│    Mrštnost:   9  [███████░░░]                    │
│    Vůle:      12  [██████████]                    │
│  Zdraví:                                          │
│    BO: 6/6  ❤️❤️❤️❤️❤️❤️                              │
│  Počáteční výbava:                                │
│    1. Pochodně (3 použití)                        │
│    2. Zásoby (3 použití)                          │
│    3. Zatížené kostky                             │
│    4. Zrcátko                                     │
│  Poznámky:                                        │
│    Počáteční ďobky: 2 ď                           │
└────────────────── ⭐ Hazardní hráč ────────────────┘
```

---

### 2.2 Hody kostkami

**Hlavní příkaz:**
```bash
python -m src.cli roll-dice <kostka>
```

**Co to dělá:**
Hodí zadanou kostkou a zobrazí výsledek.

#### 2.2.1 Podporované kostky

**Základní kostky:**
```bash
python -m src.cli roll-dice d4    # k4 (1-4)
python -m src.cli roll-dice d6    # k6 (1-6)
python -m src.cli roll-dice d8    # k8 (1-8)
python -m src.cli roll-dice d10   # k10 (1-10)
python -m src.cli roll-dice d12   # k12 (1-12)
python -m src.cli roll-dice d20   # k20 (1-20)
```

**Více kostek:**
```bash
python -m src.cli roll-dice 2d6   # 2× k6
python -m src.cli roll-dice 3d6   # 3× k6
python -m src.cli roll-dice 4d4   # 4× k4
```

**Speciální pro Mausritter:**
```bash
python -m src.cli roll-dice d66   # k66 (11-66, pro tabulky)
```

#### 2.2.2 Ukázka výstupu

```
Hod d20:
Výsledek: 14
```

```
Hod 2d6:
Jednotlivé hody: [4, 6]
Výsledek: 10
```

---

### 2.3 Testy vlastností

**Hlavní příkaz:**
```bash
python -m src.cli test <hodnota>
```

**Co to dělá:**
Roll-under test - hodí k20, úspěch pokud je výsledek ≤ hodnota vlastnosti.

#### 2.3.1 Možnosti příkazu

**Základní test:**
```bash
python -m src.cli test 12
```
Hodí k20, úspěch pokud ≤ 12.

**S modifikátorem:**
```bash
python -m src.cli test 10 --modifier 2
python -m src.cli test 8 -m -3
```
Cílové číslo = vlastnost + modifikátor
`test 10 --modifier 2` → cíl 12

#### 2.3.2 Ukázka výstupu

```
Test vlastnosti:
Cílové číslo: 12
Hod: 8
ÚSPĚCH! (8 <= 12)
```

```
Test vlastnosti:
Cílové číslo: 10
Hod: 15
NEÚSPĚCH (15 > 10)
```

---

### 2.4 Help a nápověda

**Zobrazit všechny příkazy:**
```bash
python -m src.cli --help
```

**Help pro konkrétní skupinu:**
```bash
python -m src.cli generate --help
```

**Help pro konkrétní příkaz:**
```bash
python -m src.cli generate character --help
python -m src.cli roll-dice --help
python -m src.cli test --help
```

---

## 3. Struktura projektu (Python moduly)

**Co jsou Python moduly?** Soubory `.py` s kódem - funkce, třídy, logika programu.

Tato sekce je pro ty, kdo se chtějí podívat "pod kapotu" a vidět kde je co v kódu.

---

### 3.1 Core moduly (`src/core/`)

Základní stavební kameny - kostky, modely, načítání dat.

#### 📄 `src/core/dice.py` - Hody kostkami

**Co to je:**
Všechny mechaniky pro házení kostkami.

**Hlavní funkce:**
- `roll_d6()` → hoď k6
- `roll_d20()` → hoď k20
- `roll_d66()` → hoď k66 (speciální pro Mausritter)
- `roll(dice: str)` → univerzální parser ("2d6", "3k8", atd.)
- `roll_with_details()` → vrátí celkem + jednotlivé hody
- `roll_3d6_keep_2()` → hoď 3k6, vezmi 2 nejvyšší (pro vlastnosti) ✨
- `attribute_test(value, modifier)` → roll-under d20 test
- `advantage_roll()` → 2k20, vezmi lepší
- `disadvantage_roll()` → 2k20, vezmi horší

**Status:** ✅ HOTOVO

**Příklad použití v kódu:**
```python
from src.core.dice import roll_d6, roll_3d6_keep_2

hp = roll_d6()  # 1-6
strength = roll_3d6_keep_2()  # 2-12
```

---

#### 📄 `src/core/models.py` - Datové modely

**Co to je:**
Definice datových struktur (třídy) pro postavy, předměty, NPCs, atd.

**Hlavní třídy:**
- `Character` - model postavy
  - Atributy: name, background, strength, dexterity, willpower, hp, inventory...
- `Item` - model předmětu
  - Atributy: name, description, slots, cost, usage_die...
- `NPC` - model NPC
  - Atributy: name, species, disposition, wants...
- `Condition` - stavy postavy (otráven, vyděšený...)
- `Background` - původ postavy
- `Location` - lokace/dungeon

**Status:** ✅ HOTOVO

**Příklad použití v kódu:**
```python
from src.core.models import Character

char = Character(
    name="Pepřík",
    background="Hazardní hráč",
    strength=4,
    dexterity=9,
    willpower=12,
    max_hp=6,
    current_hp=6,
    inventory=[...]
)
```

---

#### 📄 `src/core/tables.py` - Načítání JSON dat

**Co to je:**
Třída pro načítání JSON tabulek z `data/` složky. Cachuje data pro rychlost.

**Hlavní třída: `TableLoader`**

**Statické metody:**
- `load_table(path)` → načte libovolnou JSON tabulku (s cachováním)
- `get_origins()` → načte tabulku původů
- `get_first_names()` → načte vlastní jména
- `get_family_names()` → načte mateřská jména
- `lookup_origin(hp, pips)` → najdi původ podle HP a Pips
- `lookup_first_name(roll)` → najdi jméno podle hodu k100
- `lookup_family_name(roll, gender)` → najdi příjmení podle hodu k20
- `clear_cache()` → vyčisti cache (pro testy)

**Status:** ✅ HOTOVO (Fáze 1)

**Příklad použití v kódu:**
```python
from src.core.tables import TableLoader

# Načti tabulku původů
origins = TableLoader.get_origins()

# Najdi konkrétní původ
origin = TableLoader.lookup_origin(hp=3, pips=5)
print(origin["name"])  # "Stěnolezec"

# Vygeneruj jméno
first = TableLoader.lookup_first_name(75)  # "Pepřík"
family = TableLoader.lookup_family_name(6, "male")  # "Hrabal"
```

---

### 3.2 Generátory (`src/generators/`)

Moduly pro generování postav, lokací, NPCs, atd.

#### 📄 `src/generators/character.py` - Generátor postav

**Co to je:**
Kompletní generátor myších postav podle pravidel Mausritter.

**Hlavní třída: `CharacterGenerator`**

**Statické metody:**
- `roll_attributes()` → hoď 3× vlastnosti (3k6 keep 2)
  - Vrací: `(strength, dexterity, willpower)`
- `determine_origin(hp, pips)` → najdi původ podle HP a Pips
  - Vrací: Dictionary s daty původu (name, item_a, item_b)
- `generate_name(gender="male")` → vygeneruj náhodné jméno
  - Vrací: "Jméno Příjmení" (např. "Pepřík Hrabal")
- `create(name=None, gender="male")` → **hlavní metoda** - vytvoř celou postavu
  - Vrací: Character instance
- `to_dict(character)` → konvertuj Character do dictionary
- `to_json(character)` → konvertuj Character do JSON stringu

**Status:** ✅ HOTOVO (Fáze 2)

**Příklad použití v kódu:**
```python
from src.generators.character import CharacterGenerator

# Vygeneruj náhodnou postavu
char = CharacterGenerator.create()

# S vlastním jménem
char = CharacterGenerator.create(name="Pepřík")

# Ženská postava
char = CharacterGenerator.create(gender="female")

# Export do JSON
json_str = CharacterGenerator.to_json(char)
```

**Postup generování:**
1. Hod 3× vlastnosti pomocí `roll_3d6_keep_2()`
2. Hod k6 pro HP
3. Hod k6 pro Pips (počáteční ďobky)
4. Lookup původu v `origins.json` podle HP a Pips
5. Vygeneruj/použij jméno
6. Přiřaď počáteční výbavu:
   - Pochodně (3 použití)
   - Zásoby (3 použití)
   - item_a z původu
   - item_b z původu
7. Vrať Character objekt

---

### 3.3 CLI - Příkazový řádek (`src/`)

#### 📄 `src/cli.py` - CLI rozhraní

**Co to je:**
Hlavní příkazový řádek (Command Line Interface) - propojení mezi tebou a kódem.

**Technologie:**
- **Click** - framework pro CLI
- **Rich** - pěkné formátování výstupu (panely, progress bary, barvy)

**Hlavní funkce:**
- `main()` - hlavní skupina příkazů
- `generate()` - skupina pro generátory
- `character()` - příkaz `generate character`
- `display_character()` - zobrazí postavu s Rich formátováním
- `roll_dice()` - příkaz `roll-dice`
- `test()` - příkaz `test`
- `tools()` - skupina pro další nástroje (zatím prázdná)

**Windows encoding fix:**
Automaticky nastaví UTF-8 pro správné zobrazení českých znaků.

**Status:** ✅ HOTOVO

---

### 3.4 Data (`data/`)

JSON soubory s herními daty.

#### 📄 `data/core/origins.json` - 36 původů postav

**Struktura:**
```json
{
  "metadata": {
    "source": "docs/knowledge_base/02_CHARACTER_CREATION.md",
    "description": "Tabulka původů postav",
    "lookup_method": "hp_and_pips"
  },
  "origins": [
    {
      "hp": 1,
      "pips": 1,
      "name": "Pokusná myš",
      "item_a": "Kouzlo: Kouzelná střela",
      "item_b": "Olověný plášť (těžká zbroj)"
    },
    ...36 položek...
  ]
}
```

**Lookup:** Podle HP (1-6) a Pips (1-6) → 36 kombinací
**Status:** ✅ HOTOVO (Fáze 1)

---

#### 📄 `data/core/names_first.json` - 100 vlastních jmen

**Struktura:**
```json
{
  "metadata": {
    "source": "docs/knowledge_base/02_CHARACTER_CREATION.md",
    "description": "Vlastní jména myší - hoď k100",
    "dice": "d100"
  },
  "names": [
    {"roll": 1, "name": "Ada"},
    {"roll": 2, "name": "Agáta"},
    ...100 položek...
    {"roll": 100, "name": "Žitmil"}
  ]
}
```

**Lookup:** Podle hodu k100 (1-100)
**Status:** ✅ HOTOVO (Fáze 1)

---

#### 📄 `data/core/names_family.json` - 20 mateřských jmen

**Struktura:**
```json
{
  "metadata": {
    "source": "docs/knowledge_base/02_CHARACTER_CREATION.md",
    "description": "Mateřská jména myší - hoď k20",
    "dice": "d20"
  },
  "names": [
    {"roll": 1, "name_male": "Bílý", "name_female": "Bílá"},
    {"roll": 2, "name_male": "Černý", "name_female": "Černá"},
    ...20 položek...
  ]
}
```

**Lookup:** Podle hodu k20 (1-20) + gender
**Status:** ✅ HOTOVO (Fáze 1)

---

## 4. Příklady použití

### Scénář 1: Vytvořit 3 postavy pro novou kampaň

```bash
# Postava 1 - náhodná
python -m src.cli generate character --save kampan/postava1.json

# Postava 2 - ženská
python -m src.cli generate character --gender female --save kampan/postava2.json

# Postava 3 - s vlastním jménem
python -m src.cli generate character --name "Pepřík" --save kampan/postava3.json
```

### Scénář 2: Testovat hody během hry

```bash
# Hod na útok
python -m src.cli roll-dice d20

# Hod na zranění mečem
python -m src.cli roll-dice d8

# Test síly (hodnota 9)
python -m src.cli test 9

# Test mrštnosti s výhodou (+2)
python -m src.cli test 11 --modifier 2

# Náhodná tabulka k66
python -m src.cli roll-dice d66
```

### Scénář 3: Rychlá příprava na session

```bash
# Vygeneruj 5 NPC postav
python -m src.cli generate character --gender female > npcs.txt
python -m src.cli generate character >> npcs.txt
python -m src.cli generate character >> npcs.txt
python -m src.cli generate character --gender female >> npcs.txt
python -m src.cli generate character >> npcs.txt

# Poznámka: >> přidává na konec souboru
```

### Scénář 4: Export pro další nástroje

```bash
# Export do JSON pro web/app
python -m src.cli generate character --json > export.json
```

---

## 5. Status projektu

### ✅ Co máme hotové

| Komponenta | Soubor | Popis | Status |
|------------|--------|-------|--------|
| **Dice roller** | `src/core/dice.py` | Všechny typy kostek, testy | ✅ HOTOVO |
| **Data models** | `src/core/models.py` | Character, Item, NPC... | ✅ HOTOVO |
| **Table loader** | `src/core/tables.py` | Načítání JSON dat | ✅ HOTOVO |
| **Character gen** | `src/generators/character.py` | Generátor postav | ✅ HOTOVO |
| **CLI** | `src/cli.py` | Příkazový řádek | ✅ HOTOVO |
| **Origins data** | `data/core/origins.json` | 36 původů | ✅ HOTOVO |
| **Names data** | `data/core/names_first.json` | 100 jmen | ✅ HOTOVO |
| **Family names** | `data/core/names_family.json` | 20 příjmení | ✅ HOTOVO |
| **Tests** | `tests/` | 7 testů | ✅ HOTOVO |

**Dokončené fáze:**
- ✅ **Fáze 1:** Data extraction (2025-10-29)
- ✅ **Fáze 2:** Character Generator (2025-10-29)

### ❌ Co ještě chybí

**Fáze 3:** Další generátory
- ❌ Settlement Generator (generátor sídel)
- ❌ Hex Generator (generátor hexů pro hexcrawl)
- ❌ Weather Generator (generátor počasí)
- ❌ NPC Generator (rozšířený)
- ❌ Dungeon Generator

**Fáze 4:** Web interface
- ❌ FastAPI backend
- ❌ HTML frontend
- ❌ REST API

**Volitelné rozšíření:**
- ❌ Birthsigns (rodná znamení) - data + generování
- ❌ Coat colors/patterns (barvy a vzory srsti)
- ❌ Trinkets (cetky a drobnosti)

---

## 6. Testování

### 6.1 Automatické testy

**Test Character Generator:**
```bash
python test_character_simple.py
```

Mělo by projít **7/7 testů**:
- test_roll_attributes
- test_determine_origin
- test_generate_name
- test_create_character
- test_create_with_custom_name
- test_to_json
- test_multiple_characters

**Test TableLoader:**
```bash
python test_tableloader.py
```

Mělo by projít všechny testy načítání tabulek.

### 6.2 Manuální testování CLI

**Test generování postav:**
```bash
# Základní
python -m src.cli generate character

# Různé options
python -m src.cli generate character --name "Test"
python -m src.cli generate character --gender female
python -m src.cli generate character --json
python -m src.cli generate character --save test.json

# Kombinace
python -m src.cli generate character --name "Test" --save test.json
```

**Test hodů kostkami:**
```bash
python -m src.cli roll-dice d6
python -m src.cli roll-dice d20
python -m src.cli roll-dice 2d6
python -m src.cli roll-dice d66
```

**Test vlastností:**
```bash
python -m src.cli test 10
python -m src.cli test 12 --modifier 2
python -m src.cli test 8 -m -3
```

### 6.3 Validace dat

**Zkontroluj že JSON soubory jsou validní:**
```bash
python -c "import json; print(json.load(open('data/core/origins.json'))['metadata'])"
python -c "import json; print(len(json.load(open('data/core/names_first.json'))['names']))"
python -c "import json; print(len(json.load(open('data/core/names_family.json'))['names']))"
```

---

## 7. Troubleshooting

### Problém: "python" není rozpoznán jako příkaz

**Řešení:**
- Zkus `py` místo `python`
- Nebo `python3`

```bash
py -m src.cli generate character
python3 -m src.cli generate character
```

### Problém: "No module named src"

**Příčina:** Nejsi ve správné složce

**Řešení:**
```bash
# Zkontroluj kde jsi
pwd   # Linux/Mac
cd    # Windows

# Přejdi do správné složky
cd c:\Users\user\Projekty\ttrpg\mausritter

# Ověř že tam je složka src
dir   # Windows
ls    # Linux/Mac
```

### Problém: UnicodeEncodeError s českými znaky

**Příčina:** Windows encoding

**Řešení:** Již opraveno v `src/cli.py` - automaticky nastavuje UTF-8.

Pokud stále problém:
```bash
# Nastav encoding manuálně (PowerShell)
$OutputEncoding = [System.Text.Encoding]::UTF8
```

### Problém: Postava nemá český původ/jméno

**Příčina:** Chybí JSON soubory

**Řešení:** Zkontroluj že existují:
```bash
dir data\core\*.json   # Windows
ls data/core/*.json    # Linux/Mac
```

Měly by být 3 soubory:
- `origins.json`
- `names_first.json`
- `names_family.json`

### Problém: Testy selhávají

**Řešení:**
```bash
# Spusť testy s výpisem chyb
python test_character_simple.py

# Pokud chybí moduly
pip install -r requirements.txt
```

### Problém: Příkaz "generate character" nefunguje

**Kontrola:**
```bash
# Zobraz help - měl bys vidět "generate" skupinu
python -m src.cli --help

# Zobraz help pro generate
python -m src.cli generate --help

# Zkontroluj že existuje character.py
dir src\generators\character.py   # Windows
ls src/generators/character.py    # Linux/Mac
```

---

## 📞 Další pomoc

**Kde najít více informací:**
- [README.md](../README.md) - Quick start
- [IMPLEMENTATION_PLAN.md](../brainstorm/IMPLEMENTATION_PLAN.md) - Technický plán
- [Knowledge base](knowledge_base/00_INDEX.md) - Pravidla Mausritter

**Git historie:**
```bash
git log --oneline -10
```

**Aktuální verze:**
```bash
python -m src.cli --version
```

---

**Konec příručky** - Užij si generování myších dobrodruhů! 🐭🎲
