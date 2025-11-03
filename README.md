# 🐭 Mausritter Tools

Python nástroje a generátory pro stolní hru **Mausritter** - OSR TTRPG o myších dobrodružích.

## ✅ Co máme hotové

### 📖 OFICIÁLNÍ GENERÁTORY (100% kompletní)

Všechny generátory z oficiálních Mausritter pravidel:

**P1 - Základní nástroje pro hráče:**
- ✅ **Generátor postav** - kompletní generování myších postav (3k6 keep 2, HP, Pips, původy, jména)
- ✅ **Generátor NPC** - rychlé vytváření nehráčských myší (jméno, status, vzhled, quirk, touha)
- ✅ **Generátor pomocníků** - generování hirelingů s plnými statistikami (k6, 6 typů)
- ✅ **Generátor počasí** - počasí a sezónní události pro všechny čtyři roční období
- ✅ **Generátor reakcí** - reakce NPC/tvorů při setkání (2k6 tabulka)
- ✅ **Generátor kouzel** - náhodná kouzla pro objevování pokladů (2d8 tabulka, 16 kouzel)
- ✅ **Generátor pokladů** - kompletní treasure hoard (2-6× k20, kouzelné meče, kouzla, předměty)
- ✅ **Generátor semínek dobrodružství** - kombinace tvora, problému a komplikace (k66, 36 semínek)

**P2 - Tvorba světa:**
- ✅ **Generátor hospod** - názvy a speciality hospod (2× k12 + k12, pro vísky a větší osady)
- ✅ **Generátor osad** - kompletní settlements (2d6 keep-lower velikost, vláda, detaily, řemesla, prvky, události)
- ✅ **Generátor háčků dobrodružství** - motivace pro hráče (k6, 6 typů háčků s otázkami)
- ✅ **Generátor hexů** - 4 typy terénu, 48 detailů, 6 kategorií pro hexcrawl mapy
- ✅ **Generátor dungeonů** - dobrodružná místa (past/decay/inhabitants/goal/secret, 3×k6 místnosti)
- ✅ **Generátor zvěstí (CORE)** - k6 tabulka s pravdivostním systémem (1-3 pravda, 4-5 částečně, 6 fáma)

**P3 - Creature Variants:**
- ✅ **Generátor variant stvoření** - 11 typů (Ghost, Snake, Cat, Rat, Mouse, Spider, Owl, Centipede, Fairy, Crow, Frog), každý s 6 variantami

**Základní nástroje:**
- ✅ **Hody kostkami** - všechny typy kostek (d4, d6, d8, d10, d12, d20, d66)
- ✅ **Testy vlastností** - roll-under d20 mechanika
- ✅ **JSON databáze** - 60+ datových souborů podle oficiálních pravidel

### 🎨 COMMUNITY ROZŠÍŘENÍ (volitelná)

Užitečná rozšíření nad rámec oficiálních pravidel:

- 🎨 **Rumor Generator Extended** - Propojené zvěsti s world state, kategorie (threat/NPC/location/treasure/mystery), story hooks (k6×k6), gossip chains (simulace šíření fám)
- 🎨 **Adventure Seeds Custom Mode** - Mix & match creature/problem/complication ze sloupců (oficiálně se hází celý řádek najednou)
- 🎨 **Hex Settlement Integration** - Automatické generování osad v hexech s kategorií "Myší osada" (convenience feature)
- 🎨 **Dungeon Settlement Integration** - Automatické generování osad pro dungeony s past=20 "Myší osada"
- 🎨 **Hexcrawl Generator** - Orchestrátor generující celý hexcrawl najednou (25 hexů + osady + dungeony + zvěsti)

### 🌐 WEB PLATFORM (MVP v development)

**Webová platforma pro komunitu Mausritter hráčů:**

- 🚧 **Backend (FastAPI)** - REST API wrappující Python generátory
  - ✅ 5 core generátorů (Character, NPC, Hex, Settlement, Weather)
  - 📁 Folder: `web-backend/`
  - 📚 [Backend README](web-backend/README.md)

