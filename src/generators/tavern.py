"""
TavernGenerator - generátor hospod/hostinců

Hospody se objevují ve vískách a větších osadách.
Poskytují jídlo, pití a přístřeší pro místní i pocestné.

Podle oficiálních Mausritter pravidel (12_SETTLEMENTS.md, řádky 240-296).
"""

import json
from typing import Optional
from src.core.models import Tavern
from src.core.tables import TableLoader
from src.core.dice import roll_d12


class TavernGenerator:
    """
    Generátor hospod/hostinců podle oficiálních Mausritter pravidel.

    Mechanika:
    - Název: 2× k12 (přídavné jméno + podstatné jméno)
    - Formát: "U [Část1] [Část2]" → např. "U Bílého Brouka"
    - Specialita: 1× k12 (pokrm nebo nápoj)

    Použití:
        # Náhodná hospoda
        tavern = TavernGenerator.create()

        # S konkrétními hody
        tavern = TavernGenerator.create(roll_part1=1, roll_part2=12, roll_specialty=5)

        # Export do JSON
        json_str = TavernGenerator.to_json(tavern)
    """

    @classmethod
    def create(
        cls,
        roll_part1: Optional[int] = None,
        roll_part2: Optional[int] = None,
        roll_specialty: Optional[int] = None
    ) -> Tavern:
        """
        Vytvoř náhodnou hospodu.

        Args:
            roll_part1: Volitelný hod k12 pro první část názvu (1-12)
            roll_part2: Volitelný hod k12 pro druhou část názvu (1-12)
            roll_specialty: Volitelný hod k12 pro specialitu (1-12)

        Returns:
            Tavern objekt s vygenerovanými daty
        """
        # Generuj hody pokud nejsou zadány
        if roll_part1 is None:
            roll_part1 = roll_d12()
        if roll_part2 is None:
            roll_part2 = roll_d12()
        if roll_specialty is None:
            roll_specialty = roll_d12()

        # Načti data z tabulek
        name_part1 = TableLoader.lookup_tavern_name_part1(roll_part1)
        name_part2 = TableLoader.lookup_tavern_name_part2(roll_part2)
        specialty = TableLoader.lookup_tavern_specialty(roll_specialty)

        # Fallback pokud lookup selže
        if name_part1 is None:
            name_part1 = "Neznámý"
        if name_part2 is None:
            name_part2 = "Hostinec"
        if specialty is None:
            specialty = "Tradiční pokrmy"

        return Tavern(
            name_part1=name_part1,
            name_part2=name_part2,
            specialty=specialty,
            roll_part1=roll_part1,
            roll_part2=roll_part2,
            roll_specialty=roll_specialty
        )

    @staticmethod
    def to_dict(tavern: Tavern) -> dict:
        """
        Převede Tavern objekt na dictionary.

        Args:
            tavern: Tavern objekt

        Returns:
            Dictionary s daty hospody
        """
        return {
            "name_part1": tavern.name_part1,
            "name_part2": tavern.name_part2,
            "full_name": tavern.full_name,
            "specialty": tavern.specialty,
            "roll_part1": tavern.roll_part1,
            "roll_part2": tavern.roll_part2,
            "roll_specialty": tavern.roll_specialty
        }

    @staticmethod
    def to_json(tavern: Tavern, indent: int = 2) -> str:
        """
        Převede Tavern objekt na JSON string.

        Args:
            tavern: Tavern objekt
            indent: Počet mezer pro odsazení (default: 2)

        Returns:
            JSON string
        """
        data = TavernGenerator.to_dict(tavern)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(tavern: Tavern) -> str:
        """
        Naformátuj hospodu jako čitelný text.

        Args:
            tavern: Tavern objekt

        Returns:
            Formátovaný text s informacemi o hospodě
        """
        lines = []
        lines.append("═══ HOSPODA ═══")
        lines.append("")
        lines.append(f"🏠 Název: {tavern.full_name}")
        lines.append(f"🍲 Specialita: {tavern.specialty}")
        lines.append("")
        lines.append(f"🎲 Hody: {tavern.roll_part1}/{tavern.roll_part2} (název), {tavern.roll_specialty} (specialita)")

        return "\n".join(lines)
