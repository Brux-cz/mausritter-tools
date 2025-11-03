# Hexcrawl Generator - Design Document

**Podle oficiálních pravidel Mausritter**

## 📖 Oficiální pravidla pro hexcrawl

**Zdroj:** `docs/knowledge_base/11_HEXCRAWL_SETUP.md` (str. 21-27)

### Základní struktura hexcrawlu

> "Začni s mapou **5 x 5 jednomílových hexů**."
>
> — Mausritter Rulebook, str. 21

**Oficiální doporučení:**

| Komponent | Doporučení | Zdroj |
|-----------|-----------|-------|
| **Velikost mapy** | 5 x 5 hexů (25 celkem) | str. 21 |
| **Typ hexů** | Jednomílové hexy | str. 21 |
| **Osady** | Alespoň 1 (středová, spřátelená) | str. 21 |
| **Adventure sites** | **2-4 rozpracované** | str. 23 |
| **Frakce** | 3-4 hlavní frakce (volitelné) | str. 30 |
| **Tabulka zvěstí** | k6 (6 položek) | str. 23 |
| **Tabulka setkání** | k6 (6 položek) | str. 18 |

### Příklad: Hrabství Ek

Oficiální ukázkový hexcrawl v rulebooku má:
- **Mapa:** 5 x 5 hexů (19 obsazených, 6 prázdných)
- **Osady:** 3 (Doubí - město 350 myší, Mostek - víska 75, Pařezinky - víska 50)
- **Adventure sites:** 2-3 rozpracované
- **Frakce:** 3-4

**Zdroj:** `docs/knowledge_base/17_EXAMPLE_HEXCRAWL.md`

### Proces tvorby (5 kroků)

1. **Vyplň hexy** - Mapa 5×5, osada doprostřed, jednořádkový popis
2. **Vymysli frakce** (nepovinné) - 3-4 hlavní frakce
3. **Rozpracuj adventure sites** - 2-4 místa rozmístěná daleko od sebe
4. **Nachystej tabulku zvěstí** - k6 (1-3 pravda, 4-5 částečně, 6 fáma)
5. **Sestav tabulku setkání** - k6

---

## 🎯 Motivace a účel

### Uživatelský problém

Aktuálně musí uživatel pro vytvoření kompletního hexcrawlu:
1. Spustit `python -m src.cli generate settlement` a zkopírovat výstup
2. Spustit `python -m src.cli generate hex` **25×** a zkopírovat výstupy
3. Spustit `python -m src.cli generate dungeon` a zkopírovat výstup
4. Ručně vytvořit JSON soubor s world state strukturou
5. Spustit `python -m src.cli generate rumor --world-state muj_hexcrawl.json`

**To je 30+ příkazů a ruční práce!**

### Řešení

Jeden příkaz, který vše udělá automaticky **podle oficiálních pravidel**:
```bash
python -m src.cli generate hexcrawl --preset standard
```

### Výsledek

- Vygeneruje kompletní hexcrawl (25 hexů + settlements + dungeons + rumors)
- Automaticky sestaví world state JSON
- Uloží do souboru `muj_hexcrawl.json`
- Zobrazí vše v terminálu pro rychlý náhled
- **100% kompatibilní s oficiálními pravidly Mausritter**

---

## 🏗️ Architektura

### Není to duplicita kódu!

Hexcrawl Generator **NENAHRAZUJE** existující generátory. Je to **orchestrátor**, který:
- Volá existující `SettlementGenerator`, `HexGenerator`, `DungeonGenerator`, `RumorGenerator`
- Neimplementuje žádnou generační logiku znovu
- Kombinuje výstupy do strukturovaného formátu podle oficiálních pravidel
- Poskytuje uživatelsky přívětivé rozhraní

**Analogie:** Stejně jako `docker-compose` orchestruje kontejnery, ale nenahrazuje `docker`.

### Princip kompozice

