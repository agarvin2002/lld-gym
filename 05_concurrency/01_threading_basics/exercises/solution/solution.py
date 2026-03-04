"""
Reference solution: Thread-Safe Bounded Buffer (Producer-Consumer).

Key design decisions are documented in explanation.md.
"""

import threading
from collections import deque


class BoundedBuffer:
    """A thread-safe bounded buffer for producer-consumer scenarios.

    Multiple producer threads may call put() concurrently.
    Multiple consumer threads may call get() concurrently.
    put() blocks when the buffer is full; get() blocks when it is empty.
    """

    def __init__(self, capacity: int) -> None:
        """Initialise the buffer.

        Args:
            capacity: Maximum number of items the buffer may hold at once.
                      Must be >= 1.
        """
        self._capacity = capacity
        self._buffer: deque = deque()
        self._cond = threading.Condition()

    def put(self, item: object) -> None:
        """Add item to the buffer, blocking until space is available.

        Args:
            item: Any Python object to enqueue.
        """
        with self._cond:
            while len(self._buffer) >= self._capacity:
                self._cond.wait()
            self._buffer.append(item)
            self._cond.notify_all()

    def get(self) -> object:
        """Remove and return the next item, blocking until one is available.

        Returns:
            The oldest item in the buffer (FIFO order).
        """
        with self._cond:
            while len(self._buffer) == 0:
                self._cond.wait()
            item = self._buffer.popleft()
            self._cond.notify_all()
            return item

    @property
    def size(self) -> int:
        """Current number of items held in the buffer."""
        with self._cond:
            return len(self._buffer)

    @property
    def capacity(self) -> int:
        """Maximum number of items the buffer can hold."""
        return self._capacity

    def is_empty(self) -> bool:
        """Return True if the buffer currently contains no items."""
        with self._cond:
            return len(self._buffer) == 0

    def is_full(self) -> bool:
        """Return True if the buffer is at maximum capacity."""
        with self._cond:
            return len(self._buffer) >= self._capacity
