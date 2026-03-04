"""
Exercise: Thread-safe Event Bus
=================================
Implement a publish-subscribe event bus that is safe for concurrent use
by multiple threads.

Public API to implement:
    EventBus.subscribe(event_type, handler)   -> None
    EventBus.unsubscribe(event_type, handler) -> None
    EventBus.publish(event_type, data=None)   -> int
    EventBus.subscriber_count(event_type)     -> int

Thread-safety requirements:
    - Multiple threads may call any method concurrently without crashing.
    - Handlers must be invoked WITHOUT holding the internal lock so that a
      handler can safely call subscribe/publish (prevents deadlock).
    - Use snapshot isolation: copy the handler list before iterating.

Hints:
    - Use threading.Lock to protect self._handlers.
    - Use collections.defaultdict(list) to store handlers by event_type.
    - In publish(), take list(handlers) while locked, then release the lock
      before calling each handler.
"""

import threading
from collections import defaultdict


class EventBus:
    def __init__(self) -> None:
        raise NotImplementedError

    def subscribe(self, event_type: str, handler) -> None:
        """Register handler for event_type. Handler is callable(data)."""
        raise NotImplementedError

    def unsubscribe(self, event_type: str, handler) -> None:
        """Remove handler for event_type. No-op if not registered."""
        raise NotImplementedError

    def publish(self, event_type: str, data: object = None) -> int:
        """Call all handlers for event_type with data.

        Returns:
            Number of handlers called.
        """
        raise NotImplementedError

    def subscriber_count(self, event_type: str) -> int:
        """Return the number of subscribers for event_type."""
        raise NotImplementedError
