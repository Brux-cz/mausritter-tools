"""
RumorGenerator - generátor tabulky zvěstí

CORE RULES (Official Mausritter, 11_HEXCRAWL_SETUP.md str. 23):
- k6 tabulka zvěstí (6 rumors)
- Pravdivost: 1-3 true, 4-5 partial, 6 false
- O místech nebo frakcích v hexcrawlu

EXTENDED FEATURES (Community-inspired, NOT in core rules):
- B (World-Connected): Zvěsti o reálných místech z hexcrawlu
- D (Categories): Organizace do kategorií (threat/npc/location/treasure/mystery)
- C (Story Hooks): k6×k6 tabulky pro komplexní zápletky
- E (Gossip Network): Simulace šíření a zkreslení přes NPC
"""

import json
import random
from typing import Optional, List, Dict, Any
from src.core.models import Rumor
from src.core.tables import TableLoader
from src.core.dice import roll_d6


class RumorGenerator:
    """
    Generátor tabulky k6 zvěstí podle Mausritter pravidel.

    CORE MECHANIC (Official):
    Pravdivost podle k6 hodu:
    - 1-3: TRUE (50% šance) - pravdivá zvěst
    - 4-5: PARTIAL (33% šance) - částečně pravdivá
    - 6: FALSE (17% šance) - fáma

    EXTENDED FEATURES (Community-inspired):
    - World-connected rumors (variant B) - provázání s hexcrawl daty
    - Category organization (variant D) - threat/npc/location/treasure/mystery
    - Story hooks (variant C) - k6×k6 tabulky zápletků
    - Gossip network (variant E) - simulace šíření přes NPC

    Použití:
        # S world state (extended features)
        world_state = json.load(open("moje_dobrodruzstvi.json"))
        rumors = RumorGenerator.create(world_state=world_state)

        # Bez world state (fallback na templates)
        rumors = RumorGenerator.create()

        # Export
        json_str = RumorGenerator.to_json(rumors)
    """

    @classmethod
    def create(
        cls,
        world_state: Optional[Dict[str, Any]] = None,
        advanced: bool = True
    ) -> List[Rumor]:
        """
        Vytvoř kompletní k6 tabulku zvěstí.

        Args:
            world_state: Volitelný stav světa (settlements, hexes, dungeons)
            advanced: True = použij všechny varianty (B+D+C+E), False = jen B+D

        Returns:
            Seznam 6 Rumor objektů (k6 tabulka)
        """
        rumors = []

        for roll in range(1, 7):
            rumor = cls.create_single(roll=roll, world_state=world_state, advanced=advanced)
            rumors.append(rumor)

        return rumors

    @classmethod
    def create_single(
        cls,
        roll: int,
        world_state: Optional[Dict[str, Any]] = None,
        advanced: bool = True
    ) -> Rumor:
        """
        Vytvoř jednu zvěst podle k6 hodu.

        Args:
            roll: Hod k6 (1-6)
            world_state: Volitelný stav světa
            advanced: True = použij C+E varianty

        Returns:
            Rumor objekt
        """
        # 1. Zjisti truthfulness podle hodu
        if roll in [1, 2, 3]:
            truthfulness = "true"
        elif roll in [4, 5]:
            truthfulness = "partial"
        else:  # roll == 6
            truthfulness = "false"

        # 2. Zkus world-connected přístup (Variant B)
        if world_state and cls._has_locations(world_state):
            return cls._create_world_connected(
                roll=roll,
                truthfulness=truthfulness,
                world_state=world_state,
                advanced=advanced
            )
        else:
            # Fallback na template-only
            return cls._create_template_only(
                roll=roll,
                truthfulness=truthfulness
            )

    # === VARIANT B: WORLD-CONNECTED ===

    @classmethod
    def _has_locations(cls, world_state: Dict[str, Any]) -> bool:
        """Zkontroluj, jestli world state obsahuje nějaké lokace."""
        hexcrawl = world_state.get("hexcrawl", {})
        settlements = hexcrawl.get("settlements", [])
        hexes = hexcrawl.get("hexes", [])
        dungeons = hexcrawl.get("dungeons", [])

        return len(settlements) + len(hexes) + len(dungeons) > 0

    @classmethod
    def _create_world_connected(
        cls,
        roll: int,
        truthfulness: str,
        world_state: Dict[str, Any],
        advanced: bool
    ) -> Rumor:
        """Vytvoř zvěst o reálné lokaci ze světa."""
        # 1. Vyber náhodnou lokaci
        location_data = cls._select_random_location(world_state)
        location_type = location_data["type"]  # "settlement", "hex", "dungeon"
        location = location_data["data"]

        # 2. Přiřaď kategorii (Variant D)
        category = cls._assign_category(location_type, location)

        # 3. Vyber template podle kategorie a location type
        template_name = cls._select_template_name(category, location_type, location)
        template_data = TableLoader.get_rumor_template(template_name)

        if not template_data:
            # Fallback
            return cls._create_template_only(roll, truthfulness)

        # 4. Extrahuj data z lokace
        extracted_data = cls._extract_location_data(location_type, location)

        # 5. Aplikuj truthfulness modifikaci
        rumor_text, truth_part, false_part = cls._apply_truthfulness(
            template_data=template_data,
            truthfulness=truthfulness,
            extracted_data=extracted_data
        )

        # 6. Variant C: Story Hook (jen pro advanced + vybrané kategorie)
        story_hook_detail = None
        if advanced and category in ["npc", "treasure", "mystery"] and random.random() < 0.3:
            story_hook_detail = cls._roll_story_hook(category)

        # 7. Variant E: Gossip chain (jen pro advanced + partial/false)
        gossip_hops = 0
        gossip_chain = [rumor_text]
        if advanced and truthfulness in ["partial", "false"]:
            gossip_hops, gossip_chain = cls._simulate_gossip(
                base_truth=rumor_text,
                truthfulness=truthfulness
            )
            # Použij finální verzi po gossip chain
            rumor_text = gossip_chain[-1]

        # 8. GM notes
        gm_notes = cls._generate_gm_notes(
            truthfulness=truthfulness,
            location_type=location_type,
            location=location
        )

        return Rumor(
            roll=roll,
            rumor_text=rumor_text,
            category=category,
            truthfulness=truthfulness,
            source_location={
                "type": location_type,
                "data": extracted_data
            },
            gossip_hops=gossip_hops,
            gossip_chain=gossip_chain if len(gossip_chain) > 1 else [],
            story_hook_detail=story_hook_detail,
            truth_part=truth_part,
            false_part=false_part,
            gm_notes=gm_notes
        )

    @classmethod
    def _select_random_location(cls, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Vyber náhodnou lokaci z world state."""
        hexcrawl = world_state.get("hexcrawl", {})
        settlements = hexcrawl.get("settlements", [])
        hexes = hexcrawl.get("hexes", [])
        dungeons = hexcrawl.get("dungeons", [])

        # Vytvoř pool všech lokací
        all_locations = []

        for settlement in settlements:
            all_locations.append({"type": "settlement", "data": settlement})

        for hex_data in hexes:
            all_locations.append({"type": "hex", "data": hex_data})

        for dungeon in dungeons:
            all_locations.append({"type": "dungeon", "data": dungeon})

        if not all_locations:
            raise ValueError("World state neobsahuje žádné lokace!")

        return random.choice(all_locations)

    # === VARIANT D: CATEGORIES ===

    @classmethod
    def _assign_category(cls, location_type: str, location: Dict[str, Any]) -> str:
        """
        Přiřaď kategorii podle typu lokace a její dat.

        Pravidla:
        - Settlement s problem → threat
        - Settlement s notable_npc → npc
        - Settlement s feature → location
        - Hex → location
        - Dungeon s inhabitants → threat
        - Dungeon s secret → mystery/treasure
        """
        if location_type == "settlement":
            if location.get("problem"):
                return "threat"
            elif location.get("notable_npc"):
                return random.choice(["npc", "npc", "location"])  # 66% npc, 33% location
            else:
                return "location"

        elif location_type == "hex":
            # Hexy jsou většinou location nebo mystery
            return random.choice(["location", "location", "mystery"])  # 66% location, 33% mystery

        elif location_type == "dungeon":
            if location.get("inhabitants"):
                return random.choice(["threat", "mystery"])  # 50/50
            elif location.get("secret"):
                return random.choice(["treasure", "mystery"])  # 50/50
            else:
                return "mystery"

        # Default
        return random.choice(["threat", "location", "mystery"])

    @classmethod
    def _select_template_name(
        cls,
        category: str,
        location_type: str,
        location: Dict[str, Any]
    ) -> str:
        """Vyber jméno templatu podle kategorie a typu lokace."""
        # Mapping: (category, location_type) → možné templates
        template_map = {
            ("threat", "settlement"): ["threat_settlement_problem"],
            ("threat", "dungeon"): ["threat_dungeon_inhabitants"],
            ("npc", "settlement"): ["npc_quest", "npc_item"],
            ("location", "hex"): ["location_hex_detail"],
            ("location", "settlement"): ["location_settlement_feature"],
            ("treasure", "dungeon"): ["treasure_dungeon_secret"],
            ("treasure", "hex"): ["treasure_hex_location"],
            ("mystery", "dungeon"): ["mystery_dungeon_secret"],
            ("mystery", "hex"): ["mystery_hex_phenomenon"],
        }

        templates = template_map.get((category, location_type), [])

        if not templates:
            # Fallback - zkus jen podle category
            fallback_map = {
                "threat": ["threat_settlement_problem", "threat_dungeon_inhabitants"],
                "npc": ["npc_quest", "npc_item"],
                "location": ["location_hex_detail", "location_settlement_feature"],
                "treasure": ["treasure_dungeon_secret", "treasure_hex_location"],
                "mystery": ["mystery_dungeon_secret", "mystery_hex_phenomenon"],
            }
            templates = fallback_map.get(category, ["threat_settlement_problem"])

        return random.choice(templates)

    @classmethod
    def _extract_location_data(
        cls,
        location_type: str,
        location: Dict[str, Any]
    ) -> Dict[str, str]:
        """Extrahuj relevantní data z lokace pro template."""
        if location_type == "settlement":
            return {
                "settlement_name": location.get("name", "osada"),
                "problem": location.get("problem", "neznámý problém"),
                "notable_npc": location.get("notable_npc", "místní vůdce"),
                "feature": location.get("features", ["zajímavý prvek"])[0] if location.get("features") else "zajímavý prvek",
                "government": location.get("government", "vláda"),
            }

        elif location_type == "hex":
            return {
                "terrain": location.get("type", "krajina"),
                "detail": location.get("detail_name", "zajímavé místo"),
                "landmark": location.get("landmark", ""),
            }

        elif location_type == "dungeon":
            return {
                "dungeon_past": location.get("past", "staré místo"),
                "inhabitants": location.get("inhabitants", "neznámé bytosti"),
                "secret": location.get("secret", "tajemství"),
                "goal": location.get("goal", "cíl"),
            }

        return {}

    @classmethod
    def _apply_truthfulness(
        cls,
        template_data: Dict[str, Any],
        truthfulness: str,
        extracted_data: Dict[str, str]
    ) -> tuple:
        """
        Aplikuj truthfulness modifikaci na template.

        Returns:
            (rumor_text, truth_part, false_part)
        """
        modifiers = template_data.get("truthfulness_modifiers", {})
        pattern = modifiers.get(truthfulness, modifiers.get("true", ""))

        if not pattern:
            pattern = template_data.get("pattern", "")

        # Aplikuj partial/false modifikace
        if truthfulness == "partial":
            # Přidej partial modifikace
            partial_mods = template_data.get("partial_modifiers", {})
            for key, values in partial_mods.items():
                if f"[{key}]" in pattern:
                    extracted_data[key] = random.choice(values)

        elif truthfulness == "false":
            # Přidej false modifikace
            false_mods = template_data.get("false_modifiers", {})
            for key, values in false_mods.items():
                if f"[{key}]" in pattern:
                    extracted_data[key] = random.choice(values)

        # Fill placeholders
        rumor_text = pattern
        for key, value in extracted_data.items():
            rumor_text = rumor_text.replace(f"[{key}]", value)

        # Zjisti truth/false parts
        truth_part = None
        false_part = None

        if truthfulness == "partial":
            truth_part = "Základní informace je správná"
            false_part = "Detail je zveličený nebo zkreslený"
        elif truthfulness == "false":
            base_info = list(extracted_data.values())[0] if extracted_data else ""
            truth_part = f"{base_info} existuje" if base_info else "Lokace existuje"
            false_part = "Hlavní tvrzení je nepravdivé"

        return rumor_text, truth_part, false_part

    # === VARIANT C: STORY HOOKS ===

    @classmethod
    def _roll_story_hook(cls, category: str) -> Optional[str]:
        """Hoď k6×k6 pro story hook podle kategorie."""
        # Map kategorie na story hook tabulky
        hook_tables = {
            "npc": ("npc_quest_type", "npc_reward"),
            "treasure": ("treasure_type", "treasure_guardian"),
            "mystery": ("mystery_type", "mystery_cause"),
        }

        tables = hook_tables.get(category)
        if not tables:
            return None

        # Hod 2× k6
        roll1 = roll_d6()
        roll2 = roll_d6()

        entry1 = TableLoader.lookup_story_hook(tables[0], roll1)
        entry2 = TableLoader.lookup_story_hook(tables[1], roll2)

        if not entry1 or not entry2:
            return None

        return f"{entry1['name']} / {entry2['name']}"

    # === VARIANT E: GOSSIP NETWORK ===

    @classmethod
    def _simulate_gossip(
        cls,
        base_truth: str,
        truthfulness: str
    ) -> tuple:
        """
        Simuluj šíření zvěsti přes gossip chain.

        Returns:
            (hops, chain) kde chain = [base_truth, hop1, hop2, ...]
        """
        if truthfulness == "true":
            return 0, [base_truth]

        # Partial = 1-2 hopy, False = 3 hopy
        hops = random.randint(1, 2) if truthfulness == "partial" else 3

        chain = [base_truth]
        current_text = base_truth

        for i in range(hops):
            npc = TableLoader.get_random_gossip_npc()
            if not npc:
                break

            distortion_type = npc.get("distortion_type", "exaggeration")
            pattern = TableLoader.get_distortion_pattern(distortion_type)

            if pattern:
                # Přidej frázi nebo modifikátor
                phrases = pattern.get("phrases", [])
                if phrases:
                    phrase = random.choice(phrases)
                    current_text = f"{current_text}, {phrase}"

            chain.append(current_text)

        return hops, chain

    @classmethod
    def _generate_gm_notes(
        cls,
        truthfulness: str,
        location_type: str,
        location: Dict[str, Any]
    ) -> str:
        """Vygeneruj poznámky pro GM."""
        if truthfulness == "true":
            return "Toto je 100% pravda. Hráči najdou přesně to, co zvěst říká."
        elif truthfulness == "partial":
            return "Částečně pravdivé. Základní informace je správná, ale detail je zkreslený."
        else:  # false
            return "FÁMA! Lokace může existovat, ale hlavní tvrzení je lež. Může být past nebo zklamání."

    # === FALLBACK: TEMPLATE-ONLY ===

    @classmethod
    def _create_template_only(cls, roll: int, truthfulness: str) -> Rumor:
        """Vytvoř zvěst bez world state - použij fallback templates."""
        # Vyber náhodnou kategorii
        categories = ["threat", "npc", "location", "treasure", "mystery"]
        category = random.choice(categories)

        # Získej fallback templates pro kategorii
        fallbacks = TableLoader.get_rumor_fallback_templates(category)

        if not fallbacks:
            # Ultimate fallback
            rumor_text = "V okolí se děje něco podivného"
        else:
            rumor_text = random.choice(fallbacks)

        # Pro false přidej "prý"
        if truthfulness == "false":
            rumor_text = rumor_text.replace("je", "prý je").replace("V ", "Prý v ")

        return Rumor(
            roll=roll,
            rumor_text=rumor_text,
            category=category,
            truthfulness=truthfulness,
            source_location=None,
            gossip_hops=0,
            gossip_chain=[],
            story_hook_detail=None,
            truth_part=None,
            false_part=None,
            gm_notes="Generováno bez world state - obecná zvěst."
        )

    # === EXPORT METHODS ===

    @staticmethod
    def to_dict(rumors: List[Rumor]) -> Dict[str, Any]:
        """
        Převede seznam zvěstí na dictionary.

        Args:
            rumors: Seznam Rumor objektů

        Returns:
            Dictionary s metadata a zvěstmi
        """
        result = {
            "metadata": {
                "generator": "RumorGenerator",
                "version": "1.0.0",
                "rumor_count": len(rumors),
                "truthfulness_rates": {
                    "true": "50% (rolls 1-3)",
                    "partial": "33% (rolls 4-5)",
                    "false": "17% (roll 6)"
                }
            },
            "rumors": []
        }

        for rumor in rumors:
            rumor_data = {
                "roll": rumor.roll,
                "rumor": rumor.rumor_text,
                "category": {
                    "name": rumor.category,
                    "name_cz": rumor.category_name_cz,
                    "emoji": rumor.category_emoji
                },
                "truthfulness": {
                    "value": rumor.truthfulness,
                    "name_cz": rumor.truthfulness_name_cz,
                    "symbol": rumor.truthfulness_symbol
                },
                "gossip_hops": rumor.gossip_hops,
                "gm_notes": rumor.gm_notes
            }

            if rumor.source_location:
                rumor_data["source_location"] = rumor.source_location

            if rumor.gossip_chain and len(rumor.gossip_chain) > 1:
                rumor_data["gossip_chain"] = rumor.gossip_chain

            if rumor.story_hook_detail:
                rumor_data["story_hook"] = rumor.story_hook_detail

            if rumor.truth_part:
                rumor_data["truth_part"] = rumor.truth_part

            if rumor.false_part:
                rumor_data["false_part"] = rumor.false_part

            result["rumors"].append(rumor_data)

        return result

    @staticmethod
    def to_json(rumors: List[Rumor], indent: int = 2) -> str:
        """
        Převede seznam zvěstí na JSON string.

        Args:
            rumors: Seznam Rumor objektů
            indent: Počet mezer pro odsazení

        Returns:
            JSON string
        """
        data = RumorGenerator.to_dict(rumors)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(rumors: List[Rumor]) -> str:
        """
        Naformátuj zvěsti jako čitelný text.

        Args:
            rumors: Seznam Rumor objektů

        Returns:
            Formátovaný text s tabulkou zvěstí
        """
        lines = []
        lines.append("═" * 80)
        lines.append("               🎲 TABULKA ZVĚSTÍ (RUMOR TABLE) 🎲")
        lines.append("                    Kombinace B+D+C+E")
        lines.append("═" * 80)
        lines.append("")

        # Hlavička tabulky
        lines.append("K6 │ TYPE      │ ZVĚST                                      │ PRAVDA   │ HOPY")
        lines.append("───┼───────────┼────────────────────────────────────────────┼──────────┼──────")

        for rumor in rumors:
            # Zalomení dlouhého textu
            max_text_len = 42
            text = rumor.rumor_text
            if len(text) > max_text_len:
                text = text[:max_text_len - 3] + "..."

            line = f"{rumor.roll:2d} │{rumor.category_emoji} {rumor.category_name_cz:8s}│ {text:42s} │{rumor.truthfulness_symbol} {rumor.truthfulness_name_cz:6s}│  {rumor.gossip_hops}"
            lines.append(line)

            # Pokud má truth/false parts, přidej je
            if rumor.truth_part or rumor.false_part:
                if rumor.truth_part:
                    lines.append(f"   │           │ ├─ Pravda: {rumor.truth_part:32s}│          │")
                if rumor.false_part:
                    lines.append(f"   │           │ └─ Lež: {rumor.false_part:35s}│          │")

        lines.append("═" * 80)
        lines.append("")
        lines.append("💡 TIP PRO GM:")
        lines.append("   • HOPY = Počet 'telefonních hopů' ve gossip chain")
        lines.append("   • Hody 1-3 jsou pravdivé a spolehlivé")
        lines.append("   • Hody 4-5 jsou částečně pravdivé - něco je zkreslené")
        lines.append("   • Hod 6 je fáma - může vést k překvapení nebo pasti!")
        lines.append("")
        lines.append("═" * 80)

        return "\n".join(lines)
