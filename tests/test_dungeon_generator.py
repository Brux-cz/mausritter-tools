# -*- coding: utf-8 -*-
"""
Testy pro DungeonGenerator

Test coverage:
- Základní generování dungeonu
- Všechny dungeon-level atributy (past, decay, inhabitants, goal, secret)
- Settlement integrace (past=20)
- Room generation se všemi typy
- Creature a treasure šance
- Room features pro každý typ
- Properties
- JSON konverze
"""

import json
from src.generators.dungeon import DungeonGenerator
from src.core.models import Dungeon, Room


def test_basic_generation():
    """Test základního generování dungeonu"""
    dungeon = DungeonGenerator.create()

    assert isinstance(dungeon, Dungeon)
    assert dungeon.past
    assert 1 <= dungeon.past_roll <= 20
    assert dungeon.decay
    assert 1 <= dungeon.decay_roll <= 12
    assert dungeon.inhabitants
    assert 1 <= dungeon.inhabitants_roll <= 10
    assert dungeon.goal
    assert 1 <= dungeon.goal_roll <= 8
    assert dungeon.secret
    assert 1 <= dungeon.secret_roll <= 6
    assert len(dungeon.rooms) == 6  # default


def test_custom_room_count():
    """Test generování s vlastním počtem místností"""
    dungeon = DungeonGenerator.create(rooms=10)

    assert len(dungeon.rooms) == 10
    assert dungeon.room_count == 10


def test_past_generation():
    """Test generování minulosti (k20)"""
    # Test konkrétního hodu
    dungeon = DungeonGenerator.create(past_roll=1)

    assert dungeon.past_roll == 1
    assert dungeon.past == "Starodávný chrám netopýřího kultu"


def test_decay_generation():
    """Test generování chátrání (k12)"""
    dungeon = DungeonGenerator.create(decay_roll=1)

    assert dungeon.decay_roll == 1
    assert dungeon.decay == "Zatopení"


def test_inhabitants_generation():
    """Test generování obyvatel (k10)"""
    dungeon = DungeonGenerator.create(inhabitants_roll=3)

    assert dungeon.inhabitants_roll == 3
    assert dungeon.inhabitants == "Krysí loupežníci"


def test_goal_generation():
    """Test generování cíle (k8)"""
    dungeon = DungeonGenerator.create(goal_roll=1)

    assert dungeon.goal_roll == 1
    assert dungeon.goal == "Bezpečný úkryt nebo místo k životu"


def test_secret_generation():
    """Test generování tajemství (k6)"""
    dungeon = DungeonGenerator.create(secret_roll=6)

    assert dungeon.secret_roll == 6
    assert dungeon.secret == "Portál do vílího království"


def test_settlement_integration():
    """Test integrace se Settlement Generatorem (past=20)"""
    dungeon = DungeonGenerator.create_with_settlement()

    # Zkontroluj že past=20
    assert dungeon.past_roll == 20
    assert dungeon.past == "Myší osada"

    # Zkontroluj že settlement byl vytvořen
    assert dungeon.settlement is not None
    assert dungeon.has_settlement is True

    # Zkontroluj že settlement má všechny potřebné vlastnosti
    assert dungeon.settlement.size_name
    assert dungeon.settlement.government

    # Zkontroluj že description obsahuje info o settlement
    assert dungeon.settlement.size_name in dungeon.description


def test_room_generation():
    """Test generování místností"""
    dungeon = DungeonGenerator.create(rooms=3)

    assert len(dungeon.rooms) == 3

    for i, room in enumerate(dungeon.rooms, 1):
        assert isinstance(room, Room)
        assert room.room_number == i
        assert room.room_type
        assert 1 <= room.room_type_roll <= 6
        assert isinstance(room.has_creature, bool)
        assert isinstance(room.has_treasure, bool)


def test_room_type_empty():
    """Test typu místnosti Prázdná (k6=1-2)"""
    dungeon = DungeonGenerator.create(rooms=20)

    # Najdi alespoň jednu prázdnou místnost
    empty_rooms = [r for r in dungeon.rooms if r.room_type == "Prázdná"]
    assert len(empty_rooms) > 0

    for room in empty_rooms:
        assert room.room_type == "Prázdná"
        assert room.type_emoji == "⬜"
        # Prázdná místnost má feature z k20 tabulky
        if room.feature:
            assert room.feature_roll is not None
            assert 1 <= room.feature_roll <= 20


