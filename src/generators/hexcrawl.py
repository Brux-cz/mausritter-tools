"""
HexcrawlGenerator - orchestrátor pro generování kompletního hexcrawlu

Podle oficiálních pravidel Mausritter (11_HEXCRAWL_SETUP.md):
- VŽDY 5×5 jednomílových hexů (25 celkem)
- 1-3 settlements
- 2-4 adventure sites (dungeons)
- k6 tabulka zvěstí

Zdroj: Mausritter Rulebook str. 21-27
"""

import json
from dataclasses import asdict
from typing import Optional, Dict, Any
from src.core.models import Hexcrawl
from src.generators.settlement import SettlementGenerator
from src.generators.hex import HexGenerator
from src.generators.dungeon import DungeonGenerator
from src.generators.rumor import RumorGenerator


class HexcrawlGenerator:
    """
    Orchestrátor pro generování kompletního hexcrawlu.

    Neimplementuje generační logiku znovu - pouze volá existující generátory
    a kombinuje jejich výstupy podle oficiálních pravidel.
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
            "description": "Podle oficiálních pravidel Mausritter (Hrabství Ek)",
            "hexes": 25,  # VŽDY 5×5 podle pravidel!
            "settlements": 3,
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
        settlements: Optional[int] = None,
        dungeons: Optional[int] = None,
        factions: Optional[int] = None
    ) -> Hexcrawl:
        """
        Vygeneruj kompletní hexcrawl podle oficiálních pravidel.

        VŽDY generuje 5×5 mapu (25 hexů) jak doporučuje rulebook.

        Args:
            preset: Preset ("starter", "standard", "advanced")
            settlements: Override počtu settlements (1-3)
            dungeons: Override počtu dungeonů (2-4)
            factions: Override počtu frakcí (0-4)

        Returns:
            Hexcrawl objekt s 25 hexy a všemi komponentami

        Raises:
            ValueError: Pokud preset není platný
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
                "hexes": [asdict(h) for h in generated_hexes],
                "settlements": [asdict(s) for s in generated_settlements],
                "dungeons": [asdict(d) for d in generated_dungeons]
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
        return json.dumps(
            HexcrawlGenerator.to_dict(hexcrawl),
            ensure_ascii=False,
            indent=indent
        )
