# -*- coding: utf-8 -*-
"""
Testy pro TavernGenerator
"""
from src.generators.tavern import TavernGenerator
from src.core.models import Tavern


def test_create_basic():
    """Test základního generování hospody"""
    tavern = TavernGenerator.create()

    assert isinstance(tavern, Tavern), "Výsledek musí být Tavern"
    assert isinstance(tavern.name_part1, str), "name_part1 musí být string"
    assert isinstance(tavern.name_part2, str), "name_part2 musí být string"
    assert isinstance(tavern.specialty, str), "specialty musí být string"
    assert len(tavern.name_part1) > 0, "name_part1 nesmí být prázdné"
    assert len(tavern.name_part2) > 0, "name_part2 nesmí být prázdné"
    assert len(tavern.specialty) > 0, "specialty nesmí být prázdné"
    assert 1 <= tavern.roll_part1 <= 12, f"roll_part1 musí být 1-12, dostal {tavern.roll_part1}"
    assert 1 <= tavern.roll_part2 <= 12, f"roll_part2 musí být 1-12, dostal {tavern.roll_part2}"
    assert 1 <= tavern.roll_specialty <= 12, f"roll_specialty musí být 1-12, dostal {tavern.roll_specialty}"


def test_create_with_specific_rolls():
    """Test generování s konkrétními hody"""
    # Test hodu 1/1/1
    tavern = TavernGenerator.create(roll_part1=1, roll_part2=1, roll_specialty=1)

    assert tavern.roll_part1 == 1
    assert tavern.roll_part2 == 1
    assert tavern.roll_specialty == 1
    assert tavern.name_part1 == "Bílý"
    assert tavern.name_part2 == "Brouk"
    assert tavern.specialty == "Pečená kořeněná mrkev"


def test_full_name_property():
    """Test property full_name (správné skloňování)"""
    tavern = TavernGenerator.create(roll_part1=1, roll_part2=1, roll_specialty=1)

    assert tavern.full_name == "U Bílého Brouka"
    assert "U " in tavern.full_name
    assert len(tavern.full_name) > 5


def test_all_parts1():
    """Test všech 12 možností první části názvu"""
    expected = [
        (1, "Bílý"),
        (2, "Zelený"),
        (3, "Černý"),
        (4, "Červený"),
        (5, "Stříbrný"),
        (6, "Křivý"),
        (7, "Přátelský"),
        (8, "Schovaný"),
        (9, "Lstivý"),
        (10, "Skleněný"),
        (11, "Trnitý"),
        (12, "Rozbitý")
    ]

    for roll, expected_text in expected:
        tavern = TavernGenerator.create(roll_part1=roll, roll_part2=1, roll_specialty=1)
        assert tavern.name_part1 == expected_text, f"Roll {roll}: očekáváno '{expected_text}', dostali jsme '{tavern.name_part1}'"


def test_all_parts2():
    """Test všech 12 možností druhé části názvu"""
    expected = [
        (1, "Brouk"),
        (2, "Liška"),
        (3, "Špalek"),
        (4, "Semínko"),
        (5, "Krysa"),
        (6, "Sýr"),
        (7, "Orel"),
        (8, "Červ"),
        (9, "Včela"),
        (10, "Lucerna"),
        (11, "Růže"),
        (12, "Rytíř")
    ]

    for roll, expected_text in expected:
        tavern = TavernGenerator.create(roll_part1=1, roll_part2=roll, roll_specialty=1)
        assert tavern.name_part2 == expected_text, f"Roll {roll}: očekáváno '{expected_text}', dostali jsme '{tavern.name_part2}'"


def test_all_specialties():
    """Test všech 12 specialit"""
    expected = [
        (1, "Pečená kořeněná mrkev"),
        (2, "Žížalí vývar"),
        (3, "Ostružinový koláč"),
        (4, "Uleželý aromatický sýr"),
        (5, "Ječmenná kaše"),
        (6, "Tlustý rybí řízek"),
        (7, "Pečené jablko"),
        (8, "Smažené hmyzí nožičky"),
        (9, "Čerstvý máslový chléb"),
        (10, "Ukořistěné sladkosti"),
        (11, "Semínka pražená v medu"),
        (12, "Houbový guláš")
    ]

    for roll, expected_text in expected:
        tavern = TavernGenerator.create(roll_part1=1, roll_part2=1, roll_specialty=roll)
        assert tavern.specialty == expected_text, f"Roll {roll}: očekáváno '{expected_text}', dostali jsme '{tavern.specialty}'"


