"""
Testy pro NPCGenerator
"""
from src.generators.npc import NPCGenerator
from src.core.models import NPC


def test_generate_name():
    """Test generování jména"""
    name = NPCGenerator.generate_name()

    assert isinstance(name, str), "Jméno musí být string"
    assert len(name) > 0, "Jméno nesmí být prázdné"
    assert " " in name, "Jméno musí obsahovat mezeru (jméno + příjmení)"

    # Test že různé gendery fungují
    name_male = NPCGenerator.generate_name("male")
    name_female = NPCGenerator.generate_name("female")

    assert " " in name_male
    assert " " in name_female


def test_generate_name_multiple_times():
    """Test že generování jmen dává různé výsledky"""
    names = set()
    for _ in range(20):
        name = NPCGenerator.generate_name()
        names.add(name)

    # Měli bychom dostat alespoň nějakou variaci (ne všechny stejné)
    assert len(names) > 1, "Všechna jména jsou stejná - možná problém s RNG"


def test_generate_social_status():
    """Test generování společenského postavení"""
    status, payment = NPCGenerator.generate_social_status()

    assert isinstance(status, str), "Status musí být string"
    assert isinstance(payment, str), "Platba musí být string"
    assert len(status) > 0, "Status nesmí být prázdný"
    assert len(payment) > 0, "Platba nesmí být prázdná"
    assert "ď" in payment, "Platba musí obsahovat 'ď' (ďobky)"


def test_generate_social_status_multiple_times():
    """Test že generování statusu dává různé výsledky"""
    statuses = set()
    for _ in range(20):
        status, payment = NPCGenerator.generate_social_status()
        statuses.add(status)

    # Měli bychom dostat variaci (máme 6 možností, ale 2-3 jsou Prostá myš)
    assert len(statuses) > 1, "Všechny statusy jsou stejné - možná problém s RNG"


def test_generate_birthsign():
    """Test generování rodného znamení"""
    birthsign = NPCGenerator.generate_birthsign()

    assert isinstance(birthsign, str), "Rodné znamení musí být string"
    assert len(birthsign) > 0, "Rodné znamení nesmí být prázdné"
    assert "(" in birthsign and ")" in birthsign, "Rodné znamení musí obsahovat jméno a povahu"


def test_generate_birthsign_multiple_times():
    """Test že generování rodných znamení dává různé výsledky"""
    birthsigns = set()
    for _ in range(20):
        birthsign = NPCGenerator.generate_birthsign()
        birthsigns.add(birthsign)

    # Měli bychom dostat alespoň nějakou variaci (máme 6 možností)
    assert len(birthsigns) > 1, "Všechna znamení jsou stejná - možná problém s RNG"


def test_generate_appearance():
    """Test generování vzhledu"""
    appearance = NPCGenerator.generate_appearance()

    assert isinstance(appearance, str), "Vzhled musí být string"
    assert len(appearance) > 0, "Vzhled nesmí být prázdný"


def test_generate_appearance_multiple_times():
    """Test že generování vzhledu dává různé výsledky"""
    appearances = set()
    for _ in range(30):
        appearance = NPCGenerator.generate_appearance()
        appearances.add(appearance)

    # Měli bychom dostat variaci (máme 20 možností)
    assert len(appearances) > 1, "Všechny vzhledem jsou stejné - možná problém s RNG"


def test_generate_quirk():
    """Test generování zvláštnosti"""
    quirk = NPCGenerator.generate_quirk()

    assert isinstance(quirk, str), "Zvláštnost musí být string"
    assert len(quirk) > 0, "Zvláštnost nesmí být prázdná"


def test_generate_quirk_multiple_times():
    """Test že generování zvláštností dává různé výsledky"""
    quirks = set()
    for _ in range(30):
        quirk = NPCGenerator.generate_quirk()
        quirks.add(quirk)

    # Měli bychom dostat variaci (máme 20 možností)
    assert len(quirks) > 1, "Všechny zvláštnosti jsou stejné - možná problém s RNG"


def test_generate_desire():
    """Test generování tužby"""
    desire = NPCGenerator.generate_desire()

    assert isinstance(desire, str), "Tužba musí být string"
    assert len(desire) > 0, "Tužba nesmí být prázdná"


def test_generate_desire_multiple_times():
    """Test že generování tužeb dává různé výsledky"""
    desires = set()
    for _ in range(30):
        desire = NPCGenerator.generate_desire()
        desires.add(desire)

    # Měli bychom dostat variaci (máme 20 možností)
    assert len(desires) > 1, "Všechny tužby jsou stejné - možná problém s RNG"


def test_generate_relationship():
    """Test generování vztahu"""
    relationship = NPCGenerator.generate_relationship()

    assert isinstance(relationship, str), "Vztah musí být string"
    assert len(relationship) > 0, "Vztah nesmí být prázdný"


def test_generate_relationship_multiple_times():
    """Test že generování vztahů dává různé výsledky"""
    relationships = set()
    for _ in range(30):
        relationship = NPCGenerator.generate_relationship()
        relationships.add(relationship)

    # Měli bychom dostat variaci (máme 20 možností)
    assert len(relationships) > 1, "Všechny vztahy jsou stejné - možná problém s RNG"


