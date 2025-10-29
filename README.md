# Mausritter Tools

Python nástroje a generátory pro stolní hru Mausritter.

## O Projektu

Tento projekt poskytuje sadu nástrojů a generátorů pro hru Mausritter - OSR TTRPG o myších dobrodružích. Cílem je usnadnit práci Dungeon Masterům a hráčům pomocí automatizace běžných úkolů a generování obsahu.

## Struktura Projektu

```
mausritter/
├── src/                    # Python zdrojové kódy
│   ├── core/              # Základní moduly (models, dice)
│   ├── generators/        # Generátory postav, lokací, atd.
│   └── tools/             # Nástroje (inventory, dice roller)
├── docs/                   # Dokumentace
│   ├── rules/             # Zpracovaná pravidla (pro AI)
│   │   ├── databaze/
│   │   ├── mechaniky/
│   │   └── vybaveni/
│   └── original/          # Původní dokumenty
├── brainstorm/            # Nápady a zadání
├── sessions/              # Session notes (udržení kontextu)
├── tests/                 # Testy
├── data/                  # Datové soubory (JSON/YAML)
└── README.md
```

## Instalace

```bash
# Vytvoř virtuální prostředí
python -m venv venv

# Aktivuj (Windows)
venv\Scripts\activate

# Aktivuj (Linux/Mac)
source venv/bin/activate

# Nainstaluj závislosti
pip install -r requirements.txt

# Pro development
pip install -r requirements-dev.txt
```

## Použití

### Dice Roller

```python
from src.core.dice import roll, roll_d20, attribute_test

# Základní hody
result = roll("2d6")
result = roll_d20()

# Test vlastnosti
success, roll_value = attribute_test(attribute_value=12, modifier=0)
```

### Generátory

```python
# TODO: Implementovat generátory
# from src.generators.character import generate_character
#
# character = generate_character()
# print(character.name, character.background)
```

## Plánované Funkce

### V0.1 - MVP
- [ ] Generátor postav
- [ ] CLI rozhraní
- [ ] Export do JSON/markdown

### V0.2+
- [ ] Generátor lokací
- [ ] Generátor NPCs
- [ ] Generátor questů
- [ ] Správa inventáře
- [ ] DM Screen nástroje

Více v [brainstorm/features.md](brainstorm/features.md)

## Session Notes

Pro udržení kontextu mezi AI konverzacemi používáme `sessions/` adresář. Každá session má svůj markdown soubor s poznámkami o tom, co bylo řešeno a jaké soubory byly načteny.

Viz [sessions/README.md](sessions/README.md) pro více informací.

## Brainstorming

Nápady, zadání a diskuze najdeš v adresáři `brainstorm/`:
- [ideas.md](brainstorm/ideas.md) - Obecné nápady
- [generators.md](brainstorm/generators.md) - Nápady na generátory
- [tools.md](brainstorm/tools.md) - Nápady na nástroje
- [features.md](brainstorm/features.md) - Konkrétní funkce
- [questions.md](brainstorm/questions.md) - Otázky k řešení

## Vývoj

```bash
# Spusť testy
pytest

# Code formatting
black src/

# Type checking
mypy src/
```

## Dokumentace Pravidel

Pravidla Mausritter jsou zpracována do strukturované formy v `docs/rules/` pro snadné vyhledávání AI. Původní soubory jsou v `docs/original/`.

## Licence

Mausritter je © Games Omnivorous. Tento projekt je neoficiální fan-made nástroj.

## Přispění

Pro nápady a bug reporty otevři issue nebo přidej nápad do `brainstorm/`.