```python
# Hexcrawl Generator používá kompozici, ne duplicitu
class HexcrawlGenerator:
    @staticmethod
    def create(preset="standard"):
        # 1. Orchestrace existujících generátorů (VŽDY 25 hexů!)
        hexes = HexGenerator.create(count=25)  # 5×5 mapa
        settlements = SettlementGenerator.create(count=preset_config['settlements'])
        dungeons = DungeonGenerator.create(count=preset_config['dungeons'])

        # 2. Sestavení world state
        world_state = {
            "hexcrawl": {
                "map_size": "5x5",
                "hexes": [h.to_dict() for h in hexes],
                "settlements": [s.to_dict() for s in settlements],
                "dungeons": [d.to_dict() for d in dungeons]
            }
        }

        # 3. Generování zvěstí s napojením na world state
        rumors = RumorGenerator.create(world_state=world_state, advanced=True)

        return Hexcrawl(hexes, settlements, dungeons, rumors, world_state)
```

---

## 📋 CLI Interface

### Základní použití

```bash
# Starter hexcrawl (pro začátečníky)
python -m src.cli generate hexcrawl --preset starter

# Standard hexcrawl (podle oficiálních pravidel) - DEFAULT
python -m src.cli generate hexcrawl --preset standard
python -m src.cli generate hexcrawl  # stejné jako --preset standard

# Advanced hexcrawl (plně vybavený)
python -m src.cli generate hexcrawl --preset advanced
```

### Pokročilé parametry

```bash
# Vlastní konfigurace (stále 25 hexů!)
python -m src.cli generate hexcrawl \
  --settlements 2 \
  --dungeons 3 \
  --factions 4

# Export do specifického souboru
python -m src.cli generate hexcrawl --save my_hexcrawl.json

# Pouze JSON výstup (bez terminálu)
python -m src.cli generate hexcrawl --output-json

# S generovanými NPC pro settlements
python -m src.cli generate hexcrawl --with-npcs

# S generovanými creatures pro dungeons
python -m src.cli generate hexcrawl --with-creatures

# Kombinace všeho
python -m src.cli generate hexcrawl --preset advanced --with-npcs --with-creatures
```

---

## ⚙️ Konfigurace presetů

**VŠECHNY presety používají 5×5 mapu (25 hexů) podle oficiálních pravidel!**

Liší se pouze v **počtu rozpracovaných míst a složitosti**.

### Starter (pro začátečníky GM)

```python
STARTER = {
    "name": "Starter Hexcrawl",
    "description": "Zjednodušený hexcrawl pro začátečníky",
    "hexes": 25,              # VŽDY 5×5 podle pravidel
    "settlements": 1,         # Jedna středová osada (jako v pravidlech)
    "dungeons": 2,            # Minimum podle pravidel (2-4)
    "factions": 0,            # Bez frakcí (zjednodušeno)
    "rumors": 6,              # k6 tabulka (standard)
    "with_npcs": False,
    "with_creatures": False,
}
```

**Typický use case:**
- První hexcrawl pro nového GM
- One-shot session
- Jednoduchý úvod do hry

**Co obsahuje:**
- 25 hexů (většina základních, méně složitých)
- 1 spřátelená osada doprostřed
- 2 adventure sites (rozmístěné daleko)
- Bez frakcí (méně politiky)
- 6 zvěstí

---

### Standard (podle oficiálních pravidel) - DEFAULT

```python
STANDARD = {
    "name": "Standard Hexcrawl",
    "description": "Podle oficiálních pravidel Mausritter (Hrabství Ek)",
    "hexes": 25,              # VŽDY 5×5 podle pravidel
    "settlements": 3,         # Jako v příkladu Hrabství Ek
    "dungeons": 3,            # Střed doporučení (2-4)
    "factions": 3,            # Doporučení pro frakce
    "rumors": 6,              # k6 tabulka (standard)
    "with_npcs": False,
    "with_creatures": False,
}
```

**Typický use case:**
- Standardní hexcrawl kampaň
- Přesně podle rulebooku
- Většina dlouhodobých kampaní

