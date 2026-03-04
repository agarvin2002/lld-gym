# Topic 02: Locks and Semaphores

## 1. `threading.Lock` — Mutual Exclusion

A **Lock** (also called a mutex) is the simplest synchronisation primitive. At any moment only
one thread may hold the lock; all others that call `acquire()` will block until the lock is
released.

### Manual acquire / release

```python
import threading

lock = threading.Lock()
shared_list = []

def append_item(item):
    lock.acquire()          # blocks until the lock is available
    try:
        shared_list.append(item)
    finally:
        lock.release()      # ALWAYS release, even if an exception occurs
```

The `try / finally` pattern ensures the lock is never accidentally held forever.

### Context-manager form (preferred)

```python
def append_item(item):
    with lock:              # acquire on entry, release on exit (even on exception)
        shared_list.append(item)
```

`Lock` implements the context-manager protocol (`__enter__` / `__exit__`), so `with lock:` is
exactly equivalent to `acquire() … try / finally release()`.

### Thread-safe counter example

```python
import threading

counter = 0
lock = threading.Lock()

def increment(n: int) -> None:
    global counter
    for _ in range(n):
        with lock:
            counter += 1    # read-modify-write is now atomic

threads = [threading.Thread(target=increment, args=(10_000,)) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)  # always 50000
```

### Key facts about `Lock`

| Property | Value |
|---|---|
| Binary | Yes — either free (0) or held (1) |
| Re-entrant? | **No** — same thread calling `acquire()` twice will deadlock |
| `acquire(blocking=False)` | Returns `True` if acquired, `False` if already held |
| `acquire(timeout=N)` | Blocks up to N seconds; returns `False` on timeout |

---

## 2. `threading.RLock` — Re-entrant Lock

An **RLock** ("recursive lock") can be acquired multiple times by the **same thread** without
deadlocking. The lock is released only after the same thread calls `release()` an equal number
of times.

### Why you need it

If a method holds a lock and then calls another method that also tries to acquire the same lock,
a regular `Lock` will deadlock. An `RLock` allows the re-entry.

```python
import threading

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self._lock = threading.RLock()   # NOT Lock — recursion requires RLock

    def add_child(self, node):
        with self._lock:                 # first acquisition
            self.children.append(node)

    def deep_count(self):
        with self._lock:                 # second acquisition by same thread — OK with RLock
            total = 1
            for child in self.children:
                total += child.deep_count()
            return total
```

With `threading.Lock` instead of `threading.RLock`, `deep_count()` calling itself recursively
while holding the lock would block forever on the second `acquire()`.

### When to use `RLock`

- A class exposes public methods that each acquire the lock, and some methods call other methods
  on the same object.
- Recursive algorithms operating on shared state.

### Key difference from `Lock`

| | `Lock` | `RLock` |
|---|---|---|
| Same thread re-acquires | Deadlock | Allowed |
| Release count required | 1 | Must match number of acquires |
| Slightly slower | No | Yes (tracks owner thread) |

---

## 3. `threading.Semaphore` vs `BoundedSemaphore`

A **Semaphore** is a generalisation of a lock: it maintains an internal counter initialised to
`N`. Each `acquire()` decrements the counter (blocking when it reaches 0); each `release()`
increments it. This allows up to **N threads** to be in the critical section simultaneously.

```python
import threading, time

# Allow at most 3 concurrent "API calls"
sem = threading.Semaphore(3)

def call_api(name: str) -> None:
    with sem:                           # acquire (blocks if 3 already inside)
        print(f"{name} calling API")
        time.sleep(0.5)                 # simulate I/O
        print(f"{name} done")

threads = [threading.Thread(target=call_api, args=(f"T{i}",)) for i in range(8)]
for t in threads: t.start()
for t in threads: t.join()
```

At most 3 threads will be inside `call_api` at once; the others wait.

### `Semaphore(1)` vs `Lock`

`Semaphore(1)` behaves like a `Lock` except that a **different thread** can release it (a
Semaphore has no concept of "ownership"). This is intentional for signalling patterns (e.g.
producer–consumer) but dangerous if you want mutual exclusion with ownership.

### `BoundedSemaphore`

`BoundedSemaphore` is identical to `Semaphore` except that calling `release()` more times than
`acquire()` raises a `ValueError`. Use it whenever the number of releases must not exceed the
number of acquires (e.g. a connection pool where you must not return a connection you did not
acquire).

```python
sem = threading.BoundedSemaphore(3)

sem.acquire()
sem.acquire()
sem.release()
sem.release()
sem.release()   # ValueError: Semaphore released too many times
```

### Semaphore summary

| | `Semaphore` | `BoundedSemaphore` |
|---|---|---|
| Counter can exceed initial value? | Yes (over-release allowed) | **No** — raises `ValueError` |
| Use case | Signalling / one-directional | Resource pooling / rate limiting |

---

## 4. `threading.Event` — One-shot Signal / Flag

An **Event** is a simple flag that threads can wait on. It is either *set* (True) or *cleared*
(False).

| Method | Effect |
|---|---|
| `event.set()` | Set the flag to True; wake all waiting threads |
| `event.clear()` | Reset the flag to False |
| `event.wait(timeout=None)` | Block until flag is True (returns True/False) |
| `event.is_set()` | Non-blocking; returns current state |

### Stop signal example

```python
import threading, time

stop_event = threading.Event()

def worker():
    while not stop_event.is_set():
        print("Working...")
        time.sleep(0.2)
    print("Worker: stop signal received, exiting.")

t = threading.Thread(target=worker, daemon=True)
t.start()

time.sleep(0.7)
stop_event.set()    # signal all workers to stop
t.join()
```

### Start gate example (multiple threads waiting for a signal)

