# Thread-Safe Design Patterns

Thread safety means that code behaves correctly when called from multiple threads simultaneously. Python's Global Interpreter Lock (GIL) protects reference counts but does NOT protect compound operations, shared mutable state, or I/O-bound multi-threaded code.

---

## 1. Thread-safe Singleton — Double-Checked Locking

The Singleton pattern ensures only one instance of a class exists. Without synchronization, two threads can simultaneously see `_instance is None` and both create an instance.

**The Problem:**
```python
class BadSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:       # Thread A and B both reach here
            cls._instance = cls()       # Both create an instance — RACE CONDITION
        return cls._instance
```

**Double-Checked Locking Fix:**
```python
import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.connection_id = id(self)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:          # First check (no lock — fast path)
            with cls._lock:
                if cls._instance is None:  # Second check (with lock — safe)
                    cls._instance = cls()
        return cls._instance
```

**Why two checks?**
- The outer check avoids acquiring the lock on every call (performance).
- The inner check handles the case where two threads pass the outer check simultaneously — the second thread to acquire the lock sees the instance already created.

**Alternative — Module-level instance (Pythonic):**
```python
# singleton_module.py
class _DatabaseConnection:
    pass

_instance = _DatabaseConnection()   # Created once at import time

def get_instance():
    return _instance
```
Python's import system is thread-safe, so module-level singletons are safe without explicit locking.

---

## 2. Producer-Consumer — `queue.Queue`

The producer-consumer pattern decouples data production from data consumption using a thread-safe queue. Python's `queue.Queue` is fully thread-safe and handles all locking internally.

```python
import queue
import threading

def producer(q: queue.Queue, items: list):
    for item in items:
        q.put(item)           # Blocks if queue is full (if maxsize set)
    q.put(None)               # Sentinel: signal consumer to stop

def consumer(q: queue.Queue):
    while True:
        item = q.get()        # Blocks until item available
        if item is None:
            break
        process(item)
        q.task_done()         # Signal that item processing is complete

q = queue.Queue(maxsize=10)   # Bounded queue prevents memory overuse
t = threading.Thread(target=consumer, args=(q,))
t.start()
producer(q, range(100))
t.join()
```

**Key `queue.Queue` methods:**

| Method | Behavior |
|--------|----------|
| `put(item)` | Add item; blocks if full |
| `put_nowait(item)` | Add item; raises `Full` if full |
| `get()` | Remove item; blocks if empty |
| `get_nowait()` | Remove item; raises `Empty` if empty |
| `task_done()` | Signal item processed (used with `join()`) |
| `join()` | Block until all items have `task_done()` called |
| `qsize()` | Approximate size (not reliable for synchronization) |

**Multiple producers/consumers** — scale up by spawning more threads; the queue handles all coordination.

---

## 3. Thread-local Storage — `threading.local()`

Thread-local storage gives each thread its own independent copy of a variable. Changes in one thread are invisible to other threads. This is ideal for per-thread state like database connections, request contexts, or random number seeds.

```python
import threading

class RequestContext:
    _local = threading.local()   # One object, but per-thread attributes

    @classmethod
    def set(cls, user_id: str, request_id: str) -> None:
        cls._local.user_id = user_id
        cls._local.request_id = request_id

    @classmethod
    def get_user_id(cls) -> str:
        return getattr(cls._local, 'user_id', None)   # Default None if not set

    @classmethod
    def get_request_id(cls) -> str:
        return getattr(cls._local, 'request_id', None)
```

**Use cases:**
- Web framework request context (Flask's `g`, Django's `_thread_locals`)
- Database connection per thread (avoid connection sharing)
- Per-thread random number generators
- Logging context (user ID, correlation ID)

**Caution with thread pools:** Thread pool threads are reused. Always initialize thread-local values at the start of each task, not at thread creation.

---

## 4. Read-Write Lock

