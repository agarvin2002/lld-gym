"""
Solution: Thread-Safe Connection Pool

Design:
  - threading.Semaphore(size) controls how many threads may hold a connection
    at the same time.  acquire() decrements the counter (blocks at 0);
    release() increments it.
  - threading.Lock protects the _available set so that pop() and add()
    are never interleaved across threads.
  - The two primitives have distinct responsibilities:
      Semaphore  — blocks callers when the pool is exhausted
      Lock       — protects the mutable set of free connection names
"""

import threading


class ConnectionPool:
    """A thread-safe pool of reusable named connections.

    Args:
        size: Number of connections in the pool.  Must be >= 1.
    """

    def __init__(self, size: int) -> None:
        self._size = size
        self._semaphore = threading.Semaphore(size)
        self._lock = threading.Lock()
        self._available: set[str] = {f"conn-{i}" for i in range(size)}

    def acquire(self) -> str:
        """Block until a connection is available; return the connection string."""
        self._semaphore.acquire()      # blocks when all connections are in use
        with self._lock:
            return self._available.pop()

    def release(self, conn: str) -> None:
        """Return a connection back to the pool."""
        with self._lock:
            self._available.add(conn)
        self._semaphore.release()      # wake one waiting acquirer (if any)

    @property
    def available(self) -> int:
        """Number of free connections right now (thread-safe snapshot)."""
        with self._lock:
            return len(self._available)

    @property
    def size(self) -> int:
        """Total pool capacity (constant)."""
        return self._size
