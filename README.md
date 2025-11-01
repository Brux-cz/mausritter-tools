# 🐭 Mausritter Tools

Python nástroje a generátory pro stolní hru **Mausritter** - OSR TTRPG o myších dobrodružích.

## ✅ Co máme hotové

- ✅ **Generátor postav** - kompletní generování myších postav podle pravidel
- ✅ **Generátor NPC** - rychlé vytváření nehráčských myší
- ✅ **Generátor pomocníků** - generování hirelingů s plnými statistikami
- ✅ **Generátor počasí** - generování počasí a sezónních událostí pro všechny čtyři roční období
- ✅ **Generátor reakcí** - reakce NPC/tvorů při setkání (2k6 tabulka)
- ✅ **Generátor kouzel** - náhodná kouzla pro objevování pokladů (2d8 tabulka, 16 kouzel)
- ✅ **Generátor pokladů** - kompletní treasure hoard (2-6× k20, kouzelné meče, kouzla, předměty)
- ✅ **Generátor semínek dobrodružství** - kombinace tvora, problému a komplikace (k66, 36 semínek)
- ✅ **Generátor hospod** - názvy a speciality hospod (2× k12 + k12, pro vísky a větší osady)
- ✅ **Hody kostkami** - všechny typy kostek (d4, d6, d8, d10, d12, d20, d66)
- ✅ **Testy vlastností** - roll-under d20 mechanika
- ✅ **JSON databáze** - původy, jména, NPC, pomocníci, počasí, kouzla, poklady, nástroje, semínka dobrodružství

**Status:** Fáze 1, 2, 3A-F, 4A-B dokončeny (2025-11-02) - **P1 COMPLETE (100%)** + Tavern ✅

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

## 📋 Top 6 příkazů

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

### 🎭 2. Generování NPC
```bash
# Náhodné NPC
python -m src.cli generate npc

# S vlastním jménem
python -m src.cli generate npc --name "Strážný"

# Ženské NPC
python -m src.cli generate npc --gender female

# Uložit do souboru
python -m src.cli generate npc --save npc.json

# JSON výstup
python -m src.cli generate npc --json
```

### ⚔️ 3. Generování pomocníků (Hirelings)
```bash
# Náhodný pomocník
python -m src.cli generate hireling

# Konkrétní typ (1-9)
python -m src.cli generate hireling --type 6    # Zbrojmyš
python -m src.cli generate hireling --type 8    # Rytíř

# S vlastním jménem
python -m src.cli generate hireling --name "Sir Pepřík"

# Ženská pomocnice
python -m src.cli generate hireling --gender female

# Uložit do souboru
python -m src.cli generate hireling --save pomocnik.json

# JSON výstup
python -m src.cli generate hireling --json
```

**Typy pomocníků:**
1. Světlonoš (1 ď/den)
2. Dělník (2 ď/den)
3. Kopáč chodeb (5 ď/den)
4. Zbrojíř/kovář (8 ď/den)
5. Místní průvodce (10 ď/den)
6. Zbrojmyš (10 ď/den)
7. Učenec (20 ď/den)
8. Rytíř (25 ď/den)
9. Tlumočník (30 ď/den)

### 🌦️ 4. Generování počasí
```bash
# Náhodné počasí (default: jaro)
python -m src.cli generate weather

# Konkrétní roční období
python -m src.cli generate weather --season spring   # Jaro
python -m src.cli generate weather --season summer   # Léto
python -m src.cli generate weather --season autumn   # Podzim
python -m src.cli generate weather --season winter   # Zima

# S sezónní událostí
python -m src.cli generate weather --season autumn --with-event

# JSON výstup
python -m src.cli generate weather --json

# Uložit do souboru
python -m src.cli generate weather --save weather.json
```

**Roční období:**
- **Jaro** - Přívalové deště (2.78% nepříznivé)
- **Léto** - Úmorné vedro (27.78% nepříznivé)
- **Podzim** - Silný vítr (2.78% nepříznivé)
- **Zima** - Vánice, mráz (72% nepříznivé!)