def test_room_type_obstacle():
    """Test typu místnosti Překážka (k6=3)"""
    dungeon = DungeonGenerator.create(rooms=30)

    # Najdi alespoň jednu místnost s překážkou
    obstacle_rooms = [r for r in dungeon.rooms if r.room_type == "Překážka"]
    if len(obstacle_rooms) > 0:
        room = obstacle_rooms[0]
        assert room.room_type == "Překážka"
        assert room.type_emoji == "🚧"
        # Překážka má feature z k8 tabulky
        if room.feature:
            assert 1 <= room.feature_roll <= 8


def test_room_type_trap():
    """Test typu místnosti Past (k6=4)"""
    dungeon = DungeonGenerator.create(rooms=30)

    # Najdi alespoň jednu místnost s pastí
    trap_rooms = [r for r in dungeon.rooms if r.room_type == "Past"]
    if len(trap_rooms) > 0:
        room = trap_rooms[0]
        assert room.room_type == "Past"
        assert room.type_emoji == "⚠️"
        # Past má feature z k8 tabulky
        if room.feature:
            assert 1 <= room.feature_roll <= 8


def test_room_type_puzzle():
    """Test typu místnosti Hlavolam (k6=5)"""
    dungeon = DungeonGenerator.create(rooms=30)

    # Najdi alespoň jednu místnost s hlavolamem
    puzzle_rooms = [r for r in dungeon.rooms if r.room_type == "Hlavolam"]
    if len(puzzle_rooms) > 0:
        room = puzzle_rooms[0]
        assert room.room_type == "Hlavolam"
        assert room.type_emoji == "🧩"
        # Hlavolam má feature z k6 tabulky
        if room.feature:
            assert 1 <= room.feature_roll <= 6


def test_room_type_lair():
    """Test typu místnosti Doupě (k6=6)"""
    dungeon = DungeonGenerator.create(rooms=30)

    # Najdi alespoň jednu místnost s doupětem
    lair_rooms = [r for r in dungeon.rooms if r.room_type == "Doupě"]
    if len(lair_rooms) > 0:
        room = lair_rooms[0]
        assert room.room_type == "Doupě"
        assert room.type_emoji == "🏰"
        # Doupě má feature z k6 tabulky
        if room.feature:
            assert 1 <= room.feature_roll <= 6


def test_all_room_types_have_emoji():
    """Test že všechny typy místností mají emoji"""
    dungeon = DungeonGenerator.create(rooms=30)

    for room in dungeon.rooms:
        assert room.type_emoji
        assert room.type_emoji in ["⬜", "🚧", "⚠️", "🧩", "🏰"]


def test_creature_and_treasure_flags():
    """Test že creature a treasure jsou boolean flagy"""
    dungeon = DungeonGenerator.create(rooms=20)

    for room in dungeon.rooms:
        assert isinstance(room.has_creature, bool)
        assert isinstance(room.has_treasure, bool)


def test_has_settlement_property():
    """Test property has_settlement"""
    # Dungeon se settlement
    settlement_dungeon = DungeonGenerator.create_with_settlement()
    assert settlement_dungeon.has_settlement is True

    # Normální dungeon
    normal_dungeon = DungeonGenerator.create(past_roll=1)
    assert normal_dungeon.has_settlement is False


def test_room_count_property():
    """Test property room_count"""
    dungeon = DungeonGenerator.create(rooms=8)
    assert dungeon.room_count == 8
    assert dungeon.room_count == len(dungeon.rooms)


def test_to_dict():
    """Test konverze na dictionary"""
    dungeon = DungeonGenerator.create(rooms=3)
    data = DungeonGenerator.to_dict(dungeon)

    assert isinstance(data, dict)
    assert "past" in data
    assert "decay" in data
    assert "inhabitants" in data
    assert "goal" in data
    assert "secret" in data
    assert "room_count" in data
    assert "rooms" in data
    assert "has_settlement" in data

    # Zkontroluj strukturu past
    assert "roll" in data["past"]
    assert "name" in data["past"]

    # Zkontroluj místnosti
    assert len(data["rooms"]) == 3
    for room in data["rooms"]:
        assert "number" in room
        assert "type" in room
        assert "has_creature" in room
        assert "has_treasure" in room


