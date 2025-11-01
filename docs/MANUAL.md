# 📚 Mausritter Tools - Uživatelská příručka

Kompletní česká příručka pro práci s Mausritter Tools.

**Verze:** 1.5
**Datum:** 2025-11-01
**Status:** Fáze 1, 2, 3A, 3B, 3C, 3D, 3E, 3F a 4A dokončeny - **P1 COMPLETE (100%)**

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

### 2.2 Generování NPC

**Hlavní příkaz:**
```bash
python -m src.cli generate npc
```

**Co to dělá:**
Vygeneruje náhodné NPC (nehráčskou myš) pro DM použití podle tabulek z 16_RANDOM_TABLES.md:
- Hoď k100 + k20 pro jméno
- Hoď k6 pro společenské postavení a platbu za služby
- Hoď k6 pro rodné znamení s povahovým rysem
- Hoď k20 pro vzhled
- Hoď k20 pro zvláštnost
- Hoď k20 pro tužbu/motivaci
- Hoď k20 pro vztah k jiné myši
- Hoď 2k6 pro reakci při setkání

#### 2.2.1 Možnosti příkazu

**`--name` / `-n` - Vlastní jméno**
```bash
python -m src.cli generate npc --name "Strážný"
python -m src.cli generate npc -n "Kupec"
```
Použije zadané jméno místo náhodného.

**`--gender` / `-g` - Pohlaví**
```bash
python -m src.cli generate npc --gender female
python -m src.cli generate npc -g male
```
Možnosti: `male` (výchozí), `female`
Určuje tvar příjmení (Hrabal vs. Hrabalová)

**`--json` / `-j` - JSON výstup**
```bash
python -m src.cli generate npc --json
```
Zobrazí NPC jako JSON místo pěkného formátování.

**`--save` / `-s` - Uložit do souboru**
```bash
python -m src.cli generate npc --save npc.json
python -m src.cli generate npc -s npcs/strazny.json
```
Uloží NPC do JSON souboru.

#### 2.2.2 Příklady použití

**Náhodné mužské NPC:**
```bash
python -m src.cli generate npc
```

**Náhodné ženské NPC:**
```bash
python -m src.cli generate npc --gender female
```

**NPC s vlastním jménem:**
```bash
python -m src.cli generate npc --name "Strážný u brány"
```

**Kombinace možností:**
```bash
python -m src.cli generate npc --name "Žermína" --gender female --save zermina.json
```

**5 NPC za sebou pro přípravu session:**
```bash
python -m src.cli generate npc
python -m src.cli generate npc
python -m src.cli generate npc
python -m src.cli generate npc --gender female
python -m src.cli generate npc --gender female
```

#### 2.2.3 Ukázka výstupu

```
┌────────────────────── Šafrán Hrabal ──────────────────────┐
│                                                            │
│  Rodné znamení:                                            │
│    Matka (Pečující/ustaraná)                               │
│                                                            │
│  Vzhled:                                                   │
│    Zaplétaná srst                                          │
│                                                            │
│  Zvláštnost:                                               │
│    Mluví pomalu a rozvážně                                 │
│                                                            │
│  Po čem touží:                                             │
│    Ochrana                                                 │
│                                                            │
│  Vztah k jiné myši:                                        │
│    Bývalí milenci                                          │
│                                                            │
│  Reakce při setkání:                                       │
│    Nepřátelská: Jak se dá uchlácholit?                     │
│                                                            │
│  Platba za služby:                                         │
│    k4 x 1 000 ď                                            │
│                                                            │
└────────────────────── 🎭 Myší šlechtic ────────────────────┘
```

#### 2.2.4 Rozdíl oproti Character Generator

**Character Generator** (`generate character`):
- Pro hráčské postavy
- Plné statistiky (Síla, Mrštnost, Vůle)
- Body ochrany (HP)
- Kompletní inventář a výbava
- Původ postavy s příběhem
- Použití: Tvorba PC na začátku kampaně

**NPC Generator** (`generate npc`):
- Pro nehráčské postavy (DM tool)
- Osobnost a motivace (ne mechaniky)
- Rychlé vytvoření pro session
- Společenské postavení
- Použití: Rychlá příprava NPC během hry

---

### 2.3 Generování pomocníků (Hirelings)

**Hlavní příkaz:**
```bash
python -m src.cli generate hireling
```

