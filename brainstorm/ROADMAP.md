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

#### 2. ✅ Generátor NPC myší
**Název:** NPC Generator / Generátor nehráčských myší
**Popis:** Rychlé vytváření NPC - společenské postavení, vzhled, zvláštnosti, touhy, vztahy
**Zdroj:** `16_RANDOM_TABLES.md` (řádky 15-140)
**Složitost:** ⭐⭐ Jednoduchá
**Stav:** ✅ **HOTOVO** - Fáze 3A (2025-10-31)
**Tabulky:** Společenské postavení (k6), Rodné znamení (k6), Vzhled (k20), Zvláštnost (k20), Po čem touží (k20), Vztah (k20), Reakce (2k6)
**Priorita:** Vysoká - podobné Character Generatoru, ale rychlejší
**CLI:** `python -m src.cli generate npc`
**Testy:** 19 unit testů (všechny prošly ✅)

#### 3. ✅ Generátor počasí
**Název:** Weather Generator / Generátor počasí a sezónních událostí
**Popis:** Určení počasí (2k6) podle ročního období + sezónní události (k6)
**Zdroj:** `16_RANDOM_TABLES.md` (řádky 194-293)
**Složitost:** ⭐ Velmi jednoduchá
**Stav:** ✅ **HOTOVO** - Fáze 3C (2025-11-01)
**Tabulky:** Jaro/Léto/Podzim/Zima - každé má počasí (2k6) + události (k6)
**Priorita:** Střední - rychlá implementace, používá se denně v hexcrawl
**CLI:** `python -m src.cli generate weather --season winter --with-event`
**Testy:** 14 unit testů (všechny prošly ✅)

#### 4. ✅ Tabulka reakcí
**Název:** Reaction Roll / Tabulka reakcí tvorů
**Popis:** Určení nálady tvora při setkání (2k6)
**Zdroj:** `08_GM_GUIDE.md` (řádky 213-224)
**Složitost:** ⭐ Velmi jednoduchá
**Stav:** ✅ **HOTOVO** - Fáze 3D (2025-11-01)
**Tabulka:** 2k6 - Agresivní (2), Nepřátelská (3-5), Nejistá (6-8), Povídavá (9-11), Nápomocná (12)
**Priorita:** Vysoká - používá se v každém setkání
**CLI:** `python -m src.cli generate reaction --modifier 0`
**Testy:** 14 unit testů (všechny prošly ✅)

#### 5. ✅ Generátor pokladů
**Název:** Treasure Generator / Generátor pokladů
**Popis:** Určení obsahu pokladu - ďobky, předměty, kouzelné meče, kouzla
**Zdroj:** `15_TREASURE.md` (řádky 17-115)
**Složitost:** ⭐⭐⭐ Střední až složitá
**Stav:** ✅ **HOTOVO** - Fáze 3F (2025-11-01)
**Tabulky:** Hlavní (k20), Drobnosti (k6), Cenný (k6), Objemný (k6), Neobvyklý (k6), Užitečný (k6), Meče + Kouzla
**Priorita:** Vysoká - důležité pro odměňování hráčů
**CLI:** `python -m src.cli generate treasure --bonus 0-4`
**Testy:** 23 unit testů (všechny prošly ✅)
**Mechanika:**
- 2-6× k20 na hlavní tabulku (2 základní + 0-4 bonusové)
- Bonusové hody za: bývalá osada, magická oblast, velké zvíře, velké nesnáze
- Generuje: ďobky (5-600 ď), kouzelné meče (1/20), kouzla (1/20), předměty z 5 podtabulek
**Součásti:** Obsahuje generátor kouzelných mečů (typ, schopnost, prokletí) a nástroje/zbroje

#### 6. ✅ Generátor kouzelných mečů
**Název:** Magic Sword Generator / Generátor kouzelných mečů
**Popis:** Typ zbraně (k6), schopnost (k10), šance na prokletí (1/6), typ kletby (k6)
**Zdroj:** `15_TREASURE.md` (řádky 118-216)
**Složitost:** ⭐⭐ Střední
**Stav:** ✅ **HOTOVO** - Integrováno do Treasure Generatoru (Fáze 3F)
**Tabulky:** Typ (k6), 10 druhů mečů, Prokletí (k6)
**Priorita:** Střední - součást Treasure Generatoru
**Poznámka:** Tato funkcionalita je plně implementovaná jako součást TreasureGeneratoru