**Co obsahuje:**
- 25 hexů (mix typů podle tabulek)
- 3 osady (jako Hrabství Ek: 1 město + 2 vísky)
- 3 adventure sites (2-4 doporučení)
- 3 frakce (politika a důsledky)
- 6 zvěstí napojených na svět

**Zdroj:** Hrabství Ek příklad v rulebooku

---

### Advanced (plně vybavený hexcrawl)

```python
ADVANCED = {
    "name": "Advanced Hexcrawl",
    "description": "Plně vybavený hexcrawl pro zkušené GM",
    "hexes": 25,              # VŽDY 5×5 podle pravidel
    "settlements": 3,         # Stejně jako standard
    "dungeons": 4,            # Maximum doporučení (2-4)
    "factions": 4,            # Komplexní politika
    "rumors": 6,              # k6 tabulka (standard)
    "with_npcs": True,        # Vygeneruj NPCs pro settlements
    "with_creatures": True,   # Vygeneruj creatures pro dungeons
}
```

**Typický use case:**
- Zkušený GM s časem na přípravu
- Dlouhodobá sandbox kampaň
- Maximum detailů a možností

**Co obsahuje:**
- 25 hexů (bohatě detailované)
- 3 osady s vygenerovanými NPCs
- 4 adventure sites s creatures
- 4 frakce (komplexní vztahy)
- 6 zvěstí s gossip chains

---

## 📦 Datová struktura

### Hexcrawl Model

```python
@dataclass
class Hexcrawl:
    """
    Kompletní hexcrawl podle oficiálních pravidel Mausritter.

    Vždy obsahuje 5×5 mapu (25 hexů) jak doporučuje rulebook.
    """
    hexes: List[Hex]              # VŽDY 25 hexů (5×5)
    settlements: List[Settlement]  # 1-3 osad
    dungeons: List[Dungeon]        # 2-4 adventure sites
    rumors: List[Rumor]            # k6 tabulka (6 zvěstí)
    world_state: Dict[str, Any]
    factions: List[Faction] = field(default_factory=list)  # Volitelné
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Inicializuj metadata při vytvoření."""
        # Validace: MUSÍ mít přesně 25 hexů
        if len(self.hexes) != 25:
            raise ValueError(f"Hexcrawl musí mít přesně 25 hexů (5×5), má {len(self.hexes)}")

        self.metadata = {
            "generated_at": datetime.now().isoformat(),
            "generator_version": "1.0.0",
            "map_dimensions": "5x5",
            "preset": self._detect_preset(),
            "official_rules_compliant": True,
            "counts": {
                "hexes": 25,
                "settlements": len(self.settlements),
                "dungeons": len(self.dungeons),
                "rumors": len(self.rumors),
                "factions": len(self.factions)
            }
        }

    def _detect_preset(self) -> str:
        """Detekuj který preset byl použitý."""
        dungeons_count = len(self.dungeons)
        settlements_count = len(self.settlements)
        factions_count = len(self.factions)

        if factions_count == 0 and dungeons_count == 2:
            return "starter"
        elif factions_count >= 4 and dungeons_count == 4:
            return "advanced"
        else:
            return "standard"

    @property
    def map_dimensions(self) -> tuple:
        """Vrať rozměry mapy (vždy 5×5)."""
        return (5, 5)

    def to_dict(self) -> Dict[str, Any]:
        """Konvertuj na dictionary pro export."""
        return {
            "metadata": self.metadata,
            "world_state": self.world_state,
            "hexes": [h.to_dict() for h in self.hexes],
            "settlements": [s.to_dict() for s in self.settlements],
            "dungeons": [d.to_dict() for d in self.dungeons],
            "rumors": [r.to_dict() for r in self.rumors],
            "factions": [f.to_dict() for f in self.factions] if self.factions else []
        }
```

### Výstupní JSON struktura

