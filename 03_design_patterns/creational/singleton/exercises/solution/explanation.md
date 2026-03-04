# Solution Explanation: ApplicationConfig Singleton

## Overview

The solution implements a thread-safe Singleton using `__new__` override with double-checked locking. Here is a walkthrough of each design decision.

## Decision 1: Why `__new__` Instead of a Decorator or Metaclass?

The problem specifically asks to implement your own mechanism. `__new__` is the most transparent approach — it's clearly visible in the class body, it works with `isinstance()`, and subclassing works correctly.

A metaclass would also work and is arguably cleaner for production code. The decorator approach is elegant but breaks `isinstance()`.

## Decision 2: Two Separate Locks

```python
_lock: threading.Lock = threading.Lock()      # class-level: protects creation
self._data_lock: threading.Lock = threading.Lock()  # instance-level: protects data
```

Why two locks? They protect different things at different times:

- `_lock` is a **class-level lock** used only during the brief window of instance creation. Once the instance exists, this lock is never contended.
- `_data_lock` is an **instance-level lock** used on every `get()`, `set()`, and `all()` call. It protects concurrent reads and writes to `_config`.

Using a single lock for both would work but is less clean — the creation lock would be repurposed for data access, which is semantically confusing.

## Decision 3: The `_initialized` Flag

```python
def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
    if hasattr(self, "_initialized") and self._initialized:
        return
    ...
    self._initialized = True
```

Python's object protocol calls `__init__` every time the class is "called" (i.e., `ApplicationConfig()`), even though `__new__` returned the cached instance. Without the guard:

```python
# Without guard — BROKEN:
config1 = ApplicationConfig({"url": "postgresql://localhost"})
config2 = ApplicationConfig({})  # __init__ runs again!
# _config is now {} — all data lost!
```

The `hasattr` check handles the very first call when `_initialized` doesn't exist yet on the instance.

## Decision 4: Double-Checked Locking

```python
def __new__(cls, config=None):
    if cls._instance is None:           # First check (no lock)
        with cls._lock:                  # Acquire lock
            if cls._instance is None:    # Second check (inside lock)
                cls._instance = super().__new__(cls)
    return cls._instance
```

Why two checks? Consider 50 threads all arriving at the same moment:

1. All 50 threads reach the first `if cls._instance is None` check simultaneously. All find `None`. All proceed toward the lock.
2. Thread #1 acquires the lock. Creates the instance. Releases the lock.
3. Threads #2-50 each acquire the lock (one at a time). Without the second check, they would each create a new instance! The second check prevents this.
4. After initialization, all 50+ future threads hit the first check, find an instance, and return immediately — no lock overhead.

The first check is the **fast path** optimization. The second check is the **correctness guarantee**.

## Decision 5: `all()` Returns a Copy

```python
def all(self) -> dict[str, Any]:
    with self._data_lock:
        return dict(self._config)  # copy, not self._config
```

If `all()` returned `self._config` directly, external code could do:

```python
data = config.all()
data["api_key"] = "hacked"  # this would mutate the internal dict!
```

Returning a copy (`dict(self._config)`) prevents this. The caller gets a snapshot. To update the config, they must use `set()`.

## Common Mistakes to Avoid

### Mistake 1: Forgetting the `_initialized` Guard
```python
# WRONG — __init__ resets state every time:
def __init__(self, config=None):
    self._config = config or {}  # Wipes existing config on second call!
```

### Mistake 2: Only One Check in `__new__`
```python
# WRONG — race condition: two threads both pass the check, both create instances:
def __new__(cls, config=None):
    with cls._lock:
        if cls._instance is None:  # Only one check
            cls._instance = super().__new__(cls)
    return cls._instance
# This is technically correct but slower — locks on every call, even after init
```

### Mistake 3: No Data Lock
```python
# WRONG — concurrent set() calls can corrupt the dict:
def set(self, key, value):
    self._config[key] = value  # Not thread-safe!
```

### Mistake 4: Returning the Live Dict from `all()`
```python
# WRONG — caller can mutate internal state:
def all(self):
    return self._config  # Returns reference, not copy!
```

## Testing Your Singleton

The key challenge in testing Singletons is **test isolation**. Each test needs a fresh instance. The solution: reset `_instance` in `setUp()`:

```python
def setUp(self):
    ApplicationConfig._instance = None
```

This is a testing-only hack. In production code, you'd never reset a singleton. For testable code in general, prefer dependency injection over singletons — pass the config object explicitly rather than having components call `ApplicationConfig()` directly.

## When Would You Use This in Production?

A config singleton makes sense when:
- Config is loaded once from environment/files at startup
- It's read-only after initialization (or changes are rare)
- Many parts of the codebase need it and threading through constructor args is impractical

A better production approach is a combination: use the singleton for storage, but inject it into classes rather than having them call `ApplicationConfig()` directly. This keeps the "single instance" guarantee while making dependencies explicit and testable.
