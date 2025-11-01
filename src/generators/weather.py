"""
Generator počasí podle ročních období
"""
from typing import Optional, Dict, Any, Tuple
from dataclasses import asdict
import json

from src.core.dice import roll_d6
from src.core.models import Weather
from src.core.tables import TableLoader


class WeatherGenerator:
    """
    Generátor počasí a sezónních událostí podle pravidel Mausritter.
    Používá tabulky z 16_RANDOM_TABLES.md pro určení denního počasí.
    """

    # Mapování sezón pro validaci
    VALID_SEASONS = ["spring", "summer", "autumn", "winter"]

    # České názvy sezón
    SEASON_NAMES = {
        "spring": "Jaro",
        "summer": "Léto",
        "autumn": "Podzim",
        "winter": "Zima"
    }

    @staticmethod
    def generate_weather(season: str = "spring") -> Tuple[str, bool]:
        """
        Vygeneruj počasí pro dané roční období.

        Args:
            season: "spring", "summer", "autumn", nebo "winter"

        Returns:
            Tuple (weather_text, is_unfavorable)

        Example:
            >>> weather, unfavorable = WeatherGenerator.generate_weather("winter")
            >>> assert isinstance(weather, str)
            >>> assert isinstance(unfavorable, bool)
        """
        if season not in WeatherGenerator.VALID_SEASONS:
            season = "spring"  # Fallback na jaro

        # Hoď 2k6 pro počasí
        roll = roll_d6() + roll_d6()

        # Lookup v tabulce
        weather_data = TableLoader.lookup_weather(season, roll)

        if weather_data:
            return weather_data["weather"], weather_data["unfavorable"]

        # Fallback (nemělo by nastat)
        return "Jasno", False

    @staticmethod
    def generate_event(season: str = "spring") -> str:
        """
        Vygeneruj sezónní událost.

        Args:
            season: "spring", "summer", "autumn", nebo "winter"

        Returns:
            Text sezónní události

        Example:
            >>> event = WeatherGenerator.generate_event("autumn")
            >>> assert isinstance(event, str)
            >>> assert len(event) > 0
        """
        if season not in WeatherGenerator.VALID_SEASONS:
            season = "spring"  # Fallback na jaro

        # Hoď k6 pro událost
        roll = roll_d6()

        # Lookup v tabulce
        event_text = TableLoader.lookup_seasonal_event(season, roll)

        if event_text:
            return event_text

        # Fallback (nemělo by nastat)
        return "Klidný den bez zvláštních událostí"

    @classmethod
    def create(cls,
               season: str = "spring",
               with_event: bool = False) -> Weather:
        """
        Vytvoř kompletní počasí pro dané roční období.

        Args:
            season: "spring", "summer", "autumn", nebo "winter" (default: "spring")
            with_event: True pokud má zahrnout sezónní událost (default: False)

        Returns:
            Weather instance s počasím a volitelně událostí

        Example:
            >>> weather = WeatherGenerator.create(season="winter")
            >>> assert weather.season == "winter"
            >>> assert isinstance(weather.weather, str)

            >>> weather_with_event = WeatherGenerator.create(season="summer", with_event=True)
            >>> assert weather_with_event.event is not None
        """
        # Validace sezóny
        if season not in cls.VALID_SEASONS:
            season = "spring"

        # Vygeneruj počasí
        weather_text, unfavorable = cls.generate_weather(season)

        # Vygeneruj událost pokud je požadována
        event = None
        if with_event:
            event = cls.generate_event(season)

        # Vytvoř Weather objekt
        weather = Weather(
            season=season,
            weather=weather_text,
            unfavorable=unfavorable,
            event=event,
            notes=""
        )

        return weather

    @staticmethod
    def to_dict(weather: Weather) -> Dict[str, Any]:
        """
        Konvertuj Weather do dictionary.

        Args:
            weather: Weather instance

        Returns:
            Dictionary reprezentace počasí

        Example:
            >>> weather = WeatherGenerator.create()
            >>> data = WeatherGenerator.to_dict(weather)
            >>> assert "season" in data
            >>> assert "weather" in data
        """
        return asdict(weather)

    @staticmethod
    def to_json(weather: Weather, indent: int = 2) -> str:
        """
        Konvertuj Weather do JSON stringu.

        Args:
            weather: Weather instance
            indent: Počet mezer pro odsazení (default 2)

        Returns:
            JSON string reprezentace počasí

        Example:
            >>> weather = WeatherGenerator.create()
            >>> json_str = WeatherGenerator.to_json(weather)
            >>> assert '"season":' in json_str
        """
        data = WeatherGenerator.to_dict(weather)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def get_season_name(season: str) -> str:
        """
        Vrátí český název sezóny.

        Args:
            season: "spring", "summer", "autumn", nebo "winter"

        Returns:
            Český název (např. "Jaro")

        Example:
            >>> name = WeatherGenerator.get_season_name("winter")
            >>> assert name == "Zima"
        """
        return WeatherGenerator.SEASON_NAMES.get(season, "Neznámé")
