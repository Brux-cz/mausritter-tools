# -*- coding: utf-8 -*-
"""
Testy pro CreatureVariantGenerator

Test coverage:
- Základní generování variant
- Všechny typy stvoření (11×)
- Všechny varianty pro každý typ (6×)
- Vlastnosti (emoji, názvy)
- JSON konverze
- Error handling
"""

import json
import pytest
from src.generators.creature_variant import CreatureVariantGenerator
from src.core.models import CreatureVariant


def test_basic_generation():
    """Test základního generování varianty"""
    variant = CreatureVariantGenerator.create("ghost")

    assert isinstance(variant, CreatureVariant)
    assert variant.name
    assert variant.description
    assert variant.creature_type == "ghost"
    assert 1 <= variant.roll <= 6


def test_invalid_creature_type():
    """Test že neplatný typ stvoření vyvolá ValueError"""
    with pytest.raises(ValueError, match="Neplatný typ stvoření"):
        CreatureVariantGenerator.create("invalid_type")


def test_ghost_variant_1():
    """Test přízrak varianta 1: Mihotání"""
    variant = CreatureVariantGenerator.create("ghost", roll=1)

    assert variant.roll == 1
    assert variant.name == "Mihotání"
    assert variant.description  # Just check that description exists
    assert "iluzí" in variant.description.lower()  # Check for specific content
    assert variant.creature_type == "ghost"
    assert variant.creature_name_cz == "Přízrak"
    assert variant.creature_emoji == "👻"
    assert variant.variant_table_name_cz == "Přízračné schopnosti"


def test_snake_variant_1():
    """Test had varianta 1: Dřevěný"""
    variant = CreatureVariantGenerator.create("snake", roll=1)

    assert variant.roll == 1
    assert variant.name == "Dřevěný"
    assert variant.creature_type == "snake"
    assert variant.creature_name_cz == "Had"
    assert variant.creature_emoji == "🐍"
    assert variant.variant_table_name_cz == "Zvláštní hadi"


def test_cat_variant_1():
    """Test kočka varianta 1: Baltazar"""
    variant = CreatureVariantGenerator.create("cat", roll=1)

    assert variant.roll == 1
    assert variant.name == "Baltazar"
    assert variant.creature_type == "cat"
    assert variant.creature_name_cz == "Kočka"
    assert variant.creature_emoji == "🐱"
    assert variant.variant_table_name_cz == "Kočičí pánové a paní"


def test_rat_variant_1():
    """Test krysa varianta 1: Tuhoši"""
    variant = CreatureVariantGenerator.create("rat", roll=1)

    assert variant.roll == 1
    assert variant.name == "Tuhoši"
    assert variant.creature_type == "rat"
    assert variant.creature_name_cz == "Krysa"
    assert variant.creature_emoji == "🐀"
    assert variant.variant_table_name_cz == "Krysí gangy"


def test_mouse_variant_1():
    """Test myš varianta 1: Bodlák"""
    variant = CreatureVariantGenerator.create("mouse", roll=1)

    assert variant.roll == 1
    assert variant.name == "Bodlák"
    assert variant.creature_type == "mouse"
    assert variant.creature_name_cz == "Myš"
    assert variant.creature_emoji == "🐭"
    assert variant.variant_table_name_cz == "Konkurenční myší dobrodruzi"


def test_spider_variant_1():
    """Test pavouk varianta 1: Vdova"""
    variant = CreatureVariantGenerator.create("spider", roll=1)

    assert variant.roll == 1
    assert variant.name == "Vdova"
    assert variant.creature_type == "spider"
    assert variant.creature_name_cz == "Pavouk"
    assert variant.creature_emoji == "🕷️"
    assert variant.variant_table_name_cz == "Druhy pavouků"


def test_owl_variant_1():
    """Test sova varianta 1: Bezalel"""
    variant = CreatureVariantGenerator.create("owl", roll=1)

    assert variant.roll == 1
    assert variant.name == "Bezalel"
    assert variant.creature_type == "owl"
    assert variant.creature_name_cz == "Sova"
    assert variant.creature_emoji == "🦉"
    assert variant.variant_table_name_cz == "Soví čarodějové"


def test_centipede_variant_1():
    """Test stonožka varianta 1: Obří"""
    variant = CreatureVariantGenerator.create("centipede", roll=1)

    assert variant.roll == 1
    assert variant.name == "Obří"
    assert variant.creature_type == "centipede"
    assert variant.creature_name_cz == "Stonožka"
    assert variant.creature_emoji == "🐛"
    assert variant.variant_table_name_cz == "Zevlující stonožky"


