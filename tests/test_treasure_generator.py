"""
Unit testy pro TreasureGenerator

Testuje generování pokladů podle oficiálních pravidel Mausritter.
"""

import sys
from pathlib import Path

# Přidej src do cesty
sys.path.insert(0, str(Path(__file__).parent.parent))

# Fix Windows console encoding for Czech characters
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from src.generators.treasure import TreasureGenerator
from src.core.models import TreasureHoard, TreasureItem, MagicSword, Spell
from src.core.tables import TableLoader


def test_treasure_generator_basic_creation():
    """Test: TreasureGenerator.create() vytvoří TreasureHoard"""
    hoard = TreasureGenerator.create()
    assert isinstance(hoard, TreasureHoard)
    print("[OK] TreasureGenerator.create() vrací TreasureHoard")


def test_treasure_base_rolls():
    """Test: Základní poklad má 2 položky (2× k20)"""
    hoard = TreasureGenerator.create(bonus_rolls=0)
    assert hoard.total_rolls == 2
    assert hoard.bonus_rolls == 0
    assert len(hoard.items) == 2
    print(f"[OK] Základní poklad má 2 položky: {len(hoard.items)}")


def test_treasure_bonus_rolls():
    """Test: Bonusové hody fungují správně (2-6 položek)"""
    for bonus in range(5):  # 0-4
        hoard = TreasureGenerator.create(bonus_rolls=bonus)
        expected_rolls = 2 + bonus
        assert hoard.total_rolls == expected_rolls
        assert hoard.bonus_rolls == bonus
        assert len(hoard.items) == expected_rolls
    print("[OK] Bonusové hody fungují pro 0-4 bonusů")


def test_treasure_invalid_bonus():
    """Test: Neplatné bonusové hody vyhodí ValueError"""
    try:
        TreasureGenerator.create(bonus_rolls=5)
        assert False, "Mělo vyhodit ValueError"
    except ValueError:
        pass

    try:
        TreasureGenerator.create(bonus_rolls=-1)
        assert False, "Mělo vyhodit ValueError"
    except ValueError:
        pass

    print("[OK] Neplatné bonusové hody vyhazují ValueError")


def test_treasure_items_are_treasure_item():
    """Test: Všechny položky jsou TreasureItem"""
    hoard = TreasureGenerator.create(bonus_rolls=2)
    for item in hoard.items:
        assert isinstance(item, TreasureItem)
    print(f"[OK] Všech {len(hoard.items)} položek je TreasureItem")


def test_treasure_total_value():
    """Test: Celková hodnota je součet prodejných položek"""
    hoard = TreasureGenerator.create(bonus_rolls=4)

    # Spočítej hodnotu ručně
    expected_value = sum(
        item.value for item in hoard.items
        if item.value is not None
    )

    assert hoard.total_value == expected_value
    print(f"[OK] Celková hodnota: {hoard.total_value} ď")


def test_treasure_types():
    """Test: Různé typy pokladů se generují"""
    possible_types = {
        "pips", "magic_sword", "spell",
        "trinket", "valuable", "bulky", "unusual", "useful",
        "supplies", "torches", "weapon", "armor", "tool", "hireling"
    }

    # Vygeneruj hodně pokladů a sleduj typy
    found_types = set()
    for _ in range(50):
        hoard = TreasureGenerator.create(bonus_rolls=4)
        for item in hoard.items:
            found_types.add(item.type)

    # Měli bychom najít minimálně 5 různých typů
    assert len(found_types) >= 5
    print(f"[OK] Nalezeno {len(found_types)} různých typů: {sorted(found_types)}")


def test_treasure_pips_values():
    """Test: Ďobky mají správné rozsahy hodnot"""
    # Vygeneruj hodně pokladů a sleduj ďobky
    pips_items = []
    for _ in range(100):
        hoard = TreasureGenerator.create(bonus_rolls=2)
        for item in hoard.items:
            if item.type == "pips":
                pips_items.append(item)

    # Měli bychom najít nějaké ďobky
    assert len(pips_items) > 0

    # Zkontroluj rozsahy
    for item in pips_items:
        assert item.value >= 5
        assert item.value <= 600
        assert item.value % 5 == 0  # Mělo by být dělitelné 5

    print(f"[OK] Ďobky mají správné rozsahy (5-600 ď, {len(pips_items)} vzorků)")


