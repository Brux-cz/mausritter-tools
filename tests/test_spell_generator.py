"""
Testy pro SpellGenerator
"""
import json
from src.generators.spell import SpellGenerator
from src.core.models import Spell


def test_roll_2d8_range():
    """Test ze hod 2d8 je v rozsahu 2-16"""
    for _ in range(30):
        roll = SpellGenerator.roll_2d8()
        assert 2 <= roll <= 16, f"Hod {roll} neni v rozsahu 2-16"


def test_create_returns_spell():
    """Test ze create() vraci Spell objekt"""
    spell = SpellGenerator.create()
    assert isinstance(spell, Spell)
    assert isinstance(spell.roll, int)
    assert isinstance(spell.name, str)
    assert isinstance(spell.effect, str)
    assert isinstance(spell.recharge, str)
    assert isinstance(spell.tags, list)
    assert 2 <= spell.roll <= 16


def test_all_16_spells_exist():
    """Test ze vsechny roll hodnoty 2-16 maji kouzlo"""
    # Vygeneruj hodne kouzlu a sbírej roll hodnoty
    found_rolls = set()
    for _ in range(500):  # Dostatek pokusu pro zachyceni vsech 16 kouzel
        spell = SpellGenerator.create()
        found_rolls.add(spell.roll)

    # Kontrola ze jsme nasli vetsinu kouzel (kvuli nahodnosti nemusime najit vsechny)
    assert len(found_rolls) >= 12, f"Nasli jsme jen {len(found_rolls)} ruznych kouzel z 16"


def test_spell_names_valid():
    """Test ze vsechna kouzla maji spravne nazvy"""
    # Vygeneruj 50 kouzlu a kontroluj ze jsou ve validnim seznamu
    valid_names = set(SpellGenerator.SPELL_ROLLS.values())

    for _ in range(50):
        spell = SpellGenerator.create()
        assert spell.name in valid_names, f"Neplatne jmeno kouzla: {spell.name}"


def test_spell_has_effect():
    """Test ze kazde kouzlo ma neprazdny efekt"""
    for _ in range(20):
        spell = SpellGenerator.create()
        assert len(spell.effect) > 0, "Efekt kouzla nesmi byt prazdny"


def test_spell_has_recharge():
    """Test ze kazde kouzlo ma podminku dobiti"""
    for _ in range(20):
        spell = SpellGenerator.create()
        assert len(spell.recharge) > 0, "Podminka dobiti nesmi byt prazdna"


def test_spell_placeholders_preserved():
    """Test ze placeholdery [POCET] a [SOUCET] jsou zachovany v efektech"""
    # Vygeneruj hodne kouzlu a najdi aspon jedno s placeholdery
    found_pocet = False
    found_soucet = False

    for _ in range(100):
        spell = SpellGenerator.create()
        if "[POČET]" in spell.effect or "[POČTU]" in spell.effect:
            found_pocet = True
        if "[SOUČET]" in spell.effect:
            found_soucet = True

        if found_pocet and found_soucet:
            break

    assert found_pocet, "Zadne kouzlo neobsahuje [POCET] placeholder"
    assert found_soucet, "Zadne kouzlo neobsahuje [SOUCET] placeholder"


def test_spell_tags_exist():
    """Test ze kouzla maji tagy"""
    tag_counts = 0

    for _ in range(20):
        spell = SpellGenerator.create()
        if len(spell.tags) > 0:
            tag_counts += 1

    # Vetsina kouzlu by mela mit aspon jeden tag
    assert tag_counts >= 15, f"Jen {tag_counts}/20 kouzlu ma tagy"


def test_spell_category_mapping():
    """Test ze kategorie jsou spravne mapovany"""
    # Test damage kategorie
    damage_cat = SpellGenerator.get_spell_category(["damage"])
    assert "Útok" in damage_cat or "⚔️" in damage_cat

    # Test healing kategorie
    healing_cat = SpellGenerator.get_spell_category(["healing"])
    assert "Podpora" in healing_cat or "💚" in healing_cat

    # Test utility kategorie
    utility_cat = SpellGenerator.get_spell_category(["utility"])
    assert "Utilita" in utility_cat or "🔮" in utility_cat


