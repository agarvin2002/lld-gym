"""
Example 1: Locks and RLocks in Python
======================================
Demonstrates:
- Section 1: Basic Lock — thread-safe counter (unsafe vs safe comparison)
- Section 2: RLock — methods that call each other while holding the lock
- Section 3: Deadlock demo (two threads, two locks, opposite order) with timeout escape
- Section 4: Lock ordering fix — always acquire in the same global order
"""

import threading
import time


# =============================================================================
# SECTION 1: Basic Lock — unsafe vs thread-safe counter
# =============================================================================

class UnsafeCounter:
    """Counter without a lock — demonstrates a race condition."""

    def __init__(self) -> None:
        self.value: int = 0

    def increment(self) -> None:
        # Looks like one operation; internally it is READ → ADD → WRITE.
        # A context switch between READ and WRITE corrupts the result.
        current = self.value      # READ
        time.sleep(0)             # yield the CPU — makes the race very likely
        self.value = current + 1  # WRITE (another thread may have changed value)


class SafeCounter:
    """Counter protected by a Lock — no race condition."""

    def __init__(self) -> None:
        self.value: int = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:
            current = self.value
            time.sleep(0)            # CPU is yielded but lock blocks other threads
            self.value = current + 1


def run_counter(counter, n: int, num_threads: int) -> int:
    def task() -> None:
        for _ in range(n):
            counter.increment()

    threads = [threading.Thread(target=task) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter.value


def demo_lock_counter() -> None:
    print("\n--- SECTION 1: Basic Lock (unsafe vs safe counter) ---")

    n, num_threads = 500, 5
    expected = n * num_threads

    print(f"Expected: {expected}  ({num_threads} threads x {n} increments each)")

    for run in range(3):
        unsafe = UnsafeCounter()
        result = run_counter(unsafe, n, num_threads)
        status = "correct" if result == expected else "WRONG (race condition!)"
        print(f"  Unsafe run {run + 1}: {result:5d}  — {status}")

    print()
    for run in range(3):
        safe = SafeCounter()
        result = run_counter(safe, n, num_threads)
        status = "correct" if result == expected else "WRONG"
        print(f"  Safe   run {run + 1}: {result:5d}  — {status}")


# =============================================================================
# SECTION 2: RLock — methods that call each other while holding the lock
# =============================================================================

class RecursiveDirectory:
    """
    A simple nested structure where each node holds a Lock on its contents.

    'list_all()' calls '_collect()' which re-enters the same lock.
    With threading.Lock this would deadlock; with threading.RLock it works.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list["RecursiveDirectory"] = []
        # Change to threading.Lock() to observe a deadlock
        self._lock = threading.RLock()

    def add_child(self, child: "RecursiveDirectory") -> None:
        with self._lock:
            self.children.append(child)

    def _collect(self, indent: int) -> list[str]:
        """Recursive helper — re-acquires the same RLock on the way down."""
        with self._lock:                          # second (or deeper) acquisition
            lines = [" " * indent + self.name]
            for child in self.children:
                lines.extend(child._collect(indent + 2))
            return lines

    def list_all(self) -> list[str]:
        """Public method — acquires the lock then calls _collect."""
        with self._lock:                          # first acquisition
            return self._collect(0)


def demo_rlock() -> None:
    print("\n--- SECTION 2: RLock (re-entrant lock for recursive methods) ---")

    root = RecursiveDirectory("root")
    a    = RecursiveDirectory("dir_a")
    b    = RecursiveDirectory("dir_b")
    a1   = RecursiveDirectory("subdir_a1")
    a2   = RecursiveDirectory("subdir_a2")

    root.add_child(a)
    root.add_child(b)
    a.add_child(a1)
    a.add_child(a2)

    listing = root.list_all()
    print("  Directory tree (RLock allows recursive acquisition):")
    for line in listing:
        print(f"  {line}")

    print("\n  NOTE: replacing RLock with Lock in __init__ causes a deadlock here.")


# =============================================================================
# SECTION 3: Deadlock demo — two threads, two locks, opposite order
# =============================================================================

def demo_deadlock() -> None:
    print("\n--- SECTION 3: Deadlock demo (with timeout escape) ---")

    lock_a = threading.Lock()
    lock_b = threading.Lock()
    result: list[str] = []

    def thread_1_task() -> None:
        """Acquires lock_a first, then lock_b."""
        got_a = lock_a.acquire(timeout=0.3)
        if not got_a:
            result.append("T1: could not acquire lock_a (timeout)")
            return
        print("  T1: acquired lock_a")
        time.sleep(0.05)  # pause — gives T2 time to grab lock_b

        got_b = lock_b.acquire(timeout=0.3)  # will time out — T2 holds lock_b
        if not got_b:
            print("  T1: could not acquire lock_b — timeout (deadlock avoided)")
            lock_a.release()
            result.append("T1: deadlock avoided via timeout")
            return

        print("  T1: acquired both locks — done")
        lock_b.release()
        lock_a.release()

    def thread_2_task() -> None:
        """Acquires lock_b first, then lock_a — OPPOSITE order from T1."""
        got_b = lock_b.acquire(timeout=0.3)
        if not got_b:
            result.append("T2: could not acquire lock_b (timeout)")
            return
        print("  T2: acquired lock_b")
        time.sleep(0.05)

        got_a = lock_a.acquire(timeout=0.3)  # will time out — T1 holds lock_a
        if not got_a:
            print("  T2: could not acquire lock_a — timeout (deadlock avoided)")
            lock_b.release()
            result.append("T2: deadlock avoided via timeout")
            return

        print("  T2: acquired both locks — done")
        lock_a.release()
        lock_b.release()

    print("  T1 acquires lock_a then lock_b.")
    print("  T2 acquires lock_b then lock_a.  (opposite order → deadlock)")
    print("  Using acquire(timeout=0.3) so the demo does not hang forever.")
    print()

    t1 = threading.Thread(target=thread_1_task, name="T1")
    t2 = threading.Thread(target=thread_2_task, name="T2")
    t1.start()
    t2.start()
    t1.join(timeout=2.0)
    t2.join(timeout=2.0)

    for r in result:
        print(f"  Result: {r}")

    print("\n  Without the timeout, both threads would block forever.")
    print("  Root cause: acquiring multiple locks in inconsistent order.")


# =============================================================================
# SECTION 4: Lock ordering fix
# =============================================================================

def demo_lock_ordering() -> None:
    print("\n--- SECTION 4: Lock ordering fix (always acquire A before B) ---")

    lock_a = threading.Lock()
    lock_b = threading.Lock()
    done: list[str] = []

    def both_threads_task(name: str) -> None:
        """Both T1 and T2 always acquire lock_a FIRST, then lock_b."""
        with lock_a:               # Rule: always acquire lock_a first
            print(f"  {name}: acquired lock_a")
            time.sleep(0.02)       # simulate work holding lock_a
            with lock_b:           # Rule: lock_b second
                print(f"  {name}: acquired lock_b — in critical section")
                time.sleep(0.02)
        done.append(name)
        print(f"  {name}: released both locks")

    t1 = threading.Thread(target=both_threads_task, args=("T1",), name="T1")
    t2 = threading.Thread(target=both_threads_task, args=("T2",), name="T2")
    t1.start()
    t2.start()
    t1.join(timeout=2.0)
    t2.join(timeout=2.0)

    print(f"\n  Both threads finished successfully: {done}")
    print("  Lock ordering ensures no circular wait — deadlock impossible.")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Python Locks and RLocks — Complete Demo")
    print("=" * 60)

    demo_lock_counter()
    demo_rlock()
    demo_deadlock()
    demo_lock_ordering()

    print("\n" + "=" * 60)
    print("All demos complete.")
    print("=" * 60)
