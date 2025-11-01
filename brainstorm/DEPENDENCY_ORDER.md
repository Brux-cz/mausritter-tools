# Pořadí implementace generátorů (Bottom-up podle závislostí)

## 🔍 Analýza závislostí podle oficiálních pravidel

### ✅ CO UŽ MÁME (10/28)

```
Tavern Generator (4B) ✅
    ↓ používá se v
Settlement Generator (4C) ✅
```

**Důležité:** Settlement je teď k dispozici pro další generátory!

---

## 📋 ZÁVISLOSTI ZBÝVAJÍCÍCH GENERÁTORŮ

### Hex Generator používá:
- **Settlement Generator** ✅ (řádek 119 v 11_HEXCRAWL_SETUP.md: "Myší osada...")
- Odkaz: Detail k6=1: "Myší osada... (podrobnosti v 12_SETTLEMENTS.md)"

### Dungeon Generator používá:
- **Settlement Generator** ✅ (řádek 94 v 14_DUNGEON_CREATION.md: k20=20: "Myší osada")
- Různé creature typy (volitelné, jen flavor)

### Adventure Hooks:
- **Žádné závislosti!** (samostatná k6 tabulka)

### Creature Variants (14× generátorů):
- **Žádné závislosti!** (všechny jsou k6 tabulky, flavor pro tvory)

---

## 🎯 DOPORUČENÉ POŘADÍ (Bottom-up)

### FÁZE 4D: Adventure Hooks ⭐
**Složitost:** Velmi jednoduchá
**Čas:** ~30-45 minut
**Závislosti:** Žádné
**Tabulky:** 1× k6 (6 háčků)
**Proč první:** Nejjednodušší, žádné závislosti, rychlý quick win

```
┌─────────────────────────┐
│  Adventure Hooks (k6)   │ ← Fáze 4D
│  Žádné závislosti       │
└─────────────────────────┘
```

---

### FÁZE 5: Creature Variants (14× generátorů) ⭐
**Složitost:** Velmi jednoduchá (každý)
**Čas:** ~2-4 hodiny (všech 14)
**Závislosti:** Žádné
**Tabulky:** 14× k6 (každý má 6 variant)
**Proč druhé:** Jednoduché, žádné závislosti, rychle zvýší dokončenost na 86% (24/28)

```
┌─────────────────────────┐
│  Ghost Abilities (k6)   │ ← Fáze 5A
│  Snake Types (k6)       │ ← Fáze 5B
│  Cat Lords (k6)         │ ← Fáze 5C
│  Rat Gangs (k6)         │ ← Fáze 5D
│  Rival Mice (k6)        │ ← Fáze 5E
│  Spider Types (k6)      │ ← Fáze 5F
│  Owl Wizards (k6)       │ ← Fáze 5G
│  Centipede Types (k6)   │ ← Fáze 5H
│  Fairy Schemes (k6)     │ ← Fáze 5I
│  Crow Songs (k6)        │ ← Fáze 5J
│  Frog Knights (k6)      │ ← Fáze 5K
│  + 3 další (k6)         │ ← Fáze 5L-N
│  Žádné závislosti       │
└─────────────────────────┘
```

---

### FÁZE 6A: Hex Generator ⭐⭐⭐
**Složitost:** Střední
**Čas:** ~2-3 hodiny
**Závislosti:** Settlement Generator ✅
**Tabulky:** 2 (Typ hexu k6, Detaily k6×k8 = 48 možností)
**Proč třetí:** Používá Settlement, který už máme hotový

```
Settlement Generator ✅ (4C)
    ↓ používá se v
┌─────────────────────────┐
│   Hex Generator         │ ← Fáze 6A
│   - Typ hexu (k6)       │
│   - Detaily (k6×k8)     │
│   - Odkazuje na osady   │
└─────────────────────────┘
```

---

### FÁZE 6B: Dungeon Generator ⭐⭐⭐⭐
**Složitost:** Složitá (nejvyšší!)
**Čas:** ~6-8 hodin
**Závislosti:** Settlement Generator ✅
**Tabulky:** 11 různých (k20, k12, k10, k8, k6, 3×k6)
**Proč poslední:** Nejsložitější, používá Settlement

```
Settlement Generator ✅ (4C)
    ↓ používá se v
┌─────────────────────────┐
│  Dungeon Generator      │ ← Fáze 6B
│  - Minulost (k20)       │
│  - Chátrání (k12)       │
│  - Obyvatelé (k10, k8)  │
│  - Tajemství (k6)       │
│  - Místnosti (3×k6)     │
│  - Prázdné (k20)        │
│  - Překážky (k8)        │
│  - Pasti (k8)           │
│  - Hlavolamy (k6)       │
│  - Doupata (k6)         │
│  - Odkazuje na osady    │
└─────────────────────────┘
```

---

## 📊 VIZUALIZACE CELÉHO STROMU ZÁVISLOSTÍ

```
Úroveň 1 (Základní komponenty):
    Tavern Generator ✅ (4B)

Úroveň 2 (Složené komponenty):
    Settlement Generator ✅ (4C)
        ↑ používá Tavern

Úroveň 3 (Nezávislé jednoduché):
    Adventure Hooks (4D) ← DALŠÍ!
    Creature Variants (5A-N) ← PO TOM

Úroveň 4 (Používají Settlement):
    Hex Generator (6A)
        ↑ používá Settlement ✅
    Dungeon Generator (6B)
        ↑ používá Settlement ✅
```

---

## 🎯 DOPORUČENÉ STRATEGII

### Strategie A: "Quick Wins" (rychlé úspěchy)
1. **Adventure Hooks** (4D) - 30-45 min
2. **Creature Variants** (5A-N) - 2-4 hodiny (všech 14)
3. **Hex Generator** (6A) - 2-3 hodiny
4. **Dungeon Generator** (6B) - 6-8 hodin

**Výhody:** Rychle zvýšíš dokončenost, získáš momentum

### Strategie B: "Hexcrawl Focus" (zaměření na hexcrawl)
1. **Adventure Hooks** (4D) - 30-45 min
2. **Hex Generator** (6A) - 2-3 hodiny
3. **Dungeon Generator** (6B) - 6-8 hodin
4. **Creature Variants** (5A-N) - 2-4 hodiny

**Výhody:** Kompletní hexcrawl toolkit co nejdřív

---

## 💡 MÉ DOPORUČENÍ

**START:** Adventure Hooks (4D) jako další
- Nejjednodušší (1 tabulka k6)
- Žádné závislosti
- 30-45 minut
- Quick win pro momentum

**POTOM:**
- **Pokud chceš rychle zvýšit %:** → Creature Variants (5A-N)
- **Pokud chceš hexcrawl:** → Hex Generator (6A)

Obě cesty jsou správné podle bottom-up principu!

---

**Vytvořeno:** 2025-11-02
**Zdroje:** 11_HEXCRAWL_SETUP.md, 14_DUNGEON_CREATION.md, ROADMAP.md
