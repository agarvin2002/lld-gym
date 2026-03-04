"""
Singleton Pattern - Example 2: Thread-Safe Singleton
=====================================================

Problem: In a multi-threaded application, two threads can simultaneously
reach the `if _instance is None` check, both find it None, and both
create separate instances — breaking the Singleton guarantee.

Solution: Double-checked locking with threading.Lock.

Pattern:
    1. First check (no lock): fast path — if instance exists, return it immediately
    2. Acquire lock: slow path — only when instance might not exist yet
    3. Second check (with lock): prevent race condition between the lock acquire
       and the actual creation

This module demonstrates:
    - Thread-safe Singleton with double-checked locking
    - DatabaseConnectionPool as a realistic use case
    - Proof via concurrent threads that only one instance is ever created
"""

from __future__ import annotations

import threading
import time
import random
from typing import Optional


# =============================================================================
# THE PATTERN: Thread-Safe Singleton with Double-Checked Locking
# =============================================================================

class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass using double-checked locking.

    Using a metaclass means:
    - Any class with metaclass=SingletonMeta becomes a singleton
    - isinstance() and subclassing work correctly
    - Singleton behavior is centralized in one place

    _instances: maps each class to its single instance
    _lock: one lock per class (stored in _locks dict)
    """

    _instances: dict[type, object] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: object, **kwargs: object) -> object:
        # FIRST CHECK — no lock, fast path
        # For the majority of calls (after initialization), this returns
        # immediately without acquiring the lock. Locks are expensive!
        if cls not in cls._instances:

            # ACQUIRE LOCK — only reached when instance might not exist
            with cls._lock:

                # SECOND CHECK — inside the lock, safe
                # Between our first check and acquiring the lock, another
                # thread might have already created the instance. Check again.
                if cls not in cls._instances:
                    # This is the one and only time the instance is created
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
                    print(
                        f"[SingletonMeta] Created new instance of {cls.__name__} "
                        f"(thread: {threading.current_thread().name})"
                    )

        return cls._instances[cls]


# =============================================================================
# REALISTIC USE CASE: Database Connection Pool
# =============================================================================

class DatabaseConnectionPool(metaclass=SingletonMeta):
    """
    A database connection pool that should exist as exactly one instance
    across the entire application.

    Why singleton makes sense here:
    - Creating connections is expensive (network, auth)
    - We want a fixed, shared pool — not a new pool per component
    - All components should queue to the same pool

    Real-world equivalents:
    - SQLAlchemy's connection pool
    - Django's database backend
    - Redis connection pools
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "production",
        pool_size: int = 5,
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.pool_size = pool_size

        # Simulate the pool of connections
        self._connections: list[str] = [
            f"conn_{i}" for i in range(pool_size)
        ]
        self._available: list[str] = list(self._connections)
        self._in_use: list[str] = []
        self._pool_lock = threading.Lock()

        # Statistics
        self._total_acquired: int = 0
        self._total_released: int = 0

        print(
            f"[Pool] Initialized connection pool: "
            f"{host}:{port}/{database}, size={pool_size}"
        )

    def acquire(self) -> Optional[str]:
        """
        Get a connection from the pool.
        Returns a connection identifier, or None if pool is exhausted.
        Thread-safe: uses an internal lock for the pool state.
        """
        with self._pool_lock:
            if self._available:
                conn = self._available.pop(0)
                self._in_use.append(conn)
                self._total_acquired += 1
                return conn
            return None  # Pool exhausted

    def release(self, connection: str) -> None:
        """Return a connection back to the pool. Thread-safe."""
        with self._pool_lock:
            if connection in self._in_use:
                self._in_use.remove(connection)
                self._available.append(connection)
                self._total_released += 1

    def status(self) -> dict[str, object]:
        """Return current pool status."""
        with self._pool_lock:
            return {
                "host": self.host,
                "database": self.database,
                "pool_size": self.pool_size,
                "available": len(self._available),
                "in_use": len(self._in_use),
                "total_acquired": self._total_acquired,
                "total_released": self._total_released,
                "instance_id": id(self),
            }

    def __repr__(self) -> str:
        return (
            f"<DatabaseConnectionPool {self.host}:{self.port}/{self.database} "
            f"pool_size={self.pool_size} id={id(self)}>"
        )


# =============================================================================
# THREAD SIMULATION: Prove Only One Instance Is Created
# =============================================================================

# Collect all instance IDs from every thread
_instance_ids: list[int] = []
_ids_lock = threading.Lock()