#### 7. ✅ Generátor semínek dobrodružství
**Název:** Adventure Seeds / Generátor semínek dobrodružství
**Popis:** Kombinace Tvor + Problém + Komplikace (k66 tabulka)
**Zdroj:** `16_RANDOM_TABLES.md` (řádky 143-191)
**Složitost:** ⭐⭐ Střední
**Stav:** ✅ **HOTOVO** - Fáze 4A (2025-11-01)
**Tabulka:** k66 (36 kombinací)
**Priorita:** Střední - inspirace pro PJ při tvorbě questů
**CLI:** `python -m src.cli generate adventure --custom --inspiration`
**Testy:** 20 unit testů (všechny prošly ✅)
**Mechanika:**
- Základní: 1× k66 → celý řádek (Tvor + Problém + Komplikace)
- Custom: 3× k66 → kombinace ze sloupců (mix & match)
- Inspirační text pro GM s otázkami na rozvíjení příběhu

#### 8. ✅ Generátor kouzel
**Název:** Spell Generator / Generátor náhodných kouzel
**Popis:** Náhodné kouzlo z tabulky (2k8 na 16 kouzel)
**Zdroj:** `06_MAGIC.md` (řádky 83-107)
**Složitost:** ⭐ Velmi jednoduchá
**Stav:** ✅ **HOTOVO** - Fáze 3E (2025-11-01)
**Tabulka:** 2k8 - 16 kouzel s efekty ([POČET]/[SOUČET] placeholdery) a podmínkami dobití
**Priorita:** Střední - náhodné nalezení kouzel
**CLI:** `python -m src.cli generate spell`
**Testy:** 15 unit testů (všechny prošly ✅)

---

### P2: Nástroje pro tvorbu světa (6 generátorů) 🟡

Tyto generátory se používají **při přípravě kampaně** a tvorby hexcrawl mapy.

#### 9. 📝 Generátor myších osad
**Název:** Settlement Generator / Generátor myších osad
**Popis:** Velikost, společenské zřízení, podrobnosti, živnost, výrazné prvky, události, název
**Zdroj:** `12_SETTLEMENTS.md` (řádky 22-237)
**Složitost:** ⭐⭐⭐ Střední
**Stav:** ✅ **HOTOVO** - Fáze 4C (2025-11-02)
**Tabulky:** Velikost (2k6 nižší), Zřízení (k6+velikost), Podrobnosti (k20), Živnost (k20), Prvky (k20), Události (k20), Název (4×k12)
**Priorita:** Vysoká - klíčové pro hexcrawl
**CLI:** `python -m src.cli generate settlement --json --name --no-tavern`
**Testy:** 20+ unit testů (všechny prošly ✅)
**Poznámka:** Integruje TavernGenerator pro osady velikosti 3+ (víska a větší)

#### 10. ✅ Generátor hospod a hostinců
**Název:** Tavern Generator / Generátor hospod
**Popis:** Název hospody (2×k12), specialita hostince (k12)
**Zdroj:** `12_SETTLEMENTS.md` (řádky 240-296)
**Složitost:** ⭐ Velmi jednoduchá
**Stav:** ✅ **HOTOVO** - Fáze 4B (2025-11-02)
**Tabulky:** Část 1 (k12), Část 2 (k12), Specialita (k12)
**Priorita:** Nízká - doplněk Settlement Generatoru
**CLI:** `python -m src.cli generate tavern --json`
**Testy:** 14 unit testů (všechny prošly ✅)
**Poznámka:** Bottom-up implementace - nejmenší komponenta Settlement Generatoru

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
| **P1 🔴** | 8 | 5 ✅ | 3 📝 | Základní PJ nástroje - nutné pro hru |
| **P2 🟡** | 6 | 0 ✅ | 6 📝 | Nástroje pro tvorbu světa - důležité pro kampaň |
| **P3 🟢** | 14 | 0 ✅ | 14 💡 | Varianty tvorů - volitelné, ale atmosférické |
| **CELKEM** | **28** | **5** | **23** | |

### 🎯 Doporučené pořadí implementace (Bottom-up podle závislostí)

**📊 STROM ZÁVISLOSTÍ:**
```
Úroveň 1: Tavern Generator ✅ (4B)
              ↓
Úroveň 2: Settlement Generator ✅ (4C) - používá Tavern
              ↓
Úroveň 3: Hex Generator (6A) + Dungeon Generator (6B) - používají Settlement
              +
          Adventure Hooks (4D) + Creature Variants (5×) - žádné závislosti
```

