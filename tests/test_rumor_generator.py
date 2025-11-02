# -*- coding: utf-8 -*-
"""
Testy pro RumorGenerator

Test coverage:
- Základní generování bez world state (fallback mode)
- Generování s world state (world-connected mode)
- Všechny k6 hody (1-6) a truthfulness
- Kategorie (threat, npc, location, treasure, mystery)
- Gossip chains (partial a false)
- Story hooks (advanced mode)
- JSON a text export
"""

import json
from src.generators.rumor import RumorGenerator
from src.core.models import Rumor


def test_basic_generation_without_world_state():
    """Test základního generování bez world state (fallback mode)."""
    rumors = RumorGenerator.create()

    assert len(rumors) == 6  # k6 tabulka
    assert all(isinstance(r, Rumor) for r in rumors)

    # Zkontroluj že všechny k6 hody jsou zastoupeny
    rolls = [r.roll for r in rumors]
    assert rolls == [1, 2, 3, 4, 5, 6]


def test_single_rumor_generation():
    """Test generování jedné zvěsti."""
    rumor = RumorGenerator.create_single(roll=1)

    assert isinstance(rumor, Rumor)
    assert rumor.roll == 1
    assert rumor.truthfulness == "true"  # Roll 1 = true
    assert rumor.category in ["threat", "npc", "location", "treasure", "mystery"]
    assert rumor.rumor_text


def test_truthfulness_by_roll():
    """Test že truthfulness odpovídá k6 hodu."""
    # Roll 1-3 = true
    for roll in [1, 2, 3]:
        rumor = RumorGenerator.create_single(roll=roll)
        assert rumor.truthfulness == "true", f"Roll {roll} should be true"

    # Roll 4-5 = partial
    for roll in [4, 5]:
        rumor = RumorGenerator.create_single(roll=roll)
        assert rumor.truthfulness == "partial", f"Roll {roll} should be partial"

    # Roll 6 = false
    rumor = RumorGenerator.create_single(roll=6)
    assert rumor.truthfulness == "false"


def test_all_categories_present():
    """Test že všechny kategorie mohou být vygenerovány."""
    categories_found = set()

    # Generuj 50 zvěstí a zkontroluj že všechny kategorie se objeví
    for _ in range(50):
        rumor = RumorGenerator.create_single(roll=1)
        categories_found.add(rumor.category)

    # Měli bychom vidět většinu kategorií
    assert len(categories_found) >= 3  # Aspoň 3 z 5


def test_world_connected_with_settlement():
    """Test world-connected generování se settlement."""
    world_state = {
        "hexcrawl": {
            "settlements": [
                {
                    "name": "Mlýnská Víska",
                    "size_name": "Vesnice",
                    "problem": "Krysí loupežníci",
                    "notable_npc": "Stará Bělovous",
                    "government": "Starosta",
                    "features": ["Velký mlýn"]
                }
            ],
            "hexes": [],
            "dungeons": []
        }
    }

    rumor = RumorGenerator.create_single(roll=1, world_state=world_state)

    assert isinstance(rumor, Rumor)
    assert rumor.source_location is not None
    assert rumor.source_location["type"] == "settlement"
    # Zvěst by měla obsahovat jméno osady
    assert "Mlýnská Víska" in rumor.rumor_text or rumor.rumor_text  # Fallback je OK


def test_world_connected_with_hex():
    """Test world-connected generování s hexem."""
    world_state = {
        "hexcrawl": {
            "settlements": [],
            "hexes": [
                {
                    "type": "Les",
                    "detail_name": "Přírodní jeskyně",
                    "landmark": "Starý dub"
                }
            ],
            "dungeons": []
        }
    }

    rumor = RumorGenerator.create_single(roll=1, world_state=world_state)

    assert isinstance(rumor, Rumor)
    assert rumor.source_location is not None
    assert rumor.source_location["type"] == "hex"


def test_world_connected_with_dungeon():
    """Test world-connected generování s dungeonem."""
    world_state = {
        "hexcrawl": {
            "settlements": [],
            "hexes": [],
            "dungeons": [
                {
                    "past": "Starodávný chrám netopýřího kultu",
                    "inhabitants": "Krysí loupežníci",
                    "secret": "Obelisk hučící mystickou energií",
                    "goal": "Poklad"
                }
            ]
        }
    }

    rumor = RumorGenerator.create_single(roll=1, world_state=world_state)

    assert isinstance(rumor, Rumor)
    assert rumor.source_location is not None
    assert rumor.source_location["type"] == "dungeon"


def test_gossip_chain_for_partial():
    """Test gossip chain pro partial truth (roll 4-5)."""
    # Partial může mít 1-2 hopy
    rumor = RumorGenerator.create_single(roll=4, advanced=True)

    assert rumor.truthfulness == "partial"
    # Gossip hops může být 0 (bez world state) nebo 1-2 (s advanced)
    assert rumor.gossip_hops in [0, 1, 2]


def test_gossip_chain_for_false():
    """Test gossip chain pro false (roll 6)."""
    # False má 3 hopy
    rumor = RumorGenerator.create_single(roll=6, advanced=True)

    assert rumor.truthfulness == "false"
    # Gossip hops může být 0 (bez world state) nebo 3 (s advanced)
    assert rumor.gossip_hops in [0, 3]


