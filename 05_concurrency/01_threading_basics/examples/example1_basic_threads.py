"""
Example 1: Basic Threads in Python
===================================
Demonstrates:
- Creating threads with target function
- Creating threads by subclassing Thread
- join() to wait for completion
- daemon threads
- Thread naming and identification
- Race condition DEMO (intentional) and why it's a problem
"""

import threading
import time
import random


# =============================================================================
# SECTION 1: Creating threads with a target function
# =============================================================================

def worker_function(name: str, duration: float) -> None:
    """A simple worker that sleeps and prints."""
    thread_name = threading.current_thread().name
    print(f"  [{thread_name}] Worker '{name}' starting (will sleep {duration:.1f}s)")
    time.sleep(duration)
    print(f"  [{thread_name}] Worker '{name}' done")


def demo_target_function_threads() -> None:
    print("\n--- DEMO 1: Target Function Threads ---")

    threads = []
    for i in range(3):
        t = threading.Thread(
            target=worker_function,
            args=(f"Task-{i}", random.uniform(0.1, 0.4)),
            name=f"WorkerThread-{i}"  # give threads meaningful names
        )
        threads.append(t)

    print(f"Main thread: starting {len(threads)} worker threads")
    start = time.time()

    for t in threads:
        t.start()

    # Without join(), main thread would continue before workers finish
    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"Main thread: all workers done in {elapsed:.2f}s")
    print(f"Active threads now: {threading.active_count()}")


# =============================================================================
# SECTION 2: Creating threads by subclassing Thread
# =============================================================================

class DownloadThread(threading.Thread):
    """
    A thread that 'downloads' a URL and stores the result.
    Subclassing is useful when the thread needs state or results.
    """

    def __init__(self, url: str, thread_id: int) -> None:
        # Always call super().__init__() — optionally set name/daemon here
        super().__init__(name=f"Downloader-{thread_id}")
        self.url = url
        self.result: str = ""
        self.error: Exception | None = None
        self.duration: float = 0.0

    def run(self) -> None:
        """Override run(), NOT start(). This is what executes in the new thread."""
        print(f"  [{self.name}] Downloading {self.url}")
        try:
            start = time.time()
            # Simulate network I/O
            time.sleep(random.uniform(0.1, 0.5))
            self.result = f"<html><body>Content of {self.url}</body></html>"
            self.duration = time.time() - start
            print(f"  [{self.name}] Done: {self.url} ({self.duration:.2f}s)")
        except Exception as e:
            self.error = e
            print(f"  [{self.name}] Error downloading {self.url}: {e}")


def demo_subclass_threads() -> None:
    print("\n--- DEMO 2: Subclassing Thread ---")

    urls = [
        "https://api.example.com/users",
        "https://api.example.com/products",
        "https://api.example.com/orders",
        "https://api.example.com/reviews",
    ]

    threads = [DownloadThread(url, i) for i, url in enumerate(urls)]

    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.time() - start

    print(f"\nResults (collected after all threads finished):")
    for t in threads:
        if t.error:
            print(f"  FAILED {t.url}: {t.error}")
        else:
            print(f"  OK {t.url} — {len(t.result)} bytes in {t.duration:.2f}s")
    print(f"Total time: {elapsed:.2f}s (serial would be ~{sum(t.duration for t in threads):.2f}s)")


# =============================================================================
# SECTION 3: Daemon Threads
# =============================================================================

def heartbeat(interval: float) -> None:
    """A daemon thread that prints a heartbeat every interval seconds."""
    while True:
        print(f"  [Heartbeat] Alive at {time.strftime('%H:%M:%S')}")
        time.sleep(interval)


def demo_daemon_threads() -> None:
    print("\n--- DEMO 3: Daemon Threads ---")

    # Create a daemon thread
    monitor = threading.Thread(target=heartbeat, args=(0.2,), name="HeartbeatDaemon")
    monitor.daemon = True  # MUST set before start()
    monitor.start()

    print(f"Daemon thread started: {monitor.name} (daemon={monitor.daemon})")
    print("Main thread working for 0.5s...")
    time.sleep(0.5)
    print("Main thread done. Daemon will be killed automatically.")
    # No need to join daemon threads — they die when main thread exits
    # (In this demo, execution continues to next demo, so daemon keeps running briefly)


