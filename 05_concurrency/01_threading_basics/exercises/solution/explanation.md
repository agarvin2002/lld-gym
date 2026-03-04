# BoundedBuffer — Solution Explanation

## The Problem

A **bounded buffer** (also called a blocking queue) sits between producers and consumers:

- **Producers** call `put(item)` to add work; they must wait if the buffer is full.
- **Consumers** call `get()` to take work; they must wait if the buffer is empty.

The buffer must be correct when *multiple* producers and consumers run concurrently.

---

## Why `threading.Condition` Instead of a Plain `Lock`

A plain `threading.Lock` can protect a shared data structure against races, but
it cannot express "wait until a condition is true". You would need to busy-poll:

```python
# BAD — burns CPU and is still racy
while buf_is_full():
    pass  # spin
buf.append(item)
```

`threading.Condition` solves this cleanly. It bundles:

1. A **lock** (the mutual-exclusion part).
2. A **wait/notify mechanism** so a thread can sleep until another thread
   explicitly wakes it up.

This is the classic *monitor* pattern.

---

## The `while` Loop Around `wait()` — Spurious Wakeups

```python
while len(self._buffer) >= self._capacity:
    self._cond.wait()
```

`wait()` may return even when no other thread called `notify`. These are called
**spurious wakeups** and are allowed by the POSIX threading specification (and
therefore by Python's `threading` module). Always re-check the condition in a
`while` loop, never an `if`:

```python
# WRONG — vulnerable to spurious wakeups
if len(self._buffer) >= self._capacity:
    self._cond.wait()
```

The `while` loop turns each wakeup into a fresh evaluation of the guard, making
the code correct regardless of why the thread was woken.

---

## `notify_all()` vs `notify()`

`notify()` wakes **one** waiting thread; `notify_all()` wakes **all** of them.

For a buffer with a single producer type and a single consumer type you could
use `notify()` — but `notify_all()` is safer and simpler:

- With multiple distinct condition guards ("not full" for producers, "not empty"
  for consumers) all sharing a single `Condition`, `notify()` could accidentally
  wake a thread whose guard is still false, causing it to re-sleep while the
  thread that *should* have woken stays asleep indefinitely.
- `notify_all()` avoids this at a small cost: spurious wakeups increase, but
  each woken thread re-checks its guard and goes back to sleep if needed.

In performance-critical code you might use two separate `Condition` objects (one
for "not full", one for "not empty") and call `notify()` on each — but for this
exercise `notify_all()` on a single condition is the right trade-off.

---

## Why `collections.deque`

`deque` (double-ended queue) provides O(1) `append` (right end) and `popleft`
(left end), making FIFO order both correct and efficient.

A plain `list` would work too, but `list.pop(0)` is O(n) because every element
must be shifted left.

---

## Lock Acquisition in `size`, `is_empty`, `is_full`

Even read-only properties acquire the condition lock:

```python
@property
def size(self) -> int:
    with self._cond:
        return len(self._buffer)
```

Without the lock, another thread could be mid-way through `put` or `get` when
we read `len(self._buffer)`, yielding a torn (inconsistent) value. Always hold
the lock for any access to shared mutable state.

---

## Threading Model Summary

```
Producer thread          shared Condition + deque          Consumer thread
──────────────           ────────────────────────          ──────────────
acquire lock             ← protected by Condition →        acquire lock
while full: wait()                                         while empty: wait()
deque.append(item)                                         item = deque.popleft()
notify_all()                                               notify_all()
release lock                                               release lock
```

One `Condition` object owns one internal lock. `with self._cond:` acquires that
lock and releases it on exit — the same pattern as `with lock:` for a plain
`Lock`.

---

## Common Mistakes to Avoid

| Mistake | Consequence |
|---|---|
| `if` instead of `while` before `wait()` | Fails on spurious wakeups |
| Forgetting to call `notify_all()` after modifying the buffer | Threads sleep forever |
| Reading `size` / `is_empty` / `is_full` without holding the lock | Data races, stale reads |
| Using `list.pop(0)` instead of `deque.popleft()` | O(n) removals |
| Calling `wait()` without holding the Condition lock | `RuntimeError` |