def test_treasure_magic_sword_structure():
    """Test: Kouzelný meč má správnou strukturu"""
    # Vygeneruj magic sword přímo
    magic_sword_item = TreasureGenerator._generate_magic_sword_item()

    assert magic_sword_item.type == "magic_sword"
    assert magic_sword_item.magic_sword is not None
    assert isinstance(magic_sword_item.magic_sword, MagicSword)
    assert magic_sword_item.magic_sword.weapon_type in ["Střední", "Lehká", "Těžká"]
    assert magic_sword_item.magic_sword.usage_dots == 3

    # Kletba je bool
    assert isinstance(magic_sword_item.magic_sword.cursed, bool)

    if magic_sword_item.magic_sword.cursed:
        assert magic_sword_item.magic_sword.curse is not None
        assert magic_sword_item.magic_sword.curse_lift is not None

    print(f"[OK] Kouzelný meč: {magic_sword_item.magic_sword.name} ({magic_sword_item.magic_sword.weapon_type})")
    if magic_sword_item.magic_sword.cursed:
        print(f"     PROKLETÝ!")


def test_treasure_spell_structure():
    """Test: Kouzlo má správnou strukturu"""
    spell_item = TreasureGenerator._generate_spell_item()

    assert spell_item.type == "spell"
    assert spell_item.spell is not None
    assert isinstance(spell_item.spell, Spell)
    assert spell_item.value >= 100
    assert spell_item.value <= 600
    assert spell_item.value % 100 == 0
    assert spell_item.usage_dots == 3

    print(f"[OK] Kouzlo: {spell_item.spell.name} (hodnota {spell_item.value} ď)")


def test_treasure_slots():
    """Test: Položky mají přiřazené políčka"""
    hoard = TreasureGenerator.create(bonus_rolls=4)

    for item in hoard.items:
        assert isinstance(item.slots, int)
        assert item.slots >= 0
        assert item.slots <= 10  # Rozumný maximum

    print(f"[OK] Všechny položky mají přiřazené políčka (0-10)")


def test_treasure_usage_dots():
    """Test: Tečky použití jsou správně nastavené"""
    hoard = TreasureGenerator.create(bonus_rolls=4)

    for item in hoard.items:
        assert isinstance(item.usage_dots, int)
        assert item.usage_dots >= 0

        # Kouzla a kouzelné meče by měly mít 3 tečky
        if item.type == "spell":
            assert item.usage_dots == 3
        elif item.type == "magic_sword":
            assert item.usage_dots == 3

    print(f"[OK] Tečky použití jsou správně nastavené")


def test_treasure_trinkets():
    """Test: Drobnosti existují a jsou správně načtené"""
    data = TableLoader.get_treasure_trinkets()
    trinkets = data.get("trinkets", [])

    assert len(trinkets) == 6
    for trinket in trinkets:
        assert "roll" in trinket
        assert "name" in trinket
        assert trinket["roll"] >= 1
        assert trinket["roll"] <= 6

    print(f"[OK] 6 drobností načteno z tabulky")


def test_treasure_valuable():
    """Test: Cenný poklad existuje a má správné ceny"""
    data = TableLoader.get_treasure_valuable()
    valuable = data.get("valuable", [])

    assert len(valuable) == 6
    for item in valuable:
        assert item["value"] >= 100
        assert item["value"] <= 1500

    print(f"[OK] 6 cenných pokladů s cenami 100-1500 ď")


def test_treasure_bulky():
    """Test: Objemný poklad zabírá více políček"""
    data = TableLoader.get_treasure_bulky()
    bulky = data.get("bulky", [])

    assert len(bulky) == 6
    for item in bulky:
        assert item["slots"] >= 2
        assert item["slots"] <= 6

    print(f"[OK] 6 objemných pokladů se 2-6 políčky")