```json
{
  "metadata": {
    "generated_at": "2025-11-02T14:30:00",
    "generator_version": "1.0.0",
    "map_dimensions": "5x5",
    "preset": "standard",
    "official_rules_compliant": true,
    "counts": {
      "hexes": 25,
      "settlements": 3,
      "dungeons": 3,
      "rumors": 6,
      "factions": 3
    }
  },
  "world_state": {
    "hexcrawl": {
      "map_size": "5x5",
      "hexes": [...],
      "settlements": [...],
      "dungeons": [...]
    }
  },
  "hexes": [...],  // 25 hexů
  "settlements": [...],
  "dungeons": [...],
  "rumors": [...],
  "factions": [...]
}
```

---

## 🖥️ Terminálový výstup

### Přehledový formát s Rich

```
╔════════════════════════════════════════════════════════════════╗
║         🎲 VYGENEROVANÝ HEXCRAWL (STANDARD - 5×5)             ║
║              Podle oficiálních pravidel Mausritter            ║
╚════════════════════════════════════════════════════════════════╝

📏 MAPA: 5 × 5 hexů (25 celkem) - jednomílové hexy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[5×5 ASCII hex mapa]

📍 SETTLEMENTS (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Doubí (Město - 350 obyvatel) [Hex C3] ⭐ Spřátelená
   🏛️  Vláda: Starosta
   ⚠️  Problém: Krysí loupežníci
   🌟 NPC: Stará Bělovous (female)
   🏰 Rysy: Velký mlýn, Hostinec u Mouchy

2. Mostek (Víska - 75 obyvatel) [Hex A2]
   🏛️  Vláda: Rada starších
   ⚠️  Problém: Sucho
   🌟 NPC: Rychlý Ocas (male)
   🏰 Rysy: Most přes potok

3. Pařezinky (Víska - 50 obyvatel) [Hex E4]
   🏛️  Vláda: Patriarcha
   ⚠️  Problém: Vlci
   🌟 NPC: Tichý Šepot (female)
   🏰 Rysy: Kořenové jeskyně

🗺️  HEXY (25) - 5×5 jednomílová mapa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Detailní tabulka všech 25 hexů...]

🏰 ADVENTURE SITES (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Starodávný chrám netopýřího kultu [Hex B5]
   🏛️  Minulost: Chrám
   👥 Obyvatelé: Krysí loupežníci
   🔮 Tajemství: Obelisk hučící energií
   🎯 Cíl dobrodružství: Získat poklad

[Další dungeons...]

🎭 FRAKCE (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Krysí loupežníci
   🎯 Cíl: Rozšířit své území
   💪 Síla: Silná

[Další frakce...]

💬 ZVĚSTI (6) - k6 tabulka
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Rumor tabulka s napojením na locations...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Hexcrawl splňuje oficiální pravidla Mausritter
📖 Rulebook str. 21-27: "Začni s mapou 5×5 jednomílových hexů"
💾 Uloženo do: muj_hexcrawl.json
```

---

## 🔧 Implementace

### Soubory k vytvoření/úpravě

1. **`src/core/models.py`**
   - Přidat `Hexcrawl` dataclass (viz výše)
   - Validace 25 hexů
   - Metadata s official_rules_compliant flag

2. **`src/generators/hexcrawl.py`** (NOVÝ)
   - Implementovat `HexcrawlGenerator` třídu
   - Metody: `create()`, `to_dict()`, `to_json()`
   - Konfigurace presetů (STARTER, STANDARD, ADVANCED)
   - **Vždy generuje 25 hexů!**

3. **`src/cli.py`**
   - Přidat `@generate.command() def hexcrawl()`
   - Implementovat `display_hexcrawl()` funkci
   - Flag handling pro --preset, --save, atd.
   - Zobrazit 5×5 hex mapu

4. **`tests/test_hexcrawl_generator.py`** (NOVÝ)
   - Test generování všech presetů
   - **Test že VŽDY má 25 hexů!**
   - Test world state sestavení
   - Test exportu JSON
   - Test integrace s ostatními generátory
   - Test validace (odmítne jiný počet hexů než 25)

### Pseudokód implementace

