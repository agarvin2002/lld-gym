"""
Proxy Pattern — Example 2: Caching + Logging Proxy Chain
=========================================================
Demonstrates composing two proxies over the same interface.

  ProtectedProxy → LoggingProxy → CachingProxy → RealService

- ProtectedProxy : rejects unauthorised callers immediately.
- LoggingProxy   : records every allowed call with its result.
- CachingProxy   : avoids redundant calls to the slow RealService.
- RealService    : simulates an expensive external API (weather data).

The client always holds a reference typed as `WeatherService` and never
knows how many proxy layers sit in between.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime


# ---------------------------------------------------------------------------
# Subject interface
# ---------------------------------------------------------------------------

class WeatherService(ABC):
    """Retrieve current temperature for a city."""

    @abstractmethod
    def get_temperature(self, city: str) -> float:
        """Return temperature in Celsius."""
        ...


# ---------------------------------------------------------------------------
# Real Subject — slow, expensive
# ---------------------------------------------------------------------------

class RealWeatherService(WeatherService):
    """Simulates a slow HTTP call to a weather API."""

    _MOCK_DATA: dict[str, float] = {
        "London":  12.5,
        "Tokyo":   22.0,
        "Sydney":  28.3,
        "New York": 5.1,
    }

    def get_temperature(self, city: str) -> float:
        """Fetch temperature — pretend this makes a network request."""
        print(f"  [RealWeatherService] Fetching temperature for '{city}' …")
        if city not in self._MOCK_DATA:
            raise ValueError(f"No data for city: {city!r}")
        return self._MOCK_DATA[city]


# ---------------------------------------------------------------------------
# Proxy 1: Caching
# ---------------------------------------------------------------------------

class CachingWeatherProxy(WeatherService):
    """
    Caching proxy: stores results so identical queries skip the real service.

    Thread-safety is omitted here for brevity; add threading.Lock in production.
    """

    def __init__(self, real: WeatherService) -> None:
        """Wrap *real*, which may itself be another proxy."""
        self._real = real
        self._cache: dict[str, float] = {}
        self._hits = 0

    def get_temperature(self, city: str) -> float:
        if city in self._cache:
            self._hits += 1
            print(f"  [CachingProxy] Cache HIT for '{city}' (hits so far: {self._hits})")
            return self._cache[city]
        result = self._real.get_temperature(city)
        self._cache[city] = result
        return result

    def clear_cache(self) -> None:
        """Invalidate the entire cache."""
        self._cache.clear()
        self._hits = 0

    @property
    def cache_size(self) -> int:
        return len(self._cache)

    @property
    def cache_hits(self) -> int:
        return self._hits


# ---------------------------------------------------------------------------
# Proxy 2: Logging
# ---------------------------------------------------------------------------

class LoggingWeatherProxy(WeatherService):
    """Logging proxy: records every call with timestamp and result."""

    def __init__(self, real: WeatherService) -> None:
        self._real = real
        self._log: list[str] = []

    def get_temperature(self, city: str) -> float:
        result = self._real.get_temperature(city)
        entry = (
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"get_temperature({city!r}) → {result}°C"
        )
        self._log.append(entry)
        print(f"  [LoggingProxy] {entry}")
        return result

    @property
    def query_log(self) -> list[str]:
        """Return a copy of the audit log."""
        return list(self._log)


# ---------------------------------------------------------------------------
# Proxy 3: Protection
# ---------------------------------------------------------------------------

class ProtectedWeatherProxy(WeatherService):
    """
    Protection proxy: only allowed users may query.

    Note: the signature changes to accept a *user* parameter.  In a real
    system you would pass credentials via a thread-local or context object
    so the interface stays identical.  Here we accept user explicitly to
    keep the example self-contained.
    """

    def __init__(self, real: WeatherService, allowed_users: list[str]) -> None:
        self._real = real
        self._allowed = set(allowed_users)

    def get_temperature(self, city: str, *, user: str = "") -> float:  # type: ignore[override]
        """Raises PermissionError if *user* is not in the allowed set."""
        if user not in self._allowed:
            raise PermissionError(
                f"User {user!r} is not authorised to query weather data."
            )
        print(f"  [ProtectedProxy] User '{user}' authorised — forwarding …")
        return self._real.get_temperature(city)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Build the chain: ProtectedProxy → LoggingProxy → CachingProxy → Real
    real    = RealWeatherService()
    cached  = CachingWeatherProxy(real)
    logged  = LoggingWeatherProxy(cached)
    service = ProtectedWeatherProxy(logged, allowed_users=["alice", "bob"])

    print("=== Allowed user queries London twice ===")
    t1 = service.get_temperature("London", user="alice")
    print(f"  Result: {t1}°C\n")

    t2 = service.get_temperature("London", user="alice")
    print(f"  Result: {t2}°C\n")

    print("=== Allowed user queries Tokyo ===")
    t3 = service.get_temperature("Tokyo", user="bob")
    print(f"  Result: {t3}°C\n")

    print("=== Unauthorised user is rejected ===")
    try:
        service.get_temperature("Tokyo", user="eve")
    except PermissionError as e:
        print(f"  PermissionError: {e}\n")

    print(f"=== Cache stats: size={cached.cache_size}, hits={cached.cache_hits} ===")
    print("\n=== Full audit log ===")
    for entry in logged.query_log:
        print(f"  {entry}")

    print("\n=== Clearing cache and re-querying London ===")
    cached.clear_cache()
    print(f"  Cache size after clear: {cached.cache_size}")
    t4 = service.get_temperature("London", user="alice")
    print(f"  Result: {t4}°C")