# =============================================================================
# SECTION 4: Thread Identification
# =============================================================================

def demo_thread_identification() -> None:
    print("\n--- DEMO 4: Thread Identification ---")

    def print_identity() -> None:
        t = threading.current_thread()
        print(f"  Thread name: {t.name}")
        print(f"  Thread ident: {t.ident}")
        print(f"  Is daemon: {t.daemon}")
        print(f"  Is alive: {t.is_alive()}")

    t = threading.Thread(target=print_identity, name="IdentityDemo")
    t.start()
    t.join()

    print(f"\nMain thread: {threading.main_thread().name}")
    print(f"Total active threads: {threading.active_count()}")
    print(f"All threads: {[t.name for t in threading.enumerate()]}")


# =============================================================================
# SECTION 5: Race Condition DEMO (intentional)
# =============================================================================

class UnsafeCounter:
    """A counter WITHOUT a lock — demonstrates race condition."""

    def __init__(self) -> None:
        self.value: int = 0

    def increment(self) -> None:
        # This looks atomic, but it's NOT:
        # 1. READ self.value
        # 2. ADD 1
        # 3. WRITE back
        # A context switch between any two steps = race condition
        current = self.value          # READ
        time.sleep(0)                 # yield CPU — makes race more likely
        self.value = current + 1      # WRITE


class SafeCounter:
    """A counter WITH a lock — no race condition."""

    def __init__(self) -> None:
        self.value: int = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:               # acquire lock → critical section
            current = self.value       # READ
            time.sleep(0)              # yield CPU — but lock prevents others
            self.value = current + 1   # WRITE
                                       # lock released automatically


def run_counter(counter: UnsafeCounter | SafeCounter, n: int, num_threads: int) -> int:
    """Run `num_threads` threads, each incrementing `counter` `n` times."""

    def task() -> None:
        for _ in range(n):
            counter.increment()

    threads = [threading.Thread(target=task) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return counter.value


def demo_race_condition() -> None:
    print("\n--- DEMO 5: Race Condition (intentional) ---")

    n = 1000
    num_threads = 5
    expected = n * num_threads

    print(f"Each of {num_threads} threads increments {n} times.")
    print(f"Expected final value: {expected}")

    # Run multiple times to show non-determinism
    for run in range(3):
        unsafe = UnsafeCounter()
        result = run_counter(unsafe, n, num_threads)
        status = "CORRECT" if result == expected else "WRONG (race condition!)"
        print(f"  Unsafe counter run {run + 1}: {result} — {status}")

    print()
    for run in range(3):
        safe = SafeCounter()
        result = run_counter(safe, n, num_threads)
        status = "CORRECT" if result == expected else "WRONG"
        print(f"  Safe counter run {run + 1}: {result} — {status}")


# =============================================================================
# SECTION 6: join() with timeout
# =============================================================================

def slow_task(duration: float) -> None:
    time.sleep(duration)


def demo_join_timeout() -> None:
    print("\n--- DEMO 6: join() with timeout ---")

    t = threading.Thread(target=slow_task, args=(2.0,), name="SlowTask")
    t.start()

    print("Waiting up to 0.3s for slow task...")
    t.join(timeout=0.3)

    if t.is_alive():
        print("Thread still running after timeout — gave up waiting")
        print("(Thread continues running; we just stopped waiting for it)")
    else:
        print("Thread finished within timeout")

    # In real code, you'd decide what to do with a still-running thread
    # You cannot forcibly kill a thread in Python — design threads to stop themselves


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Python Threading Basics — Complete Demo")
    print("=" * 60)

    demo_target_function_threads()
    demo_subclass_threads()
    demo_daemon_threads()
    demo_thread_identification()
    demo_race_condition()
    demo_join_timeout()

    print("\n" + "=" * 60)
    print("All demos complete.")
    print("=" * 60)
