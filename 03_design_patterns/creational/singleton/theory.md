# Singleton Pattern

## What is it?

The Singleton pattern ensures a class has exactly one instance. Every call to
create the class returns the same object. The class controls its own
instantiation so callers cannot accidentally create duplicates.

## Analogy

A Zomato order tracker has one status screen for each order. No matter which
screen in the app you check from, the delivery status shown is always the same
single object tracking that order.

## Minimal code

```python
import threading

class AppConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:          # first check — no lock
            with cls._lock:
                if cls._instance is None:  # second check — inside lock
                    cls._instance = super().__new__(cls)
        return cls._instance

config1 = AppConfig()
config2 = AppConfig()
assert config1 is config2  # True — same object
```

The two `if` checks together are called **double-checked locking**. The first
skips the lock on every call after init (fast). The second prevents two threads
from both passing the first check and both creating an instance (safe).

## Real-world uses

- App config loaded once from environment variables, read everywhere
- Database connection pool shared across all request handlers
- Feature flag service (e.g. Flipkart A/B test config) initialised once at startup

## One mistake

`__init__` runs every time you call `AppConfig()`, even when `__new__` returns
the cached instance. Without a guard (`if self._initialized: return`), the
second call resets all your state.

## What to do next

- `examples/example1_naive_singleton.py` — three ways to implement Singleton
- `examples/example2_thread_safe_singleton.py` — double-checked locking in depth
- `exercises/starter.py` — build a thread-safe config singleton yourself
