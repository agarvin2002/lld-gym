"""
Singleton Pattern - Example 1: Three Ways to Implement Singleton in Python
==========================================================================

This module demonstrates three approaches to implementing the Singleton pattern:
    1. Module-level singleton (simplest, most Pythonic)
    2. __new__ override (class-level control)
    3. Decorator-based singleton (reusable, clean syntax)

Each approach ensures only ONE instance of an object/class exists.
"""

from __future__ import annotations
from typing import Any, Optional


# =============================================================================
# APPROACH 1: Module-Level Singleton
# =============================================================================
# Python modules are cached after the first import. Every subsequent
# `import module` returns the SAME module object from sys.modules.
# This means module-level state IS a singleton — no extra code needed.
#
# This is the recommended approach for simple cases in Python.
# =============================================================================

class _AppSettings:
    """
    A settings object that holds application-wide configuration.
    The underscore prefix signals this class is an implementation detail.
    External code should use the module-level `app_settings` instance below.
    """

    def __init__(self) -> None:
        # These would normally be loaded from environment variables or a file
        self._settings: dict[str, Any] = {
            "app_name": "MyApp",
            "version": "1.0.0",
            "debug": False,
            "max_retries": 3,
        }
        print(f"[_AppSettings] Instance created: id={id(self)}")

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def __repr__(self) -> str:
        return f"<_AppSettings id={id(self)}>"


# This module-level instance IS the singleton.
# Every `import example1_naive_singleton` returns the same module,
# so `app_settings` is always the same object.
app_settings = _AppSettings()


# =============================================================================
# APPROACH 2: __new__ Override
# =============================================================================
# Python creates objects in two steps:
#   1. __new__(cls) — allocates and returns the new object
#   2. __init__(self) — initializes the returned object
#
# By overriding __new__, we intercept creation and return a cached instance
# instead of a fresh one. NOTE: __init__ still runs every time!
# That's why we guard _initialized with a flag.
# =============================================================================

class DatabaseConfig:
    """
    A database configuration singleton implemented via __new__ override.

    Key points:
    - _instance stores the single object (class-level variable)
    - __new__ returns the cached instance if it exists
    - _initialized flag prevents __init__ from resetting state on every call
    """

    _instance: Optional[DatabaseConfig] = None  # class-level cache
    _initialized: bool = False

    def __new__(cls) -> DatabaseConfig:
        if cls._instance is None:
            # No instance yet — create one the normal way
            cls._instance = super().__new__(cls)
            print(f"[DatabaseConfig] New instance allocated: id={id(cls._instance)}")
        else:
            print(f"[DatabaseConfig] Returning existing instance: id={id(cls._instance)}")
        return cls._instance

    def __init__(self) -> None:
        # IMPORTANT: __init__ runs every time DatabaseConfig() is called,
        # even though __new__ returns the same object. Without this guard,
        # calling DatabaseConfig() a second time would reset all state!
        if self._initialized:
            return

        self.host: str = "localhost"
        self.port: int = 5432
        self.database: str = "myapp_db"
        self.pool_size: int = 10
        self._initialized = True
        print(f"[DatabaseConfig] Initialized with host={self.host}, db={self.database}")

    def connection_string(self) -> str:
        return f"postgresql://{self.host}:{self.port}/{self.database}"

    def __repr__(self) -> str:
        return f"<DatabaseConfig host={self.host} db={self.database} id={id(self)}>"


# =============================================================================
# APPROACH 3: Decorator-Based Singleton
# =============================================================================
# A decorator is a function that wraps another function (or class).
# Here we create a `singleton` decorator that:
#   1. Intercepts class instantiation
#   2. Caches the first instance
#   3. Returns the cached instance on subsequent calls
#
# Advantage: clean syntax (@singleton), reusable for any class.
# Disadvantage: isinstance() and subclassing don't work as expected
#               because the class is replaced by a function.
# =============================================================================

def singleton(cls: type) -> Any:
    """
    A class decorator that makes any class a singleton.

    Replaces the class with a function that returns a cached instance.
    The closure `instances` dict persists as long as the decorated function
    (i.e., the original class name) is in scope.
    """
    instances: dict[type, Any] = {}

    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            print(f"[@singleton] Creating first instance of {cls.__name__}")
            instances[cls] = cls(*args, **kwargs)
        else:
            print(f"[@singleton] Returning cached instance of {cls.__name__}")
        return instances[cls]

    # Preserve the original class name and docstring for introspection
    get_instance.__name__ = cls.__name__
    get_instance.__doc__ = cls.__doc__

    return get_instance


