"""
Generator pomocníků (hirelings) podle pravidel Mausritter
"""
import random
from typing import Optional, Dict, Any
from dataclasses import asdict
import json

from src.core.dice import roll_d6, roll
from src.core.models import Hireling
from src.core.tables import TableLoader


class HirelingGenerator:
    """
    Generátor náhodných pomocníků (hirelings) podle pravidel Mausritter.
    Používá tabulky z 10_HIRELINGS.md pro vytvoření pronajímatelných myší.
    """

    @staticmethod
    def generate_name(gender: str = "male") -> str:
        """
        Vygeneruj náhodné myší jméno.

        Args:
            gender: "male" nebo "female" pro správný tvar příjmení

        Returns:
            "Jméno Příjmení" (např. "Pepřík Hrabal")

        Example:
            >>> name = HirelingGenerator.generate_name()
            >>> assert ' ' in name  # Musí obsahovat mezeru
        """
        # Vlastní jméno (k100)
        first_roll = random.randint(1, 100)
        first_name = TableLoader.lookup_first_name(first_roll)

        # Mateřské jméno (k20)
        family_roll = random.randint(1, 20)
        family_name = TableLoader.lookup_family_name(family_roll, gender)

        # Fallback pokud lookup selhal
        if not first_name:
            first_name = "Neznámá"
        if not family_name:
            family_name = "Myš" if gender == "female" else "Myšák"

        return f"{first_name} {family_name}"

    @staticmethod
    def roll_stats() -> tuple[int, int, int, int]:
        """
        Hoď statistiky pro pomocníka.

        Podle pravidel:
        - HP: k6 (Body ochrany)
        - STR/DEX/WIL: 2k6 každý

        Returns:
            Tuple (hp, strength, dexterity, willpower)

        Example:
            >>> hp, str, dex, wil = HirelingGenerator.roll_stats()
            >>> assert 1 <= hp <= 6
            >>> assert 2 <= str <= 12
            >>> assert 2 <= dex <= 12
            >>> assert 2 <= wil <= 12
        """
        hp = roll_d6()
        strength = roll("2d6")
        dexterity = roll("2d6")
        willpower = roll("2d6")

        return hp, strength, dexterity, willpower

    @staticmethod
    def select_hireling_type(type_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Vyber typ pomocníka.

        Args:
            type_id: ID typu (1-9) nebo None pro náhodný výběr

        Returns:
            Dict s informacemi o typu pomocníka

        Example:
            >>> hireling_type = HirelingGenerator.select_hireling_type(6)
            >>> assert hireling_type["name"] == "Zbrojmyš"
        """
        if type_id is None:
            # Náhodný výběr z 9 typů
            type_id = random.randint(1, 9)

        hireling_type_data = TableLoader.lookup_hireling_type(type_id)

        if not hireling_type_data:
            # Fallback - vrať základního dělníka
            return {
                "id": 2,
                "name": "Dělník",
                "available": "k6",
                "daily_wage": 2,
                "description": "Běžný pracovní pomocník"
            }

        return hireling_type_data

    @staticmethod
    def calculate_availability(hireling_type: Dict[str, Any]) -> int:
        """
        Vypočítej kolik pomocníků tohoto typu je k dispozici.

        Args:
            hireling_type: Dictionary s informacemi o typu (obsahuje "available" klíč)

        Returns:
            Počet dostupných pomocníků (1-6 podle typu)

        Example:
            >>> hireling_type = {"available": "k6"}
            >>> count = HirelingGenerator.calculate_availability(hireling_type)
            >>> assert 1 <= count <= 6
        """
        available_dice = hireling_type.get("available", "k6")

        # Parse dostupnost (např. "k6", "k4", "k3", "k2")
        if available_dice == "k6":
            return roll_d6()
        elif available_dice == "k4":
            return random.randint(1, 4)
        elif available_dice == "k3":
            return random.randint(1, 3)
        elif available_dice == "k2":
            return random.randint(1, 2)
        else:
            # Fallback
            return roll_d6()

    @classmethod
    def create(cls,
               type_id: Optional[int] = None,
               name: Optional[str] = None,
               gender: str = "male") -> tuple[Hireling, int]:
        """
        Vytvoř kompletního náhodného pomocníka.

        Args:
            type_id: Volitelné ID typu (1-9), jinak náhodný
            name: Volitelné vlastní jméno, jinak náhodné
            gender: "male" nebo "female"

        Returns:
            Tuple (Hireling instance, availability count)

        Example:
            >>> hireling, available = HirelingGenerator.create()
            >>> assert hireling.name
            >>> assert 1 <= hireling.hp <= 6
            >>> assert 1 <= available <= 6
        """
        # 1. Vyber typ pomocníka
        hireling_type = cls.select_hireling_type(type_id)

        # 2. Vygeneruj nebo použij jméno
        if name is None:
            name = cls.generate_name(gender)

        # 3. Hoď statistiky
        hp, strength, dexterity, willpower = cls.roll_stats()

        # 4. Vytvoř pomocníka
        hireling = Hireling(
            name=name,
            type=hireling_type["name"],
            daily_wage=hireling_type["daily_wage"],
            hp=hp,
            strength=strength,
            dexterity=dexterity,
            willpower=willpower,
            inventory=[None] * 6,  # 6 prázdných slotů
            level=1,
            experience=0,
            morale="neutrální",
            notes=hireling_type.get("description", "")
        )

        # 5. Vypočítej dostupnost
        availability = cls.calculate_availability(hireling_type)

        return hireling, availability

    @staticmethod
    def to_dict(hireling: Hireling) -> Dict[str, Any]:
        """
        Konvertuj Hireling do dictionary.

        Args:
            hireling: Hireling instance

        Returns:
            Dictionary reprezentace pomocníka

        Example:
            >>> hireling, _ = HirelingGenerator.create()
            >>> data = HirelingGenerator.to_dict(hireling)
            >>> assert "name" in data
            >>> assert "hp" in data
        """
        return asdict(hireling)

    @staticmethod
    def to_json(hireling: Hireling, indent: int = 2) -> str:
        """
        Konvertuj Hireling do JSON stringu.

        Args:
            hireling: Hireling instance
            indent: Počet mezer pro odsazení (default 2)

        Returns:
            JSON string reprezentace pomocníka

        Example:
            >>> hireling, _ = HirelingGenerator.create()
            >>> json_str = HirelingGenerator.to_json(hireling)
            >>> assert '"name":' in json_str
        """
        data = HirelingGenerator.to_dict(hireling)
        return json.dumps(data, ensure_ascii=False, indent=indent)