def test_fairy_variant_1():
    """Test víla varianta 1: Únosy dětí"""
    variant = CreatureVariantGenerator.create("fairy", roll=1)

    assert variant.roll == 1
    assert variant.name == "Únosy dětí"
    assert variant.creature_type == "fairy"
    assert variant.creature_name_cz == "Víla"
    assert variant.creature_emoji == "🧚"
    assert variant.variant_table_name_cz == "Vílí plány"


def test_crow_variant_1():
    """Test vrána varianta 1: Píseň úsvitu"""
    variant = CreatureVariantGenerator.create("crow", roll=1)

    assert variant.roll == 1
    assert variant.name == "Píseň úsvitu"
    assert variant.creature_type == "crow"
    assert variant.creature_name_cz == "Vrána"
    assert variant.creature_emoji == "🦅"
    assert variant.variant_table_name_cz == "Vraní písně"


def test_frog_variant_1():
    """Test žába varianta 1: Gval"""
    variant = CreatureVariantGenerator.create("frog", roll=1)

    assert variant.roll == 1
    assert variant.name == "Gval"
    assert variant.creature_type == "frog"
    assert variant.creature_name_cz == "Žába"
    assert variant.creature_emoji == "🐸"
    assert variant.variant_table_name_cz == "Potulní žabí rytíři"


def test_all_ghost_variants():
    """Test všech 6 variant přízraků"""
    expected_names = ["Mihotání", "Poltergeist", "Uvěznění", "Zhouba", "Hniloba", "Nehmotný"]

    for roll in range(1, 7):
        variant = CreatureVariantGenerator.create("ghost", roll=roll)
        assert variant.roll == roll
        assert variant.name == expected_names[roll - 1]
        assert variant.description
        assert variant.creature_type == "ghost"


def test_all_frog_variants():
    """Test všech 6 variant žabích rytířů"""
    expected_names = ["Gval", "Filip", "Lurf", "Slup", "Uuu", "Puk"]

    for roll in range(1, 7):
        variant = CreatureVariantGenerator.create("frog", roll=roll)
        assert variant.roll == roll
        assert variant.name == expected_names[roll - 1]
        assert variant.description
        assert variant.creature_type == "frog"


def test_all_creature_types_have_variants():
    """Test že všechny typy stvoření mají varianty"""
    creature_types = [
        "ghost", "snake", "cat", "rat", "mouse", "spider",
        "owl", "centipede", "fairy", "crow", "frog"
    ]

    for creature_type in creature_types:
        variant = CreatureVariantGenerator.create(creature_type)
        assert variant.creature_type == creature_type
        assert variant.name
        assert variant.description
        assert 1 <= variant.roll <= 6


def test_all_variants_for_all_types():
    """Test že všechny typy stvoření mají 6 variant"""
    creature_types = [
        "ghost", "snake", "cat", "rat", "mouse", "spider",
        "owl", "centipede", "fairy", "crow", "frog"
    ]

    for creature_type in creature_types:
        names = []
        for roll in range(1, 7):
            variant = CreatureVariantGenerator.create(creature_type, roll=roll)
            assert variant.roll == roll
            assert variant.name
            assert variant.description
            names.append(variant.name)

        # Kontrola že všechny názvy jsou unikátní
        assert len(set(names)) == 6, f"Typ {creature_type} nemá 6 unikátních variant"


def test_creature_emoji_mapping():
    """Test že všechny typy stvoření mají správné emoji"""
    expected_emojis = {
        "ghost": "👻",
        "snake": "🐍",
        "cat": "🐱",
        "rat": "🐀",
        "mouse": "🐭",
        "spider": "🕷️",
        "owl": "🦉",
        "centipede": "🐛",
        "fairy": "🧚",
        "crow": "🦅",
        "frog": "🐸",
    }

    for creature_type, expected_emoji in expected_emojis.items():
        variant = CreatureVariantGenerator.create(creature_type)
        assert variant.creature_emoji == expected_emoji, \
            f"Nesprávné emoji pro typ {creature_type}"


