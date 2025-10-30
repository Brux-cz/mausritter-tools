"""
Jednoduchý test runner bez pytest dependency
"""
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Přidej projekt do path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.test_character_generator import (
    test_roll_attributes,
    test_roll_attributes_multiple_times,
    test_determine_origin,
    test_determine_origin_invalid,
    test_generate_name,
    test_generate_name_multiple_times,
    test_generate_birthsign,
    test_generate_birthsign_multiple_times,
    test_generate_coat,
    test_generate_coat_multiple_times,
    test_create_character,
    test_create_with_custom_name,
    test_create_with_gender,
    test_to_dict,
    test_to_json,
    test_create_multiple_characters,
)


def run_test(test_func, test_name):
    """Spusť jeden test a vyprintuj výsledek"""
    try:
        test_func()
        print(f"✓ {test_name}")
        return True
    except AssertionError as e:
        print(f"✗ {test_name}")
        print(f"  Chyba: {e}")
        return False
    except Exception as e:
        print(f"✗ {test_name}")
        print(f"  Neočekávaná chyba: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Spusť všechny testy"""
    print("=" * 60)
    print("Mausritter Character Generator - Testy")
    print("=" * 60)
    print()

    tests = [
        (test_roll_attributes, "test_roll_attributes"),
        (test_roll_attributes_multiple_times, "test_roll_attributes_multiple_times"),
        (test_determine_origin, "test_determine_origin"),
        (test_determine_origin_invalid, "test_determine_origin_invalid"),
        (test_generate_name, "test_generate_name"),
        (test_generate_name_multiple_times, "test_generate_name_multiple_times"),
        (test_generate_birthsign, "test_generate_birthsign"),
        (test_generate_birthsign_multiple_times, "test_generate_birthsign_multiple_times"),
        (test_generate_coat, "test_generate_coat"),
        (test_generate_coat_multiple_times, "test_generate_coat_multiple_times"),
        (test_create_character, "test_create_character"),
        (test_create_with_custom_name, "test_create_with_custom_name"),
        (test_create_with_gender, "test_create_with_gender"),
        (test_to_dict, "test_to_dict"),
        (test_to_json, "test_to_json"),
        (test_create_multiple_characters, "test_create_multiple_characters"),
    ]

    passed = 0
    failed = 0

    for test_func, test_name in tests:
        if run_test(test_func, test_name):
            passed += 1
        else:
            failed += 1

    print()
    print("=" * 60)
    print(f"Výsledky: {passed} úspěšných, {failed} neúspěšných")
    print("=" * 60)

    if failed == 0:
        print("\n✓ Všechny testy prošly!")
        return 0
    else:
        print(f"\n✗ {failed} testů selhalo")
        return 1


if __name__ == "__main__":
    sys.exit(main())