**Co to dělá:**
Vygeneruje náhodného pomocníka (hireling) - pronajímatelnou myš s plnými bojovými statistikami podle pravidel z 10_HIRELINGS.md:
- Vygeneruje jméno (k100 + k20)
- Vybere náhodný typ z 9 možností (nebo konkrétní --type)
- Hoď k6 pro HP (Body ochrany)
- Hoď 2k6 pro Sílu, Mrštnost a Vůli
- Vytvoří prázdný inventář (6 slotů)
- Nastaví level 1, XP 0, morálka neutrální
- Vypočítá dostupnost (kolik je jich k najímání)

#### 2.3.1 Možnosti příkazu

**`--type` / `-t` - ID typu pomocníka (1-9)**
```bash
python -m src.cli generate hireling --type 6    # Zbrojmyš
python -m src.cli generate hireling -t 8        # Rytíř
```
Vybere konkrétní typ pomocníka místo náhodného.

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

**`--name` / `-n` - Vlastní jméno**
```bash
python -m src.cli generate hireling --name "Sir Pepřík"
python -m src.cli generate hireling -n "Válečník"
```
Použije zadané jméno místo náhodného.

**`--gender` / `-g` - Pohlaví**
```bash
python -m src.cli generate hireling --gender female
python -m src.cli generate hireling -g male
```
Možnosti: `male` (výchozí), `female`
Určuje tvar příjmení (Hrabal vs. Hrabalová)

**`--json` / `-j` - JSON výstup**
```bash
python -m src.cli generate hireling --json
```
Zobrazí pomocníka jako JSON místo pěkného formátování.

**`--save` / `-s` - Uložit do souboru**
```bash
python -m src.cli generate hireling --save pomocnik.json
python -m src.cli generate hireling -s hirelings/zbrojmys.json
```
Uloží pomocníka do JSON souboru.

#### 2.3.2 Příklady použití

**Náhodný pomocník:**
```bash
python -m src.cli generate hireling
```

**Konkrétní typ - Zbrojmyš:**
```bash
python -m src.cli generate hireling --type 6
```

**Rytíř s vlastním jménem:**
```bash
python -m src.cli generate hireling --type 8 --name "Sir Bedřich"
```

**Kombinace všech možností:**
```bash
python -m src.cli generate hireling --type 6 --name "Válečnice Jana" --gender female --save jana.json
```

#### 2.3.3 Ukázka výstupu

```
┌──────────────────────────────── Sir Pepřík ─────────────────────────────────┐
│                                                                             │
│  Denní mzda: 25 ď                                                           │
│                                                                             │
│  ⚔️ Vlastnosti:                                                              │
│    Síla:       6                                                            │
│    Mrštnost:   6                                                            │
│    Vůle:       5                                                            │
│    BO:        1/1                                                           │
│                                                                             │
│  🎒 Inventář:                                                               │
│    [   ] [   ] [   ]    (packy + tělo)                                      │
│    [   ] [   ] [   ]    (batoh)                                             │
│                                                                             │
│  📊 Postup:                                                                 │
│    Level: 1  |  XP: 0/1000                                                  │
│    Morálka: neutrální                                                       │
│                                                                             │
│  📍 Dostupnost:                                                             │
│    3 pomocníci tohoto typu jsou k dispozici                                 │
│                                                                             │
│  Poznámky:                                                                  │
│    Šlechtický válečník                                                      │
│                                                                             │
└────────────────────────────────── ⚔️ Rytíř ──────────────────────────────────┘
```

#### 2.3.4 Rozdíly mezi generátory

**Character Generator** (`generate character`):
- Pro hráčské postavy
- Plné statistiky + inventář s výbavou podle původu
- Rodné znamení, barva a vzor srsti
- Použití: Tvorba PC na začátku kampaně

**NPC Generator** (`generate npc`):
- Pro nehráčské postavy (DM tool)
- ŽÁDNÉ bojové statistiky
- Osobnost, motivace, společenské postavení
- Použití: Rychlá příprava roleplay NPC během hry

**Hireling Generator** (`generate hireling`):
- Pro pronajímatelné pomocníky
- PLNÉ bojové statistiky (HP, STR/DEX/WIL)
- Prázdný inventář (6 slotů)
- Denní mzda, level, XP, morálka
- Použití: Najímání pomocníků pro party

---

### 2.4 Generování počasí

**Hlavní příkaz:**
```bash
python -m src.cli generate weather
```

**Co to dělá:**
Vygeneruje denní počasí podle ročních období a volitelně sezónní událost podle pravidel z 16_RANDOM_TABLES.md:
- Hoď 2k6 pro denní počasí (podle tabulky pro dané roční období)
- Určí zda je počasí nepříznivé pro cestování
- Volitelně hoď k6 pro sezónní událost

