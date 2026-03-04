# Topic 01: Threading Basics

## 1. What is a Thread? Process vs Thread

### Process
A **process** is an independent program in execution. Each process has:
- Its own memory space (heap, stack, code, data)
- Its own file handles, network sockets
- Isolated from other processes

Creating a process is expensive. Communication between processes (IPC) requires pipes, sockets, or shared memory.

### Thread
A **thread** is a unit of execution within a process. Multiple threads in the same process share:
- The same heap memory (global variables, objects)
- The same file handles and sockets
- The same code

Each thread has its own:
- Stack (local variables, function call chain)
- Program counter (which instruction it's on)
- Register state

**Threads are cheaper to create than processes, and share memory naturally — but that sharing is exactly what causes concurrency bugs.**

### When to use which:
| Need | Use |
|---|---|
| Shared memory, I/O-bound work | Threads (`threading`) |
| True parallelism, CPU-bound work | Processes (`multiprocessing`) |
| Async I/O (many connections, low concurrency) | `asyncio` |

---

## 2. Python's `threading` Module

### Creating a Thread

```python
import threading

# Method 1: target function
def my_task(name: str) -> None:
    print(f"Task {name} running")

t = threading.Thread(target=my_task, args=("A",))
t.start()   # starts the thread
t.join()    # waits for it to finish
```

### Thread Class Attributes and Methods

| Method/Attribute | Description |
|---|---|
| `start()` | Start the thread (call once) |
| `join(timeout=None)` | Wait for thread to finish |
| `is_alive()` | Returns True if thread is running |
| `name` | Thread name (settable) |
| `daemon` | Set before start(); daemon threads die with main thread |
| `threading.current_thread()` | Returns current thread object |
| `threading.active_count()` | Number of alive threads |

### Daemon Threads
A **daemon thread** runs in the background and is automatically killed when all non-daemon threads finish.

```python
t = threading.Thread(target=background_monitor)
t.daemon = True  # must set BEFORE start()
t.start()
# When main thread exits, this daemon dies automatically
```

**Use daemon threads for:** background cleanup, heartbeats, log flushing.
**Pitfall:** Daemon threads can be killed mid-operation, leaving state corrupted.

---

## 3. The GIL: Python's Global Interpreter Lock

### What is the GIL?
The GIL is a mutex built into CPython (the standard Python interpreter) that allows **only one thread to execute Python bytecode at a time**.

### Why does it exist?
CPython's memory management (reference counting) is not thread-safe. The GIL protects the interpreter's internal state — so the interpreter itself doesn't crash.

### What the GIL does NOT protect:
**Your application data.** The GIL is released between bytecode instructions. A context switch can happen between the instructions of `x += 1`:

```
# x += 1 compiles to roughly:
LOAD x        # read x = 5
LOAD 1        # push 1
BINARY_ADD    # compute 6
STORE x       # write x = 6

# If thread A is interrupted between LOAD and STORE,
# thread B reads the old value of x — race condition!
```

### I/O vs CPU-bound:

| Task type | GIL behavior | Threads help? |
|---|---|---|
| I/O (network, disk, DB, sleep) | GIL **released** during I/O | YES — threads overlap waiting |
| CPU (computation, parsing) | GIL **held** during execution | NO — use `multiprocessing` |

### Key rule:
> The GIL is NOT a substitute for explicit synchronization. Always use locks to protect shared mutable state.

---

## 4. Creating Threads: Two Approaches

### Approach 1: Target Function (preferred for simple cases)

```python
import threading

def download(url: str, results: list, index: int) -> None:
    # simulate download
    import time
    time.sleep(0.1)
    results[index] = f"data from {url}"

results = [None] * 3
threads = []
urls = ["http://a.com", "http://b.com", "http://c.com"]

for i, url in enumerate(urls):
    t = threading.Thread(target=download, args=(url, results, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(results)
```

### Approach 2: Subclassing Thread (for stateful thread objects)

```python
import threading

class DownloadThread(threading.Thread):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url
        self.result: str = ""

    def run(self) -> None:
        # Override run(), not start()
        import time
        time.sleep(0.1)
        self.result = f"data from {self.url}"

threads = [DownloadThread(url) for url in urls]
for t in threads:
    t.start()
for t in threads:
    t.join()

for t in threads:
    print(t.result)
```

**When to subclass:** When the thread needs to maintain state or expose methods.
**When to use target:** For simple, one-off tasks.

---

## 5. Thread Lifecycle

```
           start()                    run() completes
NEW  ─────────────────► RUNNABLE ─────────────────────► TERMINATED
                            │                                 ▲
                            │ blocked on I/O / lock / sleep   │
                            ▼                                 │
                         BLOCKED ────────────────────────────►
                            (unblocked when resource available)
```

### States explained:
- **NEW:** Thread object created, `start()` not yet called
- **RUNNABLE:** Thread is ready to run or actively running
- **BLOCKED:** Thread is waiting for a lock, I/O, or `sleep()`
- **TERMINATED:** `run()` has returned (or raised an exception)

A terminated thread cannot be restarted. Create a new `Thread` object.

---

## 6. Quick Example: Parallel File Downloads

```python
import threading
import time
import random

def fetch_url(url: str, results: dict, lock: threading.Lock) -> None:
    """Simulate fetching a URL."""
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)
    content = f"<html>{url}</html>"

    with lock:
        results[url] = content
        print(f"Fetched {url} in {delay:.2f}s")

def parallel_fetch(urls: list[str]) -> dict[str, str]:
    results: dict[str, str] = {}
    lock = threading.Lock()
    threads = []

    start = time.time()

    for url in urls:
        t = threading.Thread(target=fetch_url, args=(url, results, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"\nAll done in {elapsed:.2f}s (serial would be ~{sum(0.3 for _ in urls):.1f}s)")
    return results

# urls = ["http://a.com", "http://b.com", "http://c.com"]
# results = parallel_fetch(urls)
```

---

## 7. Common Mistakes

### Mistake 1: Assuming shared mutable state is safe
```python
# BAD: counter is shared, += is not atomic
counter = 0
def increment():
    global counter
    for _ in range(100_000):
        counter += 1  # race condition here

# GOOD: use a lock
lock = threading.Lock()
def increment_safe():
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1
```

### Mistake 2: Not joining threads (fire and forget)
```python
# BAD: main thread exits, results may be incomplete
for t in threads:
    t.start()
# main continues immediately

# GOOD: wait for all threads
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### Mistake 3: Setting daemon AFTER start()
```python
t = threading.Thread(target=task)
t.start()
t.daemon = True  # RuntimeError: cannot set daemon status of active thread
```

### Mistake 4: Calling run() instead of start()
```python
t.run()   # WRONG: runs in the CURRENT thread, no concurrency
t.start() # CORRECT: creates a new OS thread
```

### Mistake 5: Unhandled exceptions silently kill threads
```python
def risky_task():
    raise ValueError("oops")  # thread dies silently by default

t = threading.Thread(target=risky_task)
t.start()
t.join()
# No error is raised in main thread! Check t.is_alive() or handle in the thread.
```

---

## Summary

| Concept | Key Point |
|---|---|
| Thread | Lightweight execution unit sharing process memory |
| `start()` | Launches thread; call `run()` override internally |
| `join()` | Blocks caller until thread finishes |
| Daemon | Dies with main thread; set before `start()` |
| GIL | Protects CPython internals, NOT your data |
| I/O-bound | Threads give real speedup |
| CPU-bound | Use `multiprocessing` instead |
| Race condition | Unsynchronized access to shared mutable state |