**Fáze 3 - Základní PJ nástroje (P1) - HOTOVO:**
1. ✅ Character Generator
2. ✅ NPC Generator
3. ✅ Hireling Generator
4. ✅ Weather Generator
5. ✅ Reaction Roll
6. ✅ Spell Generator
7. ✅ Treasure Generator
8. ✅ Adventure Seeds

**Fáze 4 - Tvorba světa (P2):**
9. ✅ Tavern Generator (4B) - nejmenší komponenta
10. ✅ Settlement Generator (4C) - používá Tavern
11. 📝 **Adventure Hooks (4D)** ← **DALŠÍ! (30-45 min, žádné závislosti)**

**Fáze 5 - Varianty tvorů (P3):**
12-25. 📝 **Creature Variants (5A-N)** - 14× k6 tabulky, žádné závislosti (2-4 hod)

**Fáze 6 - Pokročilé hexcrawl (P2):**
26. 📝 **Hex Generator (6A)** - používá Settlement ✅ (2-3 hod)
27. 📝 **Dungeon Generator (6B)** - používá Settlement ✅ (6-8 hod)
28. 📝 **Rumor Framework** - framework pro zvěsti (volitelné)

---

## 📝 Další kroky

### 🎯 FÁZE 4D: Adventure Hooks Generator (DOPORUČENO JAKO DALŠÍ)

**Priorita:** 🟡 Střední (ale nejjednodušší ze zbývajících)
**Čas:** ~30-45 minut
**Stav:** 📝 Připraveno k implementaci
**Složitost:** ⭐ Velmi jednoduchá
**Závislosti:** ❌ Žádné

**Popis:**
Generátor háčků pro začátek dobrodružství - důvod, proč se myši vydají na výpravu.

**Zdroj:** `11_HEXCRAWL_SETUP.md` (řádky 66-75)

**Co implementovat:**
1. **Data** (10 min)
   - `data/core/adventure_hooks.json` - 6 háčků (k6)
   - Položky: Ztracený člen rodiny, Vyšetřování, Přísada do kouzla, Doupě tvora, Mapa k pokladu, Útočiště před bouřkou

2. **Generátor** (15 min)
   - `src/generators/adventure_hook.py` - AdventureHookGenerator
   - Metody: `create()`, `to_dict()`, `to_json()`, `format_text()`
   - Model: `src/core/models.py` - AdventureHook dataclass

3. **TableLoader** (5 min)
   - `get_adventure_hooks()`, `lookup_adventure_hook(roll)`

4. **CLI** (10 min)
   - `python -m src.cli generate hook`
   - Options: --json, --save

5. **Testy** (10 min)
   - `tests/test_adventure_hook_generator.py` - 6+ testů

**Proč první:** Nejrychlejší quick win, žádné závislosti, užitečné pro session starters

---

### 🎯 FÁZE 5: Creature Variants ✅ HOTOVO

**Priorita:** 🟢 Nízká (ale rychlé zvýšení dokončenosti)
**Čas:** ~2 hodiny (implementace)
**Stav:** ✅ HOTOVO (2025-11-02)
**Složitost:** ⭐ Velmi jednoduchá
**Závislosti:** ❌ Žádné

**Popis:**
11 variant tvorů - každý má k6 tabulku s unikátními vlastnostmi.
*Poznámka: Zjištěno 11 variant místo původně odhadovaných 14*

**Zdroj:** `docs/knowledge_base/09_CREATURES.md`

**Implementované varianty:**
- ✅ Ghost Abilities (k6) - Přízračné schopnosti
- ✅ Snake Types (k6) - Zvláštní hadi
- ✅ Cat Lords (k6) - Kočičí pánové a paní
- ✅ Rat Gangs (k6) - Krysí gangy
- ✅ Rival Mice (k6) - Konkurenční myší dobrodruzi
- ✅ Spider Types (k6) - Druhy pavouků
- ✅ Owl Wizards (k6) - Soví čarodějové
- ✅ Centipede Types (k6) - Zevlující stonožky
- ✅ Fairy Schemes (k6) - Vílí plány
- ✅ Crow Songs (k6) - Vraní písně
- ✅ Frog Knights (k6) - Potulní žabí rytíři