**Nepříznivé počasí:**
Pokud je počasí nepříznivé, každá myš musí při cestování uspět v **záchraně na sílu** každou hlídku, jinak dostane stav **Vyčerpání**.

#### 2.4.1 Možnosti příkazu

**`--season` / `-s` - Roční období**
```bash
python -m src.cli generate weather --season spring   # Jaro
python -m src.cli generate weather --season summer   # Léto
python -m src.cli generate weather --season autumn   # Podzim
python -m src.cli generate weather --season winter   # Zima
```
Možnosti: `spring` (výchozí), `summer`, `autumn`, `winter`

**`--with-event` / `-e` - Zahrnout sezónní událost**
```bash
python -m src.cli generate weather --with-event
python -m src.cli generate weather --season autumn -e
```
Přidá k počasí sezónní událost (hoď k6).

**`--json` / `-j` - JSON výstup**
```bash
python -m src.cli generate weather --json
```
Zobrazí počasí jako JSON místo pěkného formátování.

**`--save` - Uložit do souboru**
```bash
python -m src.cli generate weather --save weather.json
python -m src.cli generate weather --season winter -e --save winter_event.json
```
Uloží počasí do JSON souboru.

#### 2.4.2 Příklady použití

**Náhodné jarní počasí (default):**
```bash
python -m src.cli generate weather
```

**Zimní počasí:**
```bash
python -m src.cli generate weather --season winter
```

**Podzimní počasí s událostí:**
```bash
python -m src.cli generate weather --season autumn --with-event
```

**Kombinace všech možností:**
```bash
python -m src.cli generate weather --season summer --with-event --save leto.json
```

#### 2.4.3 Pravděpodobnosti nepříznivého počasí

**Jaro (Spring):** 2.78% šance
- Pouze "Přívalové deště" (hod 2 na 2k6)

**Léto (Summer):** 27.78% šance
- "Úmorné vedro" (hody 3-5 na 2k6)

**Podzim (Autumn):** 2.78% šance
- Pouze "Silný vítr" (hod 2 na 2k6)

**Zima (Winter):** 72.22% šance ❄️
- "Vánice" (hod 2)
- "Mrznoucí déšť" (hody 3-5)
- "Třeskutá zima" (hody 6-8)

#### 2.4.4 Ukázka výstupu