def test_treasure_unusual():
    """Test: Neobvyklý poklad má kupce"""
    data = TableLoader.get_treasure_unusual()
    unusual = data.get("unusual", [])

    assert len(unusual) == 6
    for item in unusual:
        assert "buyer" in item
        # Někteří kupci jsou None nebo "různí"

    print(f"[OK] 6 neobvyklých pokladů s kupci")


def test_treasure_useful():
    """Test: Užitečný poklad má správné typy"""
    data = TableLoader.get_treasure_useful()
    useful = data.get("useful", [])

    assert len(useful) == 6

    types = [item["type"] for item in useful]
    expected_types = ["supplies", "torches", "weapon", "armor", "tool", "hireling"]

    for expected_type in expected_types:
        assert expected_type in types

    print(f"[OK] 6 užitečných pokladů se správnými typy")


def test_treasure_magic_swords_table():
    """Test: Tabulka kouzelných mečů má 10 položek"""
    data = TableLoader.get_magic_swords()
    swords = data.get("swords", [])

    assert len(swords) == 10
    for i, sword in enumerate(swords, 1):
        assert sword["roll"] == i
        assert "name" in sword
        assert "ability" in sword
        assert "trigger" in sword

    print(f"[OK] 10 kouzelných mečů v tabulce")


def test_treasure_magic_sword_types():
    """Test: Typy kouzelných mečů (k6)"""
    data = TableLoader.get_magic_sword_types()
    types = data.get("types", [])

    assert len(types) == 3  # Střední, Lehká, Těžká

    type_names = [t["type"] for t in types]
    assert "Střední" in type_names
    assert "Lehká" in type_names
    assert "Těžká" in type_names

    print(f"[OK] 3 typy kouzelných mečů")


def test_treasure_magic_sword_curses():
    """Test: Kletby kouzelných mečů (k6)"""
    data = TableLoader.get_magic_sword_curses()
    curses = data.get("curses", [])

    assert len(curses) == 6
    for curse in curses:
        assert "curse" in curse
        assert "lift_condition" in curse

    print(f"[OK] 6 kleteb pro kouzelné meče")


def test_treasure_tools():
    """Test: Nástroje (44 položek)"""
    data = TableLoader.get_tools()
    mouse_made = data.get("mouse_made", [])
    human_made = data.get("human_made", [])

    assert len(mouse_made) == 32
    assert len(human_made) == 12

    total = len(mouse_made) + len(human_made)
    assert total == 44

    print(f"[OK] 44 nástrojů (32 myších + 12 lidských)")


def test_treasure_armor():
    """Test: Zbroje (3 typy)"""
    data = TableLoader.get_armor()
    armor_types = data.get("armor_types", [])

    assert len(armor_types) == 3

    types = [a["type"] for a in armor_types]
    assert "Lehká zbroj" in types
    assert "Těžká zbroj" in types
    assert "Štít" in types

    print(f"[OK] 3 typy zbrojí")


def test_treasure_quantity():
    """Test: Množství u zásob a pochodní"""
    # Vygeneruj hodně pokladů a najdi supplies/torches
    supplies_items = []
    torches_items = []

    for _ in range(50):
        hoard = TreasureGenerator.create(bonus_rolls=4)
        for item in hoard.items:
            if item.type == "supplies":
                supplies_items.append(item)
            elif item.type == "torches":
                torches_items.append(item)

    # Pokud jsme našli nějaké, zkontroluj quantity
    for item in supplies_items + torches_items:
        assert item.quantity >= 1
        assert item.quantity <= 6

    print(f"[OK] Quantity u zásob ({len(supplies_items)}) a pochodní ({len(torches_items)}) je 1-6")


# === RUNNER ===

def run_all_tests():
    """Spusť všechny testy."""
    import inspect

    # Najdi všechny test funkce
    test_functions = [
        obj for name, obj in globals().items()
        if name.startswith("test_") and callable(obj)
    ]

    passed = 0
    failed = 0

    print("\n" + "=" * 70)
    print("TREASURE GENERATOR TESTS")
    print("=" * 70 + "\n")

    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test_func.__name__}: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"VÝSLEDKY: {passed} PASSED, {failed} FAILED ({len(test_functions)} celkem)")
    print("=" * 70 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
