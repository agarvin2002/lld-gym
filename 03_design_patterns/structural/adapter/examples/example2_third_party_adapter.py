"""
Adapter Pattern - Example 2: Third-Party Weather API Adapter

Scenario:
    We have a third-party weather API (ThirdPartyWeatherAPI) that:
    - Returns temperature in Fahrenheit
    - Returns humidity as a percentage float (e.g., 72.5)
    - Returns wind speed in mph
    - Uses city_name strings as identifiers

    Our application expects a WeatherService interface that:
    - Returns temperature in Celsius
    - Returns humidity as a decimal fraction (e.g., 0.725)
    - Returns wind speed in km/h
    - Uses Location objects as identifiers

    We cannot modify ThirdPartyWeatherAPI. We write an adapter.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import random


# ---------------------------------------------------------------------------
# Domain model for our application
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
    humidity_fraction: float      # 0.0 – 1.0
    wind_speed_kmh: float
    description: str

    def __str__(self) -> str:
        return (
            f"Weather in {self.location}:\n"
            f"  Temperature : {self.temperature_celsius:.1f} °C\n"
            f"  Humidity    : {self.humidity_fraction * 100:.1f}%\n"
            f"  Wind Speed  : {self.wind_speed_kmh:.1f} km/h\n"
            f"  Description : {self.description}"
        )


# ---------------------------------------------------------------------------
# Our application's target interface
# ---------------------------------------------------------------------------

class WeatherService(ABC):
    """Interface that our application depends on."""

    @abstractmethod
    def get_current_weather(self, location: Location) -> WeatherReport:
        """Return current weather for the given location."""
        ...

    @abstractmethod
    def get_temperature_celsius(self, location: Location) -> float:
        """Return current temperature in Celsius."""
        ...

    @abstractmethod
    def get_humidity(self, location: Location) -> float:
        """Return current humidity as a fraction between 0 and 1."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the service is reachable."""
        ...


# ---------------------------------------------------------------------------
# Third-party library (cannot modify — pretend it's an external package)
# ---------------------------------------------------------------------------

class ThirdPartyWeatherAPI:
    """
    External weather API we have no control over.
    It uses different units and data formats from what our app expects.
    """

    # Simulated data store (in real life this would make HTTP requests)
    _DATA: dict[str, dict] = {
        "London": {
            "temp_f": 55.4,
            "humidity_pct": 80.0,
            "wind_mph": 12.5,
            "sky": "Overcast",
        },
        "New York": {
            "temp_f": 68.0,
            "humidity_pct": 65.0,
            "wind_mph": 8.0,
            "sky": "Partly cloudy",
        },
        "Tokyo": {
            "temp_f": 75.2,
            "humidity_pct": 70.0,
            "wind_mph": 5.5,
            "sky": "Sunny",
        },
        "Sydney": {
            "temp_f": 82.4,
            "humidity_pct": 55.0,
            "wind_mph": 15.0,
            "sky": "Clear",
        },
    }

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._connected = True

    def get_temp_fahrenheit(self, city_name: str) -> float:
        """Returns temperature in Fahrenheit."""
        self._ensure_connected()
        data = self._lookup(city_name)
        return data["temp_f"]

    def get_humidity_percent(self, city_name: str) -> float:
        """Returns relative humidity as a percentage (0–100)."""
        self._ensure_connected()
        data = self._lookup(city_name)
        return data["humidity_pct"]

    def get_wind_speed_mph(self, city_name: str) -> float:
        """Returns wind speed in miles per hour."""
        self._ensure_connected()
        data = self._lookup(city_name)
        return data["wind_mph"]

    def get_sky_condition(self, city_name: str) -> str:
        """Returns a textual sky condition."""
        self._ensure_connected()
        data = self._lookup(city_name)
        return data["sky"]

    def ping(self) -> bool:
        """Returns True if the API is reachable."""
        return self._connected

    def simulate_disconnect(self) -> None:
        """For testing — simulate API going down."""
        self._connected = False

    # --- internals ---

    def _ensure_connected(self) -> None:
        if not self._connected:
            raise ConnectionError("ThirdPartyWeatherAPI: connection failed")

    def _lookup(self, city_name: str) -> dict:
        if city_name not in self._DATA:
            raise ValueError(f"ThirdPartyWeatherAPI: unknown city '{city_name}'")
        return self._DATA[city_name]


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

