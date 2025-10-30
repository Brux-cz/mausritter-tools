"""
Testy pro CharacterGenerator
"""
from src.generators.character import CharacterGenerator
from src.core.models import Character


def test_roll_attributes():
    """Test že vlastnosti jsou v rozsahu 2-12"""
    strength, dexterity, willpower = CharacterGenerator.roll_attributes()

    # Každá vlastnost musí být v rozsahu 2-12 (3k6 keep 2)
    assert 2 <= strength <= 12, f"Síla mimo rozsah: {strength}"
    assert 2 <= dexterity <= 12, f"Mrštnost mimo rozsah: {dexterity}"
    assert 2 <= willpower <= 12, f"Vůle mimo rozsah: {willpower}"


def test_roll_attributes_multiple_times():
    """Test že generování vlastností funguje opakovaně"""
    results = []
    for _ in range(10):
        str, dex, wil = CharacterGenerator.roll_attributes()
        results.append((str, dex, wil))
        # Ověř že všechny jsou validní
        assert 2 <= str <= 12
        assert 2 <= dex <= 12
        assert 2 <= wil <= 12

    # Ověř že výsledky nejsou všechny stejné (pravděpodobnost je mizivá)
    assert len(set(results)) > 1, "Všechny hody jsou stejné - možná problém s RNG"


def test_determine_origin():
    """Test lookup v origins table"""
    # Test známých původů
    origin = CharacterGenerator.determine_origin(hp=1, pips=1)
    assert origin is not None, "Původ pro HP=1, Pips=1 nenalezen"
    assert origin["name"] == "Pokusná myš"
    assert "item_a" in origin
    assert "item_b" in origin

    # Test dalšího známého původu
    origin2 = CharacterGenerator.determine_origin(hp=3, pips=5)
    assert origin2 is not None
    assert origin2["name"] == "Stěnolezec"

    # Test rohů tabulky
    origin_corner1 = CharacterGenerator.determine_origin(hp=6, pips=6)
    assert origin_corner1 is not None
    assert origin_corner1["name"] == "Zchudlý šlechtic"


def test_determine_origin_invalid():
    """Test že nevalidní kombinace vrátí None"""
    origin = CharacterGenerator.determine_origin(hp=0, pips=1)
    assert origin is None, "Mělo vrátit None pro nevalidní HP=0"

    origin = CharacterGenerator.determine_origin(hp=7, pips=1)
    assert origin is None, "Mělo vrátit None pro HP=7 (mimo rozsah)"


def test_generate_name():
    """Test generování jména"""
    name = CharacterGenerator.generate_name()

    assert isinstance(name, str), "Jméno musí být string"
    assert len(name) > 0, "Jméno nesmí být prázdné"
    assert " " in name, "Jméno musí obsahovat mezeru (jméno + příjmení)"

    # Test že různé gendery fungují
    name_male = CharacterGenerator.generate_name("male")
    name_female = CharacterGenerator.generate_name("female")

    assert " " in name_male
    assert " " in name_female


def test_generate_name_multiple_times():
    """Test že generování jmen dává různé výsledky"""
    names = set()
    for _ in range(20):
        name = CharacterGenerator.generate_name()
        names.add(name)

    # Měli bychom dostat alespoň nějakou variaci (ne všechny stejné)
    assert len(names) > 1, "Všechna jména jsou stejná - možná problém s RNG"


def test_generate_birthsign():
    """Test generování rodného znamení"""
    birthsign = CharacterGenerator.generate_birthsign()

    assert isinstance(birthsign, dict), "Rodné znamení musí být dictionary"
    assert "name" in birthsign, "Rodné znamení musí mít 'name'"
    assert "trait" in birthsign, "Rodné znamení musí mít 'trait'"
    assert isinstance(birthsign["name"], str), "Jméno znamení musí být string"
    assert isinstance(birthsign["trait"], str), "Povaha musí být string"
    assert len(birthsign["name"]) > 0, "Jméno znamení nesmí být prázdné"
    assert len(birthsign["trait"]) > 0, "Povaha nesmí být prázdná"


