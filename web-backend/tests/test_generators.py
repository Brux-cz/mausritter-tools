# -*- coding: utf-8 -*-
"""
Unit tests pro Mausritter API generator endpoints.

Testuje všech 17 generátorů:
- MVP (5): Character, NPC, Hex, Settlement, Weather
- V2 (12): Hireling, Reaction, Spell, Treasure, Adventure, Hook,
           Creature, Tavern, Dungeon, Rumor, Hexcrawl
"""

import pytest


class TestMVPGenerators:
    """Testy pro 5 MVP generátorů."""

    def test_character_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování postavy."""
        response = test_client.post(
            f"{api_base_url}/character",
            json={"name": "TestMouse", "gender": "male"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "str" in data
        assert "dex" in data
        assert "wil" in data
        assert "hp" in data

    def test_character_generator_no_params(self, test_client, api_base_url):
        """Test generování postavy bez parametrů."""
        response = test_client.post(f"{api_base_url}/character", json={})
        assert response.status_code == 200

    def test_npc_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování NPC."""
        response = test_client.post(
            f"{api_base_url}/npc",
            json={"name": "TestNPC"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "status" in data
        assert "appearance" in data

    def test_hex_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování hexu."""
        response = test_client.post(f"{api_base_url}/hex", json={})
        assert response.status_code == 200
        data = response.json()
        assert "type" in data
        assert "detail_category" in data
        assert "detail_name" in data

    def test_settlement_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování osady."""
        response = test_client.post(f"{api_base_url}/settlement", json={})
        assert response.status_code == 200
        data = response.json()
        assert "size_name" in data
        assert "government" in data

    def test_weather_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování počasí."""
        response = test_client.post(
            f"{api_base_url}/weather",
            json={"season": "spring", "with_event": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "season" in data
        assert "weather" in data

    def test_weather_generator_invalid_season(self, test_client, api_base_url):
        """Test validace - neplatné roční období."""
        response = test_client.post(
            f"{api_base_url}/weather",
            json={"season": "invalid"}
        )
        # Should fail validation or return error
        assert response.status_code in [400, 422, 500]


class TestV2Generators:
    """Testy pro 12 rozšířených generátorů."""

    def test_hireling_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování pomocníka."""
        response = test_client.post(
            f"{api_base_url}/hireling",
            json={"type": 6}
        )
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "availability" in data

    def test_reaction_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování reakce."""
        response = test_client.post(
            f"{api_base_url}/reaction",
            json={"modifier": 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert "roll" in data
        assert "reaction" in data

    def test_spell_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování kouzla."""
        response = test_client.post(f"{api_base_url}/spell", json={})
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "effect" in data

    def test_treasure_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování pokladu."""
        response = test_client.post(
            f"{api_base_url}/treasure",
            json={"bonus": 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_adventure_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování adventure seed."""
        response = test_client.post(
            f"{api_base_url}/adventure",
            json={"custom": False, "with_inspiration": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "creature" in data
        assert "problem" in data
        assert "complication" in data

    def test_hook_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování adventure hooku."""
        response = test_client.post(f"{api_base_url}/hook", json={})
        assert response.status_code == 200
        data = response.json()
        assert "hook" in data
        assert "category" in data

    def test_creature_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování creature varianty."""
        response = test_client.post(
            f"{api_base_url}/creature/ghost",
            json={}
        )
        assert response.status_code == 200
        data = response.json()
        assert "type" in data
        assert "variant" in data

    def test_creature_generator_invalid_type(self, test_client, api_base_url):
        """Test validace - neplatný creature type."""
        response = test_client.post(
            f"{api_base_url}/creature/invalid",
            json={}
        )
        assert response.status_code == 400
        assert "Invalid creature type" in response.json()["detail"]

    def test_tavern_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování hospody."""
        response = test_client.post(f"{api_base_url}/tavern", json={})
        assert response.status_code == 200
        data = response.json()
        assert "name_part1" in data or "specialty" in data

    def test_dungeon_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování dungeonu."""
        response = test_client.post(
            f"{api_base_url}/dungeon",
            json={"rooms": 6, "with_settlement": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "past" in data
        assert "rooms" in data

    def test_rumor_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování zvěstí."""
        response = test_client.post(
            f"{api_base_url}/rumor",
            json={"core_only": True, "advanced": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "rumors" in data
        assert isinstance(data["rumors"], list)

    def test_hexcrawl_generator_success(self, test_client, api_base_url):
        """Test úspěšného generování hexcrawlu."""
        response = test_client.post(
            f"{api_base_url}/hexcrawl",
            json={"preset": "starter", "core_only": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert "hexes" in data
        assert "metadata" in data


class TestStatusEndpoint:
    """Testy pro status endpoint."""

    def test_status_endpoint(self, test_client, api_base_url):
        """Test status endpointu - měl by ukazovat 17/17 generátorů."""
        response = test_client.get(f"{api_base_url}/status")
        assert response.status_code == 200
        data = response.json()
        assert data["total_generators"] == 17
        assert data["implemented"] == 17
        assert len(data["generators"]) == 16  # 16 endpointů (creature má parametr)
        assert len(data["creature_types"]) == 11


class TestHealthCheck:
    """Testy pro health check endpoint."""

    def test_health_check(self, test_client):
        """Test health check endpointu."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestValidation:
    """Testy pro validaci parametrů."""

    def test_hireling_invalid_type(self, test_client, api_base_url):
        """Test validace - hireling type mimo rozsah."""
        response = test_client.post(
            f"{api_base_url}/hireling",
            json={"type": 100}  # Platný rozsah je 1-9
        )
        assert response.status_code == 422  # Validation error

    def test_treasure_invalid_bonus(self, test_client, api_base_url):
        """Test validace - treasure bonus mimo rozsah."""
        response = test_client.post(
            f"{api_base_url}/treasure",
            json={"bonus": 10}  # Platný rozsah je 0-4
        )
        assert response.status_code == 422  # Validation error

    def test_dungeon_invalid_rooms(self, test_client, api_base_url):
        """Test validace - dungeon rooms mimo rozsah."""
        response = test_client.post(
            f"{api_base_url}/dungeon",
            json={"rooms": 100}  # Platný rozsah je 1-20
        )
        assert response.status_code == 422  # Validation error
