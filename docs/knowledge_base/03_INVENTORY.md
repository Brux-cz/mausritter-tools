# 03 - Inventář

---
**ID:** 03_INVENTORY
**Název:** Systém inventáře a stavy
**Tagy:** #pravidla #inventář #stavy #zatížení #předměty
**Závislosti:**
- [01_CORE_RULES.md](01_CORE_RULES.md) - Základní mechaniky
- [02_CHARACTER_CREATION.md](02_CHARACTER_CREATION.md) - Tvorba postavy
**Související:**
- Vybavení a ceny → [04_EQUIPMENT.md](04_EQUIPMENT.md)
- Boj (použití zbraní) → [05_COMBAT.md](05_COMBAT.md)
---

## Políčka inventáře

Předměty, které má tvoje myš u sebe, se ukládají do **políček v inventáři**.

**Většina předmětů zabírá 1 políčko.**

**Některé větší předměty** (obouruční zbraně, zbroje) zabírají **2 políčka**.

### Struktura inventáře

Deník postavy má **celkem 10 políček**:

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ SILNĚJŠÍ    │   TĚLO 1    │   TĚLO 2    │   BATOH 1   │
│  PACKA      │             │             │             │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ SLABŠÍ      │   TĚLO 3    │   TĚLO 4    │   BATOH 2   │
│  PACKA      │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**6 políček:**
- 2× **Packy** (levá + pravá)
- 4× **Tělo** (oblečení, zbroj, pásy)
- 4× **Batoh** (záda, většina vybavení)

### Typy políček

| Typ | Počet | Vlastnosti |
|-----|-------|------------|
| **Políčka pacek** | 2 | Předměty neseš v packách, rychlý přístup |
| **Políčka těla** | 4 | Předměty na těle můžeš jako **volnou akci** prohodit s předměty v packách |
| **Políčka batohu** | 4 | Vyndat předmět **v boji tě stojí akci** (místo útoku) |

---

## Stavy

**Stavy** jsou negativní účinky, které můžou tvoji myš potkat.

### Jak fungují stavy

✅ Každý stav **musíš umístit do políčka inventáře**

✅ Myši můžou mít **víc kopií stejného stavu**

✅ Některé stavy mají **další účinky** (platí, dokud máš stav v inventáři)

✅ Stavů se zbavíš **splněním podmínky odstranění** (většinou odpočinek)

### Seznam stavů

#### Hlad
```
┌──────────────────────┐
│ HLAD                 │
│                      │
│ Odstranění:          │
│ Po jídle             │
└──────────────────────┘
```
- **Jak dostaneš:** Nenajíš se za celý den
- **Odstranění:** Sněz zásoby

#### Vyčerpání
```
┌──────────────────────┐
│ VYČERPÁNÍ            │
│                      │
│ Odstranění:          │
│ Po dlouhém odpočinku │
└──────────────────────┘
```
- **Jak dostaneš:** Bez odpočinku, náročné cestování
- **Odstranění:** Dlouhý odpočinek (1 hlídka)

#### Vystrašení
```
┌──────────────────────┐
│ VYSTRAŠENÍ           │
│                      │
│ Odstranění:          │
│ Po dlouhém odpočinku │
└──────────────────────┘
```
- **Jak dostaneš:** Kouzla, strašidelné situace
- **Odstranění:** Dlouhý odpočinek

#### Poranění
```
┌──────────────────────┐
│ PORANĚNÍ             │
│                      │
│ Nevýhoda při hodech  │
│ na sílu a mrštnost   │
│                      │
│ Odstranění:          │
│ Po úplném odpočinku  │
└──────────────────────┘
```
- **Jak dostaneš:** Kritické zranění v boji
- **Dodatečný účinek:** **Nevýhoda** při záchranách na sílu a mrštnost
- **Odstranění:** Úplný odpočinek (1 týden)

#### Pomatení
```
┌──────────────────────┐
│ POMATENÍ             │
│                      │
│ Odstranění:          │
│ Po úplném odpočinku  │
└──────────────────────┘
```
- **Jak dostaneš:** Vymknutí kouzla
- **Odstranění:** Úplný odpočinek (1 týden)

---

## Používání předmětů

### Počet použití

Většina předmětů má **tři tečky použití** ○○○

Jakmile zaškrtneš všechny tři ●●●, je předmět **spotřebovaný nebo zničený**.

### Kdy škrtat použití

#### Zbraně / Zbroje / Munice
**Po boji** hoď k6 za každý předmět, který tvoje myš v boji použila.

- **Když padne 4–6:** Zaškrtni jednu tečku ○○○ → ●○○

#### Pochodně / Lucerny / Lampy
**Po 6 směnách** škrtni jednu tečku.

#### Zásoby
**Po každém jídle** škrtni jednu tečku.

#### Jiné vybavení
**Po každém použití**, kterým se může vyčerpat nebo poškodit, ti Průvodce může říct, ať zaškrtneš tečku.

### Opravy