def test_genitive_adjectives():
    """Test skloňování přídavných jmen do genitivu"""
    test_cases = [
        (1, 1, "U Bílého Brouka"),  # Bílý → Bílého
        (2, 1, "U Zeleného Brouka"),  # Zelený → Zeleného
        (3, 1, "U Černého Brouka"),  # Černý → Černého
        (7, 1, "U Přátelského Brouka"),  # Přátelský → Přátelského
    ]

    for roll1, roll2, expected_name in test_cases:
        tavern = TavernGenerator.create(roll_part1=roll1, roll_part2=roll2, roll_specialty=1)
        assert tavern.full_name == expected_name, f"Očekáváno '{expected_name}', dostali jsme '{tavern.full_name}'"


def test_genitive_nouns():
    """Test skloňování podstatných jmen do genitivu"""
    test_cases = [
        (1, 1, "U Bílého Brouka"),  # Brouk → Brouka
        (1, 2, "U Bílého Lišky"),  # Liška → Lišky
        (1, 4, "U Bílého Semínka"),  # Semínko → Semínka
        (1, 6, "U Bílého Sýra"),  # Sýr → Sýra
        (1, 7, "U Bílého Orela"),  # Orel → Orela
    ]

    for roll1, roll2, expected_name in test_cases:
        tavern = TavernGenerator.create(roll_part1=roll1, roll_part2=roll2, roll_specialty=1)
        assert tavern.full_name == expected_name, f"Očekáváno '{expected_name}', dostali jsme '{tavern.full_name}'"


def test_to_dict():
    """Test konverze do dictionary"""
    tavern = TavernGenerator.create(roll_part1=3, roll_part2=7, roll_specialty=6)
    data = TavernGenerator.to_dict(tavern)

    assert isinstance(data, dict)
    assert "name_part1" in data
    assert "name_part2" in data
    assert "full_name" in data
    assert "specialty" in data
    assert "roll_part1" in data
    assert "roll_part2" in data
    assert "roll_specialty" in data
    assert data["name_part1"] == "Černý"
    assert data["name_part2"] == "Orel"
    assert data["full_name"] == "U Černého Orela"
    assert data["specialty"] == "Tlustý rybí řízek"


def test_to_json():
    """Test konverze do JSON"""
    tavern = TavernGenerator.create(roll_part1=1, roll_part2=2, roll_specialty=3)
    json_str = TavernGenerator.to_json(tavern)

    assert isinstance(json_str, str)
    assert '"name_part1": "Bílý"' in json_str
    assert '"name_part2": "Liška"' in json_str
    assert '"full_name"' in json_str
    assert '"specialty"' in json_str
    assert "Ostružinový koláč" in json_str


def test_to_json_custom_indent():
    """Test JSON s vlastním odsazením"""
    tavern = TavernGenerator.create(roll_part1=5, roll_part2=6, roll_specialty=7)
    json_str = TavernGenerator.to_json(tavern, indent=4)

    assert isinstance(json_str, str)
    assert "    " in json_str  # 4 mezery odsazení
    assert "Stříbrný" in json_str
    assert "Sýr" in json_str


def test_format_text():
    """Test formátování jako text"""
    tavern = TavernGenerator.create(roll_part1=7, roll_part2=6, roll_specialty=11)
    text = TavernGenerator.format_text(tavern)

    assert isinstance(text, str)
    assert "HOSPODA" in text
    assert "Název:" in text
    assert "Specialita:" in text
    assert "U Přátelského Sýra" in text
    assert "Semínka pražená v medu" in text
    assert "7/6" in text


def test_multiple_random_generations():
    """Test, že náhodné generování funguje opakovaně"""
    taverns = [TavernGenerator.create() for _ in range(10)]

    # Všechny musí být validní
    for tavern in taverns:
        assert isinstance(tavern, Tavern)
        assert 1 <= tavern.roll_part1 <= 12
        assert 1 <= tavern.roll_part2 <= 12
        assert 1 <= tavern.roll_specialty <= 12
        assert len(tavern.name_part1) > 0
        assert len(tavern.name_part2) > 0
        assert len(tavern.specialty) > 0
        assert tavern.full_name.startswith("U ")


def test_unicode_czech_characters():
    """Test, že české znaky fungují správně"""
    tavern = TavernGenerator.create(roll_part1=2, roll_part2=9, roll_specialty=8)

    # Ověř, že české znaky jsou správně uloženy
    assert "Zelený" in tavern.name_part1
    assert "Včela" in tavern.name_part2
    assert "Smažené" in tavern.specialty

    # JSON musí obsahovat české znaky
    json_str = TavernGenerator.to_json(tavern)
    assert "Zelený" in json_str
    assert "Včela" in json_str
    assert "\\u" not in json_str  # ensure_ascii=False
