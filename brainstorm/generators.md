# Nápady na Generátory

## ✅ Generátor postav - HOTOVO
**Status**: ✅ IMPLEMENTOVÁNO (Fáze 2 + 2A + 2B)

**Popis**: Generování náhodných myších postav včetně pozadí, povolání, vzhledu a vybavení

**Funkce**:
- ✅ Náhodné vlastnosti (STR, DEX, WIL) - 3k6 keep 2
- ✅ Náhodné pozadí (36 původů) podle BO × Ďobky
- ✅ Generování jména (k100 + k20, male/female varianty)
- ✅ Rodná znamení (k6)
- ✅ Barvy a vzory srsti (k6)
- ✅ Výchozí vybavení dle původu
- ✅ Export do JSON

**Data implementovaná**:
- ✅ Origins table (36 původů)
- ✅ Names tables (100 jmen + 20 příjmení)
- ✅ Birthsigns (6 znamení)
- ✅ Coat colors/patterns (6+6)

**CLI**: `python -m src.cli generate character`
**Testy**: 16 unit testů (všechny prošly)

---

## Generátor lokací
**Popis**: Generování podzemí, budov, oblastí

**Funkce**:
- Náhodné místnosti a jejich propojení
- Obsah místností (nepřátelé, poklady, překážky)
- Popis atmosféry
- Mapy (ASCII nebo grafické)

---

## Generátor questů
**Popis**: Generování úkolů a dobrodružství

**Funkce**:
- Cíl questu
- NPC zadavatel
- Odměna
- Komplikace
- Možné výsledky

---

## ✅ Generátor NPC - HOTOVO
**Status**: ✅ IMPLEMENTOVÁNO (Fáze 3A)

**Popis**: Generování NPC postav pro DM

**Funkce**:
- ✅ Jméno (male/female varianty)
- ✅ Společenské postavení + platba (k6)
- ✅ Rodné znamení (k6)
- ✅ Vzhled (k20)
- ✅ Zvláštnost/osobnost (k20)
- ✅ Motivace - po čem touží (k20)
- ✅ Vztah k jiné myši (k20)
- ✅ Reakce při setkání (2k6)
- ✅ Export do JSON

**Rozšířená data**:
- ✅ Hireling types (9 typů pronajímatelných pomocníků)
- ✅ Competitive mice (6 konkurenčních dobrodruhů)
- ✅ Cat lords (6 kočičích pánů)
- ✅ Rat gangs (6 krysích gangů)
- ✅ Owl wizards (6 sovích čarodějů)
- ✅ Frog knights (6 žabích rytířů)
- ✅ Adventure seeds (36 semínek - k66)

**CLI**: `python -m src.cli generate npc`
**Testy**: 19 unit testů (všechny prošly)

---

## Další nápady
- Generátor pokladů
- Generátor počasí a událostí
- Generátor fakcí
- Generátor oblastí/hexů na mapě