**Co bylo vytvořeno:**
1. **Data** - 11 JSON souborů v `data/core/creature_*.json`
2. **Model** - `CreatureVariant` dataclass v `models.py` s emoji a českými názvy
3. **Generátor** - `CreatureVariantGenerator` s unified přístupem pro všechny typy
4. **TableLoader** - 13 nových metod (unified + 11 specifických)
5. **CLI** - `mausritter generate creature <type>` s podporou všech 11 typů
6. **Testy** - 27 unit testů (všechny prošly ✅)
7. **Dokumentace** - README.md sekce 12 s kompletní tabulkou typů

**Použití:**
```bash
mausritter generate creature ghost      # Přízračné schopnosti
mausritter generate creature owl        # Soví čarodějové
mausritter generate creature frog       # Žabí rytíři
```

**Proč druhé:** Rychlé zvýšení dokončenosti, jednoduché implementace, žádné závislosti

---

### 🎯 FÁZE 6A: Hex Generator

**Priorita:** 🟡 Vysoká (pro hexcrawl)
**Čas:** ~2-3 hodiny
**Stav:** 📝 Připraveno k implementaci
**Složitost:** ⭐⭐⭐ Střední
**Závislosti:** ✅ Settlement Generator (HOTOVO)

**Popis:**
Generátor obsahu hexů pro hexcrawl kampaně.

**Zdroj:** `11_HEXCRAWL_SETUP.md` (řádky 93-160)

**Co implementovat:**
1. **Data** (1 hod)
   - `data/core/hex_types.json` - 4 typy hexů (k6)
   - `data/core/hex_details.json` - 48 detailů (k6×k8)
   - ❗ **Používá Settlement Generator** (detail k6=1: "Myší osada...")

2. **Generátor** (1 hod)
   - `src/generators/hex.py` - HexGenerator
   - Integrace s SettlementGenerator

**Proč třetí:** Klíčové pro hexcrawl, používá Settlement který už máme ✅

---

### 🎯 FÁZE 6B: Dungeon Generator

**Priorita:** 🟡 Vysoká (pro dungeon crawl)
**Čas:** ~6-8 hodin
**Stav:** 📝 Připraveno k implementaci
**Složitost:** ⭐⭐⭐⭐ Složitá (nejvyšší!)
**Závislosti:** ✅ Settlement Generator (HOTOVO)

**Popis:**
Generátor dobrodružných míst (dungeonů).

**Zdroj:** `14_DUNGEON_CREATION.md` (řádky 69-268)

**Co implementovat:**
1. **Data** (2-3 hod)
   - 11 různých JSON souborů (k20, k12, k10, k8, k6)
   - ❗ **Používá Settlement Generator** (k20=20: "Myší osada")

2. **Generátor** (3-4 hod)
   - `src/generators/dungeon.py` - DungeonGenerator
   - Komplexní logika pro místnosti (3×k6)
   - Integrace s SettlementGenerator

**Proč poslední:** Nejsložitější ze všech, používá Settlement který už máme ✅

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

### E: NPC Generator (Generátor NPC)

**Priorita:** 🔴 Vysoká
**Čas:** ~9 hodin
**Stav:** ✅ HOTOVO

**Popis:**
Generátor NPC myší (non-player characters) pro DM. Implementovány DVĚ verze podle oficiálních pravidel Mausritter.

**Co bylo implementováno:**

#### FÁZE 1: Základní NPC Generator (✅ HOTOVO)
1. **Data** (6 JSON souborů v `data/core/`)
   - `npc_social_status.json` - Společenské postavení (k6)
   - `npc_appearance.json` - Vzhled (k20)
   - `npc_quirk.json` - Zvláštnost (k20)
   - `npc_desire.json` - Po čem touží (k20)
   - `npc_relationship.json` - Vztah k jiné myši (k20)
   - `npc_reaction.json` - Reakce při setkání (2k6)

2. **Generátor**
   - `src/generators/npc.py` - NPCGenerator
   - Model: `src/core/models.py` - NPC dataclass (9 polí)
   - Používá existující tabulky jmen z Character Generatoru
   - Generuje: jméno, status, rodné znamení, vzhled, zvláštnost, tužbu, vztah, reakci

3. **CLI**
   - `python -m src.cli generate npc` - vygeneruje náhodné NPC
   - `python -m src.cli generate npc --name "Pepřík"` - s vlastním jménem
   - `python -m src.cli generate npc --gender female` - ženské
   - `python -m src.cli generate npc --json` - JSON výstup
   - `python -m src.cli generate npc --save npc.json` - uložit do souboru

