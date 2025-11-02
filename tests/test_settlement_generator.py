# -*- coding: utf-8 -*-
"""
Testy pro Settlement Generator

Test coverage:
- Základní generování osad
- Všechny velikosti (1-6)
- Generování s názvem
- Integrace hospody pro velikost 3+
- Počty řemesel a prvků podle velikosti
- JSON konverze
"""

import json
from src.generators.settlement import SettlementGenerator
from src.core.models import Settlement


def test_basic_generation():
    """Test základního generování osady"""
    settlement = SettlementGenerator.create()

    assert isinstance(settlement, Settlement)
    assert settlement.size_name
    assert settlement.population
    assert 1 <= settlement.size_value <= 6
    assert settlement.government
    assert settlement.detail
    assert len(settlement.trades) >= 1
    assert len(settlement.features) >= 1
    assert settlement.event


def test_size_1_farm():
    """Test generování farmy (velikost 1)"""
    settlement = SettlementGenerator.create(roll_size_die1=1, roll_size_die2=1)

    assert settlement.size_value == 1
    assert settlement.size_name == "Farma/zámeček"
    assert settlement.population == "1–3 rodiny"
    assert settlement.has_tavern is False
    assert settlement.tavern is None
    assert len(settlement.trades) == 1
    assert len(settlement.features) == 1


def test_size_2_crossroads():
    """Test generování křižovatky (velikost 2)"""
    settlement = SettlementGenerator.create(roll_size_die1=2, roll_size_die2=6)

    assert settlement.size_value == 2
    assert settlement.size_name == "Křižovatka"
    assert settlement.population == "3–5 rodin"
    assert settlement.has_tavern is False
    assert settlement.tavern is None
    assert len(settlement.trades) == 1
    assert len(settlement.features) == 1


def test_size_3_hamlet_with_tavern():
    """Test generování vísky (velikost 3) s hospodou"""
    settlement = SettlementGenerator.create(
        roll_size_die1=3,
        roll_size_die2=5,
        generate_tavern=True
    )

    assert settlement.size_value == 3
    assert settlement.size_name == "Víska"
    assert settlement.population == "50–150 myší"
    assert settlement.has_tavern is True
    assert settlement.tavern is not None
    assert settlement.tavern.full_name
    assert settlement.tavern.specialty
    assert len(settlement.trades) == 1
    assert len(settlement.features) == 1


def test_size_4_village():
    """Test generování vesnice (velikost 4)"""
    settlement = SettlementGenerator.create(roll_size_die1=4, roll_size_die2=4)

    assert settlement.size_value == 4
    assert settlement.size_name == "Vesnice"
    assert settlement.population == "150–300 myší"
    assert settlement.has_tavern is True
    assert len(settlement.trades) == 1
    assert len(settlement.features) == 1


def test_size_5_town_two_trades():
    """Test generování města (velikost 5) se 2 řemesly"""
    settlement = SettlementGenerator.create(
        roll_size_die1=5,
        roll_size_die2=6,
        roll_trades=[1, 2]  # Dva hody pro 2 řemesla
    )

    assert settlement.size_value == 5
    assert settlement.size_name == "Město"
    assert settlement.population == "300–1000 myší"
    assert settlement.has_tavern is True
    assert len(settlement.trades) == 2
    assert len(settlement.features) == 1


def test_size_6_city_two_features():
    """Test generování velkoměsta (velikost 6) se 2 prvky"""
    settlement = SettlementGenerator.create(
        roll_size_die1=6,
        roll_size_die2=6,
        roll_trades=[1, 2],  # Dva hody pro 2 řemesla
        roll_features=[1, 2]  # Dva hody pro 2 prvky
    )

    assert settlement.size_value == 6
    assert settlement.size_name == "Velkoměsto"
    assert settlement.population == "přes 1000+"
    assert settlement.has_tavern is True
    assert len(settlement.trades) == 2
    assert len(settlement.features) == 2


def test_generate_with_name():
    """Test generování osady s názvem"""
    settlement = SettlementGenerator.create(
        generate_name=True,
        roll_name_start=1,
        roll_name_end=1
    )

    assert settlement.name != ""
    assert settlement.roll_name_start == 1
    assert settlement.roll_name_end == 1


def test_no_tavern_for_small_settlement():
    """Test že malé osady (1-2) nemají hospodu"""
    settlement = SettlementGenerator.create(
        roll_size_die1=1,
        roll_size_die2=2,
        generate_tavern=True  # I když je zapnuto, neměla by se generovat
    )

    assert settlement.size_value == 1
    assert settlement.has_tavern is False
    assert settlement.tavern is None