**Tečky zbraní a zbrojí** se dají obnovit opravou.

**Oprava každé tečky stojí 10 % z původní ceny předmětu.**

**Příklad:**
- Meč (střední zbraň) stojí 20 ď
- Oprava 1 tečky = 2 ď
- Oprava všech 3 teček = 6 ď

---

## Zatížení

Když tvoje myš nese **víc předmětů nebo stavů, než kolik má volných políček** v inventáři, je **přetížená**.

### Důsledky přetížení

❌ **Zatížené myši nemůžou běhat**

❌ **Všechny záchrany házejí s nevýhodou** (2k20, použij vyšší)

### Jak se zbavit zatížení

✅ Odlož předměty do skrýše nebo u kamaráda
✅ Uložposeze do banky
✅ Odstraň stavy (odpočinkem)
✅ Zbav se zničených předmětů

---

## Banky

V myších osadách je možné uložit si **ďobky a předměty do banky**.

### Jak fungují banky

✅ **Uložení:** Zdarma
✅ **Vybírání:** Zaplatíš poplatek **1 % z hodnoty** toho, co vybíráš

**Příklad:**
- Uložíš 500 ď
- Při výběru zaplatíš 5 ď (1 %)
- Dostaneš 495 ď

### Proč používat banky

✅ Uvolníš políčka inventáře
✅ Ďobky jsou v bezpečí (nepřijdeš o ně smrtí)
✅ Můžeš si ukládat cenné předměty

---

## Váček na ďobky

**Prvních 250 ďobků** unese tvoje myš po kapsách → **nezabírají políčko**

**Každých dalších začatých 250 ďobků** zabírá **jedno políčko**

**Příklady:**
- 100 ď → 0 políček
- 250 ď → 0 políček
- 251 ď → 1 políčko
- 500 ď → 1 políčko
- 501 ď → 2 políčka
- 1000 ď → 3 políčka

### Proč ukládat do banky

Myši v osadách většinou platí **naturáliemi nebo směnkami**. Velké množství ďobků je těžké nosit.

---

## Příklad inventáře

```
┌─────────────────────┬───────────────────────┬─────────────────────┐
│ SILNĚJŠÍ PACKA      │ TĚLO 1                │ BATOH 1             │
│                     │                       │                     │
│ Meč                 │ Lehká zbroj          │ Zásoby              │
│ k6/k8 (střední)     │ ○○○ (1 obr.)         │ ○○○                 │
│ ●○○                 │                       │                     │
├─────────────────────┼───────────────────────┼─────────────────────┤
│ SLABŠÍ PACKA        │ TĚLO 2                │ BATOH 2             │
│                     │                       │                     │
│ Pochodně            │ VYČERPÁNÍ             │ Stan                │
│ ●●○                 │                       │ ○○○                 │
│                     │ Odstraň dlouhým       │                     │
│                     │ odpočinkem            │                     │
└─────────────────────┴───────────────────────┴─────────────────────┘
│ TĚLO 3              │ TĚLO 4                │ BATOH 3             │
│                     │                       │                     │
│ Luk                 │ Šípy (toulec)         │ Motouz, klubko      │
│ k6 (lehká střelná)  │ ●○○                   │ ○○○                 │
│ ○○○                 │                       │                     │
├─────────────────────┼───────────────────────┼─────────────────────┤
│                     │                       │ BATOH 4             │
│                     │                       │                     │
│                     │                       │ Lucerna             │
│                     │                       │ ●○○                 │
│                     │                       │                     │
└─────────────────────┴───────────────────────┴─────────────────────┘

VÁČEK NA ĎOBKY: 180 ď (nezabírá políčko)
```

**Tato myš má:**
- ✅ 10/10 políček obsazeno (není přetížená)
- ⚠️ Stav Vyčerpání (nevýhoda na záchrany, dokud neodpočine)
- 🗡️ Meč v silnější pacce (rychlý přístup)
- 🛡️ Lehká zbroj (zabrání 1 zranění)
- 🏹 Luk + šípy v políčkách těla (střední přístup)
- 🎒 4 užitečné předměty v batohu

---

## 📚 Související dokumenty

**Vybavení:**
- Kompletní ceník → [04_EQUIPMENT.md](04_EQUIPMENT.md)
- Zbraně a zbroje → [04_EQUIPMENT.md#zbraně](04_EQUIPMENT.md)

**Stavy v akci:**
- Kritické zranění (= Poranění) → [05_COMBAT.md#kritické-zranění](05_COMBAT.md)
- Vymknutí kouzla (= Pomatení) → [06_MAGIC.md#vymknutí-kouzla](06_MAGIC.md)
- Odpočinek (odstranění stavů) → [07_ADVANCEMENT.md#odpočinek](07_ADVANCEMENT.md)

**Pro Průvodce:**
- Následky neúspěchu → [08_GM_GUIDE.md#následky-neúspěchu](08_GM_GUIDE.md)

---

*Zdroj: Mausritter CZ - pravidla.pdf, str. 8-9*
