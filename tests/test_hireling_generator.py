"""
Testy pro HirelingGenerator
"""
from src.generators.hireling import HirelingGenerator
from src.core.models import Hireling


def test_generate_name():
    """Test generování jména"""
    name = HirelingGenerator.generate_name()

    assert isinstance(name, str), "Jméno musí být string"
    assert len(name) > 0, "Jméno nesmí být prázdné"
    assert " " in name, "Jméno musí obsahovat mezeru (jméno + příjmení)"

    # Test že různé gendery fungují
    name_male = HirelingGenerator.generate_name("male")
    name_female = HirelingGenerator.generate_name("female")

    assert " " in name_male
    assert " " in name_female


def test_generate_name_multiple_times():
    """Test že generování jmen dává různé výsledky"""
    names = set()
    for _ in range(20):
        name = HirelingGenerator.generate_name()
        names.add(name)

    # Měli bychom dostat alespoň nějakou variaci
    assert len(names) > 1, "Všechna jména jsou stejná - možná problém s RNG"


def test_roll_stats():
    """Test hodu statistik"""
    hp, strength, dexterity, willpower = HirelingGenerator.roll_stats()

    # Ověř rozsahy hodnot
    assert 1 <= hp <= 6, f"HP musí být 1-6, je {hp}"
    assert 2 <= strength <= 12, f"Síla musí být 2-12, je {strength}"
    assert 2 <= dexterity <= 12, f"Mrštnost musí být 2-12, je {dexterity}"
    assert 2 <= willpower <= 12, f"Vůle musí být 2-12, je {willpower}"


def test_roll_stats_multiple_times():
    """Test že statistiky dávají různé výsledky"""
    results = set()
    for _ in range(20):
        stats = HirelingGenerator.roll_stats()
        results.add(stats)

    # Měli bychom dostat různé kombinace statistik
    assert len(results) > 5, "Statistiky jsou moc podobné - možná problém s RNG"


def test_select_hireling_type_specific():
    """Test výběru konkrétního typu pomocníka"""
    # Test Zbrojmyš (type 6)
    hireling_type = HirelingGenerator.select_hireling_type(6)

    assert isinstance(hireling_type, dict), "Typ musí být dictionary"
    assert hireling_type["id"] == 6
    assert hireling_type["name"] == "Zbrojmyš"
    assert "daily_wage" in hireling_type
    assert "available" in hireling_type


def test_select_hireling_type_random():
    """Test náhodného výběru typu"""
    hireling_type = HirelingGenerator.select_hireling_type(None)

    assert isinstance(hireling_type, dict), "Typ musí být dictionary"
    assert "id" in hireling_type
    assert "name" in hireling_type
    assert 1 <= hireling_type["id"] <= 9


def test_select_hireling_type_all_types():
    """Test že všech 9 typů funguje"""
    for type_id in range(1, 10):
        hireling_type = HirelingGenerator.select_hireling_type(type_id)

        assert hireling_type["id"] == type_id
        assert isinstance(hireling_type["name"], str)
        assert isinstance(hireling_type["daily_wage"], int)
        assert hireling_type["daily_wage"] > 0


def test_calculate_availability():
    """Test výpočtu dostupnosti"""
    # Test s k6
    hireling_type_k6 = {"available": "k6"}
    availability = HirelingGenerator.calculate_availability(hireling_type_k6)
    assert 1 <= availability <= 6, f"k6 dostupnost musí být 1-6, je {availability}"

    # Test s k4
    hireling_type_k4 = {"available": "k4"}
    availability = HirelingGenerator.calculate_availability(hireling_type_k4)
    assert 1 <= availability <= 4, f"k4 dostupnost musí být 1-4, je {availability}"

    # Test s k3
    hireling_type_k3 = {"available": "k3"}
    availability = HirelingGenerator.calculate_availability(hireling_type_k3)
    assert 1 <= availability <= 3, f"k3 dostupnost musí být 1-3, je {availability}"

    # Test s k2
    hireling_type_k2 = {"available": "k2"}
    availability = HirelingGenerator.calculate_availability(hireling_type_k2)
    assert 1 <= availability <= 2, f"k2 dostupnost musí být 1-2, je {availability}"


