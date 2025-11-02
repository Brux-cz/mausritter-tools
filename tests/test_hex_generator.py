# -*- coding: utf-8 -*-
"""
Testy pro HexGenerator

Test coverage:
- Základní generování hexu
- Všechny typy hexů (4×)
- Všechny kategorie detailů (6×)
- Settlement integrace
- Properties
- JSON konverze
"""

import json
from src.generators.hex import HexGenerator
from src.core.models import Hex


def test_basic_generation():
    """Test základního generování hexu"""
    hex_obj = HexGenerator.create()

    assert isinstance(hex_obj, Hex)
    assert hex_obj.type
    assert hex_obj.type_roll
    assert 1 <= hex_obj.type_roll <= 6
    assert hex_obj.detail_category
    assert 1 <= hex_obj.detail_category <= 6
    assert hex_obj.detail_name
    assert hex_obj.detail_hook


def test_hex_type_open_land():
    """Test typu Otevřená krajina (k6=1-2)"""
    hex_obj = HexGenerator.create_with_type(type_roll=1)

    assert hex_obj.type_roll == 1
    assert hex_obj.type == "Otevřená krajina"
    assert hex_obj.type_emoji == "🌾"


def test_hex_type_forest():
    """Test typu Les (k6=3-4)"""
    hex_obj = HexGenerator.create_with_type(type_roll=3)

    assert hex_obj.type_roll == 3
    assert hex_obj.type == "Les"
    assert hex_obj.type_emoji == "🌲"


def test_hex_type_river():
    """Test typu Řeka (k6=5)"""
    hex_obj = HexGenerator.create_with_type(type_roll=5)

    assert hex_obj.type_roll == 5
    assert hex_obj.type == "Řeka"
    assert hex_obj.type_emoji == "🌊"


def test_hex_type_human_city():
    """Test typu Lidské město (k6=6)"""
    hex_obj = HexGenerator.create_with_type(type_roll=6)

    assert hex_obj.type_roll == 6
    assert hex_obj.type == "Lidské město"
    assert hex_obj.type_emoji == "🏛️"


def test_all_hex_types():
    """Test že všechny typy hexů se správně generují"""
    expected_types = {
        1: "Otevřená krajina",
        2: "Otevřená krajina",
        3: "Les",
        4: "Les",
        5: "Řeka",
        6: "Lidské město",
    }

    for roll, expected_type in expected_types.items():
        hex_obj = HexGenerator.create_with_type(type_roll=roll)
        assert hex_obj.type == expected_type, f"Nesprávný typ pro hod {roll}"


def test_settlement_category():
    """Test kategorie 1: Myší osada"""
    hex_obj = HexGenerator.create_with_settlement()

    assert hex_obj.detail_category == 1
    assert hex_obj.detail_name == "Myší osada"
    assert hex_obj.detail_subtype is None
    assert hex_obj.is_settlement is True
    assert hex_obj.settlement is not None
    assert hex_obj.settlement.size_name  # Settlement má vždycky size_name
    assert hex_obj.settlement.government  # Settlement má vždycky government
    assert hex_obj.category_name_cz == "Myší osada"


def test_civilization_category():
    """Test kategorie 2: Civilizační prvky"""
    hex_obj = HexGenerator.create(detail_category=2, detail_subtype=1)

    assert hex_obj.detail_category == 2
    assert hex_obj.detail_subtype == 1
    assert hex_obj.detail_name == "Menší myší farma"
    assert hex_obj.detail_hook == "Co se stalo s úrodou?"
    assert hex_obj.is_settlement is False
    assert hex_obj.settlement is None
    assert hex_obj.category_name_cz == "Civilizační prvky"


def test_animal_category():
    """Test kategorie 3: Zvířecí a přírodní prvky"""
    hex_obj = HexGenerator.create(detail_category=3, detail_subtype=1)

    assert hex_obj.detail_category == 3
    assert hex_obj.detail_subtype == 1
    assert hex_obj.detail_name == "Hnízdo zpěvného ptáka"
    assert hex_obj.detail_hook == "Jaké smutné příběhy pěje?"
    assert hex_obj.category_name_cz == "Zvířecí a přírodní prvky"