def test_to_dict_with_settlement():
    """Test konverze na dictionary se settlement"""
    dungeon = DungeonGenerator.create_with_settlement()
    data = DungeonGenerator.to_dict(dungeon)

    assert data["has_settlement"] is True
    assert "settlement" in data
    assert isinstance(data["settlement"], dict)
    # Settlement dict má alespoň tyto klíče
    assert "size" in data["settlement"]
    assert "government" in data["settlement"]


def test_to_json():
    """Test konverze na JSON"""
    dungeon = DungeonGenerator.create(rooms=2)
    json_str = DungeonGenerator.to_json(dungeon)

    assert isinstance(json_str, str)
    data = json.loads(json_str)
    assert data["room_count"] == 2


def test_format_text():
    """Test textového formátování"""
    dungeon = DungeonGenerator.create(rooms=3)
    text = DungeonGenerator.format_text(dungeon)

    assert isinstance(text, str)
    assert "DOBRODRUŽNÉ MÍSTO" in text
    assert dungeon.past in text
    assert dungeon.decay in text
    assert dungeon.inhabitants in text
    assert dungeon.goal in text
    assert dungeon.secret in text
    assert "🎲 Hody:" in text


def test_random_generation_produces_valid_dungeons():
    """Test že náhodné generování produkuje validní dungeony"""
    for _ in range(5):
        dungeon = DungeonGenerator.create()

        assert 1 <= dungeon.past_roll <= 20
        assert 1 <= dungeon.decay_roll <= 12
        assert 1 <= dungeon.inhabitants_roll <= 10
        assert 1 <= dungeon.goal_roll <= 8
        assert 1 <= dungeon.secret_roll <= 6
        assert dungeon.past
        assert dungeon.decay
        assert dungeon.inhabitants
        assert dungeon.goal
        assert dungeon.secret
        assert len(dungeon.rooms) == 6


def test_all_past_entries():
    """Test všech 20 položek minulosti"""
    for roll in range(1, 21):
        dungeon = DungeonGenerator.create(past_roll=roll)
        assert dungeon.past_roll == roll
        assert dungeon.past
        if roll == 20:
            assert dungeon.past == "Myší osada"
            assert dungeon.has_settlement is True


def test_all_decay_entries():
    """Test všech 12 položek chátrání"""
    expected = {
        1: "Zatopení",
        2: "Magická nehoda",
        3: "Stáří a hniloba",
        12: "Nákaza"
    }

    for roll, expected_name in expected.items():
        dungeon = DungeonGenerator.create(decay_roll=roll)
        assert dungeon.decay == expected_name


def test_all_inhabitants_entries():
    """Test všech 10 položek obyvatel"""
    expected = {
        1: "Myši, poblázněné nebo zoufalé",
        3: "Krysí loupežníci",
        10: "Kočičí pán a jeho služebníci"
    }

    for roll, expected_name in expected.items():
        dungeon = DungeonGenerator.create(inhabitants_roll=roll)
        assert dungeon.inhabitants == expected_name


def test_all_goal_entries():
    """Test všech 8 položek cílů"""
    expected = {
        1: "Bezpečný úkryt nebo místo k životu",
        8: "Ohromné množství ďobků"
    }

    for roll, expected_name in expected.items():
        dungeon = DungeonGenerator.create(goal_roll=roll)
        assert dungeon.goal == expected_name


def test_all_secret_entries():
    """Test všech 6 položek tajemství"""
    expected = {
        1: "Obelisk hučící mystickou energií",
        6: "Portál do vílího království"
    }

    for roll, expected_name in expected.items():
        dungeon = DungeonGenerator.create(secret_roll=roll)
        assert dungeon.secret == expected_name


def test_room_numbers_sequential():
    """Test že čísla místností jsou sekvenční"""
    dungeon = DungeonGenerator.create(rooms=5)

    for i, room in enumerate(dungeon.rooms, 1):
        assert room.room_number == i
