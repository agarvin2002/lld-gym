# Proxy Pattern

## What Is It?

The Proxy pattern provides a **surrogate or placeholder** for another object to control access to it. A proxy implements the same interface as the real object, so clients treat both identically. The proxy intercepts calls and decides whether (and how) to forward them to the real object.

In code form: you call `proxy.do_something()` — the proxy may check permissions, log the call, consult a cache, defer initialization, or simply forward directly. The caller never knows the difference.

```
Client  →  Proxy  →  RealSubject
              ↓
           (adds control: caching, auth, logging, lazy init, ...)
```

---

## Analogy

Think of a **bank teller** standing between you and the bank vault.

You ask the teller (proxy) to deposit £500. The teller:
1. Checks your ID (protection proxy).
2. Records the transaction in a log (logging proxy).
3. Only opens the vault if necessary (virtual/lazy proxy).

You never interact with the vault directly. The teller implements the same "banking interface" you expect, but adds layers of control without changing what you ask for.

Another analogy: a **credit card** is a proxy for your bank account. Same outcome (payment), but with fraud checks, spending limits, and a transaction log layered in between.

---

## Why It Matters

**Without Proxy**, access control, caching, and logging logic leaks into every call site:

```python
# Without proxy — messy, violates SRP
def run_report():
    if current_user not in allowed:        # ← access control mixed in
        raise PermissionError
    key = "report_data"
    if key in cache:                       # ← caching mixed in
        return cache[key]
    log.info(f"querying DB for {key}")     # ← logging mixed in
    result = real_db.query("SELECT ...")
    cache[key] = result
    return result
```

**With Proxy**, each concern lives in its own class, and the call site is clean:

```python
# With proxy — clean, composable
def run_report():
    return db.query("SELECT ...")          # db is whatever proxy the DI container gave us
```

Proxy satisfies three principles:
- **Single Responsibility**: each proxy class handles one cross-cutting concern.
- **Open/Closed**: add caching by wrapping in `CachingProxy` — no edits to existing code.
- **Interface Segregation / Dependency Inversion**: callers depend on the abstract interface, not the concrete implementation.

---

## Three Main Proxy Types

### 1. Virtual Proxy (Lazy Initialisation)
The real object is expensive to create. The proxy holds a reference to `None` and creates the real object only on the first call.

```
first call → proxy creates real object → forwards
later calls → real object exists → forwards directly
```

**Use case**: loading a large image, opening a database connection, parsing a config file.

### 2. Protection Proxy (Access Control)
The proxy holds a list of permitted users/roles. Before forwarding, it checks credentials.

```
call with user → proxy checks permissions → PermissionError OR forward
```

**Use case**: admin-only operations, API rate limiting, role-based access control.

### 3. Logging / Caching Proxy
The proxy records what operations are performed (logging) or stores results and returns them without hitting the real object again (caching).

```
Caching:  same query twice → second call returns cached result
Logging:  every call → append to log before/after forwarding
```

These two are often combined because they are purely additive.

---

## Python-Specific Notes

### Implementing via ABC
Define the subject interface as an `ABC`, then implement both the real class and the proxy:

```python
from abc import ABC, abstractmethod

class Subject(ABC):
    @abstractmethod
    def operation(self) -> str: ...

class RealSubject(Subject):
    def operation(self) -> str:
        return "real work"

class Proxy(Subject):
    def __init__(self, real: Subject) -> None:
        self._real = real

    def operation(self) -> str:
        # add cross-cutting concern here
        return self._real.operation()
```

### Python's `__getattr__` for Dynamic Proxies
Python allows "magic" proxies that forward *any* attribute automatically, without implementing every method:

```python
class LoggingProxy:
    def __init__(self, target):
        object.__setattr__(self, '_target', target)
        object.__setattr__(self, '_log', [])

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                self._log.append(name)
                return attr(*args, **kwargs)
            return wrapper
        return attr
```

This is powerful but hides the interface — prefer explicit ABC-based proxies for anything that crosses a module boundary or needs type checking.

### Dataclasses
Proxy classes rarely need `@dataclass` because they almost always contain mutable state (`_cache`, `_log`) and rely on constructor injection, making a plain `__init__` cleaner.

### Type Hints
Always annotate the wrapped subject using the abstract type, not the concrete type, to enable swappable chains:

```python
class CachingProxy(Database):
    def __init__(self, real: Database) -> None:  # ← uses ABC type
        ...
```

This allows a `LoggingProxy(CachingProxy(RealDatabase(...)))` chain where each layer sees only the `Database` interface.

---

## When to Use

| Situation | Proxy Type |
|-----------|------------|
| Expensive object, defer creation | Virtual / Lazy |
| Restrict callers by role | Protection |
| Record every call for audit/debug | Logging |
| Repeated identical queries | Caching |
| Remote object behind a network | Remote (RPC stubs) |
| Count references for GC | Smart Reference |

