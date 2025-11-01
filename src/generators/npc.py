"""
Generator NPC postav podle pravidel Mausritter
"""
import random
from typing import Optional, Dict, Any
from dataclasses import asdict

from src.core.dice import roll_d6, roll_d20
from src.core.models import NPC
from src.core.tables import TableLoader


class NPCGenerator:
    """
    Generátor náhodných NPC podle pravidel Mausritter.
    Používá tabulky z 16_RANDOM_TABLES.md pro rychlé vytvoření nehráčské myši.
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
            >>> name = NPCGenerator.generate_name()
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
    def generate_social_status() -> tuple[str, str]:
        """
        Vygeneruj společenské postavení NPC.

        Returns:
            Tuple (status, payment) - např. ("Prostá myš", "k6 x 10 ď")

        Example:
            >>> status, payment = NPCGenerator.generate_social_status()
            >>> assert status in ["Chuďas", "Prostá myš", "Měšťan", "Člen cechu", "Myší šlechtic"]
        """
        roll = roll_d6()
        status_data = TableLoader.lookup_npc_social_status(roll)

        if status_data:
            return status_data["status"], status_data["payment"]

        # Fallback
        return "Prostá myš", "k6 x 10 ď"

    @staticmethod
    def generate_birthsign() -> str:
        """
        Vygeneruj rodné znamení s povahovým rysem.

        Returns:
            "Znamení (povaha)" - např. "Hvězda (Statečná/zbrklá)"

        Example:
            >>> birthsign = NPCGenerator.generate_birthsign()
            >>> assert '(' in birthsign and ')' in birthsign
        """
        roll = roll_d6()
        birthsign_data = TableLoader.lookup_birthsign(roll)

        if birthsign_data:
            return f"{birthsign_data['name']} ({birthsign_data['trait']})"

        # Fallback
        return "Hvězda (Statečná/zbrklá)"

    @staticmethod
    def generate_appearance() -> str:
        """
        Vygeneruj vzhled NPC.

        Returns:
            Text popisující vzhled - např. "Dlouhé fousky"

        Example:
            >>> appearance = NPCGenerator.generate_appearance()
            >>> assert len(appearance) > 0
        """
        roll = roll_d20()
        appearance = TableLoader.lookup_npc_appearance(roll)

        if appearance:
            return appearance

        # Fallback
        return "Průměrný vzhled"

    @staticmethod
    def generate_quirk() -> str:
        """
        Vygeneruj zvláštnost NPC.

        Returns:
            Text popisující zvláštnost - např. "Extrémně zdvořilá"

        Example:
            >>> quirk = NPCGenerator.generate_quirk()
            >>> assert len(quirk) > 0
        """
        roll = roll_d20()
        quirk = TableLoader.lookup_npc_quirk(roll)

        if quirk:
            return quirk

        # Fallback
        return "Typické chování"

    @staticmethod
    def generate_desire() -> str:
        """
        Vygeneruj tužbu/motivaci NPC.

        Returns:
            Text popisující tužbu - např. "Svoboda", "Bohatství"

        Example:
            >>> desire = NPCGenerator.generate_desire()
            >>> assert len(desire) > 0
        """
        roll = roll_d20()
        desire = TableLoader.lookup_npc_desire(roll)

        if desire:
            return desire

        # Fallback
        return "Bezpečí"

    @staticmethod
    def generate_relationship() -> str:
        """
        Vygeneruj vztah k jiné myši.

        Returns:
            Text popisující vztah - např. "Sourozenec", "Manželé"

        Example:
            >>> relationship = NPCGenerator.generate_relationship()
            >>> assert len(relationship) > 0
        """
        roll = roll_d20()
        relationship = TableLoader.lookup_npc_relationship(roll)

        if relationship:
            return relationship

        # Fallback
        return "Nikdy dřív se nepotkaly"

    @staticmethod
    def generate_reaction() -> str:
        """
        Vygeneruj reakci NPC při setkání.

        Returns:
            "Reakce: Otázka" - např. "Nejistá: Jak si ho můžou naklonit?"

        Example:
            >>> reaction = NPCGenerator.generate_reaction()
            >>> assert ':' in reaction
        """
        # 2k6
        roll = roll_d6() + roll_d6()
        reaction_data = TableLoader.lookup_npc_reaction(roll)

        if reaction_data:
            return f"{reaction_data['reaction']}: {reaction_data['question']}"

        # Fallback
        return "Nejistá: Jak si ho můžou naklonit?"

    @classmethod
    def create(cls, name: Optional[str] = None, gender: str = "male") -> NPC:
        """
        Vytvoř kompletní náhodné NPC.

        Args:
            name: Volitelné vlastní jméno. Pokud None, vygeneruje se náhodné.
            gender: "male" nebo "female" pro správný tvar příjmení

        Returns:
            NPC objekt s vygenerovanými vlastnostmi

        Example:
            >>> npc = NPCGenerator.create()
            >>> assert npc.name
            >>> assert npc.social_status
            >>> assert npc.birthsign
        """
        # Jméno
        if name is None:
            name = cls.generate_name(gender)

        # Společenské postavení
        social_status, payment = cls.generate_social_status()

        # Rodné znamení
        birthsign = cls.generate_birthsign()

        # Vzhled
        appearance = cls.generate_appearance()

        # Zvláštnost
        quirk = cls.generate_quirk()

        # Tužba
        desire = cls.generate_desire()

        # Vztah
        relationship = cls.generate_relationship()

        # Reakce
        reaction = cls.generate_reaction()

        # Vytvoř NPC
        npc = NPC(
            name=name,
            social_status=social_status,
            birthsign=birthsign,
            appearance=appearance,
            quirk=quirk,
            desire=desire,
            relationship=relationship,
            reaction=reaction,
            payment=payment,
            notes=""
        )

        return npc

    @staticmethod
    def to_dict(npc: NPC) -> Dict[str, Any]:
        """
        Převeď NPC na dictionary.

        Args:
            npc: NPC objekt

        Returns:
            Dict reprezentace NPC

        Example:
            >>> npc = NPCGenerator.create()
            >>> npc_dict = NPCGenerator.to_dict(npc)
            >>> assert "name" in npc_dict
        """
        return asdict(npc)

    @staticmethod
    def to_json(npc: NPC, indent: int = 2) -> str:
        """
        Převeď NPC na JSON string.

        Args:
            npc: NPC objekt
            indent: Odsazení v JSON (pro čitelnost)

        Returns:
            JSON string

        Example:
            >>> npc = NPCGenerator.create()
            >>> json_str = NPCGenerator.to_json(npc)
            >>> assert '"name"' in json_str
        """
        import json
        return json.dumps(
            NPCGenerator.to_dict(npc),
            ensure_ascii=False,
            indent=indent
        )
