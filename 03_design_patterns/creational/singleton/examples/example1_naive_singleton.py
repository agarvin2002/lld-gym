"""
Singleton Pattern - Example 1: Three Ways to Implement Singleton in Python
==========================================================================

This module demonstrates three approaches to implementing the Singleton pattern:
    1. Module-level singleton (simplest, most Pythonic)
    2. __new__ override (class-level control)
    3. Decorator-based singleton (reusable, clean syntax)

Real-world use: app config objects, feature flag services, database connection pools.
"""

from __future__ import annotations
from typing import Any, Optional


# =============================================================================
# APPROACH 1: Module-Level Singleton
# =============================================================================
# Python modules are cached after the first import. Every subsequent
# `import module` returns the SAME module object from sys.modules.
# Module-level state IS a singleton — no extra code needed.
# =============================================================================

class _AppSettings:
    """
    Application-wide settings object.
    The underscore prefix signals this is an implementation detail.
    External code should use the module-level `app_settings` instance below.
    """

    def __init__(self) -> None:
        self._settings: dict[str, Any] = {
            "app_name": "MyApp",
            "version": "1.0.0",
            "debug": False,
            "max_retries": 3,
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def __repr__(self) -> str:
        return f"<_AppSettings id={id(self)}>"


# This module-level instance IS the singleton.
app_settings = _AppSettings()


# =============================================================================
# APPROACH 2: __new__ Override
# =============================================================================
# Python creates objects in two steps:
#   1. __new__(cls) — allocates and returns the new object
#   2. __init__(self) — initialises the returned object
#
# Override __new__ to return a cached instance instead of a fresh one.
# TIP: __init__ still runs every time — guard with _initialized flag.
# =============================================================================

class DatabaseConfig:
    """
    Database configuration singleton via __new__ override.

    _instance stores the single object at class level.
    _initialized flag prevents __init__ from resetting state on re-calls.
    """

    _instance: Optional[DatabaseConfig] = None
    _initialized: bool = False

    def __new__(cls) -> DatabaseConfig:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print(f"[DatabaseConfig] New instance: id={id(cls._instance)}")
        else:
            print(f"[DatabaseConfig] Returning existing: id={id(cls._instance)}")
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.host: str = "localhost"
        self.port: int = 5432
        self.database: str = "myapp_db"
        self.pool_size: int = 10
        self._initialized = True

    def connection_string(self) -> str:
        return f"postgresql://{self.host}:{self.port}/{self.database}"

    def __repr__(self) -> str:
        return f"<DatabaseConfig host={self.host} db={self.database} id={id(self)}>"


# =============================================================================
# APPROACH 3: Decorator-Based Singleton
# =============================================================================
# A decorator wraps the class. The closure `instances` dict caches the first
# instance and returns it on every subsequent call.
#
# Advantage: clean @singleton syntax, reusable for any class.
# Disadvantage: isinstance() checks and subclassing break.
# =============================================================================

def singleton(cls: type) -> Any:
    """Class decorator that makes any class a singleton."""
    instances: dict[type, Any] = {}

    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            print(f"[@singleton] Creating first instance of {cls.__name__}")
            instances[cls] = cls(*args, **kwargs)
        else:
            print(f"[@singleton] Returning cached instance of {cls.__name__}")
        return instances[cls]

    get_instance.__name__ = cls.__name__
    get_instance.__doc__ = cls.__doc__
    return get_instance


@singleton
class Logger:
    """Application-wide logger. All components share this single instance."""

    def __init__(self, name: str = "app") -> None:
        self.name = name
        self.log_level: str = "INFO"
        self._entries: list[str] = []

    def info(self, message: str) -> None:
        entry = f"[INFO]  [{self.name}] {message}"
        self._entries.append(entry)
        print(entry)

    def error(self, message: str) -> None:
        entry = f"[ERROR] [{self.name}] {message}"
        self._entries.append(entry)
        print(entry)

    def get_all_entries(self) -> list[str]:
        return list(self._entries)

    def __repr__(self) -> str:
        return f"<Logger name={self.name} entries={len(self._entries)} id={id(self)}>"


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_module_singleton() -> None:
    print("\n" + "=" * 60)
    print("APPROACH 1: Module-Level Singleton")
    print("=" * 60)
    settings1 = app_settings
    settings2 = app_settings
    print(f"settings1 is settings2: {settings1 is settings2}")  # True
    print(f"app_name: {settings1.get('app_name')}")


def demonstrate_new_override() -> None:
    print("\n" + "=" * 60)
    print("APPROACH 2: __new__ Override")
    print("=" * 60)
    db1 = DatabaseConfig()
    db2 = DatabaseConfig()
    print(f"db1 is db2: {db1 is db2}")  # True
    db1.host = "production-server.example.com"
    print(f"db2.host after modifying db1: {db2.host}")  # same object


def demonstrate_decorator_singleton() -> None:
    print("\n" + "=" * 60)
    print("APPROACH 3: Decorator-Based Singleton")
    print("=" * 60)
    logger1 = Logger("myapp")
    logger2 = Logger("different-name")  # argument ignored — returns cached instance
    print(f"logger1 is logger2: {logger1 is logger2}")  # True
    print(f"logger2.name: {logger2.name}")  # "myapp" — not "different-name"!
    logger1.info("Application started")
    logger2.error("Logged via logger2")
    print(f"Total entries: {len(logger1.get_all_entries())}")


if __name__ == "__main__":
    demonstrate_module_singleton()
    demonstrate_new_override()
    demonstrate_decorator_singleton()