- 🚧 **Frontend (Next.js 14)** - Modern web interface
  - ✅ Landing page
  - ✅ Tailwind CSS + Mausritter theme
  - 📁 Folder: `web-frontend/`
  - 📚 [Frontend README](web-frontend/README.md)

- 📋 **Dokumentace:**
  - [Web Architecture](docs/WEB_ARCHITECTURE.md) - Tech stack a deployment
  - [Database Schema](docs/DATABASE_SCHEMA.sql) - Supabase PostgreSQL schema
  - [API Endpoints](docs/API_ENDPOINTS.md) - REST API specifikace
  - [Web Roadmap](docs/WEB_ROADMAP.md) - Implementační plán (MVP → V4)
  - [UI Wireframes](docs/UI_WIREFRAMES.md) - Design všech stránek

**Status:** 🎉 **100% OFICIÁLNÍCH PRAVIDEL + 5 ROZŠÍŘENÍ + WEB MVP V DEVELOPMENT** 🎉

- ✅ **P1 (8/8)** - všechny základní nástroje pro hráče
- ✅ **P2 (6/6)** - všechny generátory pro tvorbu světa
- ✅ **P3 (11/11)** - všechny creature variants
- 🎨 **Extensions** - 5 community rozšíření pro větší pohodlí

**Poznámka:** Původní odhad "28 generátorů" počítal každou creature variantu jako samostatný generátor (14×). Ve skutečnosti máme 15 .py generátorů pokrývajících 23 oficiální funkce + 5 rozšíření. Všechny nástroje z rulebooku jsou hotové!

**Roadmap:** [brainstorm/ROADMAP.md](brainstorm/ROADMAP.md)

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

### 🏘️ 10. Generování osad (Settlement)
```bash
# Základní osada
python -m src.cli generate settlement

# S názvem osady
python -m src.cli generate settlement --name

# Bez hospody (i pro větší osady)
python -m src.cli generate settlement --no-tavern

# JSON výstup
python -m src.cli generate settlement --json

# Uložit do souboru
python -m src.cli generate settlement --save osada.json
```

**Co je osada:**
- **Velikost** (2d6 keep-lower) - Farma → Křižovatka → Víska → Vesnice → Město → Velkoměsto
- **Vláda** (k6 + velikost) - Typ správy osady
- **Detail** (k20) - Charakteristický rys
- **Řemesla** (k20) - 1× pro malé osady, 2× pro města
- **Prvky** (k20) - 1× pro osady, 2× pro velkoměsta
- **Událost** (k20) - Co se děje při příjezdu
- **Hospoda** - Automaticky generována pro vísku (3) a větší

**Velikosti osad:**
| Velikost | Název | Populace | Hospoda? | Řemesla | Prvky |
|----------|-------|----------|----------|---------|-------|
| 1 | Farma/zámeček | 1-3 rodiny | Ne | 1 | 1 |
| 2 | Křižovatka | 3-5 rodin | Ne | 1 | 1 |
| 3 | Víska | 50-150 myší | Ano | 1 | 1 |
| 4 | Vesnice | 150-300 myší | Ano | 1 | 1 |
| 5 | Město | 300-1000 myší | Ano | 2 | 1 |
| 6 | Velkoměsto | přes 1000+ | Ano | 2 | 2 |

**Příklady:**
- Víska / 50-150 myší / Rada starších / Postavená kolem jediného velkého stromu / Léčitel / Chrám nebo svatyně / Svatba nebo pohřeb
- Město / 300-1000 myší / Šlechtic / Proslulá okolními trhy / Pekař + Kovář / Rozsáhlý trh na náměstí / Dnes je tržní den
- Křižovatka / 3-5 rodin / Starosta / Pod vodou nebo pod zemí / Průvodce / Tajemná studna / Záhada nebo zmizení

