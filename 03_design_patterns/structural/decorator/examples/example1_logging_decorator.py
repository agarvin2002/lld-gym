"""
Decorator Pattern - Example 1: Logging and Caching Decorators

Scenario:
    DataService provides read/write operations on a key-value store.
    We want to add:
    1. Logging: log every call with timestamp and result
    2. Caching: cache read results, skip re-fetching same key

    These concerns should be composable and transparent to the client.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional
import time


# ---------------------------------------------------------------------------
# Component Interface
# ---------------------------------------------------------------------------

class DataService(ABC):
    """Abstract interface for a key-value data service."""

    @abstractmethod
    def read(self, key: str) -> Optional[str]:
        """Read a value by key. Returns None if key not found."""
        ...

    @abstractmethod
    def write(self, key: str, value: str) -> None:
        """Write a value for the given key."""
        ...

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a key. Returns True if it existed."""
        ...

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Return True if the key exists in the store."""
        ...


# ---------------------------------------------------------------------------
# Concrete Component (the real implementation)
# ---------------------------------------------------------------------------

class InMemoryDataService(DataService):
    """Real data service backed by an in-memory dictionary."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._call_count = 0

    def read(self, key: str) -> Optional[str]:
        self._call_count += 1
        # Simulate a slow storage read
        time.sleep(0.05)
        return self._store.get(key)

    def write(self, key: str, value: str) -> None:
        self._call_count += 1
        self._store[key] = value

    def delete(self, key: str) -> bool:
        self._call_count += 1
        if key in self._store:
            del self._store[key]
            return True
        return False

    def exists(self, key: str) -> bool:
        return key in self._store

    @property
    def call_count(self) -> int:
        return self._call_count


# ---------------------------------------------------------------------------
# Base Decorator (forwards all calls — subclasses only override what they need)
# ---------------------------------------------------------------------------

class DataServiceDecorator(DataService):
    """
    Base decorator class.
    Holds a reference to a DataService and forwards all calls.
    Subclasses override specific methods to add behavior.
    """

    def __init__(self, wrapped: DataService) -> None:
        self._wrapped = wrapped

    def read(self, key: str) -> Optional[str]:
        return self._wrapped.read(key)

    def write(self, key: str, value: str) -> None:
        self._wrapped.write(key, value)

    def delete(self, key: str) -> bool:
        return self._wrapped.delete(key)

    def exists(self, key: str) -> bool:
        return self._wrapped.exists(key)


# ---------------------------------------------------------------------------
# Concrete Decorator 1: Logging
# ---------------------------------------------------------------------------

class LoggingDataService(DataServiceDecorator):
    """
    Logs every read/write/delete with timestamp and result.
    """

    def __init__(self, wrapped: DataService, prefix: str = "LOG") -> None:
        super().__init__(wrapped)
        self._prefix = prefix
        self._log: list[str] = []

    def _log_entry(self, operation: str, details: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{self._prefix}] {ts} | {operation} | {details}"
        self._log.append(entry)
        print(entry)

    def read(self, key: str) -> Optional[str]:
        result = self._wrapped.read(key)
        status = f"key='{key}' → '{result}'" if result else f"key='{key}' → MISS"
        self._log_entry("READ ", status)
        return result

    def write(self, key: str, value: str) -> None:
        self._wrapped.write(key, value)
        self._log_entry("WRITE", f"key='{key}', value='{value}'")

    def delete(self, key: str) -> bool:
        result = self._wrapped.delete(key)
        status = "DELETED" if result else "NOT_FOUND"
        self._log_entry("DEL  ", f"key='{key}' → {status}")
        return result

    @property
    def logs(self) -> list[str]:
        return list(self._log)


# ---------------------------------------------------------------------------
# Concrete Decorator 2: Caching
# ---------------------------------------------------------------------------

class CachingDataService(DataServiceDecorator):
    """
    Caches read results in memory.
    - On read: check cache first, call wrapped service only on cache miss.
    - On write/delete: invalidate the relevant cache entry.
    """

    def __init__(self, wrapped: DataService, max_size: int = 100) -> None:
        super().__init__(wrapped)
        self._cache: dict[str, Optional[str]] = {}
        self._max_size = max_size
        self._hits = 0
        self._misses = 0

    def read(self, key: str) -> Optional[str]:
        if key in self._cache:
            self._hits += 1
            return self._cache[key]

        self._misses += 1
        value = self._wrapped.read(key)

        if len(self._cache) < self._max_size:
            self._cache[key] = value

        return value

    def write(self, key: str, value: str) -> None:
        # Invalidate cache on write
        self._cache.pop(key, None)
        self._wrapped.write(key, value)

    def delete(self, key: str) -> bool:
        # Invalidate cache on delete
        self._cache.pop(key, None)
        return self._wrapped.delete(key)

    @property
    def cache_hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    @property
    def stats(self) -> dict:
        return {
            "hits": self._hits,
            "misses": self._misses,
            "cached_keys": len(self._cache),
            "hit_rate": f"{self.cache_hit_rate:.1%}",
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("DECORATOR PATTERN - Logging & Caching Demo")
    print("=" * 60)

    # --- 1. Plain service ---
    print("\n--- 1. Plain InMemoryDataService ---")
    plain = InMemoryDataService()
    plain.write("user:1", "Alice")
    plain.write("user:2", "Bob")
    print("Read user:1 →", plain.read("user:1"))
    print("Call count:", plain.call_count)

    # --- 2. Logging only ---
    print("\n--- 2. With LoggingDataService ---")
    service = InMemoryDataService()
    logged = LoggingDataService(service, prefix="DS")
    logged.write("config:debug", "true")
    logged.read("config:debug")
    logged.read("config:missing")
    logged.delete("config:debug")
    logged.delete("config:debug")   # second delete → NOT_FOUND

    # --- 3. Stacked: CachingDataService(LoggingDataService(InMemoryDataService)) ---
    print("\n--- 3. Stacked: Cache → Log → Storage ---")
    base = InMemoryDataService()
    logged2 = LoggingDataService(base, prefix="STACK")
    cached = CachingDataService(logged2, max_size=50)

    # Write some data
    cached.write("product:101", "Widget A")
    cached.write("product:102", "Widget B")

    print("\nFirst reads (cache miss → goes to log → goes to storage):")
    r1 = cached.read("product:101")
    r2 = cached.read("product:102")

    print(f"\nRead results: {r1}, {r2}")
    print("Cache stats after first reads:", cached.stats)

    print("\nSecond reads (cache hit → no log, no storage call):")
    r1b = cached.read("product:101")
    r2b = cached.read("product:102")
    print(f"Read results: {r1b}, {r2b}")
    print("Cache stats after second reads:", cached.stats)

    print(f"\nUnderlying storage call_count: {base.call_count}")
    print("(writes=2, reads=2 cache misses, delete=0 → expected: 4)")

    # Demonstrate cache invalidation on delete
    print("\n--- 4. Cache Invalidation ---")
    cached.delete("product:101")
    print("After delete, re-reading product:101...")
    val = cached.read("product:101")
    print(f"Result: {val}")
    print("Cache stats:", cached.stats)

    print("\nDone.")
