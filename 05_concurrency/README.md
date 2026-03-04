# Module 05: Concurrency

## Why Concurrency Matters in LLD Interviews

LLD interviews rarely stay purely structural. Once you've designed your classes and relationships, interviewers commonly ask:

- "How would you make this thread-safe?"
- "What happens if two users update this simultaneously?"
- "How would you handle concurrent requests?"

Failing to answer these questions — or worse, saying "I'd add locks everywhere" without knowing the trade-offs — signals shallow understanding. This module gives you the vocabulary, patterns, and practical code to answer confidently.

---

## Python's Threading Model and the GIL

Python uses the **Global Interpreter Lock (GIL)**, a mutex that ensures only one thread executes Python bytecode at a time.

### What this means in practice:

| Scenario | GIL Impact |
|---|---|
| CPU-bound tasks (math, parsing) | Threads don't help — use `multiprocessing` |
| I/O-bound tasks (network, disk, DB) | Threads DO help — GIL is released during I/O |
| LLD interviews (design + correctness) | You still need locks for shared mutable state |

**Critical point:** The GIL is NOT a substitute for proper synchronization. Operations that look atomic (like `x += 1`) are not actually atomic in Python — they compile to multiple bytecode instructions, and context switches can happen between them.

---

## Common Concurrency Problems

### Race Condition
Two threads read and modify shared state "simultaneously", producing incorrect results. Example: two threads both read `counter = 5`, both increment, both write `6` — but the correct answer is `7`.

### Deadlock
Thread A holds Lock 1 and waits for Lock 2. Thread B holds Lock 2 and waits for Lock 1. Both wait forever.

### Starvation
A thread is perpetually denied access to a resource because other threads keep getting priority.

### Livelock
Threads are active but keep changing state in response to each other without making progress (like two people in a hallway stepping side to side).

---

## Module Structure

```
05_concurrency/
├── README.md                          ← You are here
├── 01_threading_basics/
│   ├── theory.md                      ← Threads, GIL, lifecycle
│   ├── examples/
│   │   ├── example1_basic_threads.py  ← Thread creation patterns
│   │   └── example2_thread_pool.py   ← ThreadPoolExecutor
│   └── exercises/
│       ├── problem.md                 ← Parallel task executor
│       ├── starter.py
│       ├── tests.py
│       └── solution/
│           ├── solution.py
│           └── explanation.md
├── 02_locks_and_semaphores/
│   ├── theory.md                      ← All sync primitives
│   ├── examples/
│   │   ├── example1_lock_basics.py   ← Lock, RLock, Semaphore, Condition
│   │   └── example2_deadlock_demo.py ← Deadlock + 3 fixes
│   └── exercises/
│       ├── problem.md                 ← BoundedQueue (blocking queue)
│       ├── starter.py
│       ├── tests.py
│       └── solution/
│           ├── solution.py
│           └── explanation.md
└── 03_thread_safe_patterns/
    ├── theory.md                      ← Patterns for thread safety
    ├── examples/
    │   ├── example1_thread_safe_lld.py ← Singleton, Observer, Cache
    │   └── example2_producer_consumer.py ← Queue-based patterns
    └── exercises/
        ├── problem.md                 ← Thread-safe Event Bus
        ├── starter.py
        ├── tests.py
        └── solution/
            ├── solution.py
            └── explanation.md
```

---

## Learning Path

1. **Start with Topic 01** — understand what threads are, how Python creates them, and see a race condition firsthand.
2. **Move to Topic 02** — learn the synchronization primitives (Lock, Semaphore, Condition) and how to avoid deadlocks.
3. **Finish with Topic 03** — see how to apply thread safety to LLD patterns you already know (Singleton, Observer, Cache).
4. **Do each exercise** — the exercises are designed to appear directly in interviews.

---

## Interview Cheat: When They Ask About Thread Safety

**Step 1:** Identify shared mutable state (what data is accessed by multiple threads).

**Step 2:** Identify critical sections (code that reads-modify-writes shared state).

**Step 3:** Choose the right primitive:
- Simple read/write protection → `Lock`
- Reentrant code (method calls itself) → `RLock`
- Limit concurrent access to N → `Semaphore`
- Wait for a condition → `Condition` or `Event`
- Producer-consumer → `queue.Queue`

**Step 4:** Minimize lock scope (hold locks for the shortest time possible).

**Step 5:** Watch for deadlocks (always acquire locks in the same order).
