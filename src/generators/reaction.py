"""
Generator reakcí NPC/tvorů při setkání
"""
from typing import Optional, Dict, Any
from dataclasses import asdict
import json

from src.core.dice import roll_d6
from src.core.models import Reaction
from src.core.tables import TableLoader


class ReactionGenerator:
    """
    Generátor reakcí NPC a tvorů při setkání podle pravidel Mausritter.
    Používá tabulku z 08_GM_GUIDE.md pro určení počáteční dispozice tvora.

    Mechanika:
    - Při setkání s tvorem, když není jasné jak bude reagovat, hoď 2k6
    - Výsledek určuje počáteční náladu (Agresivní → Nápomocná)
    - GM otázka poskytuje inspiraci pro roleplay
    """

    # Mapování reakcí na číselné hodnoty (pro snazší práci)
    REACTION_VALUES = {
        "Agresivní": 2,
        "Nepřátelská": 3,
        "Nejistá": 6,
        "Povídavá": 9,
        "Nápomocná": 12
    }

    @staticmethod
    def roll_reaction() -> int:
        """
        Hoď 2k6 pro reakci.

        Returns:
            int: Výsledek hodu 2k6 (2-12)

        Example:
            >>> roll = ReactionGenerator.roll_reaction()
            >>> assert 2 <= roll <= 12
        """
        return roll_d6() + roll_d6()

    @classmethod
    def create(cls, modifier: int = 0) -> Reaction:
        """
        Vytvoř reakci NPC/tvora.

        Args:
            modifier: Modifikátor k hodu (např. +1 za dárek, -1 za agresi)
                     Default: 0

        Returns:
            Reaction: Objekt s reakcí a GM otázkou

        Example:
            >>> reaction = ReactionGenerator.create()
            >>> assert reaction.reaction in ["Agresivní", "Nepřátelská", "Nejistá", "Povídavá", "Nápomocná"]
            >>> assert len(reaction.question) > 0
        """
        # Hoď 2k6
        roll = cls.roll_reaction()

        # Aplikuj modifikátor (omez na 2-12)
        final_roll = max(2, min(12, roll + modifier))

        # Lookup v tabulce
        reaction_data = TableLoader.lookup_npc_reaction(final_roll)

        if not reaction_data:
            # Fallback (nemělo by nastat)
            return Reaction(
                roll=final_roll,
                reaction="Nejistá",
                question="Co se děje?",
                notes="Fallback - data nenalezena"
            )

        return Reaction(
            roll=final_roll,
            reaction=reaction_data["reaction"],
            question=reaction_data["question"],
            notes=f"Modifikátor: {modifier:+d}" if modifier != 0 else ""
        )

    @staticmethod
    def get_reaction_color(reaction: str) -> str:
        """
        Vrať barvu pro danou reakci (pro terminal display).

        Args:
            reaction: Název reakce

        Returns:
            str: Název barvy ("red", "yellow", "blue", "green", "cyan")
        """
        color_map = {
            "Agresivní": "red",
            "Nepřátelská": "yellow",
            "Nejistá": "blue",
            "Povídavá": "green",
            "Nápomocná": "cyan"
        }
        return color_map.get(reaction, "white")

    @staticmethod
    def to_dict(reaction: Reaction) -> Dict[str, Any]:
        """
        Převeď reakci na dictionary.

        Args:
            reaction: Reaction objekt

        Returns:
            Dict obsahující všechny informace o reakci

        Example:
            >>> reaction = ReactionGenerator.create()
            >>> data = ReactionGenerator.to_dict(reaction)
            >>> assert "reaction" in data
            >>> assert "question" in data
        """
        return asdict(reaction)

    @staticmethod
    def to_json(reaction: Reaction, indent: int = 2) -> str:
        """
        Převeď reakci na JSON string.

        Args:
            reaction: Reaction objekt
            indent: Odsazení JSON (default: 2)

        Returns:
            JSON string reprezentace reakce

        Example:
            >>> reaction = ReactionGenerator.create()
            >>> json_str = ReactionGenerator.to_json(reaction)
            >>> assert "reaction" in json_str
        """
        data = ReactionGenerator.to_dict(reaction)
        return json.dumps(data, ensure_ascii=False, indent=indent)
