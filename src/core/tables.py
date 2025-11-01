"""
TableLoader - načítání JSON tabulek z dat
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any, List, Optional


class TableLoader:
    """
    Singleton pro načítání tabulek z JSON souborů.
    Používá LRU cache pro efektivní načítání.
    """

    # Cesta k data adresáři relativně k tomuto souboru
    # src/core/tables.py -> ../../data
    DATA_DIR = Path(__file__).parent.parent.parent / "data"

    @staticmethod
    @lru_cache(maxsize=50)
    def load_table(table_path: str) -> Dict[str, Any]:
        """
        Načte JSON tabulku ze souboru.

        Args:
            table_path: Cesta k souboru relativně k data/ adresáři
                       Např. "core/origins.json"

        Returns:
            Dict s obsahem JSON souboru

        Raises:
            FileNotFoundError: Pokud soubor neexistuje
            json.JSONDecodeError: Pokud soubor není platný JSON

        Example:
            >>> origins = TableLoader.load_table("core/origins.json")
            >>> print(origins["metadata"]["description"])
        """
        full_path = TableLoader.DATA_DIR / table_path

        if not full_path.exists():
            raise FileNotFoundError(
                f"Tabulka nenalezena: {full_path}\n"
                f"Hledal jsem v: {full_path.absolute()}"
            )

        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_origins() -> Dict[str, Any]:
        """Načte tabulku původů postav."""
        return TableLoader.load_table("core/origins.json")

    @staticmethod
    def get_first_names() -> Dict[str, Any]:
        """Načte tabulku vlastních jmen."""
        return TableLoader.load_table("core/names_first.json")

    @staticmethod
    def get_family_names() -> Dict[str, Any]:
        """Načte tabulku mateřských jmen."""
        return TableLoader.load_table("core/names_family.json")

    @staticmethod
    def lookup_origin(hp: int, pips: int) -> Optional[Dict[str, Any]]:
        """
        Najde původ postavy podle HP a počtu ďobků.

        Args:
            hp: Body ochrany (1-6)
            pips: Počet ďobků na posledním hodu (1-6)

        Returns:
            Dict s informacemi o původu nebo None pokud nenalezen

        Example:
            >>> origin = TableLoader.lookup_origin(hp=3, pips=5)
            >>> print(origin["name"])  # "Stěnolezec"
        """
        origins_data = TableLoader.get_origins()
        origins_list = origins_data.get("origins", [])

        for origin in origins_list:
            if origin["hp"] == hp and origin["pips"] == pips:
                return origin

        return None

    @staticmethod
    def lookup_first_name(roll: int) -> Optional[str]:
        """
        Najde vlastní jméno podle hodu k100.

        Args:
            roll: Výsledek hodu k100 (1-100)

        Returns:
            Jméno nebo None pokud nenalezeno
        """
        names_data = TableLoader.get_first_names()
        names_list = names_data.get("names", [])

        for name_entry in names_list:
            if name_entry["roll"] == roll:
                return name_entry["name"]

        return None

    @staticmethod
    def lookup_family_name(roll: int, gender: str = "male") -> Optional[str]:
        """
        Najde mateřské jméno podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)
            gender: "male" nebo "female" pro správný tvar příjmení

        Returns:
            Příjmení nebo None pokud nenalezeno
        """
        names_data = TableLoader.get_family_names()
        names_list = names_data.get("names", [])

        for name_entry in names_list:
            if name_entry["roll"] == roll:
                if gender == "female":
                    return name_entry["name_female"]
                else:
                    return name_entry["name_male"]

        return None

    @staticmethod
    def get_birthsigns() -> Dict[str, Any]:
        """Načte tabulku rodných znamení."""
        return TableLoader.load_table("core/birthsigns.json")

    @staticmethod
    def get_coat_colors() -> Dict[str, Any]:
        """Načte tabulku barev srsti."""
        return TableLoader.load_table("core/coat_colors.json")

    @staticmethod
    def get_coat_patterns() -> Dict[str, Any]:
        """Načte tabulku vzorů srsti."""
        return TableLoader.load_table("core/coat_patterns.json")

    @staticmethod
    def lookup_birthsign(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde rodné znamení podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s informacemi o znamení nebo None pokud nenalezeno

        Example:
            >>> birthsign = TableLoader.lookup_birthsign(1)
            >>> print(birthsign["name"])  # "Hvězda"
        """
        birthsigns_data = TableLoader.get_birthsigns()
        birthsigns_list = birthsigns_data.get("birthsigns", [])

        for birthsign in birthsigns_list:
            if birthsign["roll"] == roll:
                return birthsign

        return None

    @staticmethod
    def lookup_coat_color(roll: int) -> Optional[str]:
        """
        Najde barvu srsti podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Název barvy nebo None pokud nenalezena
        """
        colors_data = TableLoader.get_coat_colors()
        colors_list = colors_data.get("colors", [])

        for color in colors_list:
            if color["roll"] == roll:
                return color["name"]

        return None

    @staticmethod
    def lookup_coat_pattern(roll: int) -> Optional[str]:
        """
        Najde vzor srsti podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Název vzoru nebo None pokud nenalezen
        """
        patterns_data = TableLoader.get_coat_patterns()
        patterns_list = patterns_data.get("patterns", [])

        for pattern in patterns_list:
            if pattern["roll"] == roll:
                return pattern["name"]

        return None

    @staticmethod
    def get_distinctive_traits() -> Dict[str, Any]:
        """Načte tabulku výrazných rysů."""
        return TableLoader.load_table("core/distinctive_traits.json")

    @staticmethod
    def lookup_distinctive_trait(roll: int) -> Optional[str]:
        """Najde výrazný rys podle hodu k66.

        Args:
            roll: Výsledek hodu k66 (11-16, 21-26, 31-36, 41-46, 51-56, 61-66)

        Returns:
            Text výrazného rysu nebo None pokud nenalezen
        """
        traits_data = TableLoader.get_distinctive_traits()
        traits_list = traits_data.get("traits", [])

        for trait in traits_list:
            if trait["roll"] == roll:
                return trait["text"]

        return None

    @staticmethod
    def get_weapons() -> Dict[str, Any]:
        """Načte tabulku zbraní."""
        return TableLoader.load_table("core/weapons.json")

    @staticmethod
    def lookup_weapon(weapon_id: int) -> Optional[Dict[str, Any]]:
        """Najde zbraň podle ID.

        Args:
            weapon_id: ID zbraně (1-6)

        Returns:
            Dictionary se zbraní nebo None pokud nenalezena
        """
        weapons_data = TableLoader.get_weapons()
        weapons_list = weapons_data.get("weapons", [])

        for weapon in weapons_list:
            if weapon["id"] == weapon_id:
                return weapon

        return None

    # === NPC TABULKY ===

    @staticmethod
    def get_npc_social_statuses() -> Dict[str, Any]:
        """Načte tabulku společenského postavení NPC."""
        return TableLoader.load_table("core/npc_social_status.json")

    @staticmethod
    def lookup_npc_social_status(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde společenské postavení podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s postavením a platbou nebo None pokud nenalezeno
        """
        statuses_data = TableLoader.get_npc_social_statuses()
        statuses_list = statuses_data.get("social_statuses", [])

        for status in statuses_list:
            if status["roll"] == roll:
                return status

        return None

    @staticmethod
    def get_npc_appearances() -> Dict[str, Any]:
        """Načte tabulku vzhledu NPC."""
        return TableLoader.load_table("core/npc_appearance.json")

    @staticmethod
    def lookup_npc_appearance(roll: int) -> Optional[str]:
        """
        Najde vzhled NPC podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            Text popisu vzhledu nebo None pokud nenalezen
        """
        appearances_data = TableLoader.get_npc_appearances()
        appearances_list = appearances_data.get("appearances", [])

        for appearance in appearances_list:
            if appearance["roll"] == roll:
                return appearance["text"]

        return None

    @staticmethod
    def get_npc_quirks() -> Dict[str, Any]:
        """Načte tabulku zvláštností NPC."""
        return TableLoader.load_table("core/npc_quirk.json")

    @staticmethod
    def lookup_npc_quirk(roll: int) -> Optional[str]:
        """
        Najde zvláštnost NPC podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            Text zvláštnosti nebo None pokud nenalezena
        """
        quirks_data = TableLoader.get_npc_quirks()
        quirks_list = quirks_data.get("quirks", [])

        for quirk in quirks_list:
            if quirk["roll"] == roll:
                return quirk["text"]

        return None

    @staticmethod
    def get_npc_desires() -> Dict[str, Any]:
        """Načte tabulku tužeb NPC."""
        return TableLoader.load_table("core/npc_desire.json")

    @staticmethod
    def lookup_npc_desire(roll: int) -> Optional[str]:
        """
        Najde tužbu NPC podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            Text tužby nebo None pokud nenalezena
        """
        desires_data = TableLoader.get_npc_desires()
        desires_list = desires_data.get("desires", [])

        for desire in desires_list:
            if desire["roll"] == roll:
                return desire["text"]

        return None

    @staticmethod
    def get_npc_relationships() -> Dict[str, Any]:
        """Načte tabulku vztahů NPC."""
        return TableLoader.load_table("core/npc_relationship.json")

    @staticmethod
    def lookup_npc_relationship(roll: int) -> Optional[str]:
        """
        Najde vztah NPC podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            Text vztahu nebo None pokud nenalezen
        """
        relationships_data = TableLoader.get_npc_relationships()
        relationships_list = relationships_data.get("relationships", [])

        for relationship in relationships_list:
            if relationship["roll"] == roll:
                return relationship["text"]

        return None

    @staticmethod
    def get_npc_reactions() -> Dict[str, Any]:
        """Načte tabulku reakcí NPC."""
        return TableLoader.load_table("core/npc_reaction.json")

    @staticmethod
    def lookup_npc_reaction(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde reakci NPC podle hodu 2k6.

        Args:
            roll: Výsledek hodu 2k6 (2-12)

        Returns:
            Dict s reakcí a otázkou nebo None pokud nenalezena
        """
        reactions_data = TableLoader.get_npc_reactions()
        reactions_list = reactions_data.get("reactions", [])

        for reaction in reactions_list:
            # Některé reakce mají přesný roll, některé rozsah
            if "roll" in reaction and reaction["roll"] == roll:
                return reaction
            elif "roll_min" in reaction and "roll_max" in reaction:
                if reaction["roll_min"] <= roll <= reaction["roll_max"]:
                    return reaction

        return None

    # === KOMPLETNÍ NPC TABULKY ===

    @staticmethod
    def get_hireling_types() -> Dict[str, Any]:
        """Načte tabulku typů pomocníků."""
        return TableLoader.load_table("core/hireling_types.json")

    @staticmethod
    def lookup_hireling_type(type_id: int) -> Optional[Dict[str, Any]]:
        """
        Najde typ pomocníka podle ID.

        Args:
            type_id: ID typu pomocníka (1-9)

        Returns:
            Dict s informacemi o pomocníkovi nebo None pokud nenalezen
        """
        hirelings_data = TableLoader.get_hireling_types()
        hirelings_list = hirelings_data.get("hirelings", [])

        for hireling in hirelings_list:
            if hireling["id"] == type_id:
                return hireling

        return None

    @staticmethod
    def get_competitive_mice() -> Dict[str, Any]:
        """Načte tabulku konkurenčních myších dobrodruhů."""
        return TableLoader.load_table("core/competitive_mice.json")

    @staticmethod
    def lookup_competitive_mouse(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde konkurenčního dobrodruha podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s informacemi o dobrodruhovi nebo None pokud nenalezen
        """
        mice_data = TableLoader.get_competitive_mice()
        mice_list = mice_data.get("mice", [])

        for mouse in mice_list:
            if mouse["roll"] == roll:
                return mouse

        return None

    @staticmethod
    def get_cat_lords() -> Dict[str, Any]:
        """Načte tabulku kočičích pánů."""
        return TableLoader.load_table("core/cat_lords.json")

    @staticmethod
    def lookup_cat_lord(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde kočičího pána podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s informacemi o kočičím pánovi nebo None pokud nenalezen
        """
        cats_data = TableLoader.get_cat_lords()
        cats_list = cats_data.get("cats", [])

        for cat in cats_list:
            if cat["roll"] == roll:
                return cat

        return None

    @staticmethod
    def get_rat_gangs() -> Dict[str, Any]:
        """Načte tabulku krysích gangů."""
        return TableLoader.load_table("core/rat_gangs.json")

    @staticmethod
    def lookup_rat_gang(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde krysí gang podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s informacemi o gangu nebo None pokud nenalezen
        """
        gangs_data = TableLoader.get_rat_gangs()
        gangs_list = gangs_data.get("gangs", [])

        for gang in gangs_list:
            if gang["roll"] == roll:
                return gang

        return None

    @staticmethod
    def get_owl_wizards() -> Dict[str, Any]:
        """Načte tabulku sovích čarodějů."""
        return TableLoader.load_table("core/owl_wizards.json")

    @staticmethod
    def lookup_owl_wizard(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde sovího čaroděje podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s informacemi o čarodějovi nebo None pokud nenalezen
        """
        wizards_data = TableLoader.get_owl_wizards()
        wizards_list = wizards_data.get("wizards", [])

        for wizard in wizards_list:
            if wizard["roll"] == roll:
                return wizard

        return None

    @staticmethod
    def get_frog_knights() -> Dict[str, Any]:
        """Načte tabulku žabích rytířů."""
        return TableLoader.load_table("core/frog_knights.json")

    @staticmethod
    def lookup_frog_knight(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde žabího rytíře podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s informacemi o rytíři nebo None pokud nenalezen
        """
        knights_data = TableLoader.get_frog_knights()
        knights_list = knights_data.get("knights", [])

        for knight in knights_list:
            if knight["roll"] == roll:
                return knight

        return None

    @staticmethod
    def get_adventure_seeds() -> Dict[str, Any]:
        """Načte tabulku semínek dobrodružství."""
        return TableLoader.load_table("core/adventure_seeds.json")

    @staticmethod
    def lookup_adventure_seed(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde semínko dobrodružství podle hodu k66.

        Args:
            roll: Výsledek hodu k66 (11-66, např. 11, 12, 13, 21, 22, ...)

        Returns:
            Dict s tabulkou dobrodružství nebo None pokud nenalezeno
        """
        seeds_data = TableLoader.get_adventure_seeds()
        seeds_list = seeds_data.get("seeds", [])

        for seed in seeds_list:
            if seed["roll"] == roll:
                return seed

        return None

    @staticmethod
    def clear_cache():
        """Vyčistí cache načtených tabulek. Užitečné pro testy."""
        TableLoader.load_table.cache_clear()


# Convenience funkce pro rychlé použití
def load_origins() -> Dict[str, Any]:
    """Shortcut pro načtení tabulky původů."""
    return TableLoader.get_origins()


def load_first_names() -> Dict[str, Any]:
    """Shortcut pro načtení vlastních jmen."""
    return TableLoader.get_first_names()


def load_family_names() -> Dict[str, Any]:
    """Shortcut pro načtení mateřských jmen."""
    return TableLoader.get_family_names()