**Příznivé počasí (jaro):**
```
┌────────────────────────────────── 🌸 Jaro ──────────────────────────────────┐
│                                                                             │
│  Počasí: Jasno a slunečno                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Nepříznivé počasí (zima):**
```
┌────────────────────────────────── ❄️ Zima ───────────────────────────────────┐
│                                                                             │
│  Počasí: Třeskutá zima                                                      │
│                                                                             │
│  ⚠️  NEPŘÍZNIVÉ pro cestování                                                │
│                                                                             │
│  Každá myš musí při cestování uspět v záchraně na sílu                      │
│  každou hlídku, jinak dostane stav Vyčerpání.                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**S událostí (podzim):**
```
┌───────────────────────────────── 🍂 Podzim ─────────────────────────────────┐
│                                                                             │
│  Počasí: Chladno                                                            │
│                                                                             │
│  Sezónní událost:                                                           │
│  Vichřice povalila důležitý strom                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.5 Generování reakcí

**Hlavní příkaz:**
```bash
python -m src.cli generate reaction
```

**Co to dělá:**
Vygeneruje reakci NPC nebo tvora při setkání podle pravidel z 08_GM_GUIDE.md:
- Hoď 2k6 pro určení počáteční dispozice
- Poskytne GM otázku pro inspiraci k roleplayi
- Umožňuje modifikátory podle kontextu

**Kdy použít:**
- Při setkání s tvorem, když není jasné jak bude reagovat
- Pro určení počáteční nálady NPC vůči hráčům
- Kdykoliv potřebuješ rychlé rozhodnutí o chování NPC

#### 2.5.1 Možnosti příkazu

**`--modifier` / `-m` - Modifikátor k hodu**
```bash
python -m src.cli generate reaction --modifier 1    # +1 pro příznivé okolnosti
python -m src.cli generate reaction -m -2            # -2 pro nepříznivé okolnosti
```

**Běžné modifikátory:**
- **+1** - Myši přinesly dárek nebo nabídly pomoc
- **-1** - Myši jsou agresivní nebo rušivé
- **-2** - Tvor byl nedávno napaden
- **+2** - Tvor je ve výrazně dobré náladě

**`--json` / `-j` - JSON výstup**
```bash
python -m src.cli generate reaction --json
```
Zobrazí reakci jako JSON místo pěkného formátování.

**`--save` - Uložit do souboru**
```bash
python -m src.cli generate reaction --save reaction.json
python -m src.cli generate reaction -m 1 --save friendly.json
```
Uloží reakci do JSON souboru.

#### 2.5.2 Příklady použití

**Základní reakce:**
```bash
python -m src.cli generate reaction
```

**Reakce s pozitivním modifikátorem:**
```bash
python -m src.cli generate reaction --modifier 1
```

**Reakce s negativním modifikátorem:**
```bash
python -m src.cli generate reaction -m -2
```

**Kombinace s uložením:**
```bash
python -m src.cli generate reaction --modifier 1 --save npc_reaction.json
```

#### 2.5.3 Typy reakcí (2k6)

| Hod | Reakce | Pravděpodobnost | Popis |
|-----|--------|-----------------|-------|
| **2** | Agresivní ⚔️ | 2.78% | Tvor útočí nebo je extrémně nepřátelský |
| **3-5** | Nepřátelská 😠 | 25.00% | Tvor je nedůvěřivý a nepřátelský |
| **6-8** | Nejistá 🤔 | 41.67% | Tvor je opatrný, ale otevřený dialogu |
| **9-11** | Povídavá 😊 | 25.00% | Tvor je přátelský a komunikativní |
| **12** | Nápomocná 💚 | 2.78% | Tvor je velmi vstřícný a ochotný pomoci |

#### 2.5.4 Ukázka výstupu

**Nejistá reakce:**
```
┌─────────────────────────────── 🤔 Reakce NPC ───────────────────────────────┐
│                                                                             │
│  Hod: 7 (2k6)                                                               │
│  Reakce: Nejistá                                                            │
│                                                                             │
│  GM otázka:                                                                 │
│  Jak si ho můžou naklonit?                                                  │
│                                                                             │
│  💡 Tip: Toto je počáteční dispozice, může se změnit podle chování hráčů.   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Povídavá reakce s modifikátorem:**
```
┌─────────────────────────────── 😊 Reakce NPC ───────────────────────────────┐
│                                                                             │
│  Hod: 10 (2k6)                                                              │
│  Reakce: Povídavá                                                           │
│                                                                             │
│  GM otázka:                                                                 │
│  Nemůže mít něco na obchod nebo výměnu?                                     │
│                                                                             │
│  Modifikátor: +1                                                            │
│                                                                             │
│  💡 Tip: Toto je počáteční dispozice, může se změnit podle chování hráčů.   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**JSON výstup:**
```json
{
  "roll": 7,
  "reaction": "Nejistá",
  "question": "Jak si ho můžou naklonit?",
  "notes": ""
}
```

#### 2.5.5 GM tipy

**Interpretace reakcí:**
- **Agresivní:** Okamžité nebezpečí, vyžaduje rychlou akci hráčů
- **Nepřátelská:** Vyjednávání je možné, ale obtížné
- **Nejistá:** Ideální pro roleplay a diplomacii
- **Povídavá:** Otevřená k obchodu, informacím, nebo spojenectví
- **Nápomocná:** Může nabídnout quest hook nebo významnou pomoc

**Změna reakce během hry:**
- Počáteční reakce není konečná
- Chování hráčů může posunout reakci nahoru i dolů
- Použij další hod 2k6 pokud se situace dramaticky změní

---

### 2.6 Generování kouzel

**Hlavní příkaz:**
```bash
python -m src.cli generate spell
```

**Co to dělá:**
Vygeneruje náhodné kouzlo z oficiálních Mausritter pravidel (2d8 tabulka, 16 kouzel).

#### 2.6.1 Možnosti příkazu

```bash
--json              # Výstup v JSON formátu
--save <soubor>     # Ulož do souboru
```

#### 2.6.2 Příklady použití

**Základní generování:**
```bash
python -m src.cli generate spell
```

**JSON export:**
```bash
python -m src.cli generate spell --json
```

**Uložit do souboru:**
```bash
python -m src.cli generate spell --save kouzlo.json
```

#### 2.6.3 Všechna kouzla (2d8)

**16 kouzel z oficiálních pravidel:**
- Ohnivá koule, Zahojení, Kouzelná střela, Strach
- Tma, Zotavení, Srozumitelnost, Přízračný brouk
- Světlo, Neviditelný prstenec, Zaklepání, Tuk
- Zvětšení, Neviditelnost, Deštník, Šanta

**Poznámka:** Placeholdery `[POČET]` a `[SOUČET]` se nahrazují při sesílání:
- `[POČET]` = počet kostek
- `[SOUČET]` = součet hodu

#### 2.6.4 Ukázka výstupu

```
═══ KOUZLO ═══