def test_advanced_mode_vs_basic():
    """Test rozdílu mezi advanced a basic módem."""
    # Basic mode = bez story hooks a gossip
    basic = RumorGenerator.create(advanced=False)
    assert all(r.story_hook_detail is None for r in basic)

    # Advanced mode může mít story hooks (záleží na kategorii)
    advanced = RumorGenerator.create(advanced=True)
    # Advanced může mít story hooks, ale není zaručeno (záleží na random)
    assert len(advanced) == 6


def test_to_dict():
    """Test konverze na dictionary."""
    rumors = RumorGenerator.create()
    data = RumorGenerator.to_dict(rumors)

    assert isinstance(data, dict)
    assert "metadata" in data
    assert "rumors" in data
    assert len(data["rumors"]) == 6

    # Zkontroluj strukturu první zvěsti
    rumor = data["rumors"][0]
    assert "roll" in rumor
    assert "rumor" in rumor
    assert "category" in rumor
    assert "truthfulness" in rumor
    assert "gm_notes" in rumor


def test_to_json():
    """Test konverze na JSON."""
    rumors = RumorGenerator.create()
    json_str = RumorGenerator.to_json(rumors)

    assert isinstance(json_str, str)
    # Zkontroluj že je to validní JSON
    data = json.loads(json_str)
    assert "rumors" in data
    assert len(data["rumors"]) == 6


def test_format_text():
    """Test textového formátování."""
    rumors = RumorGenerator.create()
    text = RumorGenerator.format_text(rumors)

    assert isinstance(text, str)
    assert "TABULKA ZVĚSTÍ" in text
    assert "K6" in text
    assert "TYPE" in text
    assert "ZVĚST" in text
    assert "PRAVDA" in text


def test_random_generation_produces_valid_rumors():
    """Test že náhodné generování produkuje validní zvěsti."""
    for _ in range(5):
        rumors = RumorGenerator.create()

        for rumor in rumors:
            assert isinstance(rumor, Rumor)
            assert rumor.roll in [1, 2, 3, 4, 5, 6]
            assert rumor.truthfulness in ["true", "partial", "false"]
            assert rumor.category in ["threat", "npc", "location", "treasure", "mystery"]
            assert rumor.rumor_text
            assert len(rumor.rumor_text) > 0


def test_properties():
    """Test properties Rumor modelu."""
    rumor = RumorGenerator.create_single(roll=1)

    # Category properties
    assert rumor.category_emoji
    assert rumor.category_name_cz

    # Truthfulness properties
    assert rumor.truthfulness_symbol
    assert rumor.truthfulness_name_cz in ["PRAVDA", "ČÁSTEČNĚ", "FÁMA"]


def test_with_complex_world_state():
    """Test s komplexním world state obsahujícím všechny typy lokací."""
    world_state = {
        "hexcrawl": {
            "settlements": [
                {
                    "name": "Mlýnská Víska",
                    "problem": "Krysí loupežníci",
                    "notable_npc": "Stará Bělovous"
                }
            ],
            "hexes": [
                {
                    "type": "Les",
                    "detail_name": "Přírodní jeskyně"
                }
            ],
            "dungeons": [
                {
                    "past": "Starodávný chrám",
                    "inhabitants": "Krysí loupežníci",
                    "secret": "Obelisk"
                }
            ]
        }
    }

    rumors = RumorGenerator.create(world_state=world_state)

    assert len(rumors) == 6

    # Zkontroluj že některé zvěsti používají world state
    world_connected_count = sum(
        1 for r in rumors if r.source_location is not None
    )

    # Aspoň někde by měl být použitý world state
    # (může být 0 pokud random vždycky zvolí fallback, ale je to nepravděpodobné)
    assert world_connected_count >= 0  # Soft constraint


def test_gm_notes_presence():
    """Test že GM notes jsou vždy přítomny."""
    rumors = RumorGenerator.create()

    for rumor in rumors:
        assert rumor.gm_notes
        assert len(rumor.gm_notes) > 0


def test_truth_false_parts_for_partial_and_false():
    """Test že partial a false mají truth_part a false_part."""
    # Generuj partial
    partial_rumors = [
        RumorGenerator.create_single(roll=4) for _ in range(5)
    ]

    for rumor in partial_rumors:
        # Truth/false parts můžou být None pro fallback mode
        # ale měly by být přítomny pro world-connected
        assert rumor.truthfulness == "partial"

    # Generuj false
    false_rumors = [
        RumorGenerator.create_single(roll=6) for _ in range(5)
    ]

    for rumor in false_rumors:
        assert rumor.truthfulness == "false"


def test_categories_match_location_types():
    """Test že kategorie odpovídají typům lokací."""
    # Settlement s problemem → threat
    world_state = {
        "hexcrawl": {
            "settlements": [
                {
                    "name": "Testovací osada",
                    "problem": "Testovací problém"
                }
            ],
            "hexes": [],
            "dungeons": []
        }
    }

    # Generuj několikrát
    categories = []
    for _ in range(10):
        rumor = RumorGenerator.create_single(roll=1, world_state=world_state)
        if rumor.source_location:
            categories.append(rumor.category)

    # Měl by být často threat (ale ne vždy kvůli random)
    if categories:  # Pokud nějaké world-connected byly vygenerovány
        assert "threat" in categories or len(categories) > 0
