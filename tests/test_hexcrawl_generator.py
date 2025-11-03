"""
Testy pro HexcrawlGenerator

Test Coverage:
- Základní generování
- Validace 25 hexů (5×5 podle oficiálních pravidel)
- Všechny 3 presety (starter, standard, advanced)
- Override parametrů
- World state struktura
- JSON export
"""

import pytest
import json
from src.generators.hexcrawl import HexcrawlGenerator
from src.core.models import Hexcrawl, Settlement, Hex, Dungeon, Rumor


class TestHexcrawlGenerator:
    """Testy pro HexcrawlGenerator - orchestrátor pro kompletní hexcrawl."""

    def test_basic_generation(self):
        """Test 1: Základní generování hexcrawlu s default presetetem."""
        hexcrawl = HexcrawlGenerator.create()

        # Ověř že je to Hexcrawl objekt
        assert isinstance(hexcrawl, Hexcrawl)

        # Ověř že má všechny komponenty
        assert hasattr(hexcrawl, 'hexes')
        assert hasattr(hexcrawl, 'settlements')
        assert hasattr(hexcrawl, 'dungeons')
        assert hasattr(hexcrawl, 'rumors')
        assert hasattr(hexcrawl, 'world_state')
        assert hasattr(hexcrawl, 'metadata')

        # Ověř že komponenty jsou správného typu
        assert isinstance(hexcrawl.hexes, list)
        assert isinstance(hexcrawl.settlements, list)
        assert isinstance(hexcrawl.dungeons, list)
        assert isinstance(hexcrawl.rumors, list)
        assert isinstance(hexcrawl.world_state, dict)
        assert isinstance(hexcrawl.metadata, dict)

    def test_always_25_hexes(self):
        """
        Test 2: KRITICKÝ TEST - Hexcrawl VŽDY musí mít přesně 25 hexů.

        Podle oficiálních pravidel Mausritter (str. 21):
        "Draw a 5×5 grid of hexes" = vždy 25 hexů
        """
        hexcrawl = HexcrawlGenerator.create()

        # KRITICKÁ VALIDACE
        assert len(hexcrawl.hexes) == 25, \
            f"Hexcrawl MUSÍ mít přesně 25 hexů (5×5), ale má {len(hexcrawl.hexes)}"

        # Ověř že jsou to skutečně Hex objekty
        for hex_obj in hexcrawl.hexes:
            assert isinstance(hex_obj, Hex)

        # Ověř map_dimensions property
        assert hexcrawl.map_dimensions == (5, 5)

        # Ověř metadata
        assert hexcrawl.metadata['map_dimensions'] == '5x5'
        assert hexcrawl.metadata['counts']['hexes'] == 25

    def test_starter_preset(self):
        """Test 3: STARTER preset - zjednodušený hexcrawl pro začátečníky."""
        hexcrawl = HexcrawlGenerator.create(preset="starter")

        # Ověř počty podle STARTER presetu:
        # 1 settlement, 2 dungeons, 0 factions, 6 rumors
        assert len(hexcrawl.hexes) == 25
        assert len(hexcrawl.settlements) == 1
        assert len(hexcrawl.dungeons) == 2
        assert len(hexcrawl.factions) == 0
        assert len(hexcrawl.rumors) == 6

        # Ověř že první settlement je friendly a má lokaci C3
        first_settlement = hexcrawl.settlements[0]
        assert isinstance(first_settlement, Settlement)
        assert first_settlement.is_friendly is True
        assert first_settlement.hex_location == "C3"

        # Ověř metadata counts
        assert hexcrawl.metadata['counts']['settlements'] == 1
        assert hexcrawl.metadata['counts']['dungeons'] == 2
        assert hexcrawl.metadata['counts']['factions'] == 0
        assert hexcrawl.metadata['counts']['rumors'] == 6

    def test_standard_preset(self):
        """Test 4: STANDARD preset - podle oficiálních pravidel (Hrabství Ek)."""
        hexcrawl = HexcrawlGenerator.create(preset="standard")

        # Ověř počty podle STANDARD presetu:
        # 3 settlements, 3 dungeons, 3 factions (skipped), 6 rumors
        assert len(hexcrawl.hexes) == 25
        assert len(hexcrawl.settlements) == 3
        assert len(hexcrawl.dungeons) == 3
        assert len(hexcrawl.factions) == 0  # FactionGenerator není implementován
        assert len(hexcrawl.rumors) == 6

        # Ověř že první settlement je friendly
        assert hexcrawl.settlements[0].is_friendly is True
        assert hexcrawl.settlements[0].hex_location == "C3"

        # Ověř metadata
        assert hexcrawl.metadata['official_rules_compliant'] is True

    def test_advanced_preset(self):
        """Test 5: ADVANCED preset - plně vybavený hexcrawl."""
        hexcrawl = HexcrawlGenerator.create(preset="advanced")

        # Ověř počty podle ADVANCED presetu:
        # 3 settlements, 4 dungeons, 4 factions (skipped), 6 rumors
        assert len(hexcrawl.hexes) == 25
        assert len(hexcrawl.settlements) == 3
        assert len(hexcrawl.dungeons) == 4
        assert len(hexcrawl.factions) == 0  # FactionGenerator není implementován
        assert len(hexcrawl.rumors) == 6

    def test_custom_parameters(self):
        """Test 6: Override parametrů presetu."""
        # Override počtu settlements a dungeonů
        hexcrawl = HexcrawlGenerator.create(
            preset="standard",
            settlements=2,
            dungeons=5
        )

        # Ověř že override fungoval
        assert len(hexcrawl.settlements) == 2
        assert len(hexcrawl.dungeons) == 5

        # Hexy vždy 25!
        assert len(hexcrawl.hexes) == 25

        # První settlement stále friendly
        assert hexcrawl.settlements[0].is_friendly is True

    def test_world_state_structure(self):
        """Test 7: Struktura world_state pro RumorGenerator."""
        hexcrawl = HexcrawlGenerator.create(preset="starter")

        # Ověř že world_state má správnou strukturu
        assert 'hexcrawl' in hexcrawl.world_state

        world_hexcrawl = hexcrawl.world_state['hexcrawl']
        assert 'map_size' in world_hexcrawl
        assert 'hexes' in world_hexcrawl
        assert 'settlements' in world_hexcrawl
        assert 'dungeons' in world_hexcrawl

        # Ověř že je to 5×5
        assert world_hexcrawl['map_size'] == '5x5'

        # Ověř že world_state obsahuje slovníkové verze objektů
        assert isinstance(world_hexcrawl['hexes'], list)
        assert isinstance(world_hexcrawl['settlements'], list)
        assert isinstance(world_hexcrawl['dungeons'], list)

        # Ověř že jsou to dict, ne objekty
        if len(world_hexcrawl['hexes']) > 0:
            assert isinstance(world_hexcrawl['hexes'][0], dict)
        if len(world_hexcrawl['settlements']) > 0:
            assert isinstance(world_hexcrawl['settlements'][0], dict)

    def test_validation_rejects_wrong_hex_count(self):
        """Test 8: Validace v __post_init__ odmítne != 25 hexů."""
        from src.generators.hex import HexGenerator

        # Pokus vytvořit Hexcrawl s 10 hexy (MUSÍ selhat)
        wrong_hexes = [HexGenerator.create() for _ in range(10)]

        with pytest.raises(ValueError) as exc_info:
            Hexcrawl(
                hexes=wrong_hexes,
                settlements=[],
                dungeons=[],
                rumors=[],
                world_state={},
                factions=[]
            )

        # Ověř chybovou zprávu
        error_message = str(exc_info.value)
        assert "25 hexů" in error_message or "25 hexes" in error_message
        assert "10" in error_message

    def test_to_dict(self):
        """Test 9: Konverze hexcrawlu na dictionary."""
        hexcrawl = HexcrawlGenerator.create(preset="starter")

        # Konvertuj na dict
        hexcrawl_dict = HexcrawlGenerator.to_dict(hexcrawl)

        # Ověř že je to dict
        assert isinstance(hexcrawl_dict, dict)

        # Ověř že má všechny klíče
        assert 'metadata' in hexcrawl_dict
        assert 'world_state' in hexcrawl_dict
        assert 'hexes' in hexcrawl_dict
        assert 'settlements' in hexcrawl_dict
        assert 'dungeons' in hexcrawl_dict
        assert 'rumors' in hexcrawl_dict
        assert 'factions' in hexcrawl_dict

        # Ověř že listy obsahují dicts
        assert isinstance(hexcrawl_dict['hexes'], list)
        assert len(hexcrawl_dict['hexes']) == 25

        # Ověř metadata
        assert 'generated_at' in hexcrawl_dict['metadata']
        assert 'generator_version' in hexcrawl_dict['metadata']
        assert hexcrawl_dict['metadata']['counts']['hexes'] == 25

    def test_to_json(self):
        """Test 10: Konverze hexcrawlu na JSON string."""
        hexcrawl = HexcrawlGenerator.create(preset="starter")

        # Konvertuj na JSON
        hexcrawl_json = HexcrawlGenerator.to_json(hexcrawl)

        # Ověř že je to string
        assert isinstance(hexcrawl_json, str)

        # Ověř že je to validní JSON
        parsed = json.loads(hexcrawl_json)
        assert isinstance(parsed, dict)

        # Ověř strukturu
        assert 'metadata' in parsed
        assert 'hexes' in parsed
        assert len(parsed['hexes']) == 25

        # Ověř české znaky (ensure_ascii=False)
        # Pokud máme settlement s českým názvem, musí být v JSONu
        if len(parsed['settlements']) > 0:
            settlement_json = json.dumps(parsed['settlements'][0])
            # JSON by měl obsahovat UTF-8 české znaky, ne escape sekvence
            # (těžko testovat bez konkrétního settlement, ale JSON by měl být validní)
            assert isinstance(settlement_json, str)