def test_create_hireling():
    """Test vytvoření kompletního pomocníka"""
    hireling, availability = HirelingGenerator.create()

    # Ověř že je to instance Hireling
    assert isinstance(hireling, Hireling), "Musí vrátit Hireling instanci"

    # Ověř všechna povinná pole
    assert hireling.name, "Jméno nesmí být prázdné"
    assert " " in hireling.name, "Jméno musí obsahovat jméno + příjmení"
    assert hireling.type, "Typ nesmí být prázdný"
    assert isinstance(hireling.daily_wage, int), "Mzda musí být číslo"
    assert hireling.daily_wage > 0, "Mzda musí být kladná"

    # Ověř statistiky
    assert 1 <= hireling.hp <= 6, "HP musí být 1-6"
    assert 2 <= hireling.strength <= 12, "Síla musí být 2-12"
    assert 2 <= hireling.dexterity <= 12, "Mrštnost musí být 2-12"
    assert 2 <= hireling.willpower <= 12, "Vůle musí být 2-12"

    # Ověř inventář
    assert isinstance(hireling.inventory, list), "Inventář musí být list"
    assert len(hireling.inventory) == 6, "Inventář musí mít 6 slotů"

    # Ověř level a XP
    assert hireling.level == 1, "Začíná na levelu 1"
    assert hireling.experience == 0, "Začíná s 0 XP"

    # Ověř morálku
    assert hireling.morale == "neutrální", "Začíná s neutrální morálkou"

    # Ověř dostupnost
    assert isinstance(availability, int), "Dostupnost musí být číslo"
    assert 1 <= availability <= 6, "Dostupnost musí být 1-6"


def test_create_with_custom_name():
    """Test s vlastním jménem"""
    hireling, _ = HirelingGenerator.create(name="Testovací Pomocník")

    assert hireling.name == "Testovací Pomocník"


def test_create_with_specific_type():
    """Test s konkrétním typem"""
    # Vytvoř Rytíře (type 8)
    hireling, _ = HirelingGenerator.create(type_id=8)

    assert hireling.type == "Rytíř"
    assert hireling.daily_wage == 25


def test_create_with_gender():
    """Test s pohlavím"""
    hireling_male, _ = HirelingGenerator.create(gender="male")
    hireling_female, _ = HirelingGenerator.create(gender="female")

    assert hireling_male.name
    assert hireling_female.name
    # Nemůžeme testovat přesný tvar, ale měly by být rozdílné (statisticky)


def test_create_multiple_hirelings():
    """Test že generování více pomocníků dává různé výsledky"""
    hirelings = []
    for _ in range(10):
        hireling, _ = HirelingGenerator.create()
        hirelings.append(hireling)

    # Ověř že nemají všichni stejné jméno
    names = {h.name for h in hirelings}
    assert len(names) > 1, "Všichni pomocníci mají stejné jméno"

    # Ověř že nemají všichni stejné statistiky
    stats = {(h.hp, h.strength, h.dexterity, h.willpower) for h in hirelings}
    assert len(stats) > 3, "Pomocníci mají moc podobné statistiky"


def test_to_dict():
    """Test konverze do dictionary"""
    hireling, _ = HirelingGenerator.create()
    data = HirelingGenerator.to_dict(hireling)

    assert isinstance(data, dict), "Musí vrátit dictionary"
    assert "name" in data
    assert "type" in data
    assert "daily_wage" in data
    assert "hp" in data
    assert "strength" in data
    assert "dexterity" in data
    assert "willpower" in data
    assert "inventory" in data
    assert "level" in data
    assert "experience" in data
    assert "morale" in data


def test_to_json():
    """Test konverze do JSON"""
    hireling, _ = HirelingGenerator.create()
    json_str = HirelingGenerator.to_json(hireling)

    assert isinstance(json_str, str), "Musí vrátit string"
    assert '"name":' in json_str
    assert '"type":' in json_str
    assert '"daily_wage":' in json_str
    assert '"hp":' in json_str

    # Ověř že je validní JSON
    import json
    data = json.loads(json_str)
    assert isinstance(data, dict)
    assert data["name"] == hireling.name
