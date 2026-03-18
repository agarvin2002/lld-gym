"""
Decorator Pattern - Example 1: Logging and Caching Decorators

Scenario:
    DataService provides read/write operations on a key-value store.
    We want to add:
    1. Logging: log every call with timestamp and result
    2. Caching: cache read results, skip re-fetching same key

    These concerns are composable and transparent to the client.

Real-world use: Redis caching layers and audit-log decorators in Flipkart/Amazon
product catalogue services — the underlying DB service is unchanged.
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
    def read(self, key: str) -> Optional[str]: ...

    @abstractmethod
    def write(self, key: str, value: str) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> bool: ...

    @abstractmethod
    def exists(self, key: str) -> bool: ...


# ---------------------------------------------------------------------------
# Concrete Component
# ---------------------------------------------------------------------------

class InMemoryDataService(DataService):
    """Real data service backed by an in-memory dictionary."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._call_count = 0

    def read(self, key: str) -> Optional[str]:
        self._call_count += 1
        time.sleep(0.05)   # simulate slow storage
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
# Base Decorator — forwards all calls; subclasses override what they need
# ---------------------------------------------------------------------------

class DataServiceDecorator(DataService):
    """
    Base decorator. Holds a reference and forwards every call.
    Subclasses override only the methods they care about.
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
# Decorator 1: Logging
# ---------------------------------------------------------------------------

class LoggingDataService(DataServiceDecorator):
    """Logs every read/write/delete with a timestamp."""

    def __init__(self, wrapped: DataService, prefix: str = "LOG") -> None:
        super().__init__(wrapped)
        self._prefix = prefix
        self._log: list[str] = []

    def _record(self, operation: str, details: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{self._prefix}] {ts} | {operation} | {details}"
        self._log.append(entry)
        print(entry)

    def read(self, key: str) -> Optional[str]:
        result = self._wrapped.read(key)
        self._record("READ ", f"key='{key}' → {'MISS' if result is None else repr(result)}")
        return result

    def write(self, key: str, value: str) -> None:
        self._wrapped.write(key, value)
        self._record("WRITE", f"key='{key}', value='{value}'")

    def delete(self, key: str) -> bool:
        result = self._wrapped.delete(key)
        self._record("DEL  ", f"key='{key}' → {'DELETED' if result else 'NOT_FOUND'}")
        return result

    @property
    def logs(self) -> list[str]:
        return list(self._log)


# ---------------------------------------------------------------------------
# Decorator 2: Caching
# ---------------------------------------------------------------------------

class CachingDataService(DataServiceDecorator):
    """
    Caches read results in memory.
    - On read: return cached value if present; otherwise fetch and cache.
    - On write/delete: evict the relevant key from cache.
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
        self._cache.pop(key, None)   # invalidate stale entry
        self._wrapped.write(key, value)

    def delete(self, key: str) -> bool:
        self._cache.pop(key, None)   # invalidate stale entry
        return self._wrapped.delete(key)

    @property
    def stats(self) -> dict:
        total = self._hits + self._misses
        rate = self._hits / total if total > 0 else 0.0
        return {"hits": self._hits, "misses": self._misses, "hit_rate": f"{rate:.1%}"}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Stack: CachingDataService → LoggingDataService → InMemoryDataService
    base   = InMemoryDataService()
    logged = LoggingDataService(base, prefix="STORE")
    cached = CachingDataService(logged, max_size=50)

    cached.write("user:1", "Alice")
    cached.write("user:2", "Bob")

    print("\nFirst reads (cache miss → hits log → hits storage):")
    print(cached.read("user:1"))
    print(cached.read("user:2"))
    print("Stats:", cached.stats)

    print("\nSecond reads (cache hit — log and storage not called):")
    print(cached.read("user:1"))
    print(cached.read("user:2"))
    print("Stats:", cached.stats)

    print(f"\nUnderlying storage calls: {base.call_count}")

    print("\nCache invalidation on delete:")
    cached.delete("user:1")
    print("Re-read user:1:", cached.read("user:1"))
    print("Stats:", cached.stats)
