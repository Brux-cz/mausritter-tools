#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script pro TableLoader - ověření že načítání JSON tabulek funguje správně
"""

import sys
from src.core.tables import TableLoader

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def test_origins():
    """Test načítání tabulky původů"""
    print("=== Test Origins Table ===")

    # Načti celou tabulku
    origins = TableLoader.get_origins()
    print(f"[OK] Nacteno {len(origins['origins'])} puvodu")
    print(f"  Metadata: {origins['metadata']['description']}")

    # Vyhledej konkrétní původ
    origin = TableLoader.lookup_origin(hp=3, pips=5)
    if origin:
        print(f"[OK] HP=3, Pips=5 -> Nalezen puvod")
        print(f"  Nazev: {origin['name']}")
        print(f"  Predmet A: {origin['item_a']}")
        print(f"  Predmet B: {origin['item_b']}")
    else:
        print("[FAIL] Puvod nenalezen")

    # Test rohu tabulky
    origin_corner = TableLoader.lookup_origin(hp=1, pips=1)
    if origin_corner:
        print(f"[OK] HP=1, Pips=1 -> {origin_corner['name']}")

    origin_corner2 = TableLoader.lookup_origin(hp=6, pips=6)
    if origin_corner2:
        print(f"[OK] HP=6, Pips=6 -> {origin_corner2['name']}")

    print()


def test_first_names():
    """Test načítání vlastních jmen"""
    print("=== Test First Names Table ===")

    names = TableLoader.get_first_names()
    print(f"[OK] Nacteno {len(names['names'])} jmen")
    print(f"  Dice: {names['metadata']['dice']}")

    # Testuj několik náhodných jmen
    test_rolls = [1, 50, 75, 100]
    for roll in test_rolls:
        name = TableLoader.lookup_first_name(roll)
        if name:
            print(f"[OK] Roll {roll:3d} -> {name}")
        else:
            print(f"[FAIL] Roll {roll:3d} -> nenalezeno")

    print()


def test_family_names():
    """Test načítání mateřských jmen"""
    print("=== Test Family Names Table ===")

    names = TableLoader.get_family_names()
    print(f"[OK] Nacteno {len(names['names'])} prijmeni")
    print(f"  Dice: {names['metadata']['dice']}")

    # Testuj několik příjmení v obou tvarech
    test_rolls = [1, 6, 13, 20]
    for roll in test_rolls:
        male = TableLoader.lookup_family_name(roll, "male")
        female = TableLoader.lookup_family_name(roll, "female")
        if male and female:
            print(f"[OK] Roll {roll:2d} -> {male} / {female}")
        else:
            print(f"[FAIL] Roll {roll:2d} -> nenalezeno")

    print()


def test_full_character_lookup():
    """Test kompletního vyhledání pro postavu"""
    print("=== Test Full Character Lookup ===")

    # Simuluj výsledky hodů
    hp, pips = 4, 3
    first_name_roll = 75
    family_name_roll = 6

    origin = TableLoader.lookup_origin(hp, pips)
    first_name = TableLoader.lookup_first_name(first_name_roll)
    family_name = TableLoader.lookup_family_name(family_name_roll, "male")

    print(f"Postava s HP={hp}, Pips={pips}:")
    print(f"  Jmeno: {first_name} {family_name}")
    print(f"  Puvod: {origin['name']}")
    print(f"  Vybava:")
    print(f"    - {origin['item_a']}")
    print(f"    - {origin['item_b']}")

    print()


def main():
    """Spusť všechny testy"""
    print("\n" + "="*60)
    print("TableLoader Test Suite")
    print("="*60 + "\n")

    try:
        test_origins()
        test_first_names()
        test_family_names()
        test_full_character_lookup()

        print("="*60)
        print("[OK] Vsechny testy probehly uspesne!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n[FAIL] Chyba pri testech: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
