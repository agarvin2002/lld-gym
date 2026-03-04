# ConnectionPool — Design Explanation

## Problem

A fixed pool of N named connections (strings) must be shared among any number of concurrent
threads. The contract is:

- `acquire()` hands out a unique connection; if none are free it **blocks** until one is returned.
- `release(conn)` returns a connection so the next waiting thread can use it.
- No two threads may hold the same connection string at the same time.

---

## Why two synchronisation primitives?

The solution uses exactly two primitives and they serve completely different roles.

### `threading.Semaphore(size)` — controls concurrency

A Semaphore with an initial value of `size` acts as a counting ticket machine:

```
internal counter starts at N (= pool size)

acquire() → counter -= 1   (blocks the caller when counter == 0)
release() → counter += 1   (wakes one blocked acquire() if any)
```

This is the only primitive that can **block** callers when the pool is exhausted.
A plain `Lock` cannot do this because a `Lock` is binary (0 or 1), not counting.

### `threading.Lock()` — protects the free-connection set

The set `_available` is mutable shared state. Two threads calling `acquire()` at the same
time would both call `_available.pop()` — without the Lock, they might both pop the same
connection or corrupt the set.

The Lock scope is kept as tight as possible: it wraps only the `set.pop()` or `set.add()`,
not the semaphore operation.

---

## Acquire sequence

```
Thread calls acquire()
  │
  ├─ semaphore.acquire()
  │     └─ If counter > 0: decrement and continue immediately.
  │        If counter == 0: BLOCK here until another thread calls release().
  │
  └─ (holding semaphore slot now)
       lock.acquire()
         conn = _available.pop()   ← safe: only one thread at a time
       lock.release()
       return conn
```

## Release sequence

```
Thread calls release(conn)
  │
  ├─ lock.acquire()
  │    _available.add(conn)        ← put the name back in the free set
  │  lock.release()
  │
  └─ semaphore.release()           ← increment counter; wake one waiter if any
```

Note that `semaphore.release()` must come **after** adding the connection back to
`_available`. If the order were reversed, a woken thread could call `_available.pop()` before
the connection name was restored, causing a `KeyError`.

---

## Why not just use `Semaphore` alone?

`Semaphore` limits how many threads are inside the critical section, but does **not** protect
the set from concurrent mutation. Two threads that acquire simultaneously would race on
`_available.pop()`. The `Lock` is necessary to serialise those set operations.

## Why not just use a `Condition`?

A `threading.Condition` is the classic alternative: wrap the set in a Condition, `wait()` when
empty, `notify()` on release. That also works and is used in the `BoundedBuffer` exercise
(module 01). The Semaphore approach chosen here is often cleaner for pools because:

- No `while not _available: wait()` loop required — the Semaphore counter tracks availability
  exactly.
- The blocking and the mutual exclusion are cleanly separated into two primitives with
  well-understood single responsibilities.

---

## `available` property

```python
@property
def available(self) -> int:
    with self._lock:
        return len(self._available)
```

The lock ensures that `len()` reads a consistent snapshot even if another thread is
simultaneously adding or removing a connection. This is a **read under lock** — correct but not
zero-cost. For a high-frequency hot path you would use an `threading.atomic` counter (not
available in CPython) or accept a slightly stale read; for a learning resource, correctness
takes priority.

---

## Thread safety checklist

| Operation | Protected by | Correctness |
|---|---|---|
| Blocking when pool is empty | Semaphore | Count cannot go below 0 |
| Popping a connection name | Lock | Only one thread sees each name |
| Returning a connection name | Lock | `add()` is not interleaved with `pop()` |
| Waking a waiting thread | Semaphore.release() | After name is back in set |
| Reading available count | Lock | Consistent snapshot of set size |
| Reading size | None needed | Immutable after `__init__` |