**Mechanika:**
- Velikost určena hodem 2d6, vzít nižší hodnotu
- Větší osady mají více služeb a možností
- Hospoda se automaticky generuje pro velikost 3+

### 🎣 11. Generování háčků dobrodružství
```bash
# Náhodný háček
python -m src.cli generate hook

# JSON výstup
python -m src.cli generate hook --json

# Uložit do souboru
python -m src.cli generate hook --save hacek.json
```

**Co je háček:**
- **Motivace** (k6) - Důvod, proč se myši vydají na dobrodružství
- **Kategorie** - Osobní, Povinnost, Úkol, Hrozba, Poklad, Přežití
- **Otázky** - Inspirační otázky pro rozvíjení příběhu

**6 typů háčků:**
| # | Háček | Kategorie |
|---|-------|-----------|
| 1 | Hledání ztraceného člena rodiny | 👨‍👩‍👧‍👦 Osobní |
| 2 | Vyšetřování na příkaz šlechtice | ⚔️ Povinnost |
| 3 | Čaroděj potřebuje přísadu do kouzla | 🔮 Úkol |
| 4 | Tvor trápí myší osadu | ⚠️ Hrozba |
| 5 | Zděděná mapa k pokladu | 💰 Poklad |
| 6 | Útočiště před hroznou bouřkou | 🌪️ Přežití |

**Příklad výstupu:**
```
⚔️ HÁČEK DOBRODRUŽSTVÍ
Vyšetřování na příkaz myšího šlechtice

📋 Kategorie: Povinnost

❓ Otázky pro rozvíjení:
   • Kdo je šlechtic?
   • Co má být vyšetřeno?
   • Proč to šlechtic nemůže udělat sám?
   • Jaká je odměna?
```

**Použití:**
- Session starters - začátek nové kampaně nebo sezení
- Motivace hráčů - důvod proč se vydat na výpravu
- Improvizace - když potřebuješ rychle háček

### 🐉 12. Generování variant stvoření
```bash
# Přízračné schopnosti
python -m src.cli generate creature ghost

# Soví čarodějové
python -m src.cli generate creature owl

# Potulní žabí rytíři
python -m src.cli generate creature frog

# JSON výstup
python -m src.cli generate creature snake --json

# Uložit do souboru
python -m src.cli generate creature cat --save cat_lord.json
```

**Co je varianta stvoření:**
- **Typ stvoření** - 11 různých typů (přízrak, had, kočka, krysa, myš, pavouk, sova, stonožka, víla, vrána, žába)
- **Varianta** (k6) - Specifická varianta s unikátními vlastnostmi
- **Popis** - Detailní popis varianty a jejích schopností

**11 dostupných typů:**
| Typ | Příkaz | Tabulka | Emoji |
|-----|--------|---------|-------|
| Přízrak | `ghost` | Přízračné schopnosti | 👻 |
| Had | `snake` | Zvláštní hadi | 🐍 |
| Kočka | `cat` | Kočičí pánové a paní | 🐱 |
| Krysa | `rat` | Krysí gangy | 🐀 |
| Myš | `mouse` | Konkurenční myší dobrodruzi | 🐭 |
| Pavouk | `spider` | Druhy pavouků | 🕷️ |
| Sova | `owl` | Soví čarodějové | 🦉 |
| Stonožka | `centipede` | Zevlující stonožky | 🐛 |
| Víla | `fairy` | Vílí plány | 🧚 |
| Vrána | `crow` | Vraní písně | 🦅 |
| Žába | `frog` | Potulní žabí rytíři | 🐸 |

**Příklad výstupu (Soví čarodějové):**
```
🦉 SOVÍ ČARODĚJOVÉ
Bezalel

📋 Typ: Sova

📝 Popis:
   Vyrábí mechanické služebníky

🎲 Hod: 1 (k6)
```