def worker_thread(worker_id: int, delay: float) -> None:
    """
    Simulates a worker thread that:
    1. Tries to instantiate DatabaseConnectionPool (with different params)
    2. Records the instance ID it received
    3. Acquires a connection, does "work", releases it
    """
    # Small random delay to create timing overlap between threads
    time.sleep(delay)

    print(f"[Worker-{worker_id}] Calling DatabaseConnectionPool()...")

    # Every thread tries to create a pool with DIFFERENT parameters.
    # Only the FIRST call's parameters should matter.
    pool = DatabaseConnectionPool(
        host=f"server-{worker_id}.example.com",  # different host per thread
        pool_size=worker_id + 1,                  # different pool size
    )

    # Record which instance ID we got
    with _ids_lock:
        _instance_ids.append(id(pool))

    print(f"[Worker-{worker_id}] Got pool instance id={id(pool)}")

    # Simulate using the pool
    conn = pool.acquire()
    if conn:
        print(f"[Worker-{worker_id}] Acquired {conn}, doing work...")
        time.sleep(random.uniform(0.01, 0.05))  # simulate work
        pool.release(conn)
        print(f"[Worker-{worker_id}] Released {conn}")
    else:
        print(f"[Worker-{worker_id}] Pool exhausted, no connection available")


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_single_thread() -> None:
    print("\n" + "=" * 60)
    print("SINGLE-THREAD: Basic Singleton Behavior")
    print("=" * 60)

    print("\nCreating pool1...")
    pool1 = DatabaseConnectionPool(host="primary-db", pool_size=3)

    print("\nCreating pool2 (different params — should be IGNORED)...")
    pool2 = DatabaseConnectionPool(host="replica-db", pool_size=10)

    print(f"\npool1: {pool1}")
    print(f"pool2: {pool2}")
    print(f"\npool1 is pool2: {pool1 is pool2}")
    print(f"pool2.host: {pool2.host}")   # "primary-db" — not "replica-db"!
    print(f"pool2.pool_size: {pool2.pool_size}")  # 3 — not 10!

    print("\nPool status:")
    for key, val in pool1.status().items():
        print(f"  {key}: {val}")


def demonstrate_multithreaded() -> None:
    print("\n" + "=" * 60)
    print("MULTI-THREAD: Race Condition Prevention")
    print("=" * 60)

    # Reset the singleton for a clean demo
    # (In production code you would NOT do this)
    if DatabaseConnectionPool in SingletonMeta._instances:
        del SingletonMeta._instances[DatabaseConnectionPool]

    _instance_ids.clear()

    num_threads = 10
    print(f"\nLaunching {num_threads} threads simultaneously...")
    print("Each thread tries to create DatabaseConnectionPool with DIFFERENT params.")
    print("Expected: ALL threads receive the SAME instance.\n")

    threads = []
    for i in range(num_threads):
        # Small staggered delays to create realistic concurrency overlap
        delay = random.uniform(0, 0.01)
        t = threading.Thread(
            target=worker_thread,
            args=(i, delay),
            name=f"Worker-{i}",
        )
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all to complete
    for t in threads:
        t.join()

    # Analyze results
    print("\n" + "-" * 40)
    print("RESULTS:")
    print(f"Total threads: {num_threads}")
    print(f"Unique instance IDs seen: {len(set(_instance_ids))}")
    print(f"All IDs: {set(_instance_ids)}")

    if len(set(_instance_ids)) == 1:
        print("\nSUCCESS: All threads received the same instance!")
        print("The Singleton guarantee holds under concurrent access.")
    else:
        print("\nFAILURE: Multiple instances were created!")
        print("The Singleton is NOT thread-safe.")

    # Final pool state
    pool = DatabaseConnectionPool()
    print("\nFinal pool status:")
    for key, val in pool.status().items():
        print(f"  {key}: {val}")


def demonstrate_double_checked_locking_explained() -> None:
    print("\n" + "=" * 60)
    print("HOW DOUBLE-CHECKED LOCKING WORKS")
    print("=" * 60)
    print("""
    Without locking (BROKEN in multi-threaded code):
    ─────────────────────────────────────────────────
    Thread A:  if _instance is None:  ← True
    Thread B:  if _instance is None:  ← True (before A sets it)
    Thread A:      _instance = new()  ← creates instance #1
    Thread B:      _instance = new()  ← creates instance #2!  BUG!

    With single lock (SAFE but slow):
    ──────────────────────────────────
    Thread A:  with lock:
    Thread A:    if _instance is None: _instance = new()
    Thread B:  with lock:             ← blocks until A releases
    Thread B:    if _instance is None: False → return existing

    With double-checked locking (SAFE and fast):
    ─────────────────────────────────────────────
    FIRST CHECK (no lock):
        Thread A:  if _instance is None: True  → go to lock
        Thread B:  if _instance is None: True  → go to lock
    LOCK (only one thread at a time):
        Thread A:  acquires lock
        Thread A:  SECOND CHECK: if _instance is None: True → create
        Thread A:  _instance = new()
        Thread A:  releases lock
        Thread B:  acquires lock
        Thread B:  SECOND CHECK: if _instance is None: False → skip
        Thread B:  releases lock
    FAST PATH (instance exists):
        Thread C:  if _instance is None: False → return immediately
        Thread D:  if _instance is None: False → return immediately
        ... no lock acquired, very fast ...

    The double-check is needed because:
    - Thread A and Thread B both passed the first check
    - Only one should create the instance
    - The second check inside the lock ensures only the first one creates it
    """)


if __name__ == "__main__":
    demonstrate_single_thread()
    demonstrate_multithreaded()
    demonstrate_double_checked_locking_explained()