@singleton
class Logger:
    """
    Application-wide logger singleton using the decorator approach.

    All components share this logger, ensuring logs go to one place.
    """

    def __init__(self, name: str = "app") -> None:
        self.name = name
        self.log_level: str = "INFO"
        self._entries: list[str] = []
        print(f"[Logger] Initialized logger '{self.name}'")

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

    # Import the module-level instance
    # (In real usage, you'd do: from example1_naive_singleton import app_settings)
    settings1 = app_settings
    settings2 = app_settings  # Same reference — same object

    print(f"\nsettings1: {settings1}")
    print(f"settings2: {settings2}")
    print(f"settings1 is settings2: {settings1 is settings2}")  # True
    print(f"id(settings1) == id(settings2): {id(settings1) == id(settings2)}")  # True

    print(f"\napp_name: {settings1.get('app_name')}")
    print(f"version: {settings1.get('version')}")
    print(f"unknown_key: {settings1.get('unknown_key', 'not found')}")


def demonstrate_new_override() -> None:
    print("\n" + "=" * 60)
    print("APPROACH 2: __new__ Override")
    print("=" * 60)

    print("\nCreating first DatabaseConfig...")
    db1 = DatabaseConfig()

    print("\nCreating second DatabaseConfig...")
    db2 = DatabaseConfig()

    print("\nCreating third DatabaseConfig...")
    db3 = DatabaseConfig()

    print(f"\ndb1: {db1}")
    print(f"db2: {db2}")
    print(f"db3: {db3}")

    print(f"\ndb1 is db2: {db1 is db2}")  # True
    print(f"db2 is db3: {db2 is db3}")  # True
    print(f"All same object: {db1 is db2 is db3}")  # True

    print(f"\nConnection string: {db1.connection_string()}")

    # Modifying via one reference is visible through all references
    db1.host = "production-server.example.com"
    print(f"\nAfter modifying db1.host to 'production-server.example.com':")
    print(f"db2.host (same object): {db2.host}")  # production-server.example.com
    print(f"Updated connection string: {db3.connection_string()}")


def demonstrate_decorator_singleton() -> None:
    print("\n" + "=" * 60)
    print("APPROACH 3: Decorator-Based Singleton")
    print("=" * 60)

    print("\nCreating first Logger...")
    logger1 = Logger("myapp")  # Arguments only matter on first call

    print("\nCreating second Logger (arguments ignored — returns cached instance)...")
    logger2 = Logger("different-name")  # This name is IGNORED

    print(f"\nlogger1: {logger1}")
    print(f"logger2: {logger2}")
    print(f"logger1 is logger2: {logger1 is logger2}")  # True
    print(f"logger2.name: {logger2.name}")  # "myapp" — not "different-name"!

    # Actions through any reference affect the single shared instance
    logger1.info("Application started")
    logger2.error("This error was logged via logger2")

    print(f"\nAll log entries (from the single logger instance):")
    for entry in logger1.get_all_entries():
        print(f"  {entry}")

    print(f"\nEntry count via logger1: {len(logger1.get_all_entries())}")
    print(f"Entry count via logger2: {len(logger2.get_all_entries())}")  # Same!


def compare_approaches() -> None:
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)

    print("""
    Approach          | Complexity | Subclassing | isinstance() | Testing
    ------------------|------------|-------------|--------------|--------
    Module-level      | Lowest     | N/A         | N/A          | Import mock
    __new__ override  | Low        | Supported   | Works        | Reset _instance
    Decorator         | Medium     | Not easy    | Broken       | Replace instances{}
    Metaclass         | High       | Supported   | Works        | Reset _instances{}

    RECOMMENDATION:
    - For simple state/config: module-level (most Pythonic)
    - For OOP with subclassing: metaclass
    - For quick class-level singleton: __new__
    - The decorator is elegant but has isinstance() gotchas
    """)


if __name__ == "__main__":
    demonstrate_module_singleton()
    demonstrate_new_override()
    demonstrate_decorator_singleton()
    compare_approaches()
