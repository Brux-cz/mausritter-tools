#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script pro WeatherGenerator (bez pytest)
"""
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from src.generators.weather import WeatherGenerator
from src.core.models import Weather


def test_generate_weather_spring():
    """Test generování jarního počasí"""
    print("\n[TEST] test_generate_weather_spring...")
    weather, unfavorable = WeatherGenerator.generate_weather("spring")

    assert isinstance(weather, str), "Počasí musí být string"
    assert len(weather) > 0, "Počasí nesmí být prázdné"
    assert isinstance(unfavorable, bool), "Unfavorable musí být bool"

    valid_spring_weather = [
        "Přívalové deště", "Mrholení", "Zataženo",
        "Jasno a slunečno", "Jasno a teplo"
    ]
    assert weather in valid_spring_weather, f"Neplatné jarní počasí: {weather}"
    print(f"  [OK] Vygenerováno jarní počasí: {weather} (nepříznivé: {unfavorable})")


def test_generate_weather_all_seasons():
    """Test generování počasí pro všechny sezóny"""
    print("\n[TEST] test_generate_weather_all_seasons...")

    seasons = ["spring", "summer", "autumn", "winter"]
    for season in seasons:
        weather, unfavorable = WeatherGenerator.generate_weather(season)
        assert isinstance(weather, str), f"Počasí pro {season} musí být string"
        assert len(weather) > 0, f"Počasí pro {season} nesmí být prázdné"
        season_name = WeatherGenerator.get_season_name(season)
        print(f"  [OK] {season_name}: {weather}")


def test_unfavorable_weather_winter():
    """Test že zima má hodně nepříznivého počasí"""
    print("\n[TEST] test_unfavorable_weather_winter...")

    unfavorable_count = 0
    total = 20

    for _ in range(total):
        weather, unfavorable = WeatherGenerator.generate_weather("winter")

        if weather in ["Vánice", "Mrznoucí déšť", "Třeskutá zima"]:
            assert unfavorable is True, f"{weather} musí být unfavorable"
            unfavorable_count += 1
        else:
            assert unfavorable is False, f"{weather} nesmí být unfavorable"

    print(f"  [OK] Z {total} pokusů bylo {unfavorable_count} nepříznivých ({unfavorable_count*100//total}%)")
    print(f"       (Podle pravidel má zima 72% šanci na nepříznivé počasí)")


def test_generate_event():
    """Test generování sezónních událostí"""
    print("\n[TEST] test_generate_event...")

    event = WeatherGenerator.generate_event("spring")
    assert isinstance(event, str), "Událost musí být string"
    assert len(event) > 0, "Událost nesmí být prázdná"
    print(f"  [OK] Jarní událost: {event}")

    # Test všech sezón
    for season in ["summer", "autumn", "winter"]:
        event = WeatherGenerator.generate_event(season)
        assert len(event) > 0
        season_name = WeatherGenerator.get_season_name(season)
        print(f"  [OK] {season_name}: {event}")


def test_create_weather_basic():
    """Test vytvoření základního počasí"""
    print("\n[TEST] test_create_weather_basic...")

    weather = WeatherGenerator.create()

    assert isinstance(weather, Weather), "Musí vrátit Weather instanci"
    assert weather.season in ["spring", "summer", "autumn", "winter"]
    assert weather.weather, "Počasí nesmí být prázdné"
    assert isinstance(weather.unfavorable, bool), "Unfavorable musí být bool"
    assert weather.event is None, "Bez with_event by událost měla být None"

    print(f"  [OK] Weather vytvořen:")
    print(f"       Sezóna: {WeatherGenerator.get_season_name(weather.season)}")
    print(f"       Počasí: {weather.weather}")
    print(f"       Nepříznivé: {weather.unfavorable}")


def test_create_weather_with_event():
    """Test vytvoření počasí s událostí"""
    print("\n[TEST] test_create_weather_with_event...")

    weather = WeatherGenerator.create(season="summer", with_event=True)

    assert isinstance(weather, Weather)
    assert weather.season == "summer"
    assert weather.event is not None, "S with_event=True by událost měla existovat"
    assert len(weather.event) > 0, "Událost nesmí být prázdná"

    print(f"  [OK] Weather s událostí:")
    print(f"       Sezóna: Léto")
    print(f"       Počasí: {weather.weather}")
    print(f"       Událost: {weather.event}")


def test_create_all_seasons():
    """Test vytvoření počasí pro všechny sezóny"""
    print("\n[TEST] test_create_all_seasons...")

    for season in ["spring", "summer", "autumn", "winter"]:
        weather = WeatherGenerator.create(season=season)
        assert weather.season == season
        assert isinstance(weather.weather, str)
        season_name = WeatherGenerator.get_season_name(season)
        print(f"  [OK] {season_name}: {weather.weather}")


def test_invalid_season_fallback():
    """Test že neplatná sezóna se fallbackne na spring"""
    print("\n[TEST] test_invalid_season_fallback...")

    weather = WeatherGenerator.create(season="invalid")
    assert weather.season == "spring", "Neplatná sezóna by měla fallbacknout na spring"
    print(f"  [OK] Neplatná sezóna fallbackla na: {weather.season}")


def test_get_season_name():
    """Test českých názvů sezón"""
    print("\n[TEST] test_get_season_name...")

    assert WeatherGenerator.get_season_name("spring") == "Jaro"
    assert WeatherGenerator.get_season_name("summer") == "Léto"
    assert WeatherGenerator.get_season_name("autumn") == "Podzim"
    assert WeatherGenerator.get_season_name("winter") == "Zima"
    assert WeatherGenerator.get_season_name("invalid") == "Neznámé"
    print(f"  [OK] Všechny české názvy sezón fungují")


def test_generate_weather_randomness():
    """Test že generování počasí dává různé výsledky"""
    print("\n[TEST] test_generate_weather_randomness...")

    results = set()
    for _ in range(30):
        weather, _ = WeatherGenerator.generate_weather("spring")
        results.add(weather)

    assert len(results) > 1, "Všechno počasí je stejné - možná problém s RNG"
    print(f"  [OK] Z 30 hodů vygenerovány {len(results)} různé druhy počasí")


def test_generate_event_randomness():
    """Test že generování událostí dává různé výsledky"""
    print("\n[TEST] test_generate_event_randomness...")

    results = set()
    for _ in range(30):
        event = WeatherGenerator.generate_event("spring")
        results.add(event)

    assert len(results) > 1, "Všechny události jsou stejné - možná problém s RNG"
    print(f"  [OK] Z 30 hodů vygenerovány {len(results)} různé události")


def test_to_dict():
    """Test konverze do dictionary"""
    print("\n[TEST] test_to_dict...")

    weather = WeatherGenerator.create(season="winter", with_event=True)
    data = WeatherGenerator.to_dict(weather)

    assert isinstance(data, dict), "Musí vrátit dictionary"
    assert "season" in data
    assert "weather" in data
    assert "unfavorable" in data
    assert "event" in data
    assert "notes" in data
    assert data["season"] == "winter"

    print(f"  [OK] Dictionary konverze funguje")
    print(f"       Klíče: {', '.join(data.keys())}")


def test_to_json():
    """Test konverze do JSON"""
    print("\n[TEST] test_to_json...")

    weather = WeatherGenerator.create(season="autumn")
    json_str = WeatherGenerator.to_json(weather)

    assert isinstance(json_str, str), "Musí vrátit string"
    assert '"season":' in json_str
    assert '"weather":' in json_str

    # Ověř že je validní JSON
    import json
    data = json.loads(json_str)
    assert isinstance(data, dict)
    assert data["season"] == "autumn"

    print(f"  [OK] JSON konverze funguje")
    print(f"       JSON délka: {len(json_str)} znaků")


def test_multiple_weather():
    """Test že generování více počasí dává různé výsledky"""
    print("\n[TEST] test_multiple_weather...")

    weathers = []
    for _ in range(10):
        weather = WeatherGenerator.create(season="summer")
        weathers.append(weather)

    weather_types = {w.weather for w in weathers}
    assert len(weather_types) > 1, "Všechna počasí jsou stejná"

    print(f"  [OK] Vytvořeno 10 počasí (léto)")
    print(f"       Různé druhy: {len(weather_types)}")
    for weather_type in sorted(weather_types):
        count = sum(1 for w in weathers if w.weather == weather_type)
        print(f"       - {weather_type}: {count}x")


def main():
    """Spusť všechny testy"""
    print("="*70)
    print("WeatherGenerator Test Suite")
    print("="*70)

    tests = [
        test_generate_weather_spring,
        test_generate_weather_all_seasons,
        test_unfavorable_weather_winter,
        test_generate_event,
        test_create_weather_basic,
        test_create_weather_with_event,
        test_create_all_seasons,
        test_invalid_season_fallback,
        test_get_season_name,
        test_generate_weather_randomness,
        test_generate_event_randomness,
        test_to_dict,
        test_to_json,
        test_multiple_weather,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  [FAIL] {e}")
        except Exception as e:
            failed += 1
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*70)
    print(f"Výsledky: {passed} testů prošlo, {failed} selhalo")
    print("="*70 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