## When to Avoid

- When the real object is cheap and there are no cross-cutting concerns — a proxy just adds indirection noise.
- When you need deep inspection of arguments — middleware pipelines or decorator chains are more composable.
- When your language already provides the mechanism built-in (e.g., Python's `functools.lru_cache` handles caching callables natively).

---

## Quick Example

```python
from abc import ABC, abstractmethod

class FileReader(ABC):
    @abstractmethod
    def read(self, path: str) -> str: ...


class RealFileReader(FileReader):
    def read(self, path: str) -> str:
        with open(path) as f:
            return f.read()


class CachingFileReader(FileReader):
    """Virtual + Caching proxy: only reads the file once per path."""

    def __init__(self, real: FileReader) -> None:
        self._real = real
        self._cache: dict[str, str] = {}
        self._hits = 0

    def read(self, path: str) -> str:
        if path in self._cache:
            self._hits += 1
            return self._cache[path]
        result = self._real.read(path)
        self._cache[path] = result
        return result

    @property
    def cache_hits(self) -> int:
        return self._hits


# Usage — same interface, extra behaviour transparent to client
reader: FileReader = CachingFileReader(RealFileReader())
content = reader.read("/etc/hosts")
content_again = reader.read("/etc/hosts")  # served from cache
```

---

## Composing Multiple Proxies

Proxies are composable because each one implements the same interface:

```python
real = RealDatabase("postgres://...")
cached = CachingDatabaseProxy(real)        # caches results
logged = LoggingDatabaseProxy(cached)      # logs every call
protected = ProtectedDatabaseProxy(logged, allowed_users=["alice"])

# Protected → Logged → Cached → Real
result = protected.query("SELECT 1", user="alice")
```

The order matters: put `ProtectedProxy` outermost (fail fast), `LoggingProxy` second (log all allowed requests), `CachingProxy` innermost (avoid hitting the real DB).

---

## Comparison with Similar Patterns

| Pattern | Similarity | Difference |
|---------|-----------|------------|
| **Decorator** | Wraps an object, same interface | Decorator *adds behaviour*; Proxy *controls access* |
| **Adapter** | Wraps an object | Adapter *changes the interface*; Proxy *keeps it identical* |
| **Facade** | Hides complexity | Facade wraps a *subsystem*; Proxy wraps *one object* |

The practical line between Proxy and Decorator blurs — a caching proxy is functionally identical to a caching decorator. The distinction is intent: proxy is about *access control and lifecycle*, decorator is about *behavioural enrichment*.

---

## Common Mistakes

1. **Breaking the interface**: A proxy that adds extra parameters (e.g., `query(sql, user)`) on a method that the ABC defines as `query(sql)` is no longer transparent. Use a separate "authentication context" or a subtype if you must change the signature.

2. **Cache invalidation neglect**: A caching proxy that never expires entries causes stale data bugs. Always implement `clear_cache()` and consider TTL (time-to-live) for production use.

3. **Forgetting thread safety**: A cache protected by no lock will have race conditions under concurrent access. Use `threading.Lock` around cache reads and writes.

4. **Deep proxy chains causing obscure errors**: If five proxies wrap the same object, a `PermissionError` raised three levels in can be hard to trace. Log the chain or name proxies descriptively.

5. **Proxy as God Object**: Some developers put auth, logging, caching, and rate limiting all in one proxy class. This violates SRP — use one proxy per concern and compose them.

6. **Returning `None` from a protection proxy instead of raising**: Callers cannot distinguish "no data" from "access denied". Always raise `PermissionError` explicitly.

---

## Summary

```
Interface (ABC)
    ├── RealSubject      — actual work
    └── Proxy            — controls access to RealSubject
          ├── VirtualProxy      — lazy init
          ├── ProtectionProxy   — auth check
          ├── LoggingProxy      — audit trail
          └── CachingProxy      — avoid redundant calls
```

The power of Proxy is that it makes cross-cutting concerns **invisible to callers** while keeping them **fully testable in isolation**.

---

## LLD Problems That Use This Pattern

| Problem | Proxy | Real subject | Proxy type |
|---------|-------|-------------|-----------|
| [11 Rate Limiter](../../../04_lld_problems/11_rate_limiter/) | `RateLimiterService` | The actual API handler | Protection proxy |
| [12 LRU Cache](../../../04_lld_problems/12_lru_cache/) | `ThreadSafeLRUCache` / `ThreadSafeLFUCache` | `LRUCache` / `LFUCache` | Protection proxy (thread safety) |
| [14 Logging Framework](../../../04_lld_problems/14_logging_framework/) | `LogHandler` chain | Output sink (`ConsoleHandler.emit()`) | Logging proxy |

**Clearest example:** LRU Cache — `ThreadSafeLRUCache` is a textbook Protection Proxy wrapping a cache object with a `threading.Lock`.