A read-write lock (RWLock) allows:
- **Multiple readers concurrently** (reads don't conflict with each other)
- **One exclusive writer** (writes conflict with reads and other writes)

Python's standard library has no RWLock. Build one with `threading.Condition`:

```python
import threading

class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        with self._read_ready:
            self._readers += 1

    def release_read(self):
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()   # Wake any waiting writers

    def acquire_write(self):
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()             # Wait for all readers to finish

    def release_write(self):
        self._read_ready.release()
```

**Usage pattern:**
```python
rw_lock = ReadWriteLock()

# Reader
rw_lock.acquire_read()
try:
    data = shared_cache[key]    # Safe to read concurrently
finally:
    rw_lock.release_read()

# Writer
rw_lock.acquire_write()
try:
    shared_cache[key] = value   # Exclusive write access
finally:
    rw_lock.release_write()
```

**When to use:** Read-heavy workloads (e.g., shared cache, configuration store) where contention on a plain `Lock` would hurt performance.

---

## 5. Thread-safe Observer / Event System

The observer pattern notifies multiple listeners when an event occurs. Thread safety requires protecting the listener list during mutation and avoiding holding the lock while calling handlers (to prevent deadlocks if a handler tries to subscribe/publish).

**The Snapshot Pattern:**
```python
import threading
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, handler) -> None:
        with self._lock:
            self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler) -> None:
        with self._lock:
            handlers = self._handlers.get(event_type, [])
            if handler in handlers:
                handlers.remove(handler)

    def publish(self, event_type: str, data=None) -> int:
        with self._lock:
            handlers = list(self._handlers.get(event_type, []))  # SNAPSHOT
        # Lock released before calling handlers — prevents deadlock
        for handler in handlers:
            handler(data)
        return len(handlers)
```

**Key insight:** Take a snapshot (copy) of the handler list while holding the lock, then release the lock before calling handlers. This allows handlers to safely call `subscribe`/`publish` without deadlocking.

---

## 6. `queue.Queue` vs `collections.deque`

| Feature | `queue.Queue` | `collections.deque` |
|---------|---------------|---------------------|
| Thread-safe | Yes (built-in locking) | Partially (`appendleft`/`pop` are atomic due to GIL, but not compound ops) |
| Blocking `get` | Yes (`get()` blocks until item available) | No (raises `IndexError` immediately) |
| Bounded size | Yes (`maxsize` parameter) | No (unbounded by default) |
| `task_done` / `join` | Yes (producer-consumer coordination) | No |
| Performance | Slower (lock overhead) | Faster (GIL-only) |
| Use case | Multi-threaded producer-consumer | Single-thread FIFO, `popleft` in O(1) |

**Rule of thumb:**
- Use `queue.Queue` when threads need to safely pass work items.
- Use `collections.deque` for single-threaded algorithms or when you control all access (e.g., BFS).

---

## 7. Common Thread-safe Patterns Reference

| Pattern | Use Case | Python Primitive |
|---------|----------|-----------------|
| Mutex / Lock | Protect any shared mutable state | `threading.Lock` |
| Double-checked Singleton | One shared resource, lazy init | `threading.Lock` |
| Producer-Consumer | Decouple work generation from processing | `queue.Queue` |
| Thread-local Storage | Per-thread state (DB conn, request context) | `threading.local()` |
| Read-Write Lock | Read-heavy shared data | `threading.Condition` |
| Snapshot Observer | Safe event dispatch without deadlock | `threading.Lock` + `list()` copy |
| Semaphore | Limit concurrent access to N resources | `threading.Semaphore` |
| Event / Barrier | Synchronize thread startup/completion | `threading.Event`, `threading.Barrier` |
| Condition Variable | Wait for a state change | `threading.Condition` |

---

## Key Principles

1. **Minimize lock scope** — hold locks for the shortest time possible.
2. **Never call external code while holding a lock** — snapshot first, then call.
3. **Consistent lock ordering** — when acquiring multiple locks, always acquire in the same order to prevent deadlocks.
4. **Prefer higher-level primitives** — `queue.Queue` over raw `Lock` + `list` for producer-consumer.
5. **Thread-local for isolation** — use `threading.local()` instead of passing context through every function call.
6. **The GIL is not enough** — the GIL protects CPython internals, not your application logic.
