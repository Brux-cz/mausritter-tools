# -*- coding: utf-8 -*-
"""
Testy pro AdventureSeedGenerator
"""
from src.generators.adventure import AdventureSeedGenerator
from src.core.models import AdventureSeed


def test_create_basic():
    """Test základního generování semínka dobrodružství"""
    seed = AdventureSeedGenerator.create()

    assert isinstance(seed, AdventureSeed), "Výsledek musí být AdventureSeed"
    assert isinstance(seed.creature, str), "Tvor musí být string"
    assert isinstance(seed.problem, str), "Problém musí být string"
    assert isinstance(seed.complication, str), "Komplikace musí být string"
    assert len(seed.creature) > 0, "Tvor nesmí být prázdný"
    assert len(seed.problem) > 0, "Problém nesmí být prázdný"
    assert len(seed.complication) > 0, "Komplikace nesmí být prázdná"
    assert 11 <= seed.roll <= 66, f"Roll musí být 11-66, dostal {seed.roll}"


def test_create_custom():
    """Test custom kombinace semínka"""
    seed = AdventureSeedGenerator.create_custom()

    assert isinstance(seed, AdventureSeed)
    assert seed.roll == 0, "Custom kombinace má roll=0"
    assert isinstance(seed.creature, str)
    assert isinstance(seed.problem, str)
    assert isinstance(seed.complication, str)
    assert "Custom kombinace" in seed.notes


def test_create_with_specific_roll():
    """Test generování s konkrétním hodem k66"""
    # Test hodu 11 (první řádek tabulky)
    seed = AdventureSeedGenerator.create(roll=11)

    assert seed.roll == 11
    assert seed.creature == "Rybář"
    assert seed.problem == "Obviněn ze zločinu"
    assert seed.complication == "Může za to pomocník hráčské myši"


def test_create_with_roll_16():
    """Test konkrétního hodu k66 = 16"""
    seed = AdventureSeedGenerator.create(roll=16)

    assert seed.roll == 16
    assert seed.creature == "Purkmyšstr"
    assert seed.problem == "Chce nechat zavraždit soka"
    assert seed.complication == "Věc se týká domova hráčské myši"


def test_create_with_roll_22():
    """Test konkrétního hodu k66 = 22"""
    seed = AdventureSeedGenerator.create(roll=22)

    assert seed.roll == 22
    assert seed.creature == "Majitel obchodu"
    assert seed.problem == "Zničený domov"
    assert seed.complication == "Protivníkem je blízký přítel"


def test_create_with_roll_33():
    """Test konkrétního hodu k66 = 33"""
    seed = AdventureSeedGenerator.create(roll=33)

    assert seed.roll == 33
    assert seed.creature == "Pokusná myš"
    assert seed.problem == "Je na útěku před lidmi"
    assert seed.complication == "Sledují ho pomocí čipu"


def test_create_with_roll_44():
    """Test konkrétního hodu k66 = 44"""
    seed = AdventureSeedGenerator.create(roll=44)

    assert seed.roll == 44
    assert seed.creature == "Šéf cechu tunelářů"
    assert seed.problem == "Byl zavražděn"
    assert seed.complication == "Týká se to protivníka hráčské myši"


def test_create_with_roll_55():
    """Test konkrétního hodu k66 = 55"""
    seed = AdventureSeedGenerator.create(roll=55)

    assert seed.roll == 55
    assert seed.creature == "Káčátko"
    assert seed.problem == "Ztratilo maminku"
    assert seed.complication == "Potřebuje se dostat na ostrov"


def test_create_with_roll_66():
    """Test konkrétního hodu k66 = 66 (poslední řádek)"""
    seed = AdventureSeedGenerator.create(roll=66)

    assert seed.roll == 66
    assert seed.creature == "Ptáčátko"
    assert seed.problem == "Nemůže se dostat domů"
    assert seed.complication == "Potřebuje vylézt na strom"


def test_create_custom_with_specific_rolls():
    """Test custom kombinace s konkrétními hody"""
    seed = AdventureSeedGenerator.create_custom(
        creature_roll=11,
        problem_roll=22,
        complication_roll=33
    )

    assert seed.roll == 0
    assert seed.creature == "Rybář"
    assert seed.problem == "Zničený domov"
    assert seed.complication == "Sledují ho pomocí čipu"
    assert "11/22/33" in seed.notes


def test_to_dict():
    """Test konverze do dictionary"""
    seed = AdventureSeedGenerator.create(roll=11)
    data = AdventureSeedGenerator.to_dict(seed)

    assert isinstance(data, dict)
    assert "roll" in data
    assert "creature" in data
    assert "problem" in data
    assert "complication" in data
    assert "notes" in data
    assert data["roll"] == 11
    assert data["creature"] == "Rybář"


