"""
Singleton Pattern Exercise - Starter File
==========================================

Your task: Implement a thread-safe ApplicationConfig singleton.

Read problem.md for the full requirements before starting.

Instructions:
    1. Fill in the __init__, get, set, and all methods
    2. Implement the singleton mechanism (hint: __new__ or a class-level _instance)
    3. Add thread safety with threading.Lock
    4. Run tests.py to verify: python tests.py
"""

import threading
from typing import Any, Optional


class ApplicationConfig:
    """
    A thread-safe singleton that holds application-wide configuration.

    Usage:
        config = ApplicationConfig({"key": "value"})  # loads config
        config = ApplicationConfig()                   # returns same instance
        config.get("key")                              # retrieve value
        config.set("key", "new_value")                 # update value
    """

    # TODO: Add class-level variable(s) for the singleton instance
    # Hint: _instance = None

    # TODO: Add a threading.Lock for thread safety
    # Hint: _lock = threading.Lock()

    def __new__(cls, config: Optional[dict[str, Any]] = None) -> "ApplicationConfig":
        """
        Override __new__ to implement the singleton mechanism.

        Steps:
        1. Check if _instance is None (first check — no lock)
        2. If None, acquire the lock
        3. Check again if _instance is None (second check — inside lock)
        4. If still None, create the instance with super().__new__(cls)
        5. Return _instance

        Hint: Use double-checked locking pattern.
        """
        # TODO: Implement double-checked locking here
        pass

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the config on first call only.

        The challenge: __init__ runs every time ApplicationConfig() is called,
        even though __new__ returns the same object.

        Use a flag (e.g., _initialized) to guard against re-initialization.

        Steps:
        1. Check if already initialized — if so, return immediately
        2. Set self._config = config or {}
        3. Set self._data_lock = threading.Lock() (for protecting reads/writes)
        4. Set self._initialized = True
        """
        # TODO: Implement guarded initialization
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """
        Return the config value for key, or default if not found.

        Must be thread-safe (use self._data_lock).
        """
        # TODO: Implement thread-safe get
        pass

    def set(self, key: str, value: Any) -> None:
        """
        Update a config value.

        Must be thread-safe (use self._data_lock).
        """
        # TODO: Implement thread-safe set
        pass

    def all(self) -> dict[str, Any]:
        """
        Return a copy of the entire config dictionary.

        Return a COPY, not the live dict (prevent external mutation).
        Must be thread-safe.
        """
        # TODO: Implement thread-safe all()
        pass

    def __repr__(self) -> str:
        return f"<ApplicationConfig keys={list(self._config.keys())} id={id(self)}>"


# =============================================================================
# Manual smoke test — run this file directly to see basic behavior
# =============================================================================

if __name__ == "__main__":
    # Reset for a clean test (you'd never do this in production)
    ApplicationConfig._instance = None  # type: ignore

    print("Creating config1 with initial data...")
    config1 = ApplicationConfig({
        "database_url": "postgresql://localhost/mydb",
        "debug": True,
        "max_connections": 10,
    })

    print("Creating config2 (should return same instance)...")
    config2 = ApplicationConfig({"database_url": "IGNORED"})

    print(f"\nconfig1 is config2: {config1 is config2}")
    print(f"config1.get('database_url'): {config1.get('database_url')}")
    print(f"config2.get('database_url'): {config2.get('database_url')}")
    print(f"config1.get('missing', 'fallback'): {config1.get('missing', 'fallback')}")

    config1.set("debug", False)
    print(f"\nAfter config1.set('debug', False):")
    print(f"config2.get('debug'): {config2.get('debug')}")  # Should be False
