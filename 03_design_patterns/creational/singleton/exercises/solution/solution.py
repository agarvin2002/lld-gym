"""
Singleton Pattern Exercise - Solution
======================================

Thread-safe ApplicationConfig singleton using double-checked locking.

Key design decisions:
    1. __new__ controls instance creation (the singleton mechanism)
    2. _initialized flag prevents __init__ from resetting state on re-calls
    3. Two locks: _lock (singleton creation), _data_lock (data access)
    4. all() returns a copy to prevent external mutation
"""

import threading
from typing import Any, Optional


class ApplicationConfig:
    """
    A thread-safe singleton that holds application-wide configuration.

    Implemented using:
    - __new__ override with double-checked locking for singleton guarantee
    - _initialized flag to prevent repeated __init__ execution
    - threading.Lock for thread-safe data access

    Usage:
        config = ApplicationConfig({"key": "value"})  # First call: loads config
        config = ApplicationConfig()                   # Subsequent: returns same instance
        config.get("key")                              # Retrieve value
        config.set("key", "new_value")                 # Update value
    """

    _instance: Optional["ApplicationConfig"] = None
    _lock: threading.Lock = threading.Lock()  # Protects singleton creation

    def __new__(cls, config: Optional[dict[str, Any]] = None) -> "ApplicationConfig":
        """
        Double-checked locking for thread-safe singleton creation.

        FIRST CHECK (no lock): If instance already exists, return it immediately.
        This is the fast path — most calls will hit this after initialization.

        LOCK: Only acquired when instance might not exist yet.

        SECOND CHECK (inside lock): Between the first check and acquiring the lock,
        another thread might have created the instance. Check again before creating.
        """
        # First check — fast path, no lock overhead
        if cls._instance is None:
            with cls._lock:
                # Second check — inside lock, safe from race conditions
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize config data on first call only.

        Python calls __init__ every time ApplicationConfig() is called,
        even though __new__ returns the same object. The _initialized flag
        prevents re-initialization and state loss.
        """
        # Guard: only initialize once
        if hasattr(self, "_initialized") and self._initialized:
            return

        # Load the config (use provided dict or empty dict)
        self._config: dict[str, Any] = dict(config) if config else {}

        # Separate lock for data access (independent of creation lock)
        # This allows concurrent reads once the instance exists
        self._data_lock: threading.Lock = threading.Lock()

        # Mark as initialized so __init__ skips on subsequent calls
        self._initialized: bool = True

    def get(self, key: str, default: Any = None) -> Any:
        """
        Return the config value for key, or default if not found.

        Thread-safe: acquires _data_lock before reading.
        """
        with self._data_lock:
            return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Update a config value.

        Thread-safe: acquires _data_lock before writing.
        Visible through all references since all share the same object.
        """
        with self._data_lock:
            self._config[key] = value

    def all(self) -> dict[str, Any]:
        """
        Return a copy of the entire config dictionary.

        Returns a COPY to prevent external code from mutating
        the internal dict without going through set().
        Thread-safe: acquires _data_lock.
        """
        with self._data_lock:
            return dict(self._config)

    def __repr__(self) -> str:
        return f"<ApplicationConfig keys={list(self._config.keys())} id={id(self)}>"


# =============================================================================
# Demonstration
# =============================================================================

if __name__ == "__main__":
    import time

    print("=" * 60)
    print("ApplicationConfig Singleton - Solution Demo")
    print("=" * 60)

    # Basic usage
    print("\n--- Basic Singleton Behavior ---")
    config1 = ApplicationConfig({
        "database_url": "postgresql://localhost/mydb",
        "debug": True,
        "max_connections": 10,
        "api_key": "secret-key-123",
    })

    config2 = ApplicationConfig({"database_url": "IGNORED — instance already exists"})

    print(f"config1 is config2: {config1 is config2}")
    print(f"config1.get('database_url'): {config1.get('database_url')}")
    print(f"config2.get('database_url'): {config2.get('database_url')}")
    print(f"config1.get('missing'): {config1.get('missing')}")
    print(f"config1.get('missing', 'fallback'): {config1.get('missing', 'fallback')}")

    # Set visibility
    print("\n--- set() Visibility Across References ---")
    config1.set("debug", False)
    print(f"After config1.set('debug', False):")
    print(f"  config2.get('debug'): {config2.get('debug')}")  # False

    # all() is a copy
    print("\n--- all() Returns a Copy ---")
    snapshot = config1.all()
    snapshot["api_key"] = "MUTATED"
    print(f"After mutating snapshot['api_key']:")
    print(f"  config1.get('api_key'): {config1.get('api_key')}")  # Still "secret-key-123"

    # Thread safety demonstration
    print("\n--- Thread Safety (20 concurrent threads) ---")
    ApplicationConfig._instance = None  # Reset for demo

    instance_ids: list[int] = []
    lock = threading.Lock()

    def create_config(thread_id: int) -> None:
        cfg = ApplicationConfig({"thread_id": thread_id})
        with lock:
            instance_ids.append(id(cfg))

    threads = [
        threading.Thread(target=create_config, args=(i,))
        for i in range(20)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    unique = set(instance_ids)
    print(f"Threads launched: 20")
    print(f"Unique instance IDs: {len(unique)}")
    print(f"Thread-safe: {len(unique) == 1}")