```python
ready = threading.Event()

def racer(name):
    ready.wait()        # all racers block here
    print(f"{name} GO!")

threads = [threading.Thread(target=racer, args=(f"Racer-{i}",)) for i in range(5)]
for t in threads: t.start()
time.sleep(0.1)
ready.set()             # release all racers simultaneously
for t in threads: t.join()
```

### When to use `Event`

- Signalling workers to stop (a "poison pill" flag).
- Coordinating a starting gun: many threads wait until a signal fires.
- Single-direction notification where you don't need to pass data.

---

## 5. `threading.Condition` — Wait / Notify

A **Condition** combines a lock with the ability to wait for an arbitrary condition to become
true. It must always be used inside a `with condition:` block.

| Method | Effect |
|---|---|
| `condition.wait()` | Release the lock and sleep until notified; re-acquire before returning |
| `condition.wait(timeout=N)` | Like `wait()` but returns after at most N seconds |
| `condition.notify()` | Wake **one** waiting thread |
| `condition.notify_all()` | Wake **all** waiting threads |

### Producer–consumer pattern

```python
import threading
from collections import deque

buffer = deque()
MAX = 5
cond = threading.Condition()

def producer():
    for i in range(20):
        with cond:
            while len(buffer) >= MAX:
                cond.wait()             # release lock, sleep, re-acquire on wake
            buffer.append(i)
            cond.notify()               # tell consumer something is available

def consumer():
    received = 0
    while received < 20:
        with cond:
            while not buffer:
                cond.wait()             # release lock, sleep, re-acquire on wake
            item = buffer.popleft()
            cond.notify()               # tell producer there is space
        received += 1
        print(f"Consumed: {item}")

p = threading.Thread(target=producer)
c = threading.Thread(target=consumer)
p.start(); c.start()
p.join(); c.join()
```

### Critical rule: always re-check the condition in a loop

```python
# BAD — spurious wake-ups can happen
with cond:
    cond.wait()
    use(buffer.popleft())   # buffer might be empty again!

# GOOD — re-check after every wake
with cond:
    while not buffer:
        cond.wait()
    use(buffer.popleft())   # safe: buffer guaranteed non-empty
```

Python's `Condition.wait()` can return even when `notify()` was not called (spurious wake-up).
The `while` loop guards against this.

### Creating a `Condition` with an existing lock

```python
lock = threading.Lock()
cond = threading.Condition(lock)   # cond uses `lock` as its internal lock
```

---

## 6. Deadlock

### Definition

A **deadlock** occurs when two or more threads are each waiting for a resource held by another
thread in the cycle, and none can proceed.

### Classic two-lock deadlock

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:                # acquires lock_a
        time.sleep(0.01)        # context switch — thread_2 acquires lock_b
        with lock_b:            # BLOCKS — lock_b held by thread_2
            print("T1 done")

def thread_2():
    with lock_b:                # acquires lock_b
        time.sleep(0.01)
        with lock_a:            # BLOCKS — lock_a held by thread_1
            print("T2 done")

# Both threads block forever — deadlock!
```

### Four conditions for deadlock (Coffman conditions)

1. **Mutual exclusion** — resources cannot be shared.
2. **Hold and wait** — a thread holds one resource and waits for another.
3. **No preemption** — resources cannot be forcibly taken.
4. **Circular wait** — a cycle exists in the wait-for graph.

Break **any one** condition to prevent deadlock.

### Prevention strategies

| Strategy | How |
|---|---|
| Lock ordering | Always acquire locks in the same global order |
| Lock timeout | Use `acquire(timeout=N)`; back off if timeout expires |
| Try-lock | Use `acquire(blocking=False)`; retry later |
| Coarse-grained locking | Use one lock instead of many fine-grained locks |
| Lock-free algorithms | Use atomic operations or immutable data |

---

## 7. Lock Ordering as Deadlock Prevention

The simplest and most reliable strategy is to **always acquire multiple locks in the same
predetermined order** across all threads.

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

# Rule: always acquire lock_a before lock_b — no exceptions

def thread_1():
    with lock_a:            # step 1: acquire lock_a
        with lock_b:        # step 2: acquire lock_b
            print("T1 critical section")

def thread_2():
    with lock_a:            # step 1: acquire lock_a (same order as T1)
        with lock_b:        # step 2: acquire lock_b
            print("T2 critical section")

# No deadlock: if T2 holds lock_a, T1 blocks at lock_a (not inside it).
# T2 will finish and release both locks; T1 can then proceed.
```

For **N** locks, assign each a global integer rank. A thread must always acquire in ascending
rank order.

---

## 8. Quick Comparison Table

| Primitive | Allows N threads | Re-entrant | Use when |
|---|---|---|---|
| `Lock` | 1 | No | Simple mutual exclusion |
| `RLock` | 1 | Yes | Recursive / nested same-thread acquisitions |
| `Semaphore(N)` | N | No | Rate limiting, resource pools |
| `BoundedSemaphore(N)` | N | No | Resource pools (safer — detects over-release) |
| `Event` | — (signal, not mutex) | N/A | One-shot flag; stop signals; start gates |
| `Condition` | — (built on a lock) | N/A | Wait for arbitrary state change (producer–consumer) |

---

## Summary

- Use **`Lock`** for protecting a single shared resource with one thread at a time.
- Use **`RLock`** when the same thread might need to re-enter a critical section.
- Use **`Semaphore`** / **`BoundedSemaphore`** when up to N threads should access a resource
  concurrently; prefer `BoundedSemaphore` for connection/resource pools.
- Use **`Event`** for simple flag-based signalling between threads.
- Use **`Condition`** when a thread must wait for a specific data condition (not just a lock),
  as in producer–consumer scenarios.
- Prevent **deadlocks** by enforcing a consistent global lock-acquisition order.
