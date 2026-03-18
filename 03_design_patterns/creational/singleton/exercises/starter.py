"""
WHAT YOU'RE BUILDING
====================
A thread-safe ApplicationConfig singleton.

The config is loaded once (on the first call) and shared across the entire app.
Every subsequent call to ApplicationConfig() returns the same object —
even from different threads.

Your class must support:
- ApplicationConfig({"key": "value"})  → first call, loads config
- ApplicationConfig()                  → subsequent calls, returns same instance
- config.get("key")                    → read a value
- config.set("key", "new_value")       → update a value
- config.all()                         → get a copy of the entire config dict

Read exercises/problem.md for full requirements.
"""

import threading
from typing import Any, Optional


class ApplicationConfig:
    """Thread-safe singleton that holds application-wide configuration."""

    # TODO: Add _instance = None  (stores the one shared object)
    # TODO: Add _lock = threading.Lock()  (protects creation in multi-threaded code)

    def __new__(cls, config: Optional[dict[str, Any]] = None) -> "ApplicationConfig":
        """
        Return the existing instance, or create one if this is the first call.

        Use double-checked locking:
          1. if cls._instance is None  → first check, no lock (fast path)
          2. with cls._lock            → acquire lock
          3. if cls._instance is None  → second check inside lock (safe creation)
          4. cls._instance = super().__new__(cls)
          5. return cls._instance
        """
        # TODO: Implement double-checked locking here
        # HINT: copy the 5-step pattern from the docstring above
        pass

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Set up the config dict on the very first call only.

        __init__ runs every time ApplicationConfig() is called, even when
        __new__ returned the cached instance. Use a flag to skip re-init.
        """
        # TODO: Return immediately if already initialised
        # HINT: if hasattr(self, '_initialized'): return

        # TODO: Set self._config = config if config is not None, else {}
        # TODO: Set self._data_lock = threading.Lock()  (protects reads/writes)
        # TODO: Set self._initialized = True
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for key, or default if the key does not exist."""
        # TODO: Acquire self._data_lock, then return self._config.get(key, default)
        # HINT: use  with self._data_lock:
        pass

    def set(self, key: str, value: Any) -> None:
        """Add or update a key in the config."""
        # TODO: Acquire self._data_lock, then set self._config[key] = value
        pass

    def all(self) -> dict[str, Any]:
        """
        Return a snapshot of the entire config.

        Must return a COPY so callers cannot mutate the live config dict.
        """
        # TODO: Acquire self._data_lock, then return a copy of self._config
        # HINT: dict(self._config)  or  self._config.copy()
        pass

    def __repr__(self) -> str:
        return f"<ApplicationConfig keys={list(self._config.keys())} id={id(self)}>"


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/creational/singleton/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