✨ Název: Ohnivá koule

📜 Efekt:
Vystřelí [POČET] ohnivých koulí. Každá způsobí k6 poškození.

🔋 Dobití:
Spálit předmět velikosti myši v plamenech

🎲 Hod 2d8: 2 (1+1)
```

---

### 2.7 Generování pokladů

**Hlavní příkaz:**
```bash
python -m src.cli generate treasure
```

**Co to dělá:**
Vygeneruje kompletní treasure hoard (2-6 položek) podle oficiálních Mausritter pravidel.

#### 2.7.1 Možnosti příkazu

```bash
--bonus <0-4>       # Bonusové hody k20 (default: 0)
-b <0-4>            # Krátká verze --bonus
--json              # Výstup v JSON formátu
--save <soubor>     # Ulož do souboru
```

#### 2.7.2 Bonusové hody

**4 otázky pro určení bonusů (+1 hod k20 za každou kladnou odpověď):**

1. Je v **bývalé myší osadě / hradě / jeskyni**?
2. Je ve **vysoce magické oblasti**?
3. Brání ho **velké zvíře / záludná past**?
4. Překonaly myši **velké nesnáze**?

**Mechanika:**
- Základní poklad: 2× k20
- S bonusy: 2-6× k20
- Každý hod může vést k dalším hodům na podtabulky

#### 2.7.3 Příklady použití

**Základní poklad (2× k20):**
```bash
python -m src.cli generate treasure
```

**S bonusy:**
```bash
python -m src.cli generate treasure --bonus 2    # 4× k20
python -m src.cli generate treasure -b 4         # 6× k20
```

**JSON export:**
```bash
python -m src.cli generate treasure --bonus 3 --json
```

**Uložit do souboru:**
```bash
python -m src.cli generate treasure --save hoard.json
```

#### 2.7.4 Co může být v pokladu

**Typy položek:**
- 💰 **Ďobky** (5-600 ď v různých obalech)
- ⚔️ **Kouzelný meč** (5% šance, 10 typů, možné prokletí)
- ✨ **Náhodné kouzlo** (5% šance, 2d8, hodnota 100-600 ď)
- 🎁 **Drobnosti** (6 magických předmětů)
- 💎 **Cenný poklad** (šperky, umělecké předměty, 100-1500 ď)
- 📦 **Objemný poklad** (cenné, ale zabírá 2-6 políček)
- 🔮 **Neobvyklý poklad** (vzácné, speciální kupci)
- 🛠️ **Užitečný poklad** (zásoby, pochodně, zbraně, zbroje, nástroje)

#### 2.7.5 Kouzelné meče

**Generování:**
- Typ zbraně (k6): Střední/Lehká/Těžká
- Schopnost meče (k10): 10 různých efektů
- Prokletí (1/6 šance, k6): 6 typů kleteb

**Příklad:**
```
⚔️ Kouzelný meč: Vlčí zub
- Typ: Lehká (k6 poškození)
- Schopnost: Každý úspěšný zásah obnovuje 1 HP
- Prokletí: Neprokletý ✅
- Hodnota: 500 ď, 1 políčko
```

#### 2.7.6 Ukázka výstupu

```
═══ TREASURE HOARD ═══

💰 Poklad #1: Pytel s 50 ďobků
   💵 50 ď | 📦 1 políčko

⚔️ Poklad #2: Kouzelný meč: Vlčí zub
   Typ: Lehká (k6)
   Schopnost: Každý úspěšný zásah obnovuje 1 HP
   Prokletí: Neprokletý ✅
   💵 500 ď | 📦 1 políčko

💎 Poklad #3: Broušený diamant
   Typ: Cenný poklad (šperk)
   💵 1000 ď | 📦 1 políčko

🛠️ Poklad #4: 3× Zásoby
   Každé: 💵 5 ď | 📦 ○ | ⚪⚪⚪ použití

