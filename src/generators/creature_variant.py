"""
CreatureVariantGenerator - generátor variant stvoření

Generuje specifické varianty různých stvoření podle oficiálních pravidel.
Pokrývá 11 typů stvoření s jejich unikátními variantami.

Podle oficiálních Mausritter pravidel (09_CREATURES.md).
"""

import json
from typing import Optional
from src.core.models import CreatureVariant
from src.core.tables import TableLoader
from src.core.dice import roll_d6


class CreatureVariantGenerator:
    """
    Generátor variant stvoření podle oficiálních Mausritter pravidel.

    Podporované typy stvoření:
    - ghost: Přízračné schopnosti
    - snake: Zvláštní hadi
    - cat: Kočičí pánové a paní
    - rat: Krysí gangy
    - mouse: Konkurenční myší dobrodruzi
    - spider: Druhy pavouků
    - owl: Soví čarodějové
    - centipede: Zevlující stonožky
    - fairy: Vílí plány
    - crow: Vraní písně
    - frog: Potulní žabí rytíři

    Mechanika:
    - Všechny varianty: k6 (6 možností pro každý typ)

    Použití:
        # Náhodná varianta ducha
        ghost = CreatureVariantGenerator.create("ghost")

        # Konkrétní had (hod 3)
        snake = CreatureVariantGenerator.create("snake", roll=3)

        # Export do JSON
        json_str = CreatureVariantGenerator.to_json(ghost)
    """

    # Mapování typů na soubory
    CREATURE_FILES = {
        "ghost": "creature_ghost_abilities",
        "snake": "creature_snake_types",
        "cat": "creature_cat_lords",
        "rat": "creature_rat_gangs",
        "mouse": "creature_rival_mice",
        "spider": "creature_spider_types",
        "owl": "creature_owl_wizards",
        "centipede": "creature_centipede_types",
        "fairy": "creature_fairy_schemes",
        "crow": "creature_crow_songs",
        "frog": "creature_frog_knights",
    }

    @classmethod
    def create(cls, creature_type: str, roll: Optional[int] = None) -> CreatureVariant:
        """
        Vytvoř náhodnou variantu stvoření.

        Args:
            creature_type: Typ stvoření (ghost, snake, cat, rat, mouse, spider,
                          owl, centipede, fairy, crow, frog)
            roll: Volitelný hod k6 (1-6). Pokud None, hodí se náhodně.

        Returns:
            CreatureVariant objekt s vygenerovanými daty

        Raises:
            ValueError: Pokud creature_type není podporován
        """
        # Validace typu stvoření
        if creature_type not in cls.CREATURE_FILES:
            valid_types = ", ".join(cls.CREATURE_FILES.keys())
            raise ValueError(
                f"Neplatný typ stvoření: {creature_type}. "
                f"Platné typy: {valid_types}"
            )

        # 1. Hoď k6 pro variantu
        if roll is None:
            roll = roll_d6()

        # 2. Najdi variantu v tabulce
        variant_data = TableLoader.lookup_creature_variant(creature_type, roll)
        if variant_data is None:
            # Fallback
            return CreatureVariant(
                name="Neznámá varianta",
                description="Popis není k dispozici",
                creature_type=creature_type,
                roll=roll
            )

        # 3. Vytvoř CreatureVariant objekt
        return CreatureVariant(
            name=variant_data["name"],
            description=variant_data["description"],
            creature_type=creature_type,
            roll=roll
        )

    @staticmethod
    def to_dict(variant: CreatureVariant) -> dict:
        """
        Převede CreatureVariant objekt na dictionary.

        Args:
            variant: CreatureVariant objekt

        Returns:
            Dictionary s daty varianty
        """
        return {
            "name": variant.name,
            "description": variant.description,
            "creature_type": variant.creature_type,
            "creature_name": variant.creature_name_cz,
            "variant_table": variant.variant_table_name_cz,
            "roll": variant.roll
        }

    @staticmethod
    def to_json(variant: CreatureVariant, indent: int = 2) -> str:
        """
        Převede CreatureVariant objekt na JSON string.

        Args:
            variant: CreatureVariant objekt
            indent: Počet mezer pro odsazení (default: 2)

        Returns:
            JSON string
        """
        data = CreatureVariantGenerator.to_dict(variant)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(variant: CreatureVariant) -> str:
        """
        Naformátuj variantu jako čitelný text.

        Args:
            variant: CreatureVariant objekt

        Returns:
            Formátovaný text s informacemi o variantě
        """
        lines = []
        lines.append("═══ VARIANTA STVOŘENÍ ═══")
        lines.append("")
        lines.append(f"{variant.creature_emoji}  {variant.name}")
        lines.append(f"📋 Typ: {variant.creature_name_cz}")
        lines.append(f"📖 Tabulka: {variant.variant_table_name_cz}")
        lines.append("")
        lines.append(f"📝 {variant.description}")
        lines.append("")
        lines.append(f"🎲 Hod: {variant.roll} (k6)")

        return "\n".join(lines)

    @classmethod
    def get_available_types(cls) -> list:
        """
        Vrať seznam dostupných typů stvoření.

        Returns:
            Seznam stringů s typy stvoření
        """
        return list(cls.CREATURE_FILES.keys())