4. **Testy**
   - `tests/test_npc_generator.py` - 19 unit testů
   - Testuje všechny generační metody + export do JSON

#### FÁZE 2: Data pro rozšířený generátor (✅ PŘIPRAVENO)
5. **Rozšířená data** (7 dalších JSON souborů v `data/core/`)
   - `hireling_types.json` - 9 typů pronajímatelných pomocníků + statistiky
   - `competitive_mice.json` - 6 konkurenčních myších dobrodruhů
   - `cat_lords.json` - 6 kočičích pánů a paní
   - `rat_gangs.json` - 6 krysích gangů
   - `owl_wizards.json` - 6 sovích čarodějů
   - `frog_knights.json` - 6 žabích rytířů
   - `adventure_seeds.json` - 36 semínek dobrodružství (k66 tabulka)

6. **Rozšířené modely**
   - `src/core/models.py` - Hireling dataclass (statistiky, inventář, level, zkušenosti)
   - `src/core/tables.py` - 14 nových TableLoader metod pro všechny tabulky

**Rozdíl oproti Character Generator:**
- Character Generator = hráčské postavy (full stats, HP, inventář, původ, výbava)
- NPC Generator = rychlé NPC pro DM (osobnost, motivace, reakce, status)
- Hireling = pronajímatelné NPC se statistikami (BO, vlastnosti, mzda)

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

**Celková dokončenost:** ~32% (9/28 generátorů, **100% P1** ✅) 🎯

| Feature               | Status | Progress |
|-----------------------|--------|----------|
| Data Extraction       | ✅     | 100%     |
| Character Generator   | ✅     | 100%     |
| NPC Generator         | ✅     | 100%     |
| Hireling Generator    | ✅     | 100%     |
| Weather Generator     | ✅     | 100%     |
| Reaction Roll         | ✅     | 100%     |
| Spell Generator       | ✅     | 100%     |
| Treasure Generator    | ✅     | 100%     |
| Adventure Seeds       | ✅     | 100%     |
| **P1 Priority**       | **✅** | **100% (8/8)** |
| Tavern Generator      | ✅     | 100%     |
| Settlement Generator  | ✅     | 100%     |
| Hex Generator         | 💡     | 0%       |
| Documentation         | 🚧     | 75%      |
| Web Interface         | 💡     | 0%       |

---

## 🤝 Jak přispět

Pokud chceš přidat novou feature:

1. Zkontroluj tento roadmap - možná už je naplánovaná
2. Otevři issue na GitHubu s popisem
3. Diskutuj implementaci
4. Vytvoř pull request

---

**Poslední aktualizace:** 2025-11-02
**Autor:** Claude Code + uživatel

---

## 📋 Související dokumenty

- **[DEPENDENCY_ORDER.md](DEPENDENCY_ORDER.md)** - Detailní analýza závislostí mezi generátory a bottom-up pořadí implementace

---

## 📝 Changelog

### 2025-11-02 - Fáze 5 dokončena - Creature Variants 🐉
- ✅ Implementovány varianty stvoření (11 typů, každý s 6× k6 variantami)
- ✅ CreatureVariantGenerator class v src/generators/creature_variant.py
- ✅ 11 JSON datových souborů v data/core/:
  - creature_ghost_abilities.json - Přízračné schopnosti (6 variant)
  - creature_snake_types.json - Zvláštní hadi (6 typů)
  - creature_cat_lords.json - Kočičí pánové a paní (6 lordů)
  - creature_rat_gangs.json - Krysí gangy (6 gangů)
  - creature_rival_mice.json - Konkurenční myší dobrodruzi (6 soupeřů)
  - creature_spider_types.json - Druhy pavouků (6 druhů)
  - creature_owl_wizards.json - Soví čarodějové (6 čarodějů)
  - creature_centipede_types.json - Zevlující stonožky (6 typů)
  - creature_fairy_schemes.json - Vílí plány (6 plánů)
  - creature_crow_songs.json - Vraní písně (6 písní)
  - creature_frog_knights.json - Potulní žabí rytíři (6 rytířů)
- ✅ CreatureVariant dataclass přidán do models.py s emoji a českými názvy
- ✅ TableLoader rozšířen o 13 nových metod (unified + 11 specifických)
- ✅ CLI příkaz `generate creature <type>` s podporou všech 11 typů
- ✅ Click.Choice validace pro typy stvoření
- ✅ Color-coded výstup s panely (emoji + název tabulky, typ, popis)
- ✅ 27 unit testů v test_creature_variant_generator.py (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md sekce 12, ROADMAP.md)
- ✅ **Zjištěno:** 11 variant v oficiálních pravidlech (ne 14 jak původně odhadnuto)
- ✅ **Celková dokončenost: 43% (12/28 generátorů)**

