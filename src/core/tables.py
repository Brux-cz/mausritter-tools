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

    @staticmethod
    def get_random_weapon() -> Optional[Dict[str, Any]]:
        """Vrátí náhodnou zbraň ze seznamu."""
        import random
        weapons_data = TableLoader.get_weapons()
        weapons_list = weapons_data.get("weapons", [])

        if not weapons_list:
            return None

        return random.choice(weapons_list)

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

    # === TAVERN TABLES ===

    @staticmethod
    def get_tavern_name_part1() -> Dict[str, Any]:
        """Načte tabulku první části názvů hospod (přídavná jména)."""
        return TableLoader.load_table("core/tavern_name_part1.json")

    @staticmethod
    def get_tavern_name_part2() -> Dict[str, Any]:
        """Načte tabulku druhé části názvů hospod (podstatná jména)."""
        return TableLoader.load_table("core/tavern_name_part2.json")

    @staticmethod
    def get_tavern_specialty() -> Dict[str, Any]:
        """Načte tabulku specialit hospod."""
        return TableLoader.load_table("core/tavern_specialty.json")

    @staticmethod
    def lookup_tavern_name_part1(roll: int) -> Optional[str]:
        """
        Najde první část názvu hospody podle hodu k12.

        Args:
            roll: Výsledek hodu k12 (1-12)

        Returns:
            String s přídavným jménem nebo None pokud nenalezeno
        """
        data = TableLoader.get_tavern_name_part1()
        items = data.get("items", [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    @staticmethod
    def lookup_tavern_name_part2(roll: int) -> Optional[str]:
        """
        Najde druhou část názvu hospody podle hodu k12.

        Args:
            roll: Výsledek hodu k12 (1-12)

        Returns:
            String s podstatným jménem nebo None pokud nenalezeno
        """
        data = TableLoader.get_tavern_name_part2()
        items = data.get("items", [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    @staticmethod
    def lookup_tavern_specialty(roll: int) -> Optional[str]:
        """
        Najde specialitu hospody podle hodu k12.

        Args:
            roll: Výsledek hodu k12 (1-12)

        Returns:
            String se specialitou nebo None pokud nenalezeno
        """
        data = TableLoader.get_tavern_specialty()
        items = data.get("items", [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    # === WEATHER / POČASÍ ===

    @staticmethod
    def get_weather_seasons() -> Dict[str, Any]:
        """Načte tabulku ročních období (počasí a události)."""
        return TableLoader.load_table("core/weather_seasons.json")

    @staticmethod
    def lookup_weather(season: str, roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde počasí podle sezóny a hodu 2k6.

        Args:
            season: "spring", "summer", "autumn", "winter"
            roll: Výsledek hodu 2k6 (2-12)

        Returns:
            Dict s počasím {"weather": str, "unfavorable": bool} nebo None
        """
        data = TableLoader.get_weather_seasons()

        if season not in data["seasons"]:
            return None

        weather_list = data["seasons"][season]["weather"]

        for weather in weather_list:
            # Single roll match
            if "roll" in weather and weather["roll"] == roll:
                return weather
            # Roll range match
            elif "roll_min" in weather and "roll_max" in weather:
                if weather["roll_min"] <= roll <= weather["roll_max"]:
                    return weather

        return None

    @staticmethod
    def lookup_seasonal_event(season: str, roll: int) -> Optional[str]:
        """
        Najde sezónní událost podle sezóny a hodu k6.

        Args:
            season: "spring", "summer", "autumn", "winter"
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Text události nebo None
        """
        data = TableLoader.get_weather_seasons()

        if season not in data["seasons"]:
            return None

        events_list = data["seasons"][season]["events"]

        for event in events_list:
            if event["roll"] == roll:
                return event["event"]

        return None

    # === SPELLS / KOUZLA ===

    @staticmethod
    def get_spells() -> Dict[str, Any]:
        """Načte tabulku kouzel."""
        return TableLoader.load_table("core/spells.json")

    @staticmethod
    def lookup_spell(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde kouzlo podle hodu 2d8.

        Args:
            roll: Výsledek hodu 2d8 (2-16)

        Returns:
            Dict s informacemi o kouzlu nebo None pokud nenalezeno

        Example:
            >>> spell = TableLoader.lookup_spell(10)
            >>> print(spell["name"])  # "Světlo"
        """
        spells_data = TableLoader.get_spells()
        spells_list = spells_data.get("spells", [])

        for spell in spells_list:
            if spell["roll"] == roll:
                return spell

        return None

    # === TREASURE / POKLADY ===

    @staticmethod
    def get_treasure_main() -> Dict[str, Any]:
        """Načte hlavní tabulku pokladu."""
        return TableLoader.load_table("treasure/treasure_main.json")

    @staticmethod
    def get_treasure_trinkets() -> Dict[str, Any]:
        """Načte tabulku drobností."""
        return TableLoader.load_table("treasure/treasure_trinkets.json")

    @staticmethod
    def get_treasure_valuable() -> Dict[str, Any]:
        """Načte tabulku cenného pokladu."""
        return TableLoader.load_table("treasure/treasure_valuable.json")

    @staticmethod
    def get_treasure_bulky() -> Dict[str, Any]:
        """Načte tabulku objemného pokladu."""
        return TableLoader.load_table("treasure/treasure_bulky.json")

    @staticmethod
    def get_treasure_unusual() -> Dict[str, Any]:
        """Načte tabulku neobvyklého pokladu."""
        return TableLoader.load_table("treasure/treasure_unusual.json")

    @staticmethod
    def get_treasure_useful() -> Dict[str, Any]:
        """Načte tabulku užitečného pokladu."""
        return TableLoader.load_table("treasure/treasure_useful.json")

    @staticmethod
    def get_magic_swords() -> Dict[str, Any]:
        """Načte tabulku kouzelných mečů."""
        return TableLoader.load_table("treasure/magic_swords.json")

    @staticmethod
    def get_magic_sword_types() -> Dict[str, Any]:
        """Načte tabulku typů kouzelných mečů."""
        return TableLoader.load_table("treasure/magic_sword_types.json")

    @staticmethod
    def get_magic_sword_curses() -> Dict[str, Any]:
        """Načte tabulku kleteb kouzelných mečů."""
        return TableLoader.load_table("treasure/magic_sword_curses.json")

    @staticmethod
    def get_tools() -> Dict[str, Any]:
        """Načte tabulku nástrojů."""
        return TableLoader.load_table("core/tools.json")

    @staticmethod
    def get_armor() -> Dict[str, Any]:
        """Načte tabulku zbrojí."""
        return TableLoader.load_table("core/armor.json")

    @staticmethod
    def lookup_treasure_main(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde položku v hlavní tabulce pokladu podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            Dict s informacemi o položce nebo None
        """
        main_data = TableLoader.get_treasure_main()
        table = main_data.get("table", [])

        for entry in table:
            roll_value = entry.get("roll")
            # Může být jedno číslo nebo list
            if isinstance(roll_value, int):
                if roll == roll_value:
                    return entry
            elif isinstance(roll_value, list):
                if roll in roll_value:
                    return entry

        return None

    @staticmethod
    def lookup_trinket(roll: int) -> Optional[Dict[str, Any]]:
        """Najde drobnost podle hodu k6."""
        data = TableLoader.get_treasure_trinkets()
        trinkets = data.get("trinkets", [])

        for trinket in trinkets:
            if trinket["roll"] == roll:
                return trinket

        return None

    @staticmethod
    def lookup_valuable(roll: int) -> Optional[Dict[str, Any]]:
        """Najde cenný poklad podle hodu k6."""
        data = TableLoader.get_treasure_valuable()
        valuable = data.get("valuable", [])

        for item in valuable:
            if item["roll"] == roll:
                return item

        return None

    @staticmethod
    def lookup_bulky(roll: int) -> Optional[Dict[str, Any]]:
        """Najde objemný poklad podle hodu k6."""
        data = TableLoader.get_treasure_bulky()
        bulky = data.get("bulky", [])

        for item in bulky:
            if item["roll"] == roll:
                return item

        return None

    @staticmethod
    def lookup_unusual(roll: int) -> Optional[Dict[str, Any]]:
        """Najde neobvyklý poklad podle hodu k6."""
        data = TableLoader.get_treasure_unusual()
        unusual = data.get("unusual", [])

        for item in unusual:
            if item["roll"] == roll:
                return item

        return None

    @staticmethod
    def lookup_useful(roll: int) -> Optional[Dict[str, Any]]:
        """Najde užitečný poklad podle hodu k6."""
        data = TableLoader.get_treasure_useful()
        useful = data.get("useful", [])

        for item in useful:
            if item["roll"] == roll:
                return item

        return None

    @staticmethod
    def lookup_magic_sword(roll: int) -> Optional[Dict[str, Any]]:
        """Najde kouzelný meč podle hodu k10."""
        data = TableLoader.get_magic_swords()
        swords = data.get("swords", [])

        for sword in swords:
            if sword["roll"] == roll:
                return sword

        return None

    @staticmethod
    def lookup_magic_sword_type(roll: int) -> Optional[Dict[str, Any]]:
        """Najde typ kouzelného meče podle hodu k6."""
        data = TableLoader.get_magic_sword_types()
        types = data.get("types", [])

        for sword_type in types:
            roll_value = sword_type.get("roll")
            # Může být jedno číslo nebo list
            if isinstance(roll_value, int):
                if roll == roll_value:
                    return sword_type
            elif isinstance(roll_value, list):
                if roll in roll_value:
                    return sword_type

        return None

    @staticmethod
    def lookup_magic_sword_curse(roll: int) -> Optional[Dict[str, Any]]:
        """Najde kletbu kouzelného meče podle hodu k6."""
        data = TableLoader.get_magic_sword_curses()
        curses = data.get("curses", [])

        for curse in curses:
            if curse["roll"] == roll:
                return curse

        return None

    @staticmethod
    def get_random_tool() -> Optional[Dict[str, Any]]:
        """Vrátí náhodný nástroj ze seznamu."""
        import random
        data = TableLoader.get_tools()
        mouse_made = data.get("mouse_made", [])
        human_made = data.get("human_made", [])
        all_tools = mouse_made + human_made

        if not all_tools:
            return None

        return random.choice(all_tools)

    @staticmethod
    def get_random_armor() -> Optional[Dict[str, Any]]:
        """Vrátí náhodnou zbroj ze seznamu."""
        import random
        data = TableLoader.get_armor()
        armor_types = data.get("armor_types", [])

        if not armor_types:
            return None

        return random.choice(armor_types)

    @staticmethod
    def clear_cache():
        """Vyčistí cache načtených tabulek. Užitečné pro testy."""
        TableLoader.load_table.cache_clear()

    # === SETTLEMENT TABLES ===

    @staticmethod
    def get_settlement_sizes() -> Dict[str, Any]:
        """Načte tabulku velikostí osad (2d6 keep-lower)."""
        return TableLoader.load_table("core/settlement_sizes.json")

    @staticmethod
    def get_settlement_governments() -> Dict[str, Any]:
        """Načte tabulku typů vlády v osadách (k6 + sizeValue)."""
        return TableLoader.load_table("core/settlement_governments.json")

    @staticmethod
    def get_settlement_details() -> Dict[str, Any]:
        """Načte tabulku detailů osad (k20)."""
        return TableLoader.load_table("core/settlement_details.json")

    @staticmethod
    def get_settlement_trades() -> Dict[str, Any]:
        """Načte tabulku řemesel v osadách (k20)."""
        return TableLoader.load_table("core/settlement_trades.json")

    @staticmethod
    def get_settlement_features() -> Dict[str, Any]:
        """Načte tabulku prvků osad (k20)."""
        return TableLoader.load_table("core/settlement_features.json")

    @staticmethod
    def get_settlement_events() -> Dict[str, Any]:
        """Načte tabulku událostí při příjezdu do osady (k20)."""
        return TableLoader.load_table("core/settlement_events.json")

    @staticmethod
    def get_settlement_names() -> Dict[str, Any]:
        """Načte tabulku semínek názvů osad (4× k12)."""
        return TableLoader.load_table("core/settlement_names.json")

    @staticmethod
    def lookup_settlement_size(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde velikost osady podle hodu (2d6 keep-lower).

        Args:
            roll: Výsledek hodu 2d6 keep-lower (1-6)

        Returns:
            Dict s informacemi o velikosti nebo None
        """
        data = TableLoader.get_settlement_sizes()
        sizes = data.get("sizes", [])

        for size in sizes:
            if size["roll"] == roll:
                return size

        return None

    @staticmethod
    def lookup_settlement_government(roll: int) -> Optional[str]:
        """
        Najde typ vlády podle hodu (k6 + sizeValue).

        Args:
            roll: Výsledek hodu k6 + sizeValue (2-12)

        Returns:
            String s názvem vlády nebo None
        """
        data = TableLoader.get_settlement_governments()
        governments = data.get("governments", [])

        for gov in governments:
            if gov["rollMin"] <= roll <= gov["rollMax"]:
                return gov["name"]

        return None

    @staticmethod
    def lookup_settlement_detail(roll: int) -> Optional[str]:
        """
        Najde detail osady podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            String s detailem nebo None
        """
        data = TableLoader.get_settlement_details()
        items = data.get("items", [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    @staticmethod
    def lookup_settlement_trade(roll: int) -> Optional[str]:
        """
        Najde řemeslo podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            String s řemeslem nebo None
        """
        data = TableLoader.get_settlement_trades()
        items = data.get("items", [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    @staticmethod
    def lookup_settlement_feature(roll: int) -> Optional[str]:
        """
        Najde prvek osady podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            String s prvkem nebo None
        """
        data = TableLoader.get_settlement_features()
        items = data.get("items", [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    @staticmethod
    def lookup_settlement_event(roll: int) -> Optional[str]:
        """
        Najde událost při příjezdu podle hodu k20.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            String s událostí nebo None
        """
        data = TableLoader.get_settlement_events()
        items = data.get("items", [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    @staticmethod
    def lookup_settlement_name_part(table_name: str, roll: int) -> Optional[str]:
        """
        Najde část názvu osady podle tabulky a hodu k12.

        Args:
            table_name: Název tabulky ("name_start_a", "name_start_b", "name_end_a", "name_end_b")
            roll: Výsledek hodu k12 (1-12)

        Returns:
            String s částí názvu nebo None
        """
        data = TableLoader.get_settlement_names()
        items = data.get(table_name, [])

        for item in items:
            if item["roll"] == roll:
                return item["text"]

        return None

    # === ADVENTURE HOOKS ===

    @staticmethod
    def get_adventure_hooks() -> Dict[str, Any]:
        """Načte tabulku háčků dobrodružství (k6)."""
        return TableLoader.load_table("core/adventure_hooks.json")

    @staticmethod
    def lookup_adventure_hook(roll: int) -> Optional[Dict[str, Any]]:
        """
        Najde háček dobrodružství podle hodu k6.

        Args:
            roll: Výsledek hodu k6 (1-6)

        Returns:
            Dict s informacemi o háčku (hook, category, questions) nebo None
        """
        data = TableLoader.get_adventure_hooks()
        hooks = data.get("hooks", [])

        for hook in hooks:
            if hook["roll"] == roll:
                return hook

        return None


# Convenience funkce pro rychlé použití
# === SHORTCUTS ===

def load_origins() -> Dict[str, Any]:
    """Shortcut pro načtení tabulky původů."""
    return TableLoader.get_origins()


def load_first_names() -> Dict[str, Any]:
    """Shortcut pro načtení vlastních jmen."""
    return TableLoader.get_first_names()


def load_family_names() -> Dict[str, Any]:
    """Shortcut pro načtení mateřských jmen."""
    return TableLoader.get_family_names()
