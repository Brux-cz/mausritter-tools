"""
Generator náhodných kouzel
"""
from typing import Optional, Dict, Any, List
from dataclasses import asdict
import json

from src.core.dice import roll_d8
from src.core.models import Spell
from src.core.tables import TableLoader


class SpellGenerator:
    """
    Generátor náhodných kouzel podle pravidel Mausritter.
    Používá tabulku z 06_MAGIC.md pro určení náhodného kouzla.

    Mechanika:
    - Při objevení kouzla hoď 2d8 (výsledek 2-16)
    - Každý výsledek odpovídá jednomu kouzlu
    - Kouzla mají [POČET] a [SOUČET] placeholdery pro sesílání (casting)

    Note: Tento generátor slouží pro NALEZENÍ kouzla, ne pro jeho sesílání.
    """

    # Všechna kouzla s jejich roll hodnotami
    SPELL_ROLLS = {
        2: "Ohnivá koule",
        3: "Zahojení",
        4: "Kouzelná střela",
        5: "Strach",
        6: "Tma",
        7: "Zotavení",
        8: "Srozumitelnost",
        9: "Přízračný brouk",
        10: "Světlo",
        11: "Neviditelný prstenec",
        12: "Zaklepání",
        13: "Tuk",
        14: "Zvětšení",
        15: "Neviditelnost",
        16: "Šanta"
    }

    @staticmethod
    def roll_2d8() -> int:
        """
        Hoď 2d8 pro kouzlo.

        Returns:
            int: Výsledek hodu 2d8 (2-16)

        Example:
            >>> roll = SpellGenerator.roll_2d8()
            >>> assert 2 <= roll <= 16
        """
        return roll_d8() + roll_d8()

    @classmethod
    def create(cls) -> Spell:
        """
        Vytvoř náhodné kouzlo.

        Returns:
            Spell: Objekt s názvem, efektem a podmínkou dobití

        Example:
            >>> spell = SpellGenerator.create()
            >>> assert spell.name in SpellGenerator.SPELL_ROLLS.values()
            >>> assert 2 <= spell.roll <= 16
        """
        # Hoď 2d8
        roll = cls.roll_2d8()

        # Lookup v tabulce
        spell_data = TableLoader.lookup_spell(roll)

        if not spell_data:
            # Fallback (nemělo by nastat)
            return Spell(
                roll=roll,
                name="Neznámé kouzlo",
                effect="Efekt není znám.",
                recharge="Podmínka dobití není známa.",
                tags=[],
                notes="Fallback - data nenalezena"
            )

        return Spell(
            roll=roll,
            name=spell_data["name"],
            effect=spell_data["effect"],
            recharge=spell_data["recharge"],
            tags=spell_data.get("tags", []),
            notes=""
        )

    @staticmethod
    def get_spell_category(tags: List[str]) -> str:
        """
        Vrať primární kategorii kouzla podle tagů.

        Args:
            tags: Seznam tagů kouzla

        Returns:
            str: Primární kategorie pro display
        """
        # Priority: damage > healing > utility
        if "damage" in tags:
            return "⚔️ Útok"
        elif "healing" in tags or "buff" in tags:
            return "💚 Podpora"
        elif "debuff" in tags or "crowd-control" in tags:
            return "💀 Oslabení"
        else:
            return "🔮 Utilita"

    @staticmethod
    def get_spell_color(tags: List[str]) -> str:
        """
        Vrať barvu pro dané kouzlo podle kategorií.

        Args:
            tags: Seznam tagů kouzla

        Returns:
            str: Název barvy ("red", "green", "blue", atd.)
        """
        if "damage" in tags:
            return "red"
        elif "healing" in tags or "buff" in tags:
            return "green"
        elif "debuff" in tags or "crowd-control" in tags:
            return "yellow"
        else:
            return "cyan"

    @staticmethod
    def to_dict(spell: Spell) -> Dict[str, Any]:
        """
        Převeď kouzlo na dictionary.

        Args:
            spell: Spell objekt

        Returns:
            Dict obsahující všechny informace o kouzlu

        Example:
            >>> spell = SpellGenerator.create()
            >>> data = SpellGenerator.to_dict(spell)
            >>> assert "name" in data
            >>> assert "effect" in data
        """
        return asdict(spell)

    @staticmethod
    def to_json(spell: Spell, indent: int = 2) -> str:
        """
        Převeď kouzlo na JSON string.

        Args:
            spell: Spell objekt
            indent: Odsazení JSON (default: 2)

        Returns:
            JSON string reprezentace kouzla

        Example:
            >>> spell = SpellGenerator.create()
            >>> json_str = SpellGenerator.to_json(spell)
            >>> assert "name" in json_str
        """
        data = SpellGenerator.to_dict(spell)
        return json.dumps(data, ensure_ascii=False, indent=indent)