### 2025-11-02 - Fáze 4D dokončena - Adventure Hooks 🎣
- ✅ Implementován Adventure Hook Generator (generátor háčků dobrodružství)
- ✅ AdventureHookGenerator class v src/generators/adventure_hook.py
- ✅ data/core/adventure_hooks.json - 6 háčků s kategoriemi a otázkami
- ✅ Každý háček obsahuje: háček, kategorie, 4 inspirační otázky
- ✅ CLI příkaz `generate hook` s --json, --save
- ✅ AdventureHook dataclass přidán do models.py s emoji a kategoriemi
- ✅ TableLoader rozšířen o 2 nové metody pro adventure hooks
- ✅ 6 kategorií: personal, duty, quest, threat, treasure, survival
- ✅ Unikátní emoji pro každou kategorii (👨‍👩‍👧‍👦, ⚔️, 🔮, ⚠️, 💰, 🌪️)
- ✅ Color-coded výstup s panely (emoji kategorie + háček, otázky)
- ✅ 16 unit testů v test_adventure_hook_generator.py (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md sekce 11, ROADMAP.md)
- ✅ **Celková dokončenost: 39% (11/28 generátorů)**

### 2025-11-02 - Fáze 4C dokončena - Settlement Generator 🏘️
- ✅ Implementován Settlement Generator (generátor myších osad)
- ✅ SettlementGenerator class v src/generators/settlement.py
- ✅ 7 JSON datových souborů v data/core/:
  - settlement_sizes.json - Velikosti osad (2d6 keep-lower, 6 velikostí)
  - settlement_governments.json - Typy vlády (k6 + sizeValue, 6 typů)
  - settlement_details.json - Charakteristické detaily (k20, 20 položek)
  - settlement_trades.json - Řemesla a obchody (k20, 20 položek)
  - settlement_features.json - Výrazné prvky (k20, 20 položek)
  - settlement_events.json - Události při příjezdu (k20, 20 položek)
  - settlement_names.json - Semínka názvů (4× k12, celkem 48 možností)
- ✅ Settlement dataclass přidán do models.py s properties
- ✅ TableLoader rozšířen o 14+ nových metod pro settlement tabulky
- ✅ roll_2d6_keep_lower() přidáno do dice.py (speciální mechanika)
- ✅ CLI příkaz `generate settlement` s --name, --no-tavern, --json, --save
- ✅ Integrace TavernGenerator pro osady velikosti 3+ (víska a větší)
- ✅ Dynamické počty řemesel (2× pro města) a prvků (2× pro velkoměsta)
- ✅ Color-coded výstup s panely (🏘️ název, ⚖️ vláda, 🔍 detail, 🛠️ řemesla, 🏛️ prvky, 📅 událost, 🏠 hospoda)
- ✅ 20+ unit testů v test_settlement_generator.py (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md sekce 10, ROADMAP.md)
- ✅ **Bottom-up přístup dokončen:** Tavern (4B) → Settlement (4C)
- ✅ **Celková dokončenost: ~36% (10/28 generátorů)**

### 2025-11-02 - Fáze 4B dokončena - Tavern Generator 🏠
- ✅ Implementován Tavern Generator (generátor hospod a hostinců)
- ✅ TavernGenerator class v src/generators/tavern.py
- ✅ 3 JSON datové soubory v data/core/:
  - tavern_name_part1.json - Přídavná jména (k12, 12 položek)
  - tavern_name_part2.json - Podstatná jména (k12, 12 položek)
  - tavern_specialty.json - Speciality (k12, 12 pokrmů/nápojů)
- ✅ Tavern dataclass přidán do models.py
- ✅ TableLoader rozšířen o 6 nových metod pro tavern tabulky
- ✅ CLI příkaz `generate tavern` s --json, --save
- ✅ Automatické skloňování do genitivu ("U Bílého Brouka")
- ✅ Color-coded výstup s panely (🏠 název, 🍲 specialita)
- ✅ roll_d12() přidáno do dice.py
- ✅ 14 unit testů v test_tavern_generator.py (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md sekce 9, ROADMAP.md)
- ✅ **Bottom-up přístup:** Tavern jako nejmenší komponenta Settlement
- ✅ **Celková dokončenost: ~32% (9/28 generátorů)**