**Použití:**
- Zpestření encounter - unikátní varianta běžného stvoření
- Random encounters - náhodné setkání s variantou
- Boss fights - mocný jedinec s unikátními schopnostmi
- NPC tvorové - zajímavé charaktery pro interakci

### 🗺️ 13. Generování hexů pro hexcrawl
```bash
# Náhodný hex
python -m src.cli generate hex

# Hex s myší osadou
python -m src.cli generate hex --with-settlement

# JSON výstup
python -m src.cli generate hex --json

# Uložit do souboru
python -m src.cli generate hex --save muj_hex.json
```

**Co je hex:**
- **Typ hexu** (k6) - Otevřená krajina, Les, Řeka, Lidské město
- **Kategorie detailu** (k6) - 6 kategorií (Osada, Civilizace, Zvířata, Opuštěné, Mystické, Lidské)
- **Detail** (k8) - 48 konkrétních detailů s háčky pro rozvíjení příběhu
- **Settlement integrace** - Hexy s kategorií "Myší osada" automaticky generují celou osadu

**4 typy hexů:**
| Typ | k6 | Emoji |
|-----|-----|-------|
| Otevřená krajina | 1-2 | 🌾 |
| Les | 3-4 | 🌲 |
| Řeka | 5 | 🌊 |
| Lidské město | 6 | 🏛️ |

**6 kategorií detailů:**
| # | Kategorie | Počet detailů |
|---|-----------|---------------|
| 1 | Myší osada | (generuje Settlement) |
| 2 | Civilizační prvky | 8 |
| 3 | Zvířecí a přírodní prvky | 8 |
| 4 | Přírodní a opuštěné prvky | 8 |
| 5 | Mystické prvky | 8 |
| 6 | Pradávné a lidské prvky | 8 |

**Příklad výstupu:**
```
🌲 HEX PRO HEXCRAWL
Les

📋 Kategorie: Zvířecí a přírodní prvky

🔍 Detail:
   Hnízdo zpěvného ptáka

❓ Háček:
   Jaké smutné příběhy pěje?

🎲 Hody: Typ k6=3, Kategorie k6=3, Detail k8=1
```

**Příklad s osadou:**
```
🌾 HEX PRO HEXCRAWL
Otevřená krajina

📋 Kategorie: Myší osada

🏘️ MYŠÍ OSADA:
Křižovatka
Velikost: Křižovatka
Vláda: Rada starších
```

**Použití:**
- Hexcrawl kampaně - generování obsahu hexů na mapě
- Sandbox průzkum - náhodné objevy při cestování
- Příprava světa - rychlé naplnění mapy zajímavostmi
- Improvizace - když hráči jdou neočekávaným směrem

### 🏛️ 14. Generování dungeonů (dobrodružných míst)
```bash
# Náhodný dungeon (6 místností)
python -m src.cli generate dungeon

# S vlastním počtem místností
python -m src.cli generate dungeon --rooms 10

# Dungeon s myší osadou
python -m src.cli generate dungeon --with-settlement

# JSON výstup
python -m src.cli generate dungeon --json

# Uložit do souboru
python -m src.cli generate dungeon --save muj_dungeon.json
```

**Co je dungeon:**
- **Minulost** (k20) - Původní účel místa (chrám, věž, nora, osada...)
- **Chátrání** (k12) - Co způsobilo úpadek (zatopení, magie, plísně...)
- **Obyvatelé** (k10) - Kdo tu teď žije (myši, krysy, duchové, vílí...)
- **Cíl** (k8) - Co obyvatelé hledají nebo chrání
- **Tajemství** (k6) - Skrytá mystéria místa
- **Místnosti** (parametr) - Každá s typem, tvory a poklady
- **Settlement integrace** - Minulost "Myší osada" (k20=20) generuje celou osadu

