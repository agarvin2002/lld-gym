# Exercise: Thread-Safe ApplicationConfig Singleton

## Problem Statement

You are building a web application. Multiple components — the database layer, the authentication module, the API handlers, and the cache layer — all need to read configuration values. Configuration is loaded from a dictionary once at startup and should not be reloaded.

Your task is to implement an `ApplicationConfig` class that:

1. **Is a Singleton** — only one instance ever exists, no matter how many times `ApplicationConfig()` is called.
2. **Loads configuration on first access** — the config is passed as a dictionary the first time and cached forever after.
3. **Returns cached values** — subsequent calls return the already-loaded config without reloading.
4. **Is thread-safe** — safe to use from multiple threads simultaneously.
5. **Supports `get(key, default=None)`** — retrieve a config value by key; return `default` if not found.
6. **Supports `set(key, value)`** — update a config value at runtime (must also be thread-safe).

## Interface

```python
class ApplicationConfig:
    def __init__(self, config: dict | None = None) -> None:
        """
        If this is the first instantiation, load config from the provided dict.
        If config is already loaded, ignore the argument and return existing data.
        """
        ...

    def get(self, key: str, default=None):
        """Return the value for key, or default if not found."""
        ...

    def set(self, key: str, value) -> None:
        """Update a config value. Thread-safe."""
        ...

    def all(self) -> dict:
        """Return a copy of the entire config."""
        ...
```

## Requirements

### Functional Requirements
- `ApplicationConfig()` always returns the same object
- The first call with a config dict loads it; subsequent calls ignore the dict argument
- `get("key")` returns the value or `None` by default
- `get("key", "default_val")` returns `"default_val"` if key is missing
- `set("key", value)` updates the value and is visible through all references
- `all()` returns a copy (not the live dict — prevent external mutation)

### Non-Functional Requirements
- **Thread-safe**: use `threading.Lock` for all reads and writes
- **No global variables** outside the class
- All public methods must have type hints

## Example Usage

```python
# First call: loads config
config1 = ApplicationConfig({
    "database_url": "postgresql://localhost/mydb",
    "debug": True,
    "max_connections": 10,
    "api_key": "secret-key-123",
})

# Second call: ignores argument, returns same instance
config2 = ApplicationConfig({"database_url": "this_will_be_ignored"})

assert config1 is config2  # Same object

print(config1.get("database_url"))  # postgresql://localhost/mydb
print(config2.get("debug"))         # True
print(config1.get("missing_key"))   # None
print(config1.get("missing_key", "fallback"))  # fallback

config1.set("debug", False)
print(config2.get("debug"))  # False — same object, visible via config2
```

## Constraints

- Do not use any external libraries (only `threading` from the standard library)
- Do not use `@singleton` decorator from the examples — implement your own mechanism
- The `_instance` class variable must be private (single underscore prefix)
- Use double-checked locking for thread safety

## Thread-Safety Test Scenario

Your implementation must pass this test (included in `tests.py`):

```python
import threading

results = []

def create_config(initial_data):
    cfg = ApplicationConfig(initial_data)
    results.append(id(cfg))

threads = [
    threading.Thread(target=create_config, args=({"key": f"value_{i}"},))
    for i in range(50)
]
for t in threads: t.start()
for t in threads: t.join()

# All 50 threads must have received the same instance
assert len(set(results)) == 1, "Multiple instances were created!"
```

## Files

- `starter.py` — skeleton with stubs, fill in the implementation
- `tests.py` — run with `python tests.py` to verify your solution
- `solution/solution.py` — reference solution (look only after attempting)
- `solution/explanation.md` — walkthrough of design decisions