def test_generate_birthsign_multiple_times():
    """Test že generování rodných znamení dává různé výsledky"""
    birthsigns = set()
    for _ in range(20):
        birthsign = CharacterGenerator.generate_birthsign()
        birthsigns.add(birthsign["name"])

    # Měli bychom dostat alespoň nějakou variaci (máme 6 možností)
    assert len(birthsigns) > 1, "Všechna znamení jsou stejná - možná problém s RNG"


def test_generate_coat():
    """Test generování barvy a vzoru srsti"""
    coat = CharacterGenerator.generate_coat()

    assert isinstance(coat, str), "Srst musí být string"
    assert len(coat) > 0, "Srst nesmí být prázdná"
    assert " " in coat, "Srst musí obsahovat mezeru (barva + vzor)"

    # Test že jsou dvě části (barva a vzor)
    parts = coat.split()
    assert len(parts) >= 2, f"Srst musí mít alespoň 2 části, má: {parts}"


def test_generate_coat_multiple_times():
    """Test že generování srsti dává různé výsledky"""
    coats = set()
    for _ in range(20):
        coat = CharacterGenerator.generate_coat()
        coats.add(coat)

    # Měli bychom dostat variaci (máme 6 barev × 6 vzorů = 36 kombinací)
    assert len(coats) > 1, "Všechny srsti jsou stejné - možná problém s RNG"


def test_generate_distinctive_trait():
    """Test generování výrazného rysu"""
    trait = CharacterGenerator.generate_distinctive_trait()

    assert isinstance(trait, str), "Výrazný rys musí být string"
    assert len(trait) > 0, "Výrazný rys nesmí být prázdný"


def test_generate_distinctive_trait_multiple_times():
    """Test že generování výrazných rysů dává různé výsledky"""
    traits = set()
    for _ in range(30):
        trait = CharacterGenerator.generate_distinctive_trait()
        traits.add(trait)

    # Měli bychom dostat variaci (máme 36 možností)
    assert len(traits) > 1, "Všechny výrazné rysy jsou stejné - možná problém s RNG"


def test_select_weapon():
    """Test výběru zbraně"""
    weapon = CharacterGenerator.select_weapon()

    assert isinstance(weapon, str), "Zbraň musí být string"
    assert len(weapon) > 0, "Zbraň nesmí být prázdná"
    assert "(" in weapon and ")" in weapon, "Zbraň musí obsahovat název a příklady"


def test_select_weapon_specific():
    """Test výběru konkrétní zbraně podle ID"""
    # Test ID 1 = Improvizovaná zbraň
    weapon1 = CharacterGenerator.select_weapon(weapon_id=1)
    assert "Improvizovaná" in weapon1, "ID 1 musí být Improvizovaná zbraň"

    # Test ID 2 = Lehká zbraň
    weapon2 = CharacterGenerator.select_weapon(weapon_id=2)
    assert "Lehká zbraň" in weapon2, "ID 2 musí být Lehká zbraň"


def test_select_weapon_multiple_times():
    """Test že výběr zbraně dává různé výsledky"""
    weapons = set()
    for _ in range(20):
        weapon = CharacterGenerator.select_weapon()
        weapons.add(weapon)

    # Měli bychom dostat variaci (máme 6 typů)
    assert len(weapons) > 1, "Všechny zbraně jsou stejné - možná problém s RNG"


