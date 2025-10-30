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
