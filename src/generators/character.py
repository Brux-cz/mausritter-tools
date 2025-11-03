"""
Generator myších postav podle pravidel Mausritter
"""
import random
from typing import Optional, Dict, Any
from dataclasses import asdict

from src.core.dice import roll_d6, roll_3d6_keep_2, roll_d66, roll
from src.core.models import Character
from src.core.tables import TableLoader


class CharacterGenerator:
    """
    Generátor náhodných myších postav podle pravidel Mausritter.

    Postup generování postavy:
    1. Hod 3× vlastnosti (3k6 keep 2) → STR, DEX, WIL
    2. Hod k6 pro HP (Body ochrany)
    3. Hod k6 pro Pips (počáteční ďobky)
    4. Najdi původ podle HP a Pips v tabulce původů
    5. Vygeneruj náhodné jméno (nebo použij zadané)
    6. Vrať Character objekt

    Zdroj: docs/knowledge_base/02_CHARACTER_CREATION.md
    """

    @staticmethod
    def roll_attributes() -> tuple[int, int, int]:
        """
        Hoď vlastnosti postavy (3× 3k6 keep 2).

        Returns:
            (strength, dexterity, willpower) - hodnoty 2-12

        Example:
            >>> str, dex, wil = CharacterGenerator.roll_attributes()
            >>> assert 2 <= str <= 12
        """
        strength = roll_3d6_keep_2()
        dexterity = roll_3d6_keep_2()
        willpower = roll_3d6_keep_2()

        return strength, dexterity, willpower

    @staticmethod
    def determine_origin(hp: int, pips: int) -> Optional[Dict[str, Any]]:
        """
        Najdi původ postavy podle HP a počtu ďobků.

        Args:
            hp: Body ochrany (1-6)
            pips: Počet ďobků (1-6)

        Returns:
            Dict s informacemi o původu nebo None pokud nenalezen

        Example:
            >>> origin = CharacterGenerator.determine_origin(3, 5)
            >>> print(origin['name'])  # "Stěnolezec"
        """
        return TableLoader.lookup_origin(hp, pips)

    @staticmethod
    def generate_name(gender: str = "male") -> str:
        """
        Vygeneruj náhodné myší jméno.

        Args:
            gender: "male" nebo "female" pro správný tvar příjmení

        Returns:
            "Jméno Příjmení" (např. "Pepřík Hrabal")

        Example:
            >>> name = CharacterGenerator.generate_name()
            >>> assert ' ' in name  # Musí obsahovat mezeru
        """
        # Hod k100 pro vlastní jméno
        first_roll = random.randint(1, 100)
        first_name = TableLoader.lookup_first_name(first_roll)

        # Hod k20 pro mateřské jméno
        family_roll = random.randint(1, 20)
        family_name = TableLoader.lookup_family_name(family_roll, gender)

        if first_name and family_name:
            return f"{first_name} {family_name}"

        # Fallback pokud lookup selže
        return "Bezejmenná Myš"

    @staticmethod
    def generate_birthsign() -> Dict[str, str]:
        """
        Vygeneruj rodné znamení.

        Returns:
            Dictionary s názvem a povahou {"name": "Hvězda", "trait": "Statečná/zbrklá"}

        Example:
            >>> birthsign = CharacterGenerator.generate_birthsign()
            >>> print(f"{birthsign['name']} ({birthsign['trait']})")
        """
        roll = roll_d6()
        birthsign = TableLoader.lookup_birthsign(roll)

        if birthsign:
            return {
                "name": birthsign["name"],
                "trait": birthsign["trait"]
            }

        # Fallback
        return {"name": "Neznámé", "trait": "Tajemná"}

    @staticmethod
    def generate_coat() -> str:
        """
        Vygeneruj barvu a vzor srsti.

        Returns:
            String s barvou a vzorem (např. "Černá mourovatá")

        Example:
            >>> coat = CharacterGenerator.generate_coat()
            >>> print(coat)  # "Černá mourovatá"
        """
        color_roll = roll_d6()
        pattern_roll = roll_d6()

        color = TableLoader.lookup_coat_color(color_roll)
        pattern = TableLoader.lookup_coat_pattern(pattern_roll)

        if color and pattern:
            return f"{color} {pattern}"

        # Fallback
        return "Hnědá jednolitá"

    @staticmethod
    def generate_distinctive_trait() -> str:
        """
        Vygeneruj výrazný fyzický rys.

        Returns:
            String s výrazným rysem (např. "Korpulentní tělo")

        Example:
            >>> trait = CharacterGenerator.generate_distinctive_trait()
            >>> print(trait)  # "Páska přes oko"
        """
        roll = roll_d66()
        trait = TableLoader.lookup_distinctive_trait(roll)

        if trait:
            return trait

        # Fallback
        return "Běžný vzhled"

    @staticmethod
    def select_weapon(weapon_id: Optional[int] = None) -> str:
        """
        Vyber zbraň (náhodně nebo podle ID).

        Args:
            weapon_id: Volitelné ID zbraně (1-6), jinak náhodná

        Returns:
            String s názvem a příklady zbraně

        Example:
            >>> weapon = CharacterGenerator.select_weapon()
            >>> print(weapon)  # "Lehká zbraň (dýka, jehla)"
        """
        if weapon_id is None:
            weapon_id = roll_d6()

        weapon = TableLoader.lookup_weapon(weapon_id)

        if weapon:
            return f"{weapon['name']} ({weapon['examples']})"

        # Fallback
        return "Improvizovaná zbraň (klacek)"

    @classmethod
    def create(cls,
               name: Optional[str] = None,
               gender: str = "male",
               swap_attributes: bool = False) -> Character:
        """
        Vytvoř kompletní náhodnou postavu.

        Args:
            name: Volitelné vlastní jméno (jinak náhodné)
            gender: "male" nebo "female" pro správný tvar příjmení
            swap_attributes: Povolit prohození dvou vlastností (TODO)

        Returns:
            Vygenerovaná Character instance

        Example:
            >>> char = CharacterGenerator.create()
            >>> assert char.name
            >>> assert 2 <= char.strength <= 12
            >>> assert 1 <= char.max_hp <= 6
        """
        # 1. Roll vlastnosti
        strength, dexterity, willpower = cls.roll_attributes()

        # 2. Roll HP a Pips
        hp = roll_d6()
        pips = roll_d6()

        # 3. Určit původ
        origin_data = cls.determine_origin(hp, pips)

        if not origin_data:
            raise ValueError(f"Nenalezen původ pro HP={hp}, Pips={pips}")

        # 3.5. Bonusová výbava (pokud je nejvyšší vlastnost ≤ 9)
        bonus_items = []
        max_attribute = max(strength, dexterity, willpower)

        if max_attribute <= 9:
            # Hoď znovu na tabulku původů
            bonus_hp = roll_d6()
            bonus_pips = roll_d6()
            bonus_origin = cls.determine_origin(bonus_hp, bonus_pips)

            if bonus_origin:
                if max_attribute <= 7:
                    # Vezmi OBA předměty
                    bonus_items.append(bonus_origin["item_a"])
                    bonus_items.append(bonus_origin["item_b"])
                else:
                    # Vezmi JEDEN předmět (náhodně A nebo B)
                    if random.randint(0, 1) == 0:
                        bonus_items.append(bonus_origin["item_a"])
                    else:
                        bonus_items.append(bonus_origin["item_b"])

        # 4. Generovat/použít jméno
        if name is None:
            name = cls.generate_name(gender)

        # 5. Generovat rodné znamení, srst, výrazný rys a zbraň
        birthsign_data = cls.generate_birthsign()
        coat = cls.generate_coat()
        distinctive_trait = cls.generate_distinctive_trait()
        weapon = cls.select_weapon()

        # 6. Sestavit inventář
        inventory = [
            "Pochodně (3 použití)",
            "Zásoby (3 použití)",
            origin_data["item_a"],
            origin_data["item_b"],
            weapon,
        ]
        # Přidat bonusové itemy (pokud jsou)
        inventory.extend(bonus_items)
        # Doplnit na 10 slotů
        while len(inventory) < 10:
            inventory.append(None)

        # Poznámka o bonusové výbavě
        notes = f"Počáteční ďobky: {pips} ď"
        if bonus_items:
            notes += f" | Bonusová výbava (max vlastnost {max_attribute}): {len(bonus_items)} předmět(y)"

        # 7. Sestavit postavu
        character = Character(
            name=name,
            background=origin_data["name"],
            strength=strength,
            dexterity=dexterity,
            willpower=willpower,
            max_hp=hp,
            current_hp=hp,
            inventory=inventory,
            appearance=distinctive_trait,
            birthsign=f"{birthsign_data['name']} ({birthsign_data['trait']})",
            coat=coat,
            notes=notes
        )

        return character

    @staticmethod
    def to_dict(character: Character) -> Dict[str, Any]:
        """
        Konvertuj Character do dictionary.

        Args:
            character: Character instance

        Returns:
            Dict reprezentace postavy
        """
        return asdict(character)

    @staticmethod
    def to_json(character: Character, indent: int = 2) -> str:
        """
        Konvertuj Character do JSON stringu.

        Args:
            character: Character instance
            indent: Počet mezer pro odsazení

        Returns:
            JSON string
        """
        import json
        return json.dumps(
            CharacterGenerator.to_dict(character),
            ensure_ascii=False,
            indent=indent
        )