def test_create_character():
    """Test kompletní generování postavy"""
    char = CharacterGenerator.create()

    # Ověř že je to Character instance
    assert isinstance(char, Character), "Musí vrátit Character instanci"

    # Ověř základní atributy
    assert char.name, "Postava musí mít jméno"
    assert char.background, "Postava musí mít původ"

    # Ověř vlastnosti
    assert 2 <= char.strength <= 12, f"Síla mimo rozsah: {char.strength}"
    assert 2 <= char.dexterity <= 12, f"Mrštnost mimo rozsah: {char.dexterity}"
    assert 2 <= char.willpower <= 12, f"Vůle mimo rozsah: {char.willpower}"

    # Ověř HP
    assert 1 <= char.max_hp <= 6, f"HP mimo rozsah: {char.max_hp}"
    assert char.current_hp == char.max_hp, "Current HP musí být stejné jako max HP"

    # Ověř inventář
    assert isinstance(char.inventory, list), "Inventář musí být list"
    assert len(char.inventory) == 10, "Inventář musí mít 10 slotů"

    # Ověř počáteční výbavu
    assert char.inventory[0] is not None, "Slot 1 musí obsahovat Pochodně"
    assert char.inventory[1] is not None, "Slot 2 musí obsahovat Zásoby"
    assert char.inventory[2] is not None, "Slot 3 musí obsahovat item_a z původu"
    assert char.inventory[3] is not None, "Slot 4 musí obsahovat item_b z původu"
    assert char.inventory[4] is not None, "Slot 5 musí obsahovat zbraň"

    # Ověř rodné znamení a srst
    assert char.birthsign, "Postava musí mít rodné znamení"
    assert isinstance(char.birthsign, str), "Rodné znamení musí být string"
    assert "(" in char.birthsign and ")" in char.birthsign, "Rodné znamení musí obsahovat jméno a povahu"

    assert char.coat, "Postava musí mít srst"
    assert isinstance(char.coat, str), "Srst musí být string"
    assert " " in char.coat, "Srst musí obsahovat barvu a vzor"

    # Ověř výrazný rys (appearance)
    assert char.appearance, "Postava musí mít výrazný rys"
    assert isinstance(char.appearance, str), "Výrazný rys musí být string"


def test_create_with_custom_name():
    """Test s vlastním jménem"""
    custom_name = "Testovací Myš"
    char = CharacterGenerator.create(name=custom_name)

    assert char.name == custom_name, f"Očekáváno '{custom_name}', ale je '{char.name}'"
    assert char.background, "Postava musí mít původ i s vlastním jménem"


def test_create_with_gender():
    """Test generování s různými gendery"""
    char_male = CharacterGenerator.create(gender="male")
    char_female = CharacterGenerator.create(gender="female")

    # Obě postavy musí být validní
    assert char_male.name
    assert char_female.name
    assert " " in char_male.name
    assert " " in char_female.name


def test_to_dict():
    """Test konverze do dictionary"""
    char = CharacterGenerator.create(name="Test Myš")
    char_dict = CharacterGenerator.to_dict(char)

    assert isinstance(char_dict, dict), "to_dict() musí vrátit dictionary"
    assert "name" in char_dict
    assert "strength" in char_dict
    assert "dexterity" in char_dict
    assert "willpower" in char_dict
    assert char_dict["name"] == "Test Myš"


def test_to_json():
    """Test konverze do JSON"""
    char = CharacterGenerator.create(name="JSON Test")
    json_str = CharacterGenerator.to_json(char)

    assert isinstance(json_str, str), "to_json() musí vrátit string"
    assert len(json_str) > 0, "JSON string nesmí být prázdný"
    assert "JSON Test" in json_str, "JSON musí obsahovat jméno postavy"
    assert '"strength":' in json_str or '"strength": ' in json_str

    # Ověř že je to validní JSON
    import json
    parsed = json.loads(json_str)
    assert parsed["name"] == "JSON Test"


def test_create_multiple_characters():
    """Test že můžeme vytvořit více různých postav"""
    characters = []
    for _ in range(5):
        char = CharacterGenerator.create()
        characters.append(char)

    # Všechny postavy musí být validní
    for char in characters:
        assert char.name
        assert 2 <= char.strength <= 12
        assert 1 <= char.max_hp <= 6

    # Postavy by měly být různé (alespoň v některých atributech)
    names = [c.name for c in characters]
    assert len(set(names)) > 1, "Všechny postavy mají stejné jméno"
