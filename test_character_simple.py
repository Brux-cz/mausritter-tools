#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Jednoduchý test script pro CharacterGenerator (bez pytest)
"""
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from src.generators.character import CharacterGenerator
from src.core.models import Character


def test_roll_attributes():
    """Test že vlastnosti jsou v rozsahu 2-12"""
    print("\n[TEST] test_roll_attributes...")
    strength, dexterity, willpower = CharacterGenerator.roll_attributes()

    assert 2 <= strength <= 12, f"Síla mimo rozsah: {strength}"
    assert 2 <= dexterity <= 12, f"Mrštnost mimo rozsah: {dexterity}"
    assert 2 <= willpower <= 12, f"Vůle mimo rozsah: {willpower}"
    print(f"  [OK] Vlastnosti: STR={strength}, DEX={dexterity}, WIL={willpower}")


def test_determine_origin():
    """Test lookup v origins table"""
    print("\n[TEST] test_determine_origin...")

    origin = CharacterGenerator.determine_origin(hp=1, pips=1)
    assert origin is not None, "Původ pro HP=1, Pips=1 nenalezen"
    assert origin["name"] == "Pokusná myš"
    print(f"  [OK] HP=1, Pips=1 -> {origin['name']}")

    origin2 = CharacterGenerator.determine_origin(hp=3, pips=5)
    assert origin2 is not None
    assert origin2["name"] == "Stěnolezec"
    print(f"  [OK] HP=3, Pips=5 -> {origin2['name']}")

    origin3 = CharacterGenerator.determine_origin(hp=6, pips=6)
    assert origin3 is not None
    assert origin3["name"] == "Zchudlý šlechtic"
    print(f"  [OK] HP=6, Pips=6 -> {origin3['name']}")


def test_generate_name():
    """Test generování jména"""
    print("\n[TEST] test_generate_name...")

    name = CharacterGenerator.generate_name()
    assert isinstance(name, str), "Jméno musí být string"
    assert len(name) > 0, "Jméno nesmí být prázdné"
    assert " " in name, "Jméno musí obsahovat mezeru"
    print(f"  [OK] Vygenerováno jméno: {name}")

    name_female = CharacterGenerator.generate_name("female")
    assert " " in name_female
    print(f"  [OK] Ženské jméno: {name_female}")


def test_create_character():
    """Test kompletní generování postavy"""
    print("\n[TEST] test_create_character...")

    char = CharacterGenerator.create()

    assert isinstance(char, Character), "Musí vrátit Character instanci"
    assert char.name, "Postava musí mít jméno"
    assert char.background, "Postava musí mít původ"
    assert 2 <= char.strength <= 12, f"Síla mimo rozsah: {char.strength}"
    assert 2 <= char.dexterity <= 12, f"Mrštnost mimo rozsah: {char.dexterity}"
    assert 2 <= char.willpower <= 12, f"Vůle mimo rozsah: {char.willpower}"
    assert 1 <= char.max_hp <= 6, f"HP mimo rozsah: {char.max_hp}"
    assert char.current_hp == char.max_hp
    assert len(char.inventory) == 10, "Inventář musí mít 10 slotů"

    print(f"  [OK] Postava vygenerována:")
    print(f"       Jméno: {char.name}")
    print(f"       Původ: {char.background}")
    print(f"       STR={char.strength}, DEX={char.dexterity}, WIL={char.willpower}")
    print(f"       HP: {char.current_hp}/{char.max_hp}")
    print(f"       Výbava: {len([x for x in char.inventory if x])} předmětů")


def test_create_with_custom_name():
    """Test s vlastním jménem"""
    print("\n[TEST] test_create_with_custom_name...")

    custom_name = "Testovací Myš"
    char = CharacterGenerator.create(name=custom_name)

    assert char.name == custom_name
    assert char.background
    print(f"  [OK] Postava s vlastním jménem: {char.name}")
    print(f"       Původ: {char.background}")


def test_to_json():
    """Test konverze do JSON"""
    print("\n[TEST] test_to_json...")

    char = CharacterGenerator.create(name="JSON Test")
    json_str = CharacterGenerator.to_json(char)

    assert isinstance(json_str, str), "to_json() musí vrátit string"
    assert len(json_str) > 0
    assert "JSON Test" in json_str

    # Ověř že je to validní JSON
    import json
    parsed = json.loads(json_str)
    assert parsed["name"] == "JSON Test"
    print(f"  [OK] JSON konverze funguje")
    print(f"       JSON délka: {len(json_str)} znaků")


def test_multiple_characters():
    """Test že můžeme vytvořit více různých postav"""
    print("\n[TEST] test_multiple_characters...")

    characters = []
    for i in range(5):
        char = CharacterGenerator.create()
        characters.append(char)

    # Všechny postavy musí být validní
    for char in characters:
        assert char.name
        assert 2 <= char.strength <= 12
        assert 1 <= char.max_hp <= 6

    names = [c.name for c in characters]
    unique_names = len(set(names))

    print(f"  [OK] Vytvořeno 5 postav")
    print(f"       Unikátní jména: {unique_names}/5")
    for i, char in enumerate(characters, 1):
        print(f"       {i}. {char.name} ({char.background})")


def main():
    """Spusť všechny testy"""
    print("="*70)
    print("CharacterGenerator Test Suite (bez pytest)")
    print("="*70)

    tests = [
        test_roll_attributes,
        test_determine_origin,
        test_generate_name,
        test_create_character,
        test_create_with_custom_name,
        test_to_json,
        test_multiple_characters,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  [FAIL] {e}")
        except Exception as e:
            failed += 1
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*70)
    print(f"Výsledky: {passed} testů prošlo, {failed} selhalo")
    print("="*70 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