class TestHexcrawlIntegration:
    """Integrační testy - ověření že všechny generátory dobře spolupracují."""

    def test_all_components_present(self):
        """Ověř že hexcrawl obsahuje výstupy všech generátorů."""
        hexcrawl = HexcrawlGenerator.create(preset="standard")

        # HexGenerator - 25 hexů
        assert len(hexcrawl.hexes) == 25
        assert all(isinstance(h, Hex) for h in hexcrawl.hexes)

        # SettlementGenerator - 3 settlements
        assert len(hexcrawl.settlements) == 3
        assert all(isinstance(s, Settlement) for s in hexcrawl.settlements)

        # DungeonGenerator - 3 dungeons
        assert len(hexcrawl.dungeons) == 3
        assert all(isinstance(d, Dungeon) for d in hexcrawl.dungeons)

        # RumorGenerator - 6 rumors
        assert len(hexcrawl.rumors) == 6
        assert all(isinstance(r, Rumor) for r in hexcrawl.rumors)

    def test_rumors_connected_to_world_state(self):
        """Ověř že zvěsti jsou propojené s world_state."""
        hexcrawl = HexcrawlGenerator.create(preset="standard")

        # RumorGenerator dostal world_state
        assert hexcrawl.world_state is not None
        assert 'hexcrawl' in hexcrawl.world_state

        # Zvěsti byly vygenerovány (6 podle oficiálních pravidel)
        assert len(hexcrawl.rumors) == 6

        # Každá zvěst má kategorie (pokud používáme advanced=True)
        for rumor in hexcrawl.rumors:
            assert hasattr(rumor, 'truthfulness')
            assert rumor.truthfulness in ['true', 'partial', 'false']

    def test_friendly_settlement_placement(self):
        """Ověř že první settlement je vždy friendly a na C3."""
        # Test pro všechny presety
        for preset in ['starter', 'standard', 'advanced']:
            hexcrawl = HexcrawlGenerator.create(preset=preset)

            # První settlement musí být friendly
            first_settlement = hexcrawl.settlements[0]
            assert first_settlement.is_friendly is True, \
                f"První settlement v presetu {preset} není friendly!"
            assert first_settlement.hex_location == "C3", \
                f"První settlement v presetu {preset} není na C3!"

    def test_metadata_completeness(self):
        """Ověř že metadata obsahují všechny potřebné informace."""
        hexcrawl = HexcrawlGenerator.create(preset="standard")

        meta = hexcrawl.metadata

        # Základní metadata
        assert 'generated_at' in meta
        assert 'generator_version' in meta
        assert 'map_dimensions' in meta
        assert 'official_rules_compliant' in meta

        # Counts
        assert 'counts' in meta
        counts = meta['counts']
        assert counts['hexes'] == 25
        assert counts['settlements'] == 3
        assert counts['dungeons'] == 3
        assert counts['rumors'] == 6
        assert counts['factions'] == 0  # Není implementováno

        # Validita hodnot
        assert meta['map_dimensions'] == '5x5'
        assert meta['official_rules_compliant'] is True
        assert meta['generator_version'] == '1.0.0'