### 2025-11-01 - Fáze 4A dokončena - P1 COMPLETE! 🎉
- ✅ Implementován Adventure Seeds Generator (generátor semínek dobrodružství)
- ✅ AdventureSeedGenerator class v src/generators/adventure.py
- ✅ data/core/adventure_seeds.json - všech 36 semínek z oficiálních pravidel (16_RANDOM_TABLES.md)
- ✅ Každé semínko kombinuje: Tvor (KDO) + Problém (CO) + Komplikace (JAK)
- ✅ CLI příkaz `generate adventure` s --custom, --inspiration, --json, --save
- ✅ Dva režimy generování:
  - Základní: 1× k66 → celý řádek (kompletní příběh)
  - Custom: 3× k66 → kombinace ze sloupců (mix & match)
- ✅ Inspirační text pro GM s otázkami na rozvíjení příběhu
- ✅ k66 mechanika implementována v dice.py (roll_d66)
- ✅ TableLoader.lookup_adventure_seed() metoda
- ✅ Color-coded výstup s panely (🎭 Tvor, ⚠️ Problém, 💥 Komplikace)
- ✅ AdventureSeed dataclass přidán do models.py
- ✅ 20 unit testů v test_adventure_generator.py (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md sekce 8, ROADMAP.md)
- ✅ **P1 generátory: 100% hotovo (8/8)** 🎯🎉
- ✅ **Celková dokončenost: ~29% (8/28 generátorů)**

### 2025-11-01 - Fáze 3E dokončena
- ✅ Implementován Spell Generator (generátor náhodných kouzel)
- ✅ SpellGenerator class v src/generators/spell.py
- ✅ data/core/spells.json - všech 16 kouzel z oficiálních pravidel (06_MAGIC.md)
- ✅ Každé kouzlo má: název, efekt s placeholdery [POČET] a [SOUČET], podmínku dobití
- ✅ CLI příkaz `generate spell` s --json, --save
- ✅ roll_d8() přidáno do dice.py pro hody 2d8
- ✅ TableLoader.lookup_spell() metoda a get_spells()
- ✅ Color-coded výstup podle kategorie (⚔️ Útok, 💚 Podpora, 🔮 Utilita, 💀 Oslabení)
- ✅ Spell dataclass přidán do models.py
- ✅ 15 unit testů (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md sekce 6, ROADMAP.md)
- ✅ P1 generátory: 62.5% hotovo (5/8) 🎯

### 2025-11-01 - Fáze 3F dokončena
- ✅ Implementován Treasure Generator (generátor pokladů / hoard)
- ✅ TreasureGenerator class v src/generators/treasure.py
- ✅ 9 JSON datových souborů v data/treasure/:
  - treasure_main.json - Hlavní tabulka (k20)
  - treasure_trinkets.json - Drobnosti (k6, 6 položek)
  - treasure_valuable.json - Cenný poklad (k6, 6 položek, 100-1500 ď)
  - treasure_bulky.json - Objemný poklad (k6, 6 položek, 2-6 políček)
  - treasure_unusual.json - Neobvyklý poklad (k6, 6 položek, speciální kupci)
  - treasure_useful.json - Užitečný poklad (k6, zásoby/pochodně/zbraně/zbroje/nástroje)
  - magic_swords.json - 10 kouzelných mečů (k10)
  - magic_sword_types.json - Typy zbraní (k6: Střední/Lehká/Těžká)
  - magic_sword_curses.json - Kletby (k6, 6 kleteb s podmínkami sejmutí)
- ✅ 2 nové datové soubory v data/core/:
  - tools.json - 44 nástrojů (32 myších + 12 lidských)
  - armor.json - 3 typy zbrojí (Lehká/Těžká/Štít)