class ThirdPartyWeatherAdapter(WeatherService):
    """
    Adapts ThirdPartyWeatherAPI to our application's WeatherService interface.

    Unit conversions performed:
        °F → °C  :  (F - 32) × 5/9
        %  → 0-1 :  pct / 100
        mph→km/h :  mph × 1.60934
    """

    def __init__(self, api: ThirdPartyWeatherAPI) -> None:
        self._api = api

    # --- WeatherService interface ---

    def get_current_weather(self, location: Location) -> WeatherReport:
        city = location.city
        return WeatherReport(
            location=location,
            temperature_celsius=self._fahrenheit_to_celsius(
                self._api.get_temp_fahrenheit(city)
            ),
            humidity_fraction=self._percent_to_fraction(
                self._api.get_humidity_percent(city)
            ),
            wind_speed_kmh=self._mph_to_kmh(
                self._api.get_wind_speed_mph(city)
            ),
            description=self._api.get_sky_condition(city),
        )

    def get_temperature_celsius(self, location: Location) -> float:
        raw_f = self._api.get_temp_fahrenheit(location.city)
        return self._fahrenheit_to_celsius(raw_f)

    def get_humidity(self, location: Location) -> float:
        raw_pct = self._api.get_humidity_percent(location.city)
        return self._percent_to_fraction(raw_pct)

    def is_available(self) -> bool:
        return self._api.ping()

    # --- Private conversion helpers ---

    @staticmethod
    def _fahrenheit_to_celsius(fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5 / 9

    @staticmethod
    def _percent_to_fraction(percent: float) -> float:
        return percent / 100.0

    @staticmethod
    def _mph_to_kmh(mph: float) -> float:
        return mph * 1.60934


# ---------------------------------------------------------------------------
# A second, native implementation (shows the interface is stable)
# ---------------------------------------------------------------------------

class MockWeatherService(WeatherService):
    """Lightweight in-memory weather service for testing — no adapter needed."""

    def __init__(self) -> None:
        self._data: dict[str, WeatherReport] = {}

    def add(self, location: Location, report: WeatherReport) -> None:
        self._data[location.city] = report

    def get_current_weather(self, location: Location) -> WeatherReport:
        if location.city not in self._data:
            raise ValueError(f"MockWeatherService: no data for {location}")
        return self._data[location.city]

    def get_temperature_celsius(self, location: Location) -> float:
        return self.get_current_weather(location).temperature_celsius

    def get_humidity(self, location: Location) -> float:
        return self.get_current_weather(location).humidity_fraction

    def is_available(self) -> bool:
        return True


# ---------------------------------------------------------------------------
# Application code — only knows about WeatherService
# ---------------------------------------------------------------------------

class WeatherDashboard:
    """Displays weather for a list of locations. Depends only on WeatherService."""

    def __init__(self, service: WeatherService) -> None:
        self._service = service

    def show(self, locations: list[Location]) -> None:
        if not self._service.is_available():
            print("Weather service is currently unavailable.")
            return

        for loc in locations:
            try:
                report = self._service.get_current_weather(loc)
                print(report)
                print()
            except (ValueError, ConnectionError) as exc:
                print(f"  Could not fetch weather for {loc}: {exc}\n")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("ADAPTER PATTERN - Third-Party Weather API Demo")
    print("=" * 60)

    locations = [
        Location("London", "UK"),
        Location("New York", "USA"),
        Location("Tokyo", "Japan"),
        Location("Sydney", "Australia"),
    ]

    # --- Using adapter with third-party API ---
    print("\n--- Dashboard backed by ThirdPartyWeatherAPI (via adapter) ---\n")
    third_party_api = ThirdPartyWeatherAPI(api_key="secret-key-123")
    adapter = ThirdPartyWeatherAdapter(third_party_api)
    dashboard = WeatherDashboard(adapter)
    dashboard.show(locations)

    # --- Demonstrate unit conversions explicitly ---
    print("--- Unit conversion verification ---")
    london = Location("London", "UK")
    raw_f = third_party_api.get_temp_fahrenheit("London")
    converted_c = adapter.get_temperature_celsius(london)
    print(f"  London: {raw_f}°F → {converted_c:.2f}°C (expected: 13.0°C)")

    raw_pct = third_party_api.get_humidity_percent("London")
    converted_frac = adapter.get_humidity(london)
    print(f"  Humidity: {raw_pct}% → {converted_frac:.3f} fraction")

    # --- Demonstrate availability check ---
    print(f"\n  Service available: {adapter.is_available()}")
    third_party_api.simulate_disconnect()
    print(f"  After disconnect: {adapter.is_available()}")

    # --- Same dashboard with mock (no adapter) ---
    print("\n--- Dashboard backed by MockWeatherService (no adapter needed) ---\n")
    mock = MockWeatherService()
    mock.add(
        Location("London", "UK"),
        WeatherReport(Location("London", "UK"), 13.0, 0.80, 20.1, "Overcast"),
    )
    mock_dashboard = WeatherDashboard(mock)
    mock_dashboard.show([Location("London", "UK")])

    print("Done.")
