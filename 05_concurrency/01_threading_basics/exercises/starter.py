"""
Exercise: Thread-Safe Bounded Buffer (Producer-Consumer)

Implement a BoundedBuffer class that is safe for multiple producer threads
and multiple consumer threads to use simultaneously.

Requirements:
- put(item) blocks when the buffer is full until space becomes available
- get() blocks when the buffer is empty until an item becomes available
- Multiple threads can call put/get concurrently without data loss or duplication
- Use threading.Lock and/or threading.Condition for synchronization

Hint: threading.Condition provides both mutual exclusion and the ability to
wait for a condition to become true (e.g., "buffer is not full").
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
        # TODO: store capacity, initialise the internal storage, and set up
        #       the synchronisation primitive(s) you will use.
        raise NotImplementedError

    def put(self, item: object) -> None:
        """Add item to the buffer, blocking until space is available.

        Args:
            item: Any Python object to enqueue.
        """
        # TODO: acquire the lock, wait while the buffer is full, append the
        #       item, and notify waiting consumers.
        raise NotImplementedError

    def get(self) -> object:
        """Remove and return the next item, blocking until one is available.

        Returns:
            The oldest item in the buffer (FIFO order).
        """
        # TODO: acquire the lock, wait while the buffer is empty, pop the
        #       oldest item, notify waiting producers, and return the item.
        raise NotImplementedError

    @property
    def size(self) -> int:
        """Current number of items held in the buffer."""
        # TODO: return the current number of items (thread-safe read).
        raise NotImplementedError

    @property
    def capacity(self) -> int:
        """Maximum number of items the buffer can hold."""
        # TODO: return the capacity set at construction time.
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Return True if the buffer currently contains no items."""
        # TODO: implement using size or direct comparison.
        raise NotImplementedError

    def is_full(self) -> bool:
        """Return True if the buffer is at maximum capacity."""
        # TODO: implement using size and capacity.
        raise NotImplementedError