- ✅ CLI příkaz `generate treasure` s --bonus (0-4), --json, --save
- ✅ Mechanika bonusových hodů: 2-6× k20 (2 základní + 0-4 bonusové)
- ✅ Bonusové otázky: bývalá osada, magická oblast, velké zvíře, velké nesnáze
- ✅ Generuje: ďobky (5-600 ď), kouzelné meče (5% šance), kouzla (5% šance), 5 typů předmětů
- ✅ Kouzelné meče s prokletím (16.7% šance), 10 typů schopností, 6 typů kleteb
- ✅ Nové modely: TreasureHoard, TreasureItem, MagicSword, Tool, Armor
- ✅ TableLoader rozšířen o 15 nových metod pro treasure tabulky
- ✅ Color-coded výstup podle typu (💰 Ďobky, ⚔️ Meč, ✨ Kouzlo, 💎 Cenné, 📦 Objemné, 🔮 Neobvyklé, 🛠️ Užitečné)
- ✅ Detailní display pro každou položku (hodnota, políčka, tečky použití, prokletí)
- ✅ 23 unit testů v test_treasure_generator.py (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md sekce 7, ROADMAP.md)
- ✅ P1 generátory: 75% hotovo (6/8) 🎯
- ✅ Celková dokončenost: ~44% (7/28 generátorů)
- ✅ Magic Sword Generator integrován do Treasure Generatoru

### 2025-11-01 - Fáze 3D dokončena
- ✅ Implementován Reaction Roll Generator (generátor reakcí NPC/tvorů)
- ✅ ReactionGenerator class v src/generators/reaction.py
- ✅ Využívá existující data/core/npc_reaction.json (5 typů reakcí)
- ✅ CLI příkaz `generate reaction` s --modifier, --json, --save
- ✅ Podporuje modifikátory (+1 za dárek, -1 za agresi, atd.)
- ✅ Color-coded výstup podle reakce (červená=Agresivní, zelená=Povídavá, atd.)
- ✅ GM otázky pro každou reakci (inspirace k roleplayi)
- ✅ Reaction dataclass přidán do models.py
- ✅ 14 unit testů (všechny prošly ✅)
- ✅ Dokumentace aktualizována (README.md, MANUAL.md sekce 2.5, ROADMAP.md)
- ✅ P1 generátory: 50% hotovo (4/8) 🎯

### 2025-11-01 - Fáze 3C dokončena
- ✅ Implementován Weather Generator (generátor počasí a sezónních událostí)
- ✅ WeatherGenerator class v src/generators/weather.py
- ✅ data/core/weather_seasons.json - 4 roční období (jaro, léto, podzim, zima)
- ✅ Každé roční období má tabulku počasí (2k6, 5 možností) + události (k6, 6 možností)
- ✅ CLI příkaz `generate weather` s --season, --with-event, --json, --save
- ✅ 14 unit testů v test_weather_generator.py (všechny prošly ✅)
- ✅ Display funkce s barevným panelem podle sezóny (🌸🌞🍂❄️)
- ✅ Detekce nepříznivého počasí s varováním (červený rámeček)
- ✅ Pravděpodobnosti: Jaro/Podzim 2.78% nepříznivé, Léto 27.78%, Zima 72% nepříznivé
- ✅ TableLoader rozšířen o 3 metody (get_weather_seasons, lookup_weather, lookup_seasonal_event)
- ✅ Weather dataclass přidán do models.py
- ✅ Dokumentace aktualizována (README.md, MANUAL.md sekce 2.4, ROADMAP.md)

### 2025-11-01 - Fáze 3B dokončena
- ✅ Implementován Hireling Generator (generátor pomocníků)
- ✅ HirelingGenerator class v src/generators/hireling.py
- ✅ CLI příkaz `generate hireling` s --type, --name, --gender, --json, --save
- ✅ 15 unit testů (manuálně otestováno, všechny fungují)
- ✅ Display funkce s yellow panelem (odlišení od character/npc)
- ✅ Plné bojové statistiky (k6 HP, 2k6 STR/DEX/WIL)
- ✅ 9 typů pomocníků (Světlonoš, Dělník, Zbrojmyš, Rytíř, atd.)
- ✅ Výpočet dostupnosti podle typu (k6/k4/k3/k2)
- ✅ Dokumentace aktualizována (README.md, MANUAL.md nová sekce 2.3)

### 2025-10-31 - Fáze 3A dokončena
- ✅ Implementován NPC Generator (základní)
- ✅ 6 JSON tabulek (social_status, appearance, quirk, desire, relationship, reaction)
- ✅ CLI příkaz `generate npc` s --name, --gender, --json, --save
- ✅ 19 unit testů (všechny prošly)
- ✅ Rozšířená data pro kompletní generátor (7 dalších JSON souborů)
- ✅ NPCGenerator a Hireling dataclass v models.py
- ✅ 20+ nových TableLoader metod
- ✅ Dokumentace aktualizována (README.md, MANUAL.md, ROADMAP.md)

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