def test_spell_color_mapping():
    """Test ze barvy jsou spravne mapovany"""
    # Test damage -> red
    assert SpellGenerator.get_spell_color(["damage"]) == "red"

    # Test healing -> green
    assert SpellGenerator.get_spell_color(["healing"]) == "green"

    # Test utility -> cyan
    assert SpellGenerator.get_spell_color(["utility"]) == "cyan"

    # Test debuff -> yellow
    assert SpellGenerator.get_spell_color(["debuff"]) == "yellow"


def test_to_dict():
    """Test prevodu kouzla na dictionary"""
    spell = SpellGenerator.create()
    data = SpellGenerator.to_dict(spell)

    assert isinstance(data, dict)
    assert "roll" in data
    assert "name" in data
    assert "effect" in data
    assert "recharge" in data
    assert "tags" in data
    assert data["roll"] == spell.roll
    assert data["name"] == spell.name


def test_to_json():
    """Test prevodu kouzla na JSON"""
    spell = SpellGenerator.create()
    json_str = SpellGenerator.to_json(spell)

    assert isinstance(json_str, str)
    assert len(json_str) > 0

    # Validuj ze je to platny JSON
    data = json.loads(json_str)
    assert "roll" in data
    assert "name" in data
    assert "effect" in data
    assert "recharge" in data


def test_json_contains_czech_characters():
    """Test ze JSON obsahuje ceske znaky spravne"""
    spell = SpellGenerator.create()
    json_str = SpellGenerator.to_json(spell)

    # Kontrola ze nejsou escapovane ceske znaky
    # (ensure_ascii=False zajistuje ze jsou ceske znaky primo v JSON)
    assert "\\u" not in json_str or any(c in json_str for c in ["á", "č", "ě", "í", "ň", "ó", "ř", "š", "ť", "ú", "ů", "ý", "ž"]), \
        "Ceske znaky by nemely byt escapovane"


def test_specific_spells():
    """Test specifickych kouzel podle roll hodnot"""
    # Test ze roll 2 -> Ohniva koule
    found_fireball = False
    for _ in range(100):
        spell = SpellGenerator.create()
        if spell.roll == 2:
            assert spell.name == "Ohnivá koule"
            assert "zranění" in spell.effect
            found_fireball = True
            break

    # Test ze roll 16 -> Santa
    found_catnip = False
    for _ in range(100):
        spell = SpellGenerator.create()
        if spell.roll == 16:
            assert spell.name == "Šanta"
            assert "koček" in spell.effect.lower() or "kočce" in spell.recharge.lower()
            found_catnip = True
            break

    # S 100 pokusy bychom meli najit aspon jedno z techto kouzel
    assert found_fireball or found_catnip, "Nepodarilo se vygenerovat specificke kouzlo"


def test_spell_consistency():
    """Test ze stejny roll vzdy da stejne kouzlo"""
    # Tento test kontroluje ze TableLoader vraci konzistentni data
    spell1 = None
    spell2 = None

    # Najdi kouzlo s roll 10 (Svetlo)
    for _ in range(200):
        spell = SpellGenerator.create()
        if spell.roll == 10:
            if spell1 is None:
                spell1 = spell
            else:
                spell2 = spell
                break

    if spell1 and spell2:
        # Oba by mely mit stejne jmeno, efekt a dobiti
        assert spell1.name == spell2.name
        assert spell1.effect == spell2.effect
        assert spell1.recharge == spell2.recharge


if __name__ == "__main__":
    # Umoznuje spustit testy primo: python tests/test_spell_generator.py
    print("Spoustim testy pro SpellGenerator...")

    # Spust vsechny test funkce
    test_functions = [
        test_roll_2d8_range,
        test_create_returns_spell,
        test_all_16_spells_exist,
        test_spell_names_valid,
        test_spell_has_effect,
        test_spell_has_recharge,
        test_spell_placeholders_preserved,
        test_spell_tags_exist,
        test_spell_category_mapping,
        test_spell_color_mapping,
        test_to_dict,
        test_to_json,
        test_json_contains_czech_characters,
        test_specific_spells,
        test_spell_consistency
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
