# Singleton Pattern

## 1. What Is It?

The **Singleton pattern** ensures that a class has **only one instance** and provides a **global access point** to that instance.

Two things bundled together:
1. **Single instance guarantee** — no matter how many times you try to create an object of this class, you always get back the same object.
2. **Global access** — that single instance is accessible from anywhere in the application.

### The Core Mechanism

In a normal class, every call to `ClassName()` creates a brand-new object. Singleton intercepts that process and returns the same object every time. The class itself controls its own instantiation.

```python
# Normal class — two different objects
a = SomeClass()
b = SomeClass()
assert a is not b  # True — different objects

# Singleton — same object every time
a = Singleton()
b = Singleton()
assert a is b  # True — same object
```

---

## 2. The Analogy

Think of a **country's government**. A country can only have one president (or prime minister, or head of state) at a time. No matter who you ask — a journalist, a diplomat, a citizen — they all refer to *the same* president.

The president's office is the **global access point**. The "only one at a time" rule is the **single instance guarantee**.

If the president resigns and a new one is elected, there's still only one. The role, the office, the position — singular.

Other everyday analogies:
- **Printer spooler**: one queue manages all print jobs, regardless of which application sends them
- **Registry**: Windows has one, system-wide
- **Logger**: one log file written to from all parts of an application

---

## 3. Use Cases

### When Singleton Makes Sense

**Configuration Manager**
```python
config = ConfigManager()
config.get("DATABASE_URL")  # loaded once, read from everywhere
```
Your app loads configuration from a file or environment once. Every component needs to read it. Singleton ensures they all see the same config, and you don't load the file a hundred times.

**Database Connection Pool**
Creating a database connection is expensive. A connection pool maintains a fixed set of reusable connections. You want one pool shared across the entire app — not one pool per module.

**Logger**
All parts of your application write to the same log file. A singleton logger ensures consistent formatting, a single file handle, and thread-safe writes.

**Thread Pool / Executor**
You want a fixed number of worker threads for the entire application. Creating multiple thread pools wastes resources and causes chaos.

**Registry / Service Locator**
A centralized registry of services or components. One registry, looked up from anywhere.

---

## 4. Python-Specific Implementations

Python gives you several ways to implement Singleton. Here they are, from simplest to most explicit.

### Approach 1: Module-Level Singleton (Recommended)

Python modules are **singletons by nature**. When you import a module, Python caches it. Every subsequent import returns the cached module object.

```python
# config_module.py
import os

_database_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
_debug = os.getenv("DEBUG", "false").lower() == "true"

def get(key: str):
    return globals().get(f"_{key}")
```

```python
# anywhere in your app
import config_module
url = config_module.get("database_url")
```

This is the idiomatic Python approach. Simple, readable, and leverages language semantics.

**When to use:** When your singleton is stateless or its state is set once at import time.

### Approach 2: `__new__` Override

Override `__new__` to return a cached instance instead of creating a new one.

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

Every call to `Singleton()` goes through `__new__`, finds the existing instance, and returns it. `__init__` still runs each time — a common gotcha.

### Approach 3: Metaclass

Define the singleton behavior once in a metaclass and reuse it across multiple singleton classes.

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    pass

class Config(metaclass=SingletonMeta):
    pass
```

### Approach 4: Decorator

A decorator that wraps any class and makes it a singleton.

```python
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabasePool:
    pass
```

### Thread Safety

In multi-threaded applications, two threads can simultaneously reach the `if _instance is None` check, both find it `None`, and both create an instance. Fix this with a lock:

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:          # First check (no lock — fast path)
            with cls._lock:                # Acquire lock
                if cls._instance is None:  # Second check (with lock — safe)
                    cls._instance = super().__new__(cls)
        return cls._instance
```

This is **double-checked locking**. The first check avoids acquiring the lock on every access (the common case after initialization). The second check inside the lock prevents a race condition during initialization.

---

## 5. Pros and Cons

### Pros

| Benefit | Explanation |
|---------|-------------|
| Controlled access | The class itself manages its single instance |
| Reduced memory | One object instead of many identical copies |
| Global consistency | All callers share the same state |
| Lazy initialization | Instance created only when first needed |

### Cons

| Drawback | Explanation |
|----------|-------------|
| Global state | Introduces shared mutable state — the root of many bugs |
| Testing difficulty | Hard to reset between tests; one test's state bleeds into another |
| Hidden dependencies | Code that uses a singleton hides its dependency; not explicit in the constructor |
| Violates SRP | The class manages both its purpose and its own instantiation lifecycle |
| Concurrency complexity | Requires careful thread-safe implementation |

---

## 6. Quick Example

```python
class ConfigManager:
    _instance = None
    _config: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Load config once
            cls._instance._config = {
                "database_url": "postgresql://localhost/mydb",
                "debug": False,
                "max_connections": 10,
            }
        return cls._instance

    def get(self, key: str, default=None):
        return self._config.get(key, default)


# Usage
config1 = ConfigManager()
config2 = ConfigManager()

assert config1 is config2  # Same object
print(config1.get("database_url"))  # postgresql://localhost/mydb
```

---

## 7. When NOT to Use Singleton

The Singleton is one of the **most overused and most criticized** patterns. Here's when to avoid it:

**Don't use Singleton when:**

1. **You just want convenience** — "I want to access this from anywhere." Use dependency injection instead. Pass the object explicitly.

2. **The object has meaningful variation** — If different parts of your app need different configurations (e.g., test config vs production config), Singleton breaks this.

3. **You're writing testable code** — Singletons make unit tests brittle. Use dependency injection so tests can inject mock objects.

4. **The "singleton" is an implementation detail** — If callers don't care whether it's shared or not, don't enforce it. Let the caller decide.

5. **You're working in a multi-process environment** — Each process gets its own Python interpreter and memory space. A "singleton" isn't shared across processes anyway.

### The Better Alternative: Dependency Injection

Instead of:
```python
# Everywhere in your code
def some_function():
    config = ConfigManager()  # hidden dependency
    return config.get("api_key")
```

Do:
```python
# Explicit dependency
def some_function(config: ConfigManager) -> str:
    return config.get("api_key")

# Wire up once at application startup
config = ConfigManager()
result = some_function(config)
```

This is testable, explicit, and flexible. The object happens to be shared — but that's not enforced by the Singleton pattern, it's controlled by *you*.

---

## Summary

| Aspect | Detail |
|--------|--------|
| Intent | Single instance + global access |
| Also known as | None (it's just Singleton) |
| Applicability | Config, logger, connection pool, registry |
| Python idiom | Module-level (simplest), `__new__`, metaclass |
| Thread safety | Double-checked locking with `threading.Lock` |
| Watch out | Testing, global state, overuse |
| Better alternative | Dependency injection |
