"""
Testy pro WeatherGenerator
"""
from src.generators.weather import WeatherGenerator
from src.core.models import Weather


def test_generate_weather_spring():
    """Test generování jarního počasí"""
    weather, unfavorable = WeatherGenerator.generate_weather("spring")

    assert isinstance(weather, str), "Počasí musí být string"
    assert len(weather) > 0, "Počasí nesmí být prázdné"
    assert isinstance(unfavorable, bool), "Unfavorable musí být bool"

    # Jarní počasí (podle tabulky)
    valid_spring_weather = [
        "Přívalové deště",
        "Mrholení",
        "Zataženo",
        "Jasno a slunečno",
        "Jasno a teplo"
    ]
    assert weather in valid_spring_weather, f"Neplatné jarní počasí: {weather}"


def test_generate_weather_summer():
    """Test generování letního počasí"""
    weather, unfavorable = WeatherGenerator.generate_weather("summer")

    assert isinstance(weather, str)
    assert len(weather) > 0

    # Letní počasí
    valid_summer_weather = [
        "Bouřka",
        "Úmorné vedro",
        "Jasno a teplo",
        "Příjemně slunečno",
        "Krásně teplo"
    ]
    assert weather in valid_summer_weather, f"Neplatné letní počasí: {weather}"


def test_generate_weather_autumn():
    """Test generování podzimního počasí"""
    weather, unfavorable = WeatherGenerator.generate_weather("autumn")

    assert isinstance(weather, str)
    assert len(weather) > 0

    # Podzimní počasí
    valid_autumn_weather = [
        "Silný vítr",
        "Slejvák",
        "Chladno",
        "Přeháňky",
        "Jasno a chladno"
    ]
    assert weather in valid_autumn_weather, f"Neplatné podzimní počasí: {weather}"


def test_generate_weather_winter():
    """Test generování zimního počasí"""
    weather, unfavorable = WeatherGenerator.generate_weather("winter")

    assert isinstance(weather, str)
    assert len(weather) > 0

    # Zimní počasí
    valid_winter_weather = [
        "Vánice",
        "Mrznoucí déšť",
        "Třeskutá zima",
        "Zataženo",
        "Jasno a chladno"
    ]
    assert weather in valid_winter_weather, f"Neplatné zimní počasí: {weather}"


def test_unfavorable_weather_spring():
    """Test že jaro má správně označené nepříznivé počasí"""
    # V jaře je nepříznivé jen "Přívalové deště" (hod 2)
    # Zkoušíme vícekrát, abychom měli šanci to trefit
    unfavorable_found = False
    favorable_found = False

    for _ in range(50):
        weather, unfavorable = WeatherGenerator.generate_weather("spring")

        if weather == "Přívalové deště":
            assert unfavorable is True, "Přívalové deště musí být unfavorable"
            unfavorable_found = True
        else:
            assert unfavorable is False, f"{weather} nesmí být unfavorable"
            favorable_found = True

    # Měli bychom vidět oba případy
    assert favorable_found, "Měli bychom vidět nějaké příznivé počasí"


def test_unfavorable_weather_winter():
    """Test že zima má hodně nepříznivého počasí"""
    # V zimě je nepříznivé: Vánice (2), Mrznoucí déšť (3-5), Třeskutá zima (6-8)
    # To je 72% šance na unfavorable
    unfavorable_count = 0

    for _ in range(30):
        weather, unfavorable = WeatherGenerator.generate_weather("winter")

        if weather in ["Vánice", "Mrznoucí déšť", "Třeskutá zima"]:
            assert unfavorable is True, f"{weather} musí být unfavorable"
            unfavorable_count += 1
        else:
            assert unfavorable is False, f"{weather} nesmí být unfavorable"

    # Měli bychom vidět alespoň nějaké unfavorable (statisticky velmi pravděpodobné)
    assert unfavorable_count > 0, "V zimě by mělo být nějaké nepříznivé počasí"


def test_generate_event_spring():
    """Test generování jarních událostí"""
    event = WeatherGenerator.generate_event("spring")

    assert isinstance(event, str), "Událost musí být string"
    assert len(event) > 0, "Událost nesmí být prázdná"

    # Jarní události (podle tabulky)
    valid_spring_events = [
        "Povodeň spláchla důležitý výrazný prvek",
        "Ptačí matka chránící vajíčka",
        "Kupcovi uvízla kárka v rozblácené kaluži",
        "Migrující motýli lačnící po nektaru",
        "Myši tkají květinové věnce v přípravě na…",
        "Svatební slavnosti, veselé procesí"
    ]
    assert event in valid_spring_events, f"Neplatná jarní událost: {event}"