───────────────────────────────
CELKEM: 4 položky, 1515 ď, 4 políčka
```

---

### 2.8 Generování semínek dobrodružství

**Hlavní příkaz:**
```bash
python -m src.cli generate adventure
```

**Co to dělá:**
Vygeneruje semínko dobrodružství - kombinaci Tvora, Problému a Komplikace (k66 tabulka, 36 možností).

#### 2.8.1 Možnosti příkazu

```bash
--custom, -c        # Hoď na každý sloupec zvlášť (3× k66)
--inspiration, -i   # Zobraz inspirační text pro GM
--json              # Výstup v JSON formátu
--save <soubor>     # Ulož do souboru
```

#### 2.8.2 Dva způsoby generování

**Podle oficiálních pravidel:**

**Varianta A: "Hoď jednou a přečti celý řádek"**
```bash
python -m src.cli generate adventure
```
- 1× k66 hod
- Získáš kompletní řádek: Tvor + Problém + Komplikace
- Rychlé, hotové semínko dobrodružství

**Varianta B: "Hoď na každý sloupec zvlášť"**
```bash
python -m src.cli generate adventure --custom
```
- 3× k66 hody
- Každý hod určí jeden sloupec
- Kreativní mix & match kombinace

#### 2.8.3 Struktura semínka

Každé semínko má tři části:

- 🎭 **Tvor** (KDO) - Kdo je zapojen do situace
- ⚠️ **Problém** (CO) - Co se stalo
- 💥 **Komplikace** (JAK) - Co to zhoršuje

#### 2.8.4 Příklady použití

**Základní generování:**
```bash
python -m src.cli generate adventure
```

**Custom kombinace:**
```bash
python -m src.cli generate adventure --custom
```

**S inspiračním textem:**
```bash
python -m src.cli generate adventure --inspiration
python -m src.cli generate adventure -c -i  # custom + inspirace
```

**JSON export:**
```bash
python -m src.cli generate adventure --json
```

**Uložit do souboru:**
```bash
python -m src.cli generate adventure --save seed.json
```

#### 2.8.5 Inspirační text

S flaggem `--inspiration` získáš:
- Otázky k rozvíjení každé části (KDO/CO/JAK)
- GM tipy na motivace, vzhled, odměnu
- Praktické otázky (Kde? Proč? Jak? Co když?)

#### 2.8.6 Ukázka výstupu

**Základní:**
```
═══ SEMÍNKO DOBRODRUŽSTVÍ ═══

🎭 Tvor: Pokusná myš
⚠️  Problém: Je na útěku před lidmi
💥 Komplikace: Sledují ho pomocí čipu

📜 (Hod k66: 33)
```

**S inspirací:**
```
═══ SEMÍNKO DOBRODRUŽSTVÍ ═══

🎭 Tvor: Káčátko
⚠️  Problém: Ztratilo maminku
💥 Komplikace: Potřebuje se dostat na ostrov

💡 INSPIRACE PRO GM:

KDO: Káčátko
  → Jaké má motivace? Jak vypadá?

CO: Ztratilo maminku
  → Jak se to stalo? Kde to je?

JAK: Potřebuje se dostat na ostrov
  → Proč je to složité? Co může selhat?

❓ OTÁZKY K ROZVÍJENÍ:
  - Kde se hráčské myši s tímto setkají?
  - Proč by jim mělo záležet?
  - Jaká je odměna za pomoc?
  - Co se stane, když to ignorují?
```

#### 2.8.7 Příklady semínek

**Z oficiálních pravidel (36 možností):**
- Rybář / Obviněn ze zločinu / Může za to pomocník hráčské myši
- Pokusná myš / Je na útěku před lidmi / Sledují ho pomocí čipu
- Káčátko / Ztratilo maminku / Potřebuje se dostat na ostrov
- Pavoučí babizna / Ztratila starodávný poklad / Snědla ho
- Kočičí pán / Chce se nechat bavit / Uvěznil hráčské myši

#### 2.8.8 GM tipy

**Jak používat semínka:**
1. Vygeneruj semínko na začátku přípravy
2. Rozviň každou část otázkami (použij --inspiration)
3. Přidej konkrétní detaily z tvého světa
4. Umísti do hexcrawl mapy nebo jako quest hook

**Pro improvizaci:**
- Vygeneruj během hry pokud hráči změní plány
- Custom kombinace pro překvapivé zápletky
- Kombinuj s NPC generátorem pro bohaté postavy

---

### 2.9 Hody kostkami

**Hlavní příkaz:**
```bash
python -m src.cli roll-dice <kostka>
```

**Co to dělá:**
Hodí zadanou kostkou a zobrazí výsledek.

#### 2.9.1 Podporované kostky

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

#### 2.9.2 Ukázka výstupu

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

### 2.10 Testy vlastností

**Hlavní příkaz:**
```bash
python -m src.cli test <hodnota>
```

**Co to dělá:**
Roll-under test - hodí k20, úspěch pokud je výsledek ≤ hodnota vlastnosti.

#### 2.10.1 Možnosti příkazu

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

#### 2.10.2 Ukázka výstupu

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

### 2.11 Help a nápověda

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
python -m src.cli generate npc --help
python -m src.cli generate hireling --help
python -m src.cli generate weather --help
python -m src.cli generate reaction --help
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

#### 📄 `src/generators/npc.py` - Generátor NPC

**Co to je:**
Generátor náhodných NPC (nehráčských myší) pro rychlé použití během hry.

**Hlavní třída: `NPCGenerator`**

**Statické metody:**
- `generate_name(gender="male")` → vygeneruj náhodné jméno
- `generate_social_status()` → určí společenské postavení a platbu
- `generate_birthsign()` → rodné znamení s povahovým rysem
- `generate_appearance()` → vzhled (k20)
- `generate_quirk()` → zvláštnost (k20)
- `generate_desire()` → tužba/motivace (k20)
- `generate_relationship()` → vztah k jiné myši (k20)
- `generate_reaction()` → reakce při setkání (2k6)
- `create(name=None, gender="male")` → **hlavní metoda** - vytvoř celé NPC
  - Vrací: NPC instance
- `to_dict(npc)` → konvertuj NPC do dictionary
- `to_json(npc)` → konvertuj NPC do JSON stringu

**Status:** ✅ HOTOVO (Fáze 3A)

**Příklad použití v kódu:**
```python
from src.generators.npc import NPCGenerator

