# 🐭 Mausritter Tools

Python nástroje a generátory pro stolní hru **Mausritter** - OSR TTRPG o myších dobrodružích.

## ✅ Co máme hotové

- ✅ **Generátor postav** - kompletní generování myších postav podle pravidel
- ✅ **Hody kostkami** - všechny typy kostek (d4, d6, d8, d10, d12, d20, d66)
- ✅ **Testy vlastností** - roll-under d20 mechanika
- ✅ **JSON databáze** - původy postav, jména, příjmení

**Status:** Fáze 1 a 2 dokončeny (2025-10-29)

---

## 🚀 Quick Start

### 1. Otevři terminál

Ve VS Code: **Ctrl + `** (nebo Terminal → New Terminal)

### 2. Přejdi do složky projektu

```bash
cd c:\Users\user\Projekty\ttrpg\mausritter
```

### 3. Zkus základní příkazy

**Vygeneruj postavu:**
```bash
python -m src.cli generate character
```

**Hoď kostkou:**
```bash
python -m src.cli roll-dice d20
```

**Test vlastnosti:**
```bash
python -m src.cli test 12
```

---

## 📋 Top 5 příkazů

### 🎭 1. Generování postav
```bash
# Náhodná postava
python -m src.cli generate character

# S vlastním jménem
python -m src.cli generate character --name "Pepřík"

# Ženská postava (správný tvar příjmení)
python -m src.cli generate character --gender female

# Uložit do souboru
python -m src.cli generate character --save postava.json

# JSON výstup
python -m src.cli generate character --json
```

### 🎲 2. Hody kostkami
```bash
python -m src.cli roll-dice d6
python -m src.cli roll-dice d20
python -m src.cli roll-dice 2d6
python -m src.cli roll-dice d66
```

### 🎯 3. Test vlastnosti
```bash
python -m src.cli test 12
python -m src.cli test 10 --modifier 2
```

### ❓ 4. Zobrazit help
```bash
python -m src.cli --help
python -m src.cli generate --help
```

### 🧪 5. Spustit testy
```bash
python test_character_simple.py
python test_tableloader.py
```

---

## 📚 Detailní dokumentace

👉 **[MANUAL.md](docs/MANUAL.md)** - Kompletní česká příručka

Obsahuje:
- Detailní popis všech CLI příkazů
- Strukturu projektu (Python moduly)
- Příklady použití
- Co máme hotové / co chybí

---

## 📊 Status projektu

| Fáze | Status | Popis |
|------|--------|-------|
| **Fáze 1** | ✅ HOTOVO | Data extraction (JSON tabulky) |
| **Fáze 2** | ✅ HOTOVO | Generátor postav + CLI |
| **Fáze 3** | ❌ TODO | Další generátory (Settlement, Hex, Weather, NPC) |
| **Fáze 4** | ❌ TODO | Web interface |

---

## 🗂️ Struktura projektu

```
mausritter/
├── src/
│   ├── core/              # Základní moduly
│   │   ├── dice.py        # ✅ Hody kostkami
│   │   ├── models.py      # ✅ Datové modely
│   │   └── tables.py      # ✅ Načítání JSON dat
│   ├── generators/
│   │   └── character.py   # ✅ Generátor postav
│   └── cli.py             # ✅ CLI rozhraní
├── data/
│   └── core/
│       ├── origins.json       # ✅ 36 původů postav
│       ├── names_first.json   # ✅ 100 vlastních jmen
│       └── names_family.json  # ✅ 20 mateřských jmen
├── docs/
│   ├── knowledge_base/    # Pravidla Mausritter (21 souborů)
│   └── MANUAL.md          # 📚 Uživatelská příručka
├── tests/                 # ✅ Testy
└── brainstorm/            # Plány a dokumentace
    └── IMPLEMENTATION_PLAN.md
```

---

## 🎯 Příklad výstupu

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

## 🔧 Instalace (volitelné)

```bash
# Vytvoř virtuální prostředí
python -m venv venv

# Aktivuj (Windows)
venv\Scripts\activate

# Nainstaluj závislosti
pip install -r requirements.txt
```

---

## 📖 Git commits

```bash
git log --oneline -3
```

```
ad83895 Fáze 2: Character Generator - kompletní implementace
c5944a9 Dokumentace: Aktualizace IMPLEMENTATION_PLAN.md - Fáze 1 dokončena
b868e82 Fáze 1: Data extraction a TableLoader implementace
```

---

## 📝 Poznámky

- **Jazyk:** CLI je v češtině, včetně výstupů
- **Python verze:** 3.10+
- **Platform:** Windows (testováno), Linux/Mac (mělo by fungovat)

---

## 📄 Licence

Mausritter je © Games Omnivorous.
Tento projekt je neoficiální fan-made nástroj.

---

## 🤝 Přispění

- Nápady: přidej do `brainstorm/`
- Bug reporty: vytvoř issue
- Implementation plan: [brainstorm/IMPLEMENTATION_PLAN.md](brainstorm/IMPLEMENTATION_PLAN.md)