**5 typů místností:**
| Typ | k6 | Emoji | Feature |
|-----|-----|-------|---------|
| Prázdná | 1-2 | ⬜ | k20 atmosférických prvků |
| Překážka | 3 | 🚧 | k8 překážek k obejití |
| Past | 4 | ⚠️ | k8 zjevných a smrtících pastí |
| Hlavolam | 5 | 🧩 | k6 hlavolamů |
| Doupě | 6 | 🏰 | k6 typů doupat |

**3×k6 systém generování místností:**
- **1. hod k6** - Typ místnosti (prázdná, překážka, past, hlavolam, doupě)
- **2. hod k6** - Šance na tvora (závisí na typu místnosti)
- **3. hod k6** - Šance na poklad (závisí na typu místnosti)

**Příklad výstupu:**
```
🏛️ DOBRODRUŽNÉ MÍSTO (DUNGEON)

Minulost: Starodávný chrám netopýřího kultu
Chátrání: Magická nehoda

👥 Obyvatelé: Přízrační duchové
🎯 Cíl: Zvláštní a mocné kouzlo
🔮 Tajemství: Obelisk hučící mystickou energií

🚪 MÍSTNOSTI (6):

#1 ⬜ Prázdná | 💎 Poklad
   📋 Trs hub

#2 🚧 Překážka | 👹 Tvor
   📋 Zamčené dveře. Klíč se nachází v jiné místnosti.

#3 ⚠️ Past | 👹 Tvor | 💎 Poklad
   📋 Temná chodba naplněná výbušným plynem.

#4 🧩 Hlavolam | 👹 Tvor | 💎 Poklad
   📋 Krystal a v něm zapuštěný kouzelný meč.

#5 🏰 Doupě | 👹 Tvor | 💎 Poklad
   📋 Tvor chrání mladé

#6 ⬜ Prázdná
   📋 Neustálé kapání vody ze stropu

🎲 Hody: Minulost k20=1, Chátrání k12=2, Obyvatelé k10=6, Cíl k8=7, Tajemství k6=1
```

**Příklad s osadou:**
```
🏛️ DOBRODRUŽNÉ MÍSTO (DUNGEON)

Minulost: Myší osada
Chátrání: Stáří a hniloba

🏘️ MYŠÍ OSADA:
Křižovatka
Velikost: Křižovatka
Vláda: Rada starších
```

**Použití:**
- Dungeon crawl - kompletní dobrodružné místo připravené za pár sekund
- One-shot hry - rychlá příprava místa pro jednorázovou hru
- Hexcrawl - když hráči objeví zajímavé místo na mapě
- Improvizace - když potřebuješ dungeon TEĎ
- Inspirace - základní kostra pro vlastní rozšíření

**Design filozofie:**
- **Tvorové = Obyvatelé dungeonu** - Všichni tvorové patří k jedné frakci (inhabitants)
- **Boolean flagy** - `has_creature` a `has_treasure` podle oficiálních pravidel
- **GM kreativita** - Konkrétní tvory a poklady si volí GM podle tématu dungeonu
- **3×k6 systém** - Podmíněné pravděpodobnosti pro různé typy místností

### 🎲 15. Hody kostkami
```bash
python -m src.cli roll-dice d6
python -m src.cli roll-dice d20
python -m src.cli roll-dice 2d6
python -m src.cli roll-dice d66
```

### 🎯 16. Test vlastnosti
```bash
python -m src.cli test 12
python -m src.cli test 10 --modifier 2
```

### ❓ 17. Zobrazit help
```bash
python -m src.cli --help
python -m src.cli generate --help
```

### 🧪 18. Spustit testy
```bash
python test_character_simple.py
python test_tableloader.py
python -m tests.test_weather_generator
python -m tests.test_reaction_generator
python -m tests.test_spell_generator
python -m tests.test_treasure_generator
python -m tests.test_adventure_generator
python -m tests.test_tavern_generator
python -m tests.test_settlement_generator
python -m tests.test_adventure_hook_generator
python -m tests.test_creature_variant_generator
python -m tests.test_hex_generator
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