### 🎭 5. Generování reakcí
```bash
# Náhodná reakce NPC/tvora
python -m src.cli generate reaction

# S modifikátorem
python -m src.cli generate reaction --modifier 1    # +1 za dárek
python -m src.cli generate reaction -m -2           # -2 za agresi

# JSON výstup
python -m src.cli generate reaction --json

# Uložit do souboru
python -m src.cli generate reaction --save reaction.json
```

**Typy reakcí (2k6):**
- **2** - Agresivní ⚔️
- **3-5** - Nepřátelská 😠
- **6-8** - Nejistá 🤔
- **9-11** - Povídavá 😊
- **12** - Nápomocná 💚

### ✨ 6. Generování kouzel
```bash
# Náhodné kouzlo
python -m src.cli generate spell

# JSON výstup
python -m src.cli generate spell --json

# Uložit do souboru
python -m src.cli generate spell --save kouzlo.json
```

**Kouzla (2d8, 16 kouzel):**
- Ohnivá koule, Zahojení, Kouzelná střela, Strach
- Tma, Zotavení, Srozumitelnost, Přízračný brouk
- Světlo, Neviditelný prstenec, Zaklepání, Tuk
- Zvětšení, Neviditelnost, Šanta

**Note:** [POČET] a [SOUČET] jsou placeholdery pro sesílání

### 💰 7. Generování pokladů
```bash
# Základní poklad (2× k20)
python -m src.cli generate treasure

# S bonusovými hody (0-4)
python -m src.cli generate treasure --bonus 2
python -m src.cli generate treasure -b 4

# JSON výstup
python -m src.cli generate treasure --bonus 3 --json

# Uložit do souboru
python -m src.cli generate treasure --save hoard.json
```

**Bonusové hody (za každou kladnou odpověď +1 hod k20):**
1. Je v bývalé myší osadě / hradě / jeskyni?
2. Je ve vysoce magické oblasti?
3. Brání ho velké zvíře / záludná past?
4. Překonaly myši velké nesnáze?

**Mechanika:**
- 2-6 hodů k20 na hlavní tabulku (2 základní + 0-4 bonusové)
- Každý hod může vést k dalším hodům na podtabulky

**Co může být v pokladu:**
- 💰 **Ďobky** (5-600 ď v různých obalech)
- ⚔️ **Kouzelný meč** (1/20 šance, 10 typů, možné prokletí)
- ✨ **Náhodné kouzlo** (2d8, hodnota 100-600 ď)
- 🎁 **Drobnosti** (6 magických předmětů)
- 💎 **Cenný poklad** (šperky, 100-1500 ď)
- 📦 **Objemný poklad** (cenné, ale zabírá 2-6 políček)
- 🔮 **Neobvyklý poklad** (speciální kupci)
- 🛠️ **Užitečný poklad** (zásoby, pochodně, zbraně, zbroje, nástroje)

**Příklad výstupu:**
- Pytel s 50 ďobků (50 ď, 1 políčko)
- Kouzelný meč: Vlčí zub - Lehká (k6), neprokletý
- Broušený diamant (1000 ď, šperk)
- 3× Zásoby (15 ď, ○○○ každé)

### 📖 8. Generování semínek dobrodružství
```bash
# Základní semínko (jeden hod k66)
python -m src.cli generate adventure

# Custom kombinace (tři hody k66)
python -m src.cli generate adventure --custom

# S inspiračním textem pro GM
python -m src.cli generate adventure --inspiration

# JSON výstup
python -m src.cli generate adventure --json

# Uložit do souboru
python -m src.cli generate adventure --save seed.json
```

**Co je semínko dobrodružství:**
- **Tvor** (KDO) - Kdo je zapojen do situace
- **Problém** (CO) - Co se stalo
- **Komplikace** (JAK) - Co to zhoršuje

**Dva způsoby generování:**
1. **Základní** - Jeden hod k66 → celý řádek (kompletní příběh)
2. **Custom** - Tři hody k66 → mix a match ze sloupců

**Příklady:**
- Rybář / Obviněn ze zločinu / Může za to pomocník hráčské myši
- Pokusná myš / Je na útěku před lidmi / Sledují ho pomocí čipu
- Káčátko / Ztratilo maminku / Potřebuje se dostat na ostrov

