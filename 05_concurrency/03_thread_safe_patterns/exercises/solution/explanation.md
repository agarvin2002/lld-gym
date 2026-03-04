# Thread-safe Event Bus — Explanation

## Problem recap

Build a publish-subscribe event bus where any number of threads may concurrently subscribe, unsubscribe, and publish events without data corruption, crashes, or deadlocks.

---

## Core data structure

```python
self._handlers: dict[str, list] = defaultdict(list)
self._lock = threading.Lock()
```

`defaultdict(list)` means `_handlers["unknown_event"]` silently returns `[]` instead of raising `KeyError`. This simplifies every method — no `setdefault` or `if key not in` guards needed.

---

## subscribe / unsubscribe — straightforward mutation

```python
def subscribe(self, event_type: str, handler) -> None:
    with self._lock:
        self._handlers[event_type].append(handler)

def unsubscribe(self, event_type: str, handler) -> None:
    with self._lock:
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)
```

Both methods are short critical sections: acquire the lock, mutate the list, release. Using `with self._lock` (a context manager) guarantees the lock is always released, even if an exception is raised.

`unsubscribe` uses `.get(event_type, [])` (not `defaultdict` access) to avoid creating an empty list entry for events that have no subscribers. The `if handler in handlers` guard makes the operation idempotent — calling it on an unregistered handler is a safe no-op.

---

## publish — the snapshot pattern (critical for deadlock prevention)

```python
def publish(self, event_type: str, data: object = None) -> int:
    with self._lock:
        handlers = list(self._handlers.get(event_type, []))  # snapshot
    # Lock is RELEASED here — before calling any handler
    for handler in handlers:
        handler(data)
    return len(handlers)
```

**Why snapshot first, then release?**

Consider this scenario without the snapshot pattern:

```
Thread A calls publish("click", ...)
  → Acquires lock
  → Iterates over handlers list
  → Calls handler_1(data)
      → handler_1 tries to call bus.subscribe("click", handler_2)
          → Tries to acquire the SAME lock
          → DEADLOCK — lock is already held by Thread A
```

The fix is to:
1. Copy the handler list while holding the lock (`list(...)` creates a new list).
2. Release the lock immediately (exit `with self._lock`).
3. Iterate and call handlers on the copy.

Now any handler can call `subscribe`, `unsubscribe`, or `publish` safely because the lock is free. The snapshot is consistent — it captured the handler list at the moment of the publish call.

**Note on stale snapshots:** A handler added during a publish call will not be called for that publish, but will be called for the next one. This is the standard and correct behaviour for event buses.

---

## subscriber_count

```python
def subscriber_count(self, event_type: str) -> int:
    with self._lock:
        return len(self._handlers.get(event_type, []))
```

Reads must also be protected. Without the lock, a concurrent `subscribe` could be modifying the list while `len()` reads it, producing an inconsistent result (or in extreme cases a crash on some Python implementations).

---

## Why `defaultdict` but `.get()` in publish/unsubscribe?

`defaultdict` is used so `subscribe` can append without checking: `self._handlers[event_type].append(handler)`. However in `publish` and `unsubscribe` we use `.get(event_type, [])` to avoid creating an empty list for every event type that is merely queried. This keeps memory tidy — `_handlers` only has entries for event types that have at least one subscriber.

---

## Concurrency guarantees

| Scenario | Safe? | Why |
|----------|-------|-----|
| Two threads subscribe simultaneously | Yes | Both hold lock sequentially |
| Thread subscribes while another publishes | Yes | Lock prevents interleaving |
| Handler calls publish (re-entrant) | Yes | Lock is released before handler call |
| Thread unsubscribes during publish | Yes | Snapshot is already taken; change takes effect on next publish |
| Multiple threads publish concurrently | Yes | Each takes its own snapshot; lists are independent |

---

## Common mistakes to avoid

1. **Calling handlers while holding the lock** — leads to deadlock when handlers call back into the bus.
2. **Iterating directly over `self._handlers[event_type]`** — a concurrent `subscribe` or `unsubscribe` mutates the list during iteration, causing `RuntimeError: dictionary changed size during iteration` or skipped/duplicated handlers.
3. **Using a plain `dict` without a default** — requires `setdefault` or `if` guards everywhere, cluttering the code.
4. **Not protecting reads** — `subscriber_count` and `publish` both read `_handlers`; without a lock, a concurrent write can corrupt the read.