def test_creature_name_cz_mapping():
    """Test že všechny typy stvoření mají české názvy"""
    expected_names = {
        "ghost": "Přízrak",
        "snake": "Had",
        "cat": "Kočka",
        "rat": "Krysa",
        "mouse": "Myš",
        "spider": "Pavouk",
        "owl": "Sova",
        "centipede": "Stonožka",
        "fairy": "Víla",
        "crow": "Vrána",
        "frog": "Žába",
    }

    for creature_type, expected_name in expected_names.items():
        variant = CreatureVariantGenerator.create(creature_type)
        assert variant.creature_name_cz == expected_name, \
            f"Nesprávný český název pro typ {creature_type}"


def test_variant_table_name_cz_mapping():
    """Test že všechny typy stvoření mají české názvy tabulek"""
    expected_table_names = {
        "ghost": "Přízračné schopnosti",
        "snake": "Zvláštní hadi",
        "cat": "Kočičí pánové a paní",
        "rat": "Krysí gangy",
        "mouse": "Konkurenční myší dobrodruzi",
        "spider": "Druhy pavouků",
        "owl": "Soví čarodějové",
        "centipede": "Zevlující stonožky",
        "fairy": "Vílí plány",
        "crow": "Vraní písně",
        "frog": "Potulní žabí rytíři",
    }

    for creature_type, expected_table_name in expected_table_names.items():
        variant = CreatureVariantGenerator.create(creature_type)
        assert variant.variant_table_name_cz == expected_table_name, \
            f"Nesprávný název tabulky pro typ {creature_type}"


def test_to_dict():
    """Test konverze na dictionary"""
    variant = CreatureVariantGenerator.create("owl", roll=1)
    data = CreatureVariantGenerator.to_dict(variant)

    assert isinstance(data, dict)
    assert "name" in data
    assert "description" in data
    assert "creature_type" in data
    assert "creature_name" in data
    assert "variant_table" in data
    assert "roll" in data
    assert data["roll"] == 1
    assert data["creature_name"] == "Sova"
    assert data["creature_type"] == "owl"
    assert data["name"] == "Bezalel"


def test_to_json():
    """Test konverze na JSON"""
    variant = CreatureVariantGenerator.create("snake", roll=2)
    json_str = CreatureVariantGenerator.to_json(variant)

    assert isinstance(json_str, str)
    data = json.loads(json_str)
    assert data["creature_type"] == "snake"
    assert data["roll"] == 2
    assert "name" in data
    assert "description" in data


def test_format_text():
    """Test textového formátování"""
    variant = CreatureVariantGenerator.create("cat", roll=3)
    text = CreatureVariantGenerator.format_text(variant)

    assert isinstance(text, str)
    assert "VARIANTA STVOŘENÍ" in text
    assert variant.name in text
    assert variant.creature_name_cz in text
    assert variant.description in text
    assert "🎲 Hod:" in text


def test_random_generation_produces_valid_variants():
    """Test že náhodné generování produkuje validní varianty"""
    for _ in range(20):
        variant = CreatureVariantGenerator.create("ghost")
        assert 1 <= variant.roll <= 6
        assert variant.name
        assert variant.description
        assert variant.creature_type == "ghost"


def test_get_available_types():
    """Test získání seznamu dostupných typů"""
    types = CreatureVariantGenerator.get_available_types()

    assert isinstance(types, list)
    assert len(types) == 11
    assert "ghost" in types
    assert "snake" in types
    assert "cat" in types
    assert "rat" in types
    assert "mouse" in types
    assert "spider" in types
    assert "owl" in types
    assert "centipede" in types
    assert "fairy" in types
    assert "crow" in types
    assert "frog" in types


def test_specific_owl_wizards():
    """Test specifických sovích čarodějů"""
    expected_wizards = {
        1: "Bezalel",
        2: "Morgana",
        3: "Prospero",
        4: "Krahujka",
        5: "Raistlin",
        6: "Saxana",
    }

    for roll, expected_name in expected_wizards.items():
        variant = CreatureVariantGenerator.create("owl", roll=roll)
        assert variant.name == expected_name
        assert variant.creature_type == "owl"


def test_specific_crow_songs():
    """Test specifických vraních písní"""
    expected_songs = {
        1: "Píseň úsvitu",
        2: "Píseň žalu",
        3: "Píseň zraku",
        4: "Píseň větru",
        5: "Píseň minulosti",
        6: "Píseň pravdy",
    }

    for roll, expected_name in expected_songs.items():
        variant = CreatureVariantGenerator.create("crow", roll=roll)
        assert variant.name == expected_name
        assert variant.creature_type == "crow"