# Vygeneruj náhodné NPC
npc = NPCGenerator.create()

# S vlastním jménem
npc = NPCGenerator.create(name="Strážný")

# Ženské NPC
npc = NPCGenerator.create(gender="female")

# Export do JSON
json_str = NPCGenerator.to_json(npc)
```

**Postup generování:**
1. Generuj/použij jméno (k100 + k20)
2. Hoď k6 pro společenské postavení
3. Hoď k6 pro rodné znamení
4. Hoď k20 pro vzhled
5. Hoď k20 pro zvláštnost
6. Hoď k20 pro tužbu
7. Hoď k20 pro vztah
8. Hoď 2k6 pro reakci
9. Vrať NPC objekt

**Datové zdroje:**
- `data/core/npc_social_status.json` - 6 úrovní postavení (k6)
- `data/core/npc_appearance.json` - 20 vzhledů (k20)
- `data/core/npc_quirk.json` - 20 zvláštností (k20)
- `data/core/npc_desire.json` - 20 tužeb (k20)
- `data/core/npc_relationship.json` - 20 vztahů (k20)
- `data/core/npc_reaction.json` - 5 reakcí (2k6)

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

#### 📄 `data/core/npc_*.json` - 6 NPC tabulek

**Status:** ✅ HOTOVO (Fáze 3A)

**Soubory:**
1. **npc_social_status.json** - Společenské postavení (k6)
2. **npc_appearance.json** - Vzhled (k20)
3. **npc_quirk.json** - Zvláštnost (k20)
4. **npc_desire.json** - Po čem touží (k20)
5. **npc_relationship.json** - Vztah k jiné myši (k20)
6. **npc_reaction.json** - Reakce při setkání (2k6)

**Struktura příkladu (npc_social_status.json):**
```json
{
  "metadata": {
    "source": "docs/knowledge_base/16_RANDOM_TABLES.md",
    "description": "Společenské postavení NPC myší",
    "dice": "d6"
  },
  "social_statuses": [
    {
      "roll": 1,
      "status": "Chuďas",
      "payment": "k6 ď"
    },
    ...
  ]
}
```

**Lookup:** Podle hodu kostky (k6, k20, nebo 2k6)

---

#### 📄 Rozšířené NPC tabulky - 7 souborů

**Status:** ✅ HOTOVO (Fáze 3A)

**Soubory:**
1. **hireling_types.json** - 9 typů pronajímatelných pomocníků + statistiky
2. **competitive_mice.json** - 6 konkurenčních myších dobrodruhů
3. **cat_lords.json** - 6 kočičích pánů a paní
4. **rat_gangs.json** - 6 krysích gangů
5. **owl_wizards.json** - 6 sovích čarodějů
6. **frog_knights.json** - 6 žabích rytířů
7. **adventure_seeds.json** - 36 semínek dobrodružství (k66 tabulka)

**Použití:** Připraveno pro budoucí rozšíření NPC generátoru (hirelings, předpřipravené NPC, adventure hooks)

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

#### 🎯 P1 Priority - COMPLETE (8/8) 🎉

| Komponenta | Soubor | Popis | Status |
|------------|--------|-------|--------|
| **Character gen** | `src/generators/character.py` | Generátor postav | ✅ HOTOVO |
| **NPC gen** | `src/generators/npc.py` | Generátor NPC | ✅ HOTOVO |
| **Hireling gen** | `src/generators/hireling.py` | Generátor pomocníků | ✅ HOTOVO |
| **Weather gen** | `src/generators/weather.py` | Generátor počasí | ✅ HOTOVO |
| **Reaction gen** | `src/generators/reaction.py` | Generátor reakcí | ✅ HOTOVO |
| **Spell gen** | `src/generators/spell.py` | Generátor kouzel | ✅ HOTOVO |
| **Treasure gen** | `src/generators/treasure.py` | Generátor pokladů | ✅ HOTOVO |
| **Adventure gen** | `src/generators/adventure.py` | Generátor semínek dobrodružství | ✅ HOTOVO |

#### 🧱 Základní systémy

| Komponenta | Soubor | Popis | Status |
|------------|--------|-------|--------|
| **Dice roller** | `src/core/dice.py` | Všechny typy kostek, k66 | ✅ HOTOVO |
| **Data models** | `src/core/models.py` | 8 dataclass modelů | ✅ HOTOVO |
| **Table loader** | `src/core/tables.py` | Načítání JSON dat, LRU cache | ✅ HOTOVO |
| **CLI** | `src/cli.py` | Příkazový řádek, 11 příkazů | ✅ HOTOVO |

#### 📦 Data tabulky

| Data | Soubor | Položek | Status |
|------|--------|---------|--------|
| **Origins** | `data/core/origins.json` | 36 původů | ✅ HOTOVO |
| **Names** | `data/core/names_*.json` | 120 jmen | ✅ HOTOVO |
| **NPC tables** | `data/core/npc_*.json` | 6 tabulek | ✅ HOTOVO |
| **Hirelings** | `data/core/hireling_*.json` | 9 typů | ✅ HOTOVO |
| **Weather** | `data/core/weather_seasons.json` | 4 roční období | ✅ HOTOVO |
| **Spells** | `data/core/spells.json` | 16 kouzel | ✅ HOTOVO |
| **Treasure** | `data/treasure/*.json` | 9 tabulek | ✅ HOTOVO |
| **Adventure seeds** | `data/core/adventure_seeds.json` | 36 semínek | ✅ HOTOVO |

#### 🧪 Testy

| Test suite | Soubor | Testů | Status |
|------------|--------|-------|--------|
| **Character** | `tests/test_character_*.py` | 16 testů | ✅ HOTOVO |
| **NPC** | `tests/test_npc_generator.py` | 19 testů | ✅ HOTOVO |
| **Weather** | `tests/test_weather_generator.py` | 14 testů | ✅ HOTOVO |
| **Reaction** | `tests/test_reaction_generator.py` | 14 testů | ✅ HOTOVO |
| **Spell** | `tests/test_spell_generator.py` | 15 testů | ✅ HOTOVO |
| **Treasure** | `tests/test_treasure_generator.py` | 23 testů | ✅ HOTOVO |
| **Adventure** | `tests/test_adventure_generator.py` | 20 testů | ✅ HOTOVO |

**Celkem:** 121+ testů, všechny prošly ✅

**Dokončené fáze:**
- ✅ **Fáze 1:** Data extraction (2025-10-29)
- ✅ **Fáze 2:** Character Generator (2025-10-29)
- ✅ **Fáze 3A:** NPC Generator (2025-10-31)
- ✅ **Fáze 3B:** Hireling Generator (2025-11-01)
- ✅ **Fáze 3C:** Weather Generator (2025-11-01)
- ✅ **Fáze 3D:** Reaction Roll Generator (2025-11-01)
- ✅ **Fáze 3E:** Spell Generator (2025-11-01)
- ✅ **Fáze 3F:** Treasure Generator (2025-11-01)
- ✅ **Fáze 4A:** Adventure Seeds Generator (2025-11-01)

**Celková dokončenost:** ~29% (8/28 generátorů), **P1: 100% (8/8)** 🎉

### 📋 Co bude dál (P2 Priority)

**Nástroje pro tvorbu světa:**
- 📝 Settlement Generator (generátor myších osad)
- 📝 Tavern Generator (generátor hospod)
- 📝 Hex Generator (generátor hexů pro hexcrawl)
- 📝 Dungeon/Adventure Site Generator (generátor dobrodružných míst)
- 📝 Adventure Hook Generator (generátor háčků dobrodružství)
- 📝 Rumor Framework (framework pro tvorbu zvěstí)

**Fáze 4:** Web interface
- ❌ FastAPI backend
- ❌ HTML frontend
- ❌ REST API
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