def test_to_json():
    """Test konverze do JSON"""
    seed = AdventureSeedGenerator.create(roll=22)
    json_str = AdventureSeedGenerator.to_json(seed)

    assert isinstance(json_str, str)
    assert '"roll": 22' in json_str
    assert '"creature"' in json_str
    assert '"problem"' in json_str
    assert '"complication"' in json_str
    assert "Majitel obchodu" in json_str


def test_to_json_custom_indent():
    """Test JSON s vlastním odsazením"""
    seed = AdventureSeedGenerator.create(roll=33)
    json_str = AdventureSeedGenerator.to_json(seed, indent=4)

    assert isinstance(json_str, str)
    assert "    " in json_str  # 4 mezery odsazení
    assert "Pokusná myš" in json_str


def test_format_text():
    """Test formátování jako text"""
    seed = AdventureSeedGenerator.create(roll=44)
    text = AdventureSeedGenerator.format_text(seed)

    assert isinstance(text, str)
    assert "SEMÍNKO DOBRODRUŽSTVÍ" in text
    assert "Tvor:" in text
    assert "Problém:" in text
    assert "Komplikace:" in text
    assert "Šéf cechu tunelářů" in text
    assert "Byl zavražděn" in text
    assert "Týká se to protivníka hráčské myši" in text
    assert "Hod k66: 44" in text


def test_format_text_custom():
    """Test formátování custom kombinace"""
    seed = AdventureSeedGenerator.create_custom(
        creature_roll=11,
        problem_roll=22,
        complication_roll=33
    )
    text = AdventureSeedGenerator.format_text(seed)

    assert isinstance(text, str)
    assert "Custom kombinace" in text
    assert "Rybář" in text
    assert "Zničený domov" in text
    assert "Sledují ho pomocí čipu" in text


def test_get_inspiration_text():
    """Test generování inspiračního textu pro GM"""
    seed = AdventureSeedGenerator.create(roll=55)
    inspiration = AdventureSeedGenerator.get_inspiration_text(seed)

    assert isinstance(inspiration, str)
    assert "INSPIRACE PRO GM" in inspiration
    assert "KDO:" in inspiration
    assert "CO:" in inspiration
    assert "JAK:" in inspiration
    assert "Káčátko" in inspiration
    assert "Ztratilo maminku" in inspiration
    assert "Potřebuje se dostat na ostrov" in inspiration
    assert "OTÁZKY K ROZVÍJENÍ" in inspiration
    assert "Kde se hráčské myši s tímto setkají?" in inspiration


def test_all_36_seeds_valid():
    """Test všech 36 semínek z tabulky (kompletní pokrytí)"""
    valid_rolls = []

    # Vygeneruj všechny k66 kombinace (11-66)
    for tens in range(1, 7):
        for ones in range(1, 7):
            roll = tens * 10 + ones
            valid_rolls.append(roll)

    assert len(valid_rolls) == 36, "Musí být 36 kombinací k66"

    # Ověř, že všechny fungují
    for roll in valid_rolls:
        seed = AdventureSeedGenerator.create(roll=roll)
        assert isinstance(seed, AdventureSeed)
        assert seed.roll == roll
        assert len(seed.creature) > 0
        assert len(seed.problem) > 0
        assert len(seed.complication) > 0


def test_multiple_random_generations():
    """Test, že náhodné generování funguje opakovaně"""
    seeds = [AdventureSeedGenerator.create() for _ in range(10)]

    # Všechny musí být validní
    for seed in seeds:
        assert isinstance(seed, AdventureSeed)
        assert 11 <= seed.roll <= 66
        assert len(seed.creature) > 0
        assert len(seed.problem) > 0
        assert len(seed.complication) > 0


def test_custom_without_parameters():
    """Test custom generování bez parametrů (náhodné)"""
    seed = AdventureSeedGenerator.create_custom()

    assert isinstance(seed, AdventureSeed)
    assert seed.roll == 0
    assert len(seed.creature) > 0
    assert len(seed.problem) > 0
    assert len(seed.complication) > 0


def test_unicode_czech_characters():
    """Test, že české znaky fungují správně"""
    seed = AdventureSeedGenerator.create(roll=11)

    # Ověř, že české znaky jsou správně uloženy
    assert "ř" in seed.creature  # Rybář
    assert "č" in seed.problem or "č" in seed.complication

    # JSON musí obsahovat české znaky
    json_str = AdventureSeedGenerator.to_json(seed)
    assert "Rybář" in json_str
    assert "\\u" not in json_str  # ensure_ascii=False