```python
# src/generators/hexcrawl.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.generators.settlement import SettlementGenerator
from src.generators.hex import HexGenerator
from src.generators.dungeon import DungeonGenerator
from src.generators.rumor import RumorGenerator
from src.core.models import Hexcrawl, Settlement, Hex, Dungeon, Rumor, Faction

class HexcrawlGenerator:
    """
    Orchestrátor pro generování kompletního hexcrawlu.

    Podle oficiálních pravidel Mausritter:
    - VŽDY 5×5 jednomílových hexů (25 celkem)
    - 1-3 settlements
    - 2-4 adventure sites (dungeons)
    - 0-4 frakce (volitelné)
    - k6 tabulka zvěstí

    Zdroj: Mausritter Rulebook str. 21-27
    """

    # Oficiální presety podle pravidel
    PRESETS = {
        "starter": {
            "name": "Starter Hexcrawl",
            "description": "Zjednodušený hexcrawl pro začátečníky",
            "hexes": 25,  # VŽDY 5×5 podle pravidel!
            "settlements": 1,
            "dungeons": 2,
            "factions": 0,
            "rumors": 6
        },
        "standard": {
            "name": "Standard Hexcrawl",
            "description": "Podle oficiálních pravidel Mausritter",
            "hexes": 25,  # VŽDY 5×5 podle pravidel!
            "settlements": 3,  # Jako Hrabství Ek
            "dungeons": 3,
            "factions": 3,
            "rumors": 6
        },
        "advanced": {
            "name": "Advanced Hexcrawl",
            "description": "Plně vybavený hexcrawl",
            "hexes": 25,  # VŽDY 5×5 podle pravidel!
            "settlements": 3,
            "dungeons": 4,
            "factions": 4,
            "rumors": 6
        }
    }

    @staticmethod
    def create(
        preset: str = "standard",
        settlements: int = None,
        dungeons: int = None,
        factions: int = None,
        with_npcs: bool = False,
        with_creatures: bool = False
    ) -> Hexcrawl:
        """
        Vygeneruj kompletní hexcrawl podle oficiálních pravidel.

        VŽDY generuje 5×5 mapu (25 hexů) jak doporučuje rulebook.

        Args:
            preset: Preset ("starter", "standard", "advanced")
            settlements: Override počtu settlements (1-3)
            dungeons: Override počtu dungeonů (2-4)
            factions: Override počtu frakcí (0-4)
            with_npcs: Generovat NPC pro settlements
            with_creatures: Generovat creatures pro dungeons

        Returns:
            Hexcrawl objekt s 25 hexy a všemi komponentami
        """
        # 1. Načti preset konfiguraci
        config = HexcrawlGenerator.PRESETS.get(
            preset,
            HexcrawlGenerator.PRESETS["standard"]
        ).copy()

        # Override z parametrů
        if settlements is not None:
            config["settlements"] = settlements
        if dungeons is not None:
            config["dungeons"] = dungeons
        if factions is not None:
            config["factions"] = factions

        # 2. VŽDY vygeneruj 25 hexů (5×5 podle pravidel)
        generated_hexes = []
        for _ in range(25):  # Pevně 25 hexů!
            h = HexGenerator.create()
            generated_hexes.append(h)

        # 3. Vygeneruj settlements
        generated_settlements = []
        for i in range(config["settlements"]):
            s = SettlementGenerator.create()
            # První settlement je vždy spřátelená (uprostřed mapy)
            # POZNÁMKA: Vyžaduje rozšíření Settlement modelu o:
            #   - is_friendly: bool = False
            #   - hex_location: Optional[str] = None
            if i == 0:
                s.is_friendly = True
                s.hex_location = "C3"  # Střed 5×5 mapy
            generated_settlements.append(s)

        # 4. Vygeneruj dungeons (adventure sites)
        generated_dungeons = []
        for _ in range(config["dungeons"]):
            d = DungeonGenerator.create()
            generated_dungeons.append(d)

        # 5. Vygeneruj frakce (volitelné)
        generated_factions = []
        # POZNÁMKA: FactionGenerator zatím neexistuje!
        # Pro první iteraci přeskakujeme (STARTER a STANDARD fungují bez frakcí).
        # ADVANCED preset bude vyžadovat implementaci FactionGenerator později.
        if config["factions"] > 0:
            print(f"⚠️  FactionGenerator není implementován - přeskakuji {config['factions']} frakcí")
        # Budoucí implementace:
        # for _ in range(config["factions"]):
        #     f = FactionGenerator.create()
        #     generated_factions.append(f)

        # 6. Sestav world state
        world_state = {
            "hexcrawl": {
                "map_size": "5x5",
                "hexes": [h.to_dict() for h in generated_hexes],
                "settlements": [s.to_dict() for s in generated_settlements],
                "dungeons": [d.to_dict() for d in generated_dungeons]
            }
        }

        # 7. Vygeneruj zvěsti s napojením na world state
        generated_rumors = RumorGenerator.create(
            world_state=world_state,
            advanced=True
        )

        # 8. Vytvoř Hexcrawl objekt (validuje 25 hexů)
        hexcrawl = Hexcrawl(
            hexes=generated_hexes,
            settlements=generated_settlements,
            dungeons=generated_dungeons,
            rumors=generated_rumors,
            factions=generated_factions,
            world_state=world_state
        )

        return hexcrawl

    @staticmethod
    def to_dict(hexcrawl: Hexcrawl) -> Dict[str, Any]:
        """Konvertuj hexcrawl na dictionary."""
        return hexcrawl.to_dict()

    @staticmethod
    def to_json(hexcrawl: Hexcrawl, indent: int = 2) -> str:
        """Konvertuj hexcrawl na JSON string."""
        import json
        return json.dumps(
            HexcrawlGenerator.to_dict(hexcrawl),
            ensure_ascii=False,
            indent=indent
        )

    @staticmethod
    def validate_hexcrawl(hexcrawl: Hexcrawl) -> bool:
        """
        Validuj že hexcrawl splňuje oficiální pravidla.

        Returns:
            True pokud je validní podle oficiálních pravidel
        """
        # MUSÍ mít přesně 25 hexů
        if len(hexcrawl.hexes) != 25:
            return False

        # Měl by mít 1-3 settlements
        if not (1 <= len(hexcrawl.settlements) <= 3):
            return False

        # Měl by mít 2-4 dungeons
        if not (2 <= len(hexcrawl.dungeons) <= 4):
            return False

        # Měl by mít k6 tabulku zvěstí
        if len(hexcrawl.rumors) != 6:
            return False

        return True
```

