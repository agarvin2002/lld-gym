"""
Exercise: Thread-Safe Connection Pool

Implement a ConnectionPool class that manages a fixed pool of reusable
"connections" (represented as strings like "conn-0", "conn-1", …).

Requirements:
- acquire() blocks until a connection is available, then returns it.
- release(conn) returns a connection back to the pool so others can use it.
- available reports the number of free connections at any moment.
- size reports the total (fixed) pool size.
- Thread-safe: multiple threads can call acquire() / release() concurrently.

Hint:
  Use threading.Semaphore(size) to limit how many threads can acquire
  concurrently, and a threading.Lock-protected set to track which
  connections are free.
"""

import threading


class ConnectionPool:
    """A thread-safe pool of reusable named connections.

    Args:
        size: Number of connections in the pool.  Must be >= 1.
    """

    def __init__(self, size: int) -> None:
        # TODO: store size, create a Semaphore(size), a Lock, and initialise
        #       the set of available connections: {"conn-0", "conn-1", ...}
        pass  # replace with your initialisation

    def acquire(self) -> str:
        """Block until a connection is available; return the connection string."""
        raise NotImplementedError

    def release(self, conn: str) -> None:
        """Return a connection back to the pool."""
        raise NotImplementedError

    @property
    def available(self) -> int:
        """Number of free connections right now (thread-safe snapshot)."""
        raise NotImplementedError

    @property
    def size(self) -> int:
        """Total pool capacity (constant)."""
        raise NotImplementedError
