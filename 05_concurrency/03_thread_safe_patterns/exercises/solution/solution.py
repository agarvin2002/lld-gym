"""
Thread-safe Event Bus — Solution
=================================
A publish-subscribe event bus safe for concurrent use by multiple threads.

Key design decisions:
- A single Lock protects _handlers (the mutable shared state).
- publish() takes a snapshot of the handler list while holding the lock,
  then releases the lock before calling any handler. This prevents deadlock
  when a handler itself calls subscribe() or publish() on the same bus.
- unsubscribe() is a no-op if the handler was never registered (safe to call
  from any thread without error).
"""

import threading
from collections import defaultdict


class EventBus:
    """Thread-safe publish-subscribe event bus.

    Multiple threads may call subscribe, unsubscribe, and publish concurrently.
    Handler invocations happen outside the lock to prevent deadlock when
    handlers themselves publish further events.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list] = defaultdict(list)
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, handler) -> None:
        """Register handler for event_type. Handler must be callable(data)."""
        with self._lock:
            self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler) -> None:
        """Remove handler for event_type. No-op if not registered."""
        with self._lock:
            handlers = self._handlers.get(event_type, [])
            if handler in handlers:
                handlers.remove(handler)

    def publish(self, event_type: str, data: object = None) -> int:
        """Call all handlers for event_type with data.

        Handlers are invoked outside the lock (snapshot isolation) so that
        a handler may safely call subscribe/unsubscribe/publish without
        deadlocking.

        Returns:
            Number of handlers that were called.
        """
        with self._lock:
            handlers = list(self._handlers.get(event_type, []))  # snapshot
        for handler in handlers:
            handler(data)
        return len(handlers)

    def subscriber_count(self, event_type: str) -> int:
        """Return the number of subscribers currently registered for event_type."""
        with self._lock:
            return len(self._handlers.get(event_type, []))