class TestPresetConfigurations:
    """Testy pro všechny oficiální presety."""

    def test_all_presets_exist(self):
        """Ověř že všechny 3 presety jsou definované."""
        assert 'starter' in HexcrawlGenerator.PRESETS
        assert 'standard' in HexcrawlGenerator.PRESETS
        assert 'advanced' in HexcrawlGenerator.PRESETS

    def test_preset_metadata(self):
        """Ověř že každý preset má správnou strukturu."""
        for preset_name, preset_config in HexcrawlGenerator.PRESETS.items():
            assert 'name' in preset_config
            assert 'description' in preset_config
            assert 'hexes' in preset_config
            assert 'settlements' in preset_config
            assert 'dungeons' in preset_config
            assert 'factions' in preset_config
            assert 'rumors' in preset_config

            # Hexy VŽDY 25!
            assert preset_config['hexes'] == 25, \
                f"Preset {preset_name} nemá 25 hexů!"

    def test_invalid_preset_fallback(self):
        """Ověř že neplatný preset použije standard jako fallback."""
        hexcrawl = HexcrawlGenerator.create(preset="neexistujici_preset")

        # Mělo by použít standard preset (3/3/6)
        assert len(hexcrawl.settlements) == 3
        assert len(hexcrawl.dungeons) == 3
        assert len(hexcrawl.rumors) == 6
