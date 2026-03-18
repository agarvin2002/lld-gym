# Advanced topic — adapting a third-party API with incompatible units and data shapes
"""
Adapter Pattern - Example 2: Third-Party Weather API Adapter

A third-party weather API returns temperature in Fahrenheit, humidity as a
percentage, and wind speed in mph. Our app expects Celsius, fraction (0–1),
and km/h. We adapt the third-party API to our WeatherService interface using
composition — no inheritance from the third-party class.

Real-world use: Aggregating multiple weather providers (OpenWeatherMap, AccuWeather)
behind one interface so the app can swap providers without any other code changing.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Our app's domain types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Location:
    city: str
    country: str

    def __str__(self) -> str:
        return f"{self.city}, {self.country}"


@dataclass
class WeatherReport:
    location: Location
    temperature_celsius: float
    humidity_fraction: float   # 0.0 – 1.0
    wind_speed_kmh: float
    description: str


# ---------------------------------------------------------------------------
# Our app's target interface
# ---------------------------------------------------------------------------

class WeatherService(ABC):
    @abstractmethod
    def get_current_weather(self, location: Location) -> WeatherReport: ...

    @abstractmethod
    def is_available(self) -> bool: ...


# ---------------------------------------------------------------------------
# Third-party library (cannot modify)
# ---------------------------------------------------------------------------

class ThirdPartyWeatherAPI:
    """External API — uses Fahrenheit, percentage, and mph."""

    _DATA: dict[str, dict] = {
        "Mumbai":  {"temp_f": 95.0, "humidity_pct": 85.0, "wind_mph": 10.0, "sky": "Humid"},
        "London":  {"temp_f": 55.4, "humidity_pct": 80.0, "wind_mph": 12.5, "sky": "Overcast"},
        "New York":{"temp_f": 68.0, "humidity_pct": 65.0, "wind_mph":  8.0, "sky": "Partly cloudy"},
    }

    def __init__(self, api_key: str) -> None:
        self._connected = True

    def get_temp_fahrenheit(self, city: str) -> float:
        return self._lookup(city)["temp_f"]

    def get_humidity_percent(self, city: str) -> float:
        return self._lookup(city)["humidity_pct"]

    def get_wind_speed_mph(self, city: str) -> float:
        return self._lookup(city)["wind_mph"]

    def get_sky_condition(self, city: str) -> str:
        return self._lookup(city)["sky"]

    def ping(self) -> bool:
        return self._connected

    def simulate_disconnect(self) -> None:
        self._connected = False

    def _lookup(self, city: str) -> dict:
        if city not in self._DATA:
            raise ValueError(f"Unknown city: {city}")
        return self._DATA[city]


# ---------------------------------------------------------------------------
# Adapter — composition-based (preferred over multiple inheritance)
# ---------------------------------------------------------------------------

class ThirdPartyWeatherAdapter(WeatherService):
    """
    Wraps ThirdPartyWeatherAPI and converts units to what our app expects.

    Conversions:
        °F → °C  : (F - 32) × 5/9
        %  → 0–1 : pct / 100
        mph→km/h : mph × 1.60934
    """

    def __init__(self, api: ThirdPartyWeatherAPI) -> None:
        self._api = api  # composition: hold a reference, do not inherit

    def get_current_weather(self, location: Location) -> WeatherReport:
        city = location.city
        return WeatherReport(
            location=location,
            temperature_celsius=(self._api.get_temp_fahrenheit(city) - 32) * 5 / 9,
            humidity_fraction=self._api.get_humidity_percent(city) / 100.0,
            wind_speed_kmh=self._api.get_wind_speed_mph(city) * 1.60934,
            description=self._api.get_sky_condition(city),
        )

    def is_available(self) -> bool:
        return self._api.ping()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    api     = ThirdPartyWeatherAPI(api_key="demo-key")
    adapter = ThirdPartyWeatherAdapter(api)

    for city, country in [("Mumbai", "IN"), ("London", "UK"), ("New York", "US")]:
        loc    = Location(city, country)
        report = adapter.get_current_weather(loc)
        print(
            f"{loc}: {report.temperature_celsius:.1f}°C, "
            f"{report.humidity_fraction * 100:.0f}% humidity, "
            f"{report.wind_speed_kmh:.1f} km/h — {report.description}"
        )

    print(f"\nService available: {adapter.is_available()}")
    api.simulate_disconnect()
    print(f"After disconnect: {adapter.is_available()}")
