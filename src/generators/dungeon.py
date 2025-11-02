"""
DungeonGenerator - generátor dobrodružných míst (dungeonů)

Generuje náhodné dungeony s místnostmi, tvory a poklady podle oficiálních pravidel.
Používá Settlement Generator pro dungeony s minulostí "Myší osada".

Podle oficiálních Mausritter pravidel (14_DUNGEON_CREATION.md).
"""

import json
from typing import Optional
from src.core.models import Dungeon, Room
from src.core.tables import TableLoader
from src.core.dice import roll_d6, roll_d8, roll_d10, roll_d12, roll_d20
from src.generators.settlement import SettlementGenerator


class DungeonGenerator:
    """
    Generátor dungeonů podle oficiálních Mausritter pravidel.

    Mechanika:
    - Dungeon level: k20 (past) × k12 (decay) × k10 (inhabitants) × k8 (goal) × k6 (secret)
    - Room generation: 3×k6 systém (type, creature chance, treasure chance)
    - Settlement integrace: past=20 generuje Settlement

    Použití:
        # Náhodný dungeon s 6 místnostmi
        dungeon = DungeonGenerator.create()

        # Dungeon s konkrétním počtem místností
        dungeon = DungeonGenerator.create(rooms=10)

        # Dungeon s osadou
        dungeon = DungeonGenerator.create_with_settlement()

        # Export do JSON
        json_str = DungeonGenerator.to_json(dungeon)
    """

    @classmethod
    def create(
        cls,
        rooms: int = 6,
        past_roll: Optional[int] = None,
        decay_roll: Optional[int] = None,
        inhabitants_roll: Optional[int] = None,
        goal_roll: Optional[int] = None,
        secret_roll: Optional[int] = None
    ) -> Dungeon:
        """
        Vytvoř náhodný dungeon.

        Args:
            rooms: Počet místností (default: 6)
            past_roll: Volitelný hod k20 pro minulost
            decay_roll: Volitelný hod k12 pro chátrání
            inhabitants_roll: Volitelný hod k10 pro obyvatele
            goal_roll: Volitelný hod k8 pro cíl
            secret_roll: Volitelný hod k6 pro tajemství

        Returns:
            Dungeon objekt s vygenerovanými daty
        """
        # 1. Hoď k20 pro minulost
        if past_roll is None:
            past_roll = roll_d20()

        past_data = TableLoader.lookup_dungeon_past(past_roll)
        if past_data is None:
            past = "Neznámá minulost"
        else:
            past = past_data["name"]

        # 2. Hoď k12 pro chátrání
        if decay_roll is None:
            decay_roll = roll_d12()

        decay_data = TableLoader.lookup_dungeon_decay(decay_roll)
        if decay_data is None:
            decay = "Neznámé chátrání"
        else:
            decay = decay_data["name"]

        # 3. Hoď k10 pro obyvatele
        if inhabitants_roll is None:
            inhabitants_roll = roll_d10()

        inhabitants_data = TableLoader.lookup_dungeon_inhabitants(inhabitants_roll)
        if inhabitants_data is None:
            inhabitants = "Neznámí obyvatelé"
        else:
            inhabitants = inhabitants_data["name"]

        # 4. Hoď k8 pro cíl
        if goal_roll is None:
            goal_roll = roll_d8()

        goal_data = TableLoader.lookup_dungeon_goal(goal_roll)
        if goal_data is None:
            goal = "Neznámý cíl"
        else:
            goal = goal_data["name"]

        # 5. Hoď k6 pro tajemství
        if secret_roll is None:
            secret_roll = roll_d6()

        secret_data = TableLoader.lookup_dungeon_secret(secret_roll)
        if secret_data is None:
            secret = "Neznámé tajemství"
        else:
            secret = secret_data["name"]

        # 6. Speciální případ: Myší osada (past=20)
        settlement = None
        description = ""
        if past_roll == 20:
            settlement = SettlementGenerator.create()
            description = f"{settlement.name} - {settlement.size_name}"

        # 7. Generuj místnosti
        room_list = []
        for i in range(1, rooms + 1):
            room = cls._generate_room(i)
            room_list.append(room)

        # 8. Vytvoř Dungeon objekt
        return Dungeon(
            past=past,
            past_roll=past_roll,
            decay=decay,
            decay_roll=decay_roll,
            inhabitants=inhabitants,
            inhabitants_roll=inhabitants_roll,
            goal=goal,
            goal_roll=goal_roll,
            secret=secret,
            secret_roll=secret_roll,
            rooms=room_list,
            settlement=settlement,
            description=description
        )

    @classmethod
    def create_with_settlement(cls, rooms: int = 6) -> Dungeon:
        """
        Vytvoř dungeon s myší osadou (past_roll=20).

        Args:
            rooms: Počet místností (default: 6)

        Returns:
            Dungeon objekt s osadou
        """
        return cls.create(rooms=rooms, past_roll=20)

    @classmethod
    def _generate_room(cls, room_number: int) -> Room:
        """
        Vygeneruj jednu místnost pomocí 3×k6 systému.

        Args:
            room_number: Číslo místnosti

        Returns:
            Room objekt
        """
        # 1. Hoď k6 pro typ místnosti
        type_roll = roll_d6()
        room_type_data = TableLoader.lookup_room_type(type_roll)

        if room_type_data is None:
            # Fallback
            return Room(
                room_number=room_number,
                room_type="Prázdná",
                room_type_roll=type_roll,
                has_creature=False,
                has_treasure=False
            )

        room_type = room_type_data["name"]

        # 2. Hoď k6 pro šanci na tvora (podmíněné na typu místnosti)
        creature_roll = roll_d6()
        has_creature = creature_roll in room_type_data["creature_chance"]["has_creature_rolls"]

        # 3. Hoď k6 pro šanci na poklad (podmíněné na typu místnosti)
        treasure_roll = roll_d6()
        has_treasure = treasure_roll in room_type_data["treasure_chance"]["has_treasure_rolls"]

        # 4. Generuj konkrétní feature podle typu místnosti
        feature = None
        feature_roll = None

        if room_type == "Prázdná":
            # k20 pro prázdné místnosti
            feature_roll = roll_d20()
            feature_data = TableLoader.lookup_empty_room_feature(feature_roll)
            if feature_data:
                feature = feature_data["name"]

        elif room_type == "Překážka":
            # k8 pro překážky
            feature_roll = roll_d8()
            feature_data = TableLoader.lookup_room_obstacle(feature_roll)
            if feature_data:
                feature = feature_data["name"]

        elif room_type == "Past":
            # k8 pro pasti
            feature_roll = roll_d8()
            feature_data = TableLoader.lookup_room_trap(feature_roll)
            if feature_data:
                feature = feature_data["name"]

        elif room_type == "Hlavolam":
            # k6 pro hlavolamy
            feature_roll = roll_d6()
            feature_data = TableLoader.lookup_room_puzzle(feature_roll)
            if feature_data:
                feature = feature_data["name"]

        elif room_type == "Doupě":
            # k6 pro doupata
            feature_roll = roll_d6()
            feature_data = TableLoader.lookup_room_lair(feature_roll)
            if feature_data:
                feature = feature_data["name"]

        return Room(
            room_number=room_number,
            room_type=room_type,
            room_type_roll=type_roll,
            has_creature=has_creature,
            has_treasure=has_treasure,
            feature=feature,
            feature_roll=feature_roll
        )

    @staticmethod
    def to_dict(dungeon: Dungeon) -> dict:
        """
        Převede Dungeon objekt na dictionary.

        Args:
            dungeon: Dungeon objekt

        Returns:
            Dictionary s daty dungeonu
        """
        result = {
            "past": {
                "roll": dungeon.past_roll,
                "name": dungeon.past
            },
            "decay": {
                "roll": dungeon.decay_roll,
                "name": dungeon.decay
            },
            "inhabitants": {
                "roll": dungeon.inhabitants_roll,
                "name": dungeon.inhabitants
            },
            "goal": {
                "roll": dungeon.goal_roll,
                "name": dungeon.goal
            },
            "secret": {
                "roll": dungeon.secret_roll,
                "name": dungeon.secret
            },
            "room_count": dungeon.room_count,
            "rooms": [],
            "has_settlement": dungeon.has_settlement,
            "description": dungeon.description
        }

        # Přidej místnosti
        for room in dungeon.rooms:
            room_data = {
                "number": room.room_number,
                "type": {
                    "roll": room.room_type_roll,
                    "name": room.room_type,
                    "emoji": room.type_emoji
                },
                "has_creature": room.has_creature,
                "has_treasure": room.has_treasure
            }
            if room.feature:
                room_data["feature"] = {
                    "roll": room.feature_roll,
                    "name": room.feature
                }
            result["rooms"].append(room_data)

        # Pokud obsahuje settlement, přidej settlement data
        if dungeon.has_settlement and dungeon.settlement:
            from src.generators.settlement import SettlementGenerator
            result["settlement"] = SettlementGenerator.to_dict(dungeon.settlement)

        return result

    @staticmethod
    def to_json(dungeon: Dungeon, indent: int = 2) -> str:
        """
        Převede Dungeon objekt na JSON string.

        Args:
            dungeon: Dungeon objekt
            indent: Počet mezer pro odsazení (default: 2)

        Returns:
            JSON string
        """
        data = DungeonGenerator.to_dict(dungeon)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(dungeon: Dungeon) -> str:
        """
        Naformátuj dungeon jako čitelný text.

        Args:
            dungeon: Dungeon objekt

        Returns:
            Formátovaný text s informacemi o dungeonu
        """
        lines = []
        lines.append("═══ DOBRODRUŽNÉ MÍSTO (DUNGEON) ═══")
        lines.append("")
        lines.append(f"🏛️  Minulost: {dungeon.past}")
        lines.append(f"💔 Chátrání: {dungeon.decay}")
        lines.append(f"👥 Obyvatelé: {dungeon.inhabitants}")
        lines.append(f"🎯 Cíl: {dungeon.goal}")
        lines.append(f"🔮 Tajemství: {dungeon.secret}")
        lines.append("")

        if dungeon.has_settlement and dungeon.settlement:
            lines.append("🏘️ MYŠÍ OSADA:")
            from src.generators.settlement import SettlementGenerator
            settlement_text = SettlementGenerator.format_text(dungeon.settlement)
            lines.append(settlement_text)
            lines.append("")

        lines.append(f"🚪 Místnosti ({dungeon.room_count}):")
        lines.append("")

        for room in dungeon.rooms:
            lines.append(f"  #{room.room_number} {room.type_emoji} {room.room_type}")

            # Tvor a poklad
            status_parts = []
            if room.has_creature:
                status_parts.append("👹 Tvor")
            if room.has_treasure:
                status_parts.append("💎 Poklad")
            if status_parts:
                lines.append(f"     {' | '.join(status_parts)}")

            # Feature
            if room.feature:
                lines.append(f"     📋 {room.feature}")
            lines.append("")

        # Hody
        lines.append("🎲 Hody:")
        lines.append(f"   Minulost k20={dungeon.past_roll}")
        lines.append(f"   Chátrání k12={dungeon.decay_roll}")
        lines.append(f"   Obyvatelé k10={dungeon.inhabitants_roll}")
        lines.append(f"   Cíl k8={dungeon.goal_roll}")
        lines.append(f"   Tajemství k6={dungeon.secret_roll}")

        return "\n".join(lines)