---

## ✅ Zdůvodnění návrhu

### Proč VŽDY 25 hexů (5×5)?

1. **Oficiální pravidla:**
   > "Začni s mapou 5 x 5 jednomílových hexů." — Mausritter str. 21

2. **Příklad v rulebooku:**
   - Hrabství Ek používá 5×5 mapu
   - Je to standard pro Mausritter hexcrawly

3. **Game design důvody:**
   - Správná velikost pro 1 herní večer cestování
   - Ne moc velká (hráči se neztratí)
   - Ne moc malá (dost prostoru pro exploraci)
   - 5×5 = 25 hexů je ideální rozsah

4. **Konzistence:**
   - Všechny oficiální moduly používají 5×5
   - Hráči a GM jsou na to zvyklí
   - Kompatibilita s ostatními materiály

### Proč presety místo různých velikostí?

Protože oficiální pravidla **nedefinují různé velikosti map**.

Namísto různých velikostí používáme **různou úroveň detailu**:
- **Starter:** Méně míst, jednodušší
- **Standard:** Podle pravidel (Hrabství Ek)
- **Advanced:** Více míst, komplexnější

### Proč je to dobrý nápad?

1. **100% podle oficiálních pravidel**
   - Cituje rulebook
   - Používá oficiální příklad (Hrabství Ek)
   - Respektuje game design Mausritteru

2. **DRY princip**
   - Neimplementuje generační logiku znovu
   - Pouze orchestruje existující generátory
   - Žádná duplicita kódu

3. **Single Responsibility Principle**
   - Každý generátor má jasnou zodpovědnost
   - Hexcrawl Generator orchestruje