def test_disable_tavern_generation():
    """Test vypnutí generování hospody i pro větší osady"""
    settlement = SettlementGenerator.create(
        roll_size_die1=5,
        roll_size_die2=6,
        generate_tavern=False
    )

    assert settlement.size_value == 5
    assert settlement.has_tavern is True  # Property říká že by měla mít
    assert settlement.tavern is None  # Ale není vygenerována


def test_government_calculation():
    """Test výpočtu vlády (k6 + sizeValue)"""
    settlement = SettlementGenerator.create(
        roll_size_die1=1,
        roll_size_die2=1,  # size = 1
        roll_government=1   # 1 + 1 = 2 → "Vedená vesnickými stařešiny"
    )

    assert settlement.government == "Vedená vesnickými stařešiny"

    settlement2 = SettlementGenerator.create(
        roll_size_die1=6,
        roll_size_die2=6,  # size = 6
        roll_government=6   # 6 + 6 = 12 → "Hlavní sídlo šlechtické moci"
    )

    assert settlement2.government == "Hlavní sídlo šlechtické moci"


def test_specific_detail():
    """Test konkrétního detailu"""
    settlement = SettlementGenerator.create(roll_detail=1)

    assert settlement.detail == "Holí si v srsti složité vzory"
    assert settlement.roll_detail == 1


def test_specific_trade():
    """Test konkrétního řemesla"""
    settlement = SettlementGenerator.create(roll_trades=[1])

    assert "Zemědělci pečující o tyčící se plodiny" in settlement.trades
    assert settlement.roll_trades == [1]


def test_specific_feature():
    """Test konkrétního prvku"""
    settlement = SettlementGenerator.create(roll_features=[1])

    assert "Bludiště obranných chodeb plných pastí" in settlement.features
    assert settlement.roll_features == [1]


def test_specific_event():
    """Test konkrétní události"""
    settlement = SettlementGenerator.create(roll_event=1)

    assert settlement.event == "Katastrofa, všichni se balí a odcházejí"
    assert settlement.roll_event == 1


def test_to_dict():
    """Test konverze na dictionary"""
    settlement = SettlementGenerator.create(
        roll_size_die1=3,
        roll_size_die2=4,
        generate_name=True
    )

    data = SettlementGenerator.to_dict(settlement)

    assert isinstance(data, dict)
    assert "size" in data
    assert data["size"]["value"] == 3
    assert "government" in data
    assert "detail" in data
    assert "trades" in data
    assert "features" in data
    assert "event" in data
    assert "rolls" in data
    assert "name" in data


def test_to_json():
    """Test konverze na JSON"""
    settlement = SettlementGenerator.create(roll_size_die1=2, roll_size_die2=2)

    json_str = SettlementGenerator.to_json(settlement)

    assert isinstance(json_str, str)
    data = json.loads(json_str)
    assert data["size"]["value"] == 2
    assert "government" in data
    assert "rolls" in data


def test_json_with_tavern():
    """Test JSON včetně hospody"""
    settlement = SettlementGenerator.create(
        roll_size_die1=4,
        roll_size_die2=6,
        generate_tavern=True
    )

    data = SettlementGenerator.to_dict(settlement)

    assert "tavern" in data
    assert "full_name" in data["tavern"]
    assert "specialty" in data["tavern"]


def test_format_text():
    """Test textového formátování"""
    settlement = SettlementGenerator.create()

    text = SettlementGenerator.format_text(settlement)

    assert isinstance(text, str)
    assert "OSADA" in text
    assert settlement.size_name in text
    assert settlement.government in text


def test_2d6_keep_lower_mechanism():
    """Test mechaniky 2d6 keep-lower pro velikost"""
    # Roll 6,2 → velikost by měla být 2
    settlement = SettlementGenerator.create(roll_size_die1=6, roll_size_die2=2)

    assert settlement.roll_size_die1 == 6
    assert settlement.roll_size_die2 == 2
    assert settlement.size_value == 2  # min(6, 2) = 2

    # Roll 1,5 → velikost by měla být 1
    settlement2 = SettlementGenerator.create(roll_size_die1=1, roll_size_die2=5)

    assert settlement2.size_value == 1  # min(1, 5) = 1


def test_rolls_are_stored():
    """Test že všechny hody jsou uloženy pro reprodukovatelnost"""
    settlement = SettlementGenerator.create(
        roll_size_die1=3,
        roll_size_die2=4,
        roll_government=2,
        roll_detail=5,
        roll_trades=[10],
        roll_features=[15],
        roll_event=20
    )

    assert settlement.roll_size_die1 == 3
    assert settlement.roll_size_die2 == 4
    assert settlement.roll_government == 2
    assert settlement.roll_detail == 5
    assert settlement.roll_trades == [10]
    assert settlement.roll_features == [15]
    assert settlement.roll_event == 20
