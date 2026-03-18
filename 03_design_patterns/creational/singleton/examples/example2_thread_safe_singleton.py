# Advanced topic — thread-safe Singleton using double-checked locking with threading.Lock
"""
Singleton Pattern - Example 2: Thread-Safe Singleton

Two threads can both see _instance is None and both create separate instances.
Double-checked locking fixes this using threading.Lock.

Real-world use: database connection pools in multi-threaded web servers
(e.g. a Razorpay payment gateway service).
"""
from __future__ import annotations
import threading
from typing import Optional


class DatabaseConnectionPool:
    """Connection pool — exactly one instance, safe under concurrent access."""

    _instance: Optional[DatabaseConnectionPool] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, host: str = "localhost", pool_size: int = 5) -> DatabaseConnectionPool:
        # FIRST CHECK — no lock (fast path once instance exists)
        if cls._instance is None:
            with cls._lock:
                # SECOND CHECK — inside lock (prevents race condition)
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str = "localhost", pool_size: int = 5) -> None:
        if hasattr(self, "_initialized"):
            return
        self.host = host
        self.pool_size = pool_size
        self._available = [f"conn_{i}" for i in range(pool_size)]
        self._pool_lock = threading.Lock()
        self._initialized = True

    def acquire(self) -> Optional[str]:
        with self._pool_lock:
            return self._available.pop(0) if self._available else None

    def release(self, connection: str) -> None:
        with self._pool_lock:
            self._available.append(connection)

    def __repr__(self) -> str:
        return f"<Pool host={self.host} available={len(self._available)}>"


# Why two checks?
#
#   WITHOUT locking:
#     Thread A: if _instance is None → True
#     Thread B: if _instance is None → True   (before A sets it)
#     Thread A: _instance = new()             → instance #1
#     Thread B: _instance = new()             → instance #2  BUG!
#
#   WITH double-checked locking:
#     Thread A: first check → True  → acquire lock → second check → True  → create
#     Thread B: first check → True  → acquire lock → second check → False → skip
#     Thread C: first check → False → return immediately (no lock needed!)
#
#   The first check avoids locking on every call once the instance exists.
#   The second check (inside the lock) stops two threads both passing the first check.


if __name__ == "__main__":
    DatabaseConnectionPool._instance = None   # reset for demo
    ids: list[int] = []
    lock = threading.Lock()

    def worker(i: int) -> None:
        pool = DatabaseConnectionPool(host=f"server-{i}", pool_size=3)
        with lock:
            ids.append(id(pool))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Unique instances across 10 threads: {len(set(ids))}")  # expect 1