def test_abandoned_category():
    """Test kategorie 4: Přírodní a opuštěné prvky"""
    hex_obj = HexGenerator.create(detail_category=4, detail_subtype=1)

    assert hex_obj.detail_category == 4
    assert hex_obj.detail_subtype == 1
    assert hex_obj.detail_name == "Nebezpečný přírodní prvek"
    assert hex_obj.detail_hook == "Jak se mu vyhnout?"
    assert hex_obj.category_name_cz == "Přírodní a opuštěné prvky"


def test_mystical_category():
    """Test kategorie 5: Mystické prvky"""
    hex_obj = HexGenerator.create(detail_category=5, detail_subtype=1)

    assert hex_obj.detail_category == 5
    assert hex_obj.detail_subtype == 1
    assert hex_obj.detail_name == "Starý chrám netopýřího kultu"
    assert hex_obj.detail_hook == "Co tu vyvolali?"
    assert hex_obj.category_name_cz == "Mystické prvky"


def test_ancient_category():
    """Test kategorie 6: Pradávné a lidské prvky"""
    hex_obj = HexGenerator.create(detail_category=6, detail_subtype=1)

    assert hex_obj.detail_category == 6
    assert hex_obj.detail_subtype == 1
    assert hex_obj.detail_name == "Zřícená vzducholoď liliputů"
    assert hex_obj.detail_hook == "Jak se dá opravit?"
    assert hex_obj.category_name_cz == "Pradávné a lidské prvky"


def test_all_categories():
    """Test že všechny kategorie detailů se správně generují"""
    categories = [1, 2, 3, 4, 5, 6]

    for category in categories:
        if category == 1:
            # Settlement - speciální případ
            hex_obj = HexGenerator.create_with_settlement()
        else:
            # Normální kategorie
            hex_obj = HexGenerator.create(detail_category=category, detail_subtype=1)

        assert hex_obj.detail_category == category, f"Nesprávná kategorie pro k6={category}"
        assert hex_obj.detail_name, f"Kategorie {category} nemá název"
        assert hex_obj.detail_hook, f"Kategorie {category} nemá háček"


def test_type_emoji_property():
    """Test že všechny typy mají správné emoji"""
    expected_emojis = {
        "Otevřená krajina": "🌾",
        "Les": "🌲",
        "Řeka": "🌊",
        "Lidské město": "🏛️",
    }

    for type_roll in range(1, 7):
        hex_obj = HexGenerator.create_with_type(type_roll=type_roll)
        expected_emoji = expected_emojis.get(hex_obj.type)
        assert hex_obj.type_emoji == expected_emoji, \
            f"Nesprávné emoji pro typ {hex_obj.type}"


def test_is_settlement_property():
    """Test property is_settlement"""
    # Settlement hex
    settlement_hex = HexGenerator.create_with_settlement()
    assert settlement_hex.is_settlement is True

    # Non-settlement hex
    normal_hex = HexGenerator.create(detail_category=2, detail_subtype=1)
    assert normal_hex.is_settlement is False


def test_to_dict():
    """Test konverze na dictionary"""
    hex_obj = HexGenerator.create(detail_category=2, detail_subtype=1)
    data = HexGenerator.to_dict(hex_obj)

    assert isinstance(data, dict)
    assert "type" in data
    assert "type_roll" in data
    assert "type_emoji" in data
    assert "detail" in data
    assert "category" in data["detail"]
    assert "category_name" in data["detail"]
    assert "subtype" in data["detail"]
    assert "name" in data["detail"]
    assert "hook" in data["detail"]
    assert "is_settlement" in data
    assert data["is_settlement"] is False