def test_generate_reaction():
    """Test generování reakce"""
    reaction = NPCGenerator.generate_reaction()

    assert isinstance(reaction, str), "Reakce musí být string"
    assert len(reaction) > 0, "Reakce nesmí být prázdná"
    assert ":" in reaction, "Reakce musí obsahovat ':' (odděluje reakci a otázku)"


def test_generate_reaction_multiple_times():
    """Test že generování reakcí dává různé výsledky"""
    reactions = set()
    for _ in range(30):
        reaction = NPCGenerator.generate_reaction()
        reactions.add(reaction)

    # Měli bychom dostat variaci (máme 5 možností na 2k6)
    assert len(reactions) > 1, "Všechny reakce jsou stejné - možná problém s RNG"


def test_create_npc():
    """Test kompletní generování NPC"""
    npc = NPCGenerator.create()

    # Ověř že je to NPC instance
    assert isinstance(npc, NPC), "Musí vrátit NPC instanci"

    # Ověř všechna povinná pole
    assert npc.name, "NPC musí mít jméno"
    assert " " in npc.name, "Jméno musí obsahovat mezeru (jméno + příjmení)"

    assert npc.social_status, "NPC musí mít společenské postavení"
    assert isinstance(npc.social_status, str), "Status musí být string"

    assert npc.birthsign, "NPC musí mít rodné znamení"
    assert isinstance(npc.birthsign, str), "Rodné znamení musí být string"
    assert "(" in npc.birthsign, "Rodné znamení musí obsahovat povahu"

    assert npc.appearance, "NPC musí mít vzhled"
    assert isinstance(npc.appearance, str), "Vzhled musí být string"

    assert npc.quirk, "NPC musí mít zvláštnost"
    assert isinstance(npc.quirk, str), "Zvláštnost musí být string"

    assert npc.desire, "NPC musí mít tužbu"
    assert isinstance(npc.desire, str), "Tužba musí být string"

    assert npc.relationship, "NPC musí mít vztah"
    assert isinstance(npc.relationship, str), "Vztah musí být string"

    assert npc.reaction, "NPC musí mít reakci"
    assert isinstance(npc.reaction, str), "Reakce musí být string"
    assert ":" in npc.reaction, "Reakce musí obsahovat oddělení reakce a otázky"

    # Ověř volitelná pole
    assert npc.payment is not None, "NPC musí mít platbu"
    assert isinstance(npc.payment, str), "Platba musí být string"

    assert isinstance(npc.notes, str), "Poznámky musí být string (může být prázdný)"


def test_create_with_custom_name():
    """Test s vlastním jménem"""
    custom_name = "Testovací NPC"
    npc = NPCGenerator.create(name=custom_name)

    assert npc.name == custom_name, f"Očekáváno '{custom_name}', ale je '{npc.name}'"
    assert npc.social_status, "NPC musí mít status i s vlastním jménem"


def test_create_with_gender():
    """Test generování s různými gendery"""
    npc_male = NPCGenerator.create(gender="male")
    npc_female = NPCGenerator.create(gender="female")

    # Obě NPC musí být validní
    assert npc_male.name
    assert npc_female.name
    assert " " in npc_male.name
    assert " " in npc_female.name


def test_to_dict():
    """Test konverze do dictionary"""
    npc = NPCGenerator.create(name="Test NPC")
    npc_dict = NPCGenerator.to_dict(npc)

    assert isinstance(npc_dict, dict), "to_dict() musí vrátit dictionary"
    assert "name" in npc_dict
    assert "social_status" in npc_dict
    assert "birthsign" in npc_dict
    assert "appearance" in npc_dict
    assert "quirk" in npc_dict
    assert "desire" in npc_dict
    assert "relationship" in npc_dict
    assert "reaction" in npc_dict
    assert npc_dict["name"] == "Test NPC"


def test_to_json():
    """Test konverze do JSON"""
    npc = NPCGenerator.create(name="JSON Test NPC")
    json_str = NPCGenerator.to_json(npc)

    assert isinstance(json_str, str), "to_json() musí vrátit string"
    assert len(json_str) > 0, "JSON string nesmí být prázdný"
    assert "JSON Test NPC" in json_str, "JSON musí obsahovat jméno NPC"
    assert '"social_status":' in json_str or '"social_status": ' in json_str

    # Ověř že je to validní JSON
    import json
    parsed = json.loads(json_str)
    assert parsed["name"] == "JSON Test NPC"


def test_create_multiple_npcs():
    """Test že můžeme vytvořit více různých NPC"""
    npcs = []
    for _ in range(5):
        npc = NPCGenerator.create()
        npcs.append(npc)

    # Všechny NPC musí být validní
    for npc in npcs:
        assert npc.name
        assert npc.social_status
        assert npc.birthsign
        assert npc.appearance

    # NPC by měly být různé (alespoň v některých atributech)
    names = [n.name for n in npcs]
    assert len(set(names)) > 1, "Všechny NPC mají stejné jméno"

    # Zkontroluj variabilitu v dalších atributech
    desires = [n.desire for n in npcs]
    quirks = [n.quirk for n in npcs]

    # Alespoň jeden atribut by měl být různý
    assert len(set(names)) > 1 or len(set(desires)) > 1 or len(set(quirks)) > 1, \
        "Všechny NPC jsou identické - možná problém s RNG"