**Inspirační text:**
- Otázky pro rozvíjení (Kde? Proč? Jak? Co když?)
- Nápady na motivace, vzhled, odměnu

### 🏠 9. Generování hospod
```bash
# Základní hospoda
python -m src.cli generate tavern

# JSON výstup
python -m src.cli generate tavern --json

# Uložit do souboru
python -m src.cli generate tavern --save hospoda.json
```

**Co je hospoda:**
- **Název** (2× k12) - "U [Přídavné jméno] [Podstatné jméno]"
- **Specialita** (k12) - Pokrm nebo nápoj

**Kdy se objevují:**
- Ve vískách (50-150 myší) a větších osadách
- Poskytují jídlo, pití a přístřeší

**Příklady:**
- U Bílého Brouka - Pečená kořeněná mrkev
- U Černého Orela - Tlustý rybí řízek
- U Přátelského Sýra - Semínka pražená v medu

**Součást:**
- Tavern je součást Settlement Generatoru
- Používá se pro vísky a větší osady

### 🎲 10. Hody kostkami
```bash
python -m src.cli roll-dice d6
python -m src.cli roll-dice d20
python -m src.cli roll-dice 2d6
python -m src.cli roll-dice d66
```

### 🎯 11. Test vlastnosti
```bash
python -m src.cli test 12
python -m src.cli test 10 --modifier 2
```

### ❓ 12. Zobrazit help
```bash
python -m src.cli --help
python -m src.cli generate --help
```

### 🧪 13. Spustit testy
```bash
python test_character_simple.py
python test_tableloader.py
python -m tests.test_weather_generator
python -m tests.test_reaction_generator
python -m tests.test_spell_generator
python -m tests.test_treasure_generator
python -m tests.test_adventure_generator
python -m tests.test_tavern_generator
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
| **Fáze 3A** | ✅ HOTOVO | NPC Generator (2025-10-31) |
| **Fáze 3B** | ✅ HOTOVO | Hireling Generator (2025-11-01) |
| **Fáze 3C** | ✅ HOTOVO | Weather Generator (2025-11-01) |
| **Fáze 3D** | ✅ HOTOVO | Reaction Roll Generator (2025-11-01) |
| **Fáze 3E** | ✅ HOTOVO | Spell Generator (2025-11-01) |
| **Fáze 3F** | ✅ HOTOVO | Treasure Generator (2025-11-01) |
| **Fáze 4A** | ✅ HOTOVO | Adventure Seeds Generator (2025-11-01) |
| **P1 Priority** | ✅ 100% (8/8) | Všechny P1 generátory kompletní |
| **Fáze 3G+** | 🚧 DALŠÍ | Další generátory (Magic Sword, Maze, Settlement) |
| **Fáze 4** | ❌ TODO | Web interface |

---

## 🗂️ Struktura projektu

```
mausritter/
├── src/
│   ├── core/              # Základní moduly
│   │   ├── dice.py        # ✅ Hody kostkami
│   │   ├── models.py      # ✅ Datové modely (Character, NPC, Hireling, Weather)
│   │   └── tables.py      # ✅ Načítání JSON dat
│   ├── generators/
│   │   ├── character.py   # ✅ Generátor postav
│   │   ├── npc.py         # ✅ Generátor NPC
│   │   ├── hireling.py    # ✅ Generátor pomocníků
│   │   └── weather.py     # ✅ Generátor počasí
│   └── cli.py             # ✅ CLI rozhraní
├── data/
│   └── core/
│       ├── origins.json           # ✅ 36 původů postav
│       ├── names_first.json       # ✅ 100 vlastních jmen
│       ├── names_family.json      # ✅ 20 mateřských jmen
│       ├── npc_*.json             # ✅ 6 NPC tabulek
│       ├── hireling_types.json    # ✅ 9 typů pomocníků
│       ├── weather_seasons.json   # ✅ 4 roční období (počasí + události)
│       ├── competitive_mice.json  # ✅ 6 konkurenčních dobrodruhů
│       └── adventure_seeds.json   # ✅ 36 semínek dobrodružství
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