def test_generate_event_all_seasons():
    """Test že všechny sezóny mají události"""
    for season in ["spring", "summer", "autumn", "winter"]:
        event = WeatherGenerator.generate_event(season)

        assert isinstance(event, str), f"Událost pro {season} musí být string"
        assert len(event) > 0, f"Událost pro {season} nesmí být prázdná"


def test_create_weather_basic():
    """Test vytvoření základního počasí"""
    weather = WeatherGenerator.create()

    # Ověř že je to instance Weather
    assert isinstance(weather, Weather), "Musí vrátit Weather instanci"

    # Ověř všechna povinná pole
    assert weather.season in ["spring", "summer", "autumn", "winter"], "Neplatná sezóna"
    assert weather.weather, "Počasí nesmí být prázdné"
    assert isinstance(weather.unfavorable, bool), "Unfavorable musí být bool"
    assert weather.event is None, "Bez --with-event by událost měla být None"
    assert weather.notes == "", "Notes by měly být prázdné"


def test_create_weather_with_event():
    """Test vytvoření počasí s událostí"""
    weather = WeatherGenerator.create(season="summer", with_event=True)

    assert isinstance(weather, Weather)
    assert weather.season == "summer"
    assert weather.weather, "Počasí nesmí být prázdné"
    assert weather.event is not None, "S with_event=True by událost měla existovat"
    assert len(weather.event) > 0, "Událost nesmí být prázdná"


def test_create_all_seasons():
    """Test vytvoření počasí pro všechny sezóny"""
    for season in ["spring", "summer", "autumn", "winter"]:
        weather = WeatherGenerator.create(season=season)

        assert weather.season == season
        assert isinstance(weather.weather, str)
        assert len(weather.weather) > 0


def test_create_invalid_season():
    """Test že neplatná sezóna se fallbackne na spring"""
    weather = WeatherGenerator.create(season="invalid")

    assert weather.season == "spring", "Neplatná sezóna by měla fallbacknout na spring"


def test_get_season_name():
    """Test českých názvů sezón"""
    assert WeatherGenerator.get_season_name("spring") == "Jaro"
    assert WeatherGenerator.get_season_name("summer") == "Léto"
    assert WeatherGenerator.get_season_name("autumn") == "Podzim"
    assert WeatherGenerator.get_season_name("winter") == "Zima"
    assert WeatherGenerator.get_season_name("invalid") == "Neznámé"


def test_generate_weather_randomness():
    """Test že generování počasí dává různé výsledky"""
    results = set()

    for _ in range(30):
        weather, _ = WeatherGenerator.generate_weather("spring")
        results.add(weather)

    # Měli bychom dostat alespoň 2 různé výsledky
    assert len(results) > 1, "Všechno počasí je stejné - možná problém s RNG"


def test_generate_event_randomness():
    """Test že generování událostí dává různé výsledky"""
    results = set()

    for _ in range(30):
        event = WeatherGenerator.generate_event("spring")
        results.add(event)

    # Měli bychom dostat alespoň 2 různé události
    assert len(results) > 1, "Všechny události jsou stejné - možná problém s RNG"


def test_to_dict():
    """Test konverze do dictionary"""
    weather = WeatherGenerator.create(season="winter", with_event=True)
    data = WeatherGenerator.to_dict(weather)

    assert isinstance(data, dict), "Musí vrátit dictionary"
    assert "season" in data
    assert "weather" in data
    assert "unfavorable" in data
    assert "event" in data
    assert "notes" in data

    assert data["season"] == "winter"
    assert isinstance(data["weather"], str)
    assert isinstance(data["unfavorable"], bool)


def test_to_json():
    """Test konverze do JSON"""
    weather = WeatherGenerator.create(season="autumn")
    json_str = WeatherGenerator.to_json(weather)

    assert isinstance(json_str, str), "Musí vrátit string"
    assert '"season":' in json_str
    assert '"weather":' in json_str
    assert '"unfavorable":' in json_str

    # Ověř že je validní JSON
    import json
    data = json.loads(json_str)
    assert isinstance(data, dict)
    assert data["season"] == "autumn"


def test_create_multiple_weather():
    """Test že generování více počasí dává různé výsledky"""
    weathers = []
    for _ in range(20):
        weather = WeatherGenerator.create(season="summer")
        weathers.append(weather)

    # Ověř že nemají všichni stejné počasí
    weather_types = {w.weather for w in weathers}
    assert len(weather_types) > 1, "Všechna počasí jsou stejná"