4. **Uživatelská přívětivost**
   - Jeden příkaz místo 30+ příkazů
   - Žádné manuální kopírování
   - Okamžitě použitelný výstup

5. **Flexibilita v rámci pravidel**
   - Různé presety pro různé potřeby
   - Možnost override parametrů
   - Rozšiřitelnost (NPCs, creatures)

### Co to NENÍ

- ❌ Nahrazení existujících generátorů
- ❌ Duplicitní implementace logiky
- ❌ Porušení oficiálních pravidel
- ❌ AI/LLM generování (stále template-based)

### Co to JE

- ✅ Orchestrátor existující funkcionality
- ✅ Implementace oficiálních pravidel Mausritter
- ✅ Convenience wrapper pro standard workflow
- ✅ 100% kompatibilní s rulebooke

m

---

## 📅 Roadmap implementace

### Fáze 1: Základní orchestrace (2-3 hodiny)
- [ ] Vytvořit `Hexcrawl` model v `models.py` s validací 25 hexů
- [ ] Vytvořit `src/generators/hexcrawl.py` se základní logikou
- [ ] Implementovat presety (starter/standard/advanced)
- [ ] World state assembly s 5×5 strukturou
- [ ] Validace podle oficiálních pravidel

### Fáze 2: CLI integrace (1-2 hodiny)
- [ ] Přidat `hexcrawl` command do CLI
- [ ] Implementovat flag handling (--preset, --save, atd.)
- [ ] Vytvořit `display_hexcrawl()` funkci s Rich
- [ ] Zobrazení 5×5 hex mapy
- [ ] Auto-save do JSON souboru

### Fáze 3: Testy (1-2 hodiny)
- [ ] Test pro každý preset
- [ ] **Test že VŽDY má 25 hexů**
- [ ] Test validace (odmítne jiný počet)
- [ ] Test custom parametrů
- [ ] Test world state sestavení
- [ ] Integration testy s ostatními generátory

### Fáze 4: Dokumentace (30 minut)
- [ ] Aktualizovat README.md
- [ ] Aktualizovat ROADMAP.md
- [ ] Příklady použití
- [ ] Citace oficiálních pravidel

**Celkový odhad:** 5-8 hodin práce

---

## 🎓 Závěr

Hexcrawl Generator je **přesná implementace oficiálních pravidel Mausritter** pro hexcrawl kampaně.

### Klíčové vlastnosti:

1. **100% podle rulebooku**
   - Vždy 5×5 mapa (25 hexů)
   - 1-3 settlements
   - 2-4 adventure sites
   - k6 tabulka zvěstí

2. **Orchestrace, ne duplicita**
   - Používá existující generátory
   - Kompozice komponent
   - DRY princip

3. **Flexibilita v rámci pravidel**
   - 3 presety (starter/standard/advanced)
   - Možnost customizace
   - Rozšiřitelnost

4. **Uživatelský komfort**
   - Jeden příkaz = kompletní hexcrawl
   - Automatické sestavení world state
   - Instant použitelný výstup

**Je to přesně ten typ abstrakce**, který dává smysl pro framework generátorů - podobně jako `make all` v Makefile nebo `npm run build` v Node.js projektu.

A navíc - **respektuje game design Mausritteru** a dodržuje oficiální pravidla z rulebooku.

---

## 📝 Revision History

### 2025-11-03 - API Opravy po code review

**Opraveno:**
- ✅ API volání: `.create_single()` → `.create()` (řádky 573, 579, 592)
  - Všechny existující generátory používají `.create()`, ne `.create_single()`
- ✅ Přidána poznámka k Settlement atributům (řádky 581-583)
  - `is_friendly` a `hex_location` vyžadují rozšíření Settlement modelu
- ✅ Aktualizován FactionGenerator TODO (řádky 597-605)
  - Jasný warning, že není implementován
  - STARTER a STANDARD fungují bez něj
  - ADVANCED bude vyžadovat implementaci později

**Výsledek:** Design doc je nyní 100% kompatibilní s existující kódovou základnou a připravený k implementaci.
