# Advanced topic — shows how to compose three independent proxy layers (caching, logging, protection) over a single interface so each concern stays in its own class.
"""
Proxy Pattern — Example 2: Composing a Proxy Chain

  ProtectedProxy → LoggingProxy → CachingProxy → RealService

Each proxy handles one concern. The client only sees the WeatherService interface.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime


# Subject interface
class WeatherService(ABC):
    @abstractmethod
    def get_temperature(self, city: str) -> float: ...


# Real Subject — simulates a slow HTTP call
class RealWeatherService(WeatherService):
    _MOCK_DATA: dict[str, float] = {
        "Mumbai": 32.0, "Delhi": 18.5, "Bengaluru": 24.0, "Chennai": 29.3,
    }

    def get_temperature(self, city: str) -> float:
        print(f"  [RealService] Fetching temperature for '{city}' …")
        if city not in self._MOCK_DATA:
            raise ValueError(f"No data for city: {city!r}")
        return self._MOCK_DATA[city]


# Proxy 1: Caching — avoids redundant calls to the real service
class CachingWeatherProxy(WeatherService):
    def __init__(self, real: WeatherService) -> None:
        self._real = real
        self._cache: dict[str, float] = {}
        self._hits = 0

    def get_temperature(self, city: str) -> float:
        if city in self._cache:
            self._hits += 1
            print(f"  [CachingProxy] Cache HIT for '{city}' (hits: {self._hits})")
            return self._cache[city]
        result = self._real.get_temperature(city)
        self._cache[city] = result
        return result

    def clear_cache(self) -> None:
        self._cache.clear()
        self._hits = 0

    @property
    def cache_size(self) -> int:
        return len(self._cache)

    @property
    def cache_hits(self) -> int:
        return self._hits


# Proxy 2: Logging — records every call with timestamp
class LoggingWeatherProxy(WeatherService):
    def __init__(self, real: WeatherService) -> None:
        self._real = real
        self._log: list[str] = []

    def get_temperature(self, city: str) -> float:
        result = self._real.get_temperature(city)
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] get_temperature({city!r}) → {result}°C"
        self._log.append(entry)
        print(f"  [LoggingProxy] {entry}")
        return result

    @property
    def query_log(self) -> list[str]:
        return list(self._log)


# Proxy 3: Protection — rejects unauthorised callers before forwarding
class ProtectedWeatherProxy(WeatherService):
    def __init__(self, real: WeatherService, allowed_users: list[str]) -> None:
        self._real = real
        self._allowed = set(allowed_users)

    def get_temperature(self, city: str, *, user: str = "") -> float:  # type: ignore[override]
        if user not in self._allowed:
            raise PermissionError(f"User {user!r} is not authorised.")
        print(f"  [ProtectedProxy] '{user}' authorised — forwarding …")
        return self._real.get_temperature(city)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Build chain: Protected → Logging → Caching → Real
    real    = RealWeatherService()
    cached  = CachingWeatherProxy(real)
    logged  = LoggingWeatherProxy(cached)
    service = ProtectedWeatherProxy(logged, allowed_users=["alice", "bob"])

    print("=== Allowed user queries Mumbai twice ===")
    t1 = service.get_temperature("Mumbai", user="alice")
    print(f"  Result: {t1}°C\n")
    t2 = service.get_temperature("Mumbai", user="alice")
    print(f"  Result: {t2}°C\n")

    print("=== Unauthorised user is rejected ===")
    try:
        service.get_temperature("Delhi", user="eve")
    except PermissionError as e:
        print(f"  PermissionError: {e}\n")

    print(f"=== Cache: size={cached.cache_size}, hits={cached.cache_hits} ===")
    print("=== Audit log ===")
    for entry in logged.query_log:
        print(f"  {entry}")
