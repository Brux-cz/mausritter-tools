"""
Testy pro ReactionGenerator
"""
import json
from src.generators.reaction import ReactionGenerator
from src.core.models import Reaction


def test_roll_reaction_range():
    """Test že hod je v rozsahu 2-12"""
    for _ in range(20):
        roll = ReactionGenerator.roll_reaction()
        assert 2 <= roll <= 12, f"Hod {roll} není v rozsahu 2-12"


def test_create_returns_reaction():
    """Test že create() vrací Reaction objekt"""
    reaction = ReactionGenerator.create()
    assert isinstance(reaction, Reaction)
    assert isinstance(reaction.roll, int)
    assert isinstance(reaction.reaction, str)
    assert isinstance(reaction.question, str)
    assert 2 <= reaction.roll <= 12


def test_all_reaction_types():
    """Test že všechny typy reakcí jsou možné"""
    # Známé reakce z tabulky
    expected_reactions = {
        "Agresivní",
        "Nepřátelská",
        "Nejistá",
        "Povídavá",
        "Nápomocná"
    }

    # Vygeneruj hodně reakcí a sbírej typy
    found_reactions = set()
    for _ in range(200):  # Dostatek pokusů pro zachycení všech typů
        reaction = ReactionGenerator.create()
        found_reactions.add(reaction.reaction)

    # Kontrola že jsme našli většinu typů (kvůli náhodnosti nemusíme najít všechny)
    assert len(found_reactions) >= 3, f"Našli jsme jen {len(found_reactions)} různých reakcí"
    assert found_reactions.issubset(expected_reactions), f"Neznámé reakce: {found_reactions - expected_reactions}"


def test_reaction_questions_not_empty():
    """Test že každá reakce má neprázdnou otázku"""
    for _ in range(10):
        reaction = ReactionGenerator.create()
        assert len(reaction.question) > 0, "Otázka nesmí být prázdná"
        assert reaction.question.endswith("?"), "Otázka by měla končit otazníkem"


def test_modifier_changes_result():
    """Test že modifikátor ovlivňuje výsledek"""
    # S velkým pozitivním modifikátorem by měly být příznivější reakce
    positive_results = []
    for _ in range(20):
        reaction = ReactionGenerator.create(modifier=5)
        positive_results.append(reaction.roll)

    # Průměrný hod by měl být vyšší než bez modifikátoru
    avg_positive = sum(positive_results) / len(positive_results)
    assert avg_positive > 7.5, f"Průměr s +5 modifikátorem je jen {avg_positive}"


def test_modifier_clamped_to_valid_range():
    """Test že modifikátor je omezen na validní rozsah 2-12"""
    # Extrémně velký pozitivní modifikátor
    reaction = ReactionGenerator.create(modifier=100)
    assert 2 <= reaction.roll <= 12, f"Roll {reaction.roll} mimo rozsah 2-12"
    assert reaction.roll == 12, "S velkým modifikátorem by mělo být 12"

    # Extrémně velký negativní modifikátor
    reaction = ReactionGenerator.create(modifier=-100)
    assert 2 <= reaction.roll <= 12, f"Roll {reaction.roll} mimo rozsah 2-12"
    assert reaction.roll == 2, "S velkým záporným modifikátorem by mělo být 2"


def test_negative_modifier_notes():
    """Test že negativní modifikátor je zaznamenán v notes"""
    reaction = ReactionGenerator.create(modifier=-2)
    assert "Modifikátor: -2" in reaction.notes


def test_positive_modifier_notes():
    """Test že pozitivní modifikátor je zaznamenán v notes"""
    reaction = ReactionGenerator.create(modifier=1)
    assert "Modifikátor: +1" in reaction.notes


def test_zero_modifier_no_notes():
    """Test že nulový modifikátor není v notes"""
    reaction = ReactionGenerator.create(modifier=0)
    assert reaction.notes == ""


def test_get_reaction_color():
    """Test že každá reakce má přiřazenou barvu"""
    colors = {
        "Agresivní": "red",
        "Nepřátelská": "yellow",
        "Nejistá": "blue",
        "Povídavá": "green",
        "Nápomocná": "cyan"
    }

    for reaction_type, expected_color in colors.items():
        color = ReactionGenerator.get_reaction_color(reaction_type)
        assert color == expected_color, f"Reakce {reaction_type} má barvu {color}, očekáváno {expected_color}"


def test_to_dict():
    """Test převodu reakce na dictionary"""
    reaction = ReactionGenerator.create()
    data = ReactionGenerator.to_dict(reaction)

    assert isinstance(data, dict)
    assert "roll" in data
    assert "reaction" in data
    assert "question" in data
    assert "notes" in data
    assert data["roll"] == reaction.roll
    assert data["reaction"] == reaction.reaction


def test_to_json():
    """Test převodu reakce na JSON"""
    reaction = ReactionGenerator.create()
    json_str = ReactionGenerator.to_json(reaction)

    assert isinstance(json_str, str)
    assert len(json_str) > 0

    # Validuj že je to platný JSON
    data = json.loads(json_str)
    assert "roll" in data
    assert "reaction" in data
    assert "question" in data


def test_json_contains_czech_characters():
    """Test že JSON obsahuje české znaky správně"""
    reaction = ReactionGenerator.create()
    json_str = ReactionGenerator.to_json(reaction)

    # Kontrola že nejsou escapované české znaky
    assert "\\u" not in json_str or "Agresivní" in json_str, "České znaky by neměly být escapované"


def test_specific_roll_values():
    """Test specifických hodnot hodů a jejich reakcí"""
    # Agresivní = 2
    # Nepřátelská = 3-5
    # Nejistá = 6-8
    # Povídavá = 9-11
    # Nápomocná = 12

    # Použijeme modifikátor pro vynucení specifických hodnot
    # Roll 2k6 má průměr 7, takže:
    # Pro roll 2: modifier = 2 - 7 = -5 (ale může být víc/míň, opakujeme)
    # Pro roll 12: modifier = 12 - 7 = +5

    # Test že roll 2 dává Agresivní (s velkým záporným modifikátorem)
    found_aggressive = False
    for _ in range(50):
        reaction = ReactionGenerator.create(modifier=-10)
        if reaction.roll == 2:
            assert reaction.reaction == "Agresivní"
            found_aggressive = True
            break
    assert found_aggressive, "Nepodařilo se vygenerovat Agresivní reakci"

    # Test že roll 12 dává Nápomocná (s velkým pozitivním modifikátorem)
    found_helpful = False
    for _ in range(50):
        reaction = ReactionGenerator.create(modifier=10)
        if reaction.roll == 12:
            assert reaction.reaction == "Nápomocná"
            found_helpful = True
            break
    assert found_helpful, "Nepodařilo se vygenerovat Nápomocnou reakci"


if __name__ == "__main__":
    # Umožňuje spustit testy přímo: python tests/test_reaction_generator.py
    print("Spouštím testy pro ReactionGenerator...")

    # Spusť všechny test funkce
    test_functions = [
        test_roll_reaction_range,
        test_create_returns_reaction,
        test_all_reaction_types,
        test_reaction_questions_not_empty,
        test_modifier_changes_result,
        test_modifier_clamped_to_valid_range,
        test_negative_modifier_notes,
        test_positive_modifier_notes,
        test_zero_modifier_no_notes,
        test_get_reaction_color,
        test_to_dict,
        test_to_json,
        test_json_contains_czech_characters,
        test_specific_roll_values
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            print(f"[OK] {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test_func.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\nVysledky: {passed} proslo, {failed} selhalo")

    if failed > 0:
        exit(1)
