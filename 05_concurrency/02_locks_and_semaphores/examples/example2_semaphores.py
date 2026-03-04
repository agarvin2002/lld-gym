"""
Example 2: Semaphores and Events in Python
==========================================
Demonstrates:
- Section 1: Semaphore as rate limiter — max 3 concurrent "API calls"
- Section 2: BoundedSemaphore to guard a connection pool (prevent over-release)
- Section 3: threading.Event — stop signal for workers
- Section 4: Semaphore vs Lock distinction (Lock is binary; Semaphore counts)
"""

import threading
import time
import random


# =============================================================================
# SECTION 1: Semaphore as rate limiter — max N concurrent workers
# =============================================================================

def demo_semaphore_rate_limiter() -> None:
    print("\n--- SECTION 1: Semaphore as rate limiter (max 3 concurrent API calls) ---")

    MAX_CONCURRENT = 3
    sem = threading.Semaphore(MAX_CONCURRENT)
    active_count = 0
    peak_active = 0
    count_lock = threading.Lock()

    def api_call(name: str) -> None:
        nonlocal active_count, peak_active
        with sem:                               # blocks if 3 threads are already inside
            with count_lock:
                active_count += 1
                peak_active = max(peak_active, active_count)
                current = active_count
            print(f"  {name}: in progress  (active={current})")
            time.sleep(random.uniform(0.05, 0.15))   # simulate I/O
            with count_lock:
                active_count -= 1
            print(f"  {name}: done")

    threads = [
        threading.Thread(target=api_call, args=(f"Request-{i:02d}",))
        for i in range(10)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\n  Peak concurrent API calls: {peak_active} (limit was {MAX_CONCURRENT})")
    assert peak_active <= MAX_CONCURRENT, "Semaphore failed to limit concurrency!"
    print("  Rate limit respected.")


# =============================================================================
# SECTION 2: BoundedSemaphore for a connection pool — prevent over-release
# =============================================================================

class SimpleConnectionPool:
    """
    Minimal connection pool using BoundedSemaphore.
    BoundedSemaphore raises ValueError if a caller tries to release more
    times than it acquired, catching bugs where a connection is returned twice.
    """

    def __init__(self, size: int) -> None:
        self._size = size
        self._semaphore = threading.BoundedSemaphore(size)
        self._lock = threading.Lock()
        self._available: set[str] = {f"conn-{i}" for i in range(size)}

    def acquire(self) -> str:
        self._semaphore.acquire()         # blocks when pool is exhausted
        with self._lock:
            return self._available.pop()

    def release(self, conn: str) -> None:
        with self._lock:
            self._available.add(conn)
        self._semaphore.release()         # ValueError if released too many times


def demo_bounded_semaphore() -> None:
    print("\n--- SECTION 2: BoundedSemaphore for connection pool ---")

    pool = SimpleConnectionPool(size=3)
    print(f"  Pool size: 3")

    # Normal usage: acquire then release
    c1 = pool.acquire()
    c2 = pool.acquire()
    print(f"  Acquired: {c1}, {c2}  (1 connection still available)")
    pool.release(c1)
    pool.release(c2)
    print(f"  Released both — pool fully available again")

    # Demonstrate BoundedSemaphore catching over-release
    c3 = pool.acquire()
    pool.release(c3)
    try:
        pool.release(c3)   # BUG: releasing a connection we no longer hold
        print("  ERROR: over-release was not caught!")
    except ValueError as e:
        print(f"  BoundedSemaphore caught over-release: {e}")

    print("\n  With a plain Semaphore, the over-release would silently")
    print("  increase the counter above 3, allowing 4 concurrent acquirers.")


# =============================================================================
# SECTION 3: threading.Event — cooperative stop signal
# =============================================================================

def demo_event_stop_signal() -> None:
    print("\n--- SECTION 3: threading.Event as a stop signal ---")

    stop_event = threading.Event()
    iterations_done: list[int] = [0]
    count_lock = threading.Lock()

    def worker(name: str) -> None:
        local_count = 0
        while not stop_event.is_set():
            # Simulate work
            time.sleep(0.05)
            local_count += 1
        with count_lock:
            iterations_done[0] += local_count
        print(f"  {name}: stopped after {local_count} iterations")

    workers = [
        threading.Thread(target=worker, args=(f"Worker-{i}",), daemon=True)
        for i in range(3)
    ]
    for t in workers:
        t.start()

    print("  Workers running ... (will stop after 0.25s)")
    time.sleep(0.25)

    stop_event.set()         # signal all workers to stop
    print("  Stop signal sent.")

    for t in workers:
        t.join(timeout=1.0)

    print(f"  Total iterations across all workers: {iterations_done[0]}")
    print("  All workers stopped cleanly.")

    # Demonstrate wait() with timeout
    gate_event = threading.Event()

    def gated_worker(name: str) -> None:
        print(f"  {name}: waiting for start gate...")
        fired = gate_event.wait(timeout=0.5)   # returns True if set, False on timeout
        if fired:
            print(f"  {name}: gate opened — running")
        else:
            print(f"  {name}: timed out waiting for gate")

    print("\n  Starting gated workers (gate will open after 0.1s):")
    gated_threads = [
        threading.Thread(target=gated_worker, args=(f"Racer-{i}",))
        for i in range(4)
    ]
    for t in gated_threads:
        t.start()
    time.sleep(0.1)
    gate_event.set()            # open the gate for all racers
    for t in gated_threads:
        t.join()


# =============================================================================
# SECTION 4: Semaphore vs Lock — conceptual distinction
# =============================================================================

def demo_semaphore_vs_lock() -> None:
    print("\n--- SECTION 4: Semaphore vs Lock distinction ---")

    print("""
  threading.Lock:
    - Binary (0 or 1).  Exactly ONE thread can hold it.
    - Has ownership: the thread that acquired it must release it.
    - Releasing a Lock you did not acquire raises RuntimeError.
    - Use for: mutual exclusion (one writer at a time).

  threading.Semaphore(N):
    - Counting (0 … N).  Up to N threads inside the critical section.
    - No ownership: ANY thread can call release().
    - Semaphore(1) resembles a Lock but lacks ownership tracking.
    - Use for: rate limiting, resource pools, producer-consumer signalling.

  Key example — cross-thread signalling (impossible with Lock):
    sem = threading.Semaphore(0)   # starts at 0 (no permits)

    # Producer thread:
    sem.release()                  # signal: "data is ready"  (increments to 1)

    # Consumer thread:
    sem.acquire()                  # block until producer signals (decrements to 0)
    process_data()

  A Lock cannot be used for this because the consumer thread would be
  releasing a Lock it never acquired, which raises RuntimeError.
    """)

    # Live demo: cross-thread signalling with Semaphore(0)
    sem = threading.Semaphore(0)
    result: list[str] = []

    def producer_task() -> None:
        time.sleep(0.1)
        result.append("data produced")
        print("  Producer: data ready, releasing semaphore")
        sem.release()

    def consumer_task() -> None:
        print("  Consumer: waiting for semaphore (data not ready yet)")
        sem.acquire()
        print(f"  Consumer: received signal — {result[-1]}")

    p = threading.Thread(target=producer_task)
    c = threading.Thread(target=consumer_task)
    c.start()   # consumer starts first but will block on acquire()
    p.start()
    c.join()
    p.join()

    print("\n  Cross-thread signalling with Semaphore(0) works correctly.")
    print("  This pattern would be impossible with a plain Lock.")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Python Semaphores and Events — Complete Demo")
    print("=" * 60)

    demo_semaphore_rate_limiter()
    demo_bounded_semaphore()
    demo_event_stop_signal()
    demo_semaphore_vs_lock()

    print("\n" + "=" * 60)
    print("All demos complete.")
    print("=" * 60)