def test_to_dict_with_settlement():
    """Test konverze na dictionary s osadou"""
    hex_obj = HexGenerator.create_with_settlement()
    data = HexGenerator.to_dict(hex_obj)

    assert isinstance(data, dict)
    assert data["is_settlement"] is True
    assert "settlement" in data
    assert isinstance(data["settlement"], dict)
    # Settlement dict má alespoň tyto klíče (podle SettlementGenerator.to_dict)
    assert "size" in data["settlement"]
    assert "government" in data["settlement"]
    assert "detail" in data["settlement"]


def test_to_json():
    """Test konverze na JSON"""
    hex_obj = HexGenerator.create(detail_category=3, detail_subtype=2)
    json_str = HexGenerator.to_json(hex_obj)

    assert isinstance(json_str, str)
    data = json.loads(json_str)
    assert data["detail"]["category"] == 3
    assert data["detail"]["subtype"] == 2


def test_format_text():
    """Test textového formátování"""
    hex_obj = HexGenerator.create(detail_category=4, detail_subtype=3)
    text = HexGenerator.format_text(hex_obj)

    assert isinstance(text, str)
    assert "HEX PRO HEXCRAWL" in text
    assert hex_obj.type in text
    assert hex_obj.detail_name in text
    assert hex_obj.detail_hook in text
    assert "🎲 Hody:" in text


def test_random_generation_produces_valid_hexes():
    """Test že náhodné generování produkuje validní hexy"""
    for _ in range(10):
        hex_obj = HexGenerator.create()

        assert 1 <= hex_obj.type_roll <= 6
        assert hex_obj.type
        assert 1 <= hex_obj.detail_category <= 6
        assert hex_obj.detail_name
        assert hex_obj.detail_hook

        # Pokud není settlement, musí mít subtype
        if not hex_obj.is_settlement:
            assert hex_obj.detail_subtype is not None
            assert 1 <= hex_obj.detail_subtype <= 8


def test_specific_civilization_details():
    """Test specifických civilizačních detailů"""
    expected_details = {
        1: ("Menší myší farma", "Co se stalo s úrodou?"),
        2: ("Hrad myšího šlechtice", "Před čím chrání?"),
        3: ("Vlídný myší zájezdní hostinec", "Co je ve sklepě?"),
        4: ("Myší lovecký srub", "Co zdejší myši loví?"),
        5: ("Hornická osada", "Co vykopali?"),
        6: ("Bouda myšího poustevníka", "Proč se straní společnosti?"),
        7: ("Přírodní jeskyně", "Co v ní žije?"),
        8: ("Věž potulného rytíře", "Co je jeho posláním?"),
    }

    for subtype, (expected_name, expected_hook) in expected_details.items():
        hex_obj = HexGenerator.create(detail_category=2, detail_subtype=subtype)
        assert hex_obj.detail_name == expected_name
        assert hex_obj.detail_hook == expected_hook


def test_specific_mystical_details():
    """Test specifických mystických detailů"""
    expected_details = {
        1: "Starý chrám netopýřího kultu",
        2: "Vílí kruh",
        3: "Broučí hřbitov",
        4: "Chýše myší čarodějnice",
        5: "Malé, ale hluboké jezírko",
        6: "Rostliny z jiného ročního období",
        7: "Hnízdo soví čarodějky",
        8: "Zvláštní magická anomálie",
    }

    for subtype, expected_name in expected_details.items():
        hex_obj = HexGenerator.create(detail_category=5, detail_subtype=subtype)
        assert hex_obj.detail_name == expected_name


def test_settlement_integration():
    """Test integrace se Settlement Generatorem"""
    hex_obj = HexGenerator.create_with_settlement()

    # Zkontroluj že settlement byl vytvořen
    assert hex_obj.settlement is not None

    # Zkontroluj že settlement má všechny potřebné vlastnosti
    assert hex_obj.settlement.size_name  # Vždycky přítomný
    assert hex_obj.settlement.government  # Vždycky přítomný
    assert hex_obj.settlement.detail  # Vždycky přítomný

    # Zkontroluj že description obsahuje info o settlement
    assert hex_obj.settlement.size_name in hex_obj.description
