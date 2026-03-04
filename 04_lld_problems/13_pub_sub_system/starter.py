"""Problem 13: Pub/Sub Messaging System — Reference Solution."""
from __future__ import annotations

import threading
import queue
import uuid
import time
from enum import Enum
from typing import Any, Callable, Dict, List


class TopicNotFoundError(Exception):
    """Raised when operating on a topic that does not exist."""
    pass


class DeliveryMode(Enum):
    """Delivery strategy for messages."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"


class Message:
    """Represents a single message published to a topic."""

    def __init__(self, topic: str, payload: Any, publisher_id: str) -> None:
        self.message_id: str = str(uuid.uuid4())
        self.topic: str = topic
        self.payload: Any = payload
        self.timestamp: float = time.time()
        self.publisher_id: str = publisher_id

    def __repr__(self) -> str:
        return (
            f"Message(id={self.message_id!r}, topic={self.topic!r}, "
            f"payload={self.payload!r})"
        )


class Topic:
    """
    A named channel that holds a subscriber registry and a message history.

    Thread safety: a single ``threading.Lock`` protects both the subscriber
    dict and the message list.  ``get_subscribers()`` and ``get_messages()``
    return *copies* so that the broker can iterate over subscribers (or callers
    can read history) without holding the lock during the callback execution.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self._subscribers: Dict[str, Callable[[Message], None]] = {}
        self._messages: List[Message] = []
        self._lock = threading.Lock()

    def add_subscriber(
        self, subscriber_id: str, callback: Callable[[Message], None]
    ) -> None:
        """Register a subscriber callback. Thread-safe."""
        with self._lock:
            self._subscribers[subscriber_id] = callback

    def remove_subscriber(self, subscriber_id: str) -> None:
        """Remove a subscriber. No-op if not present. Thread-safe."""
        with self._lock:
            self._subscribers.pop(subscriber_id, None)

    def get_subscribers(self) -> Dict[str, Callable[[Message], None]]:
        """Return a snapshot (copy) of the current subscriber mapping. Thread-safe."""
        with self._lock:
            return dict(self._subscribers)

    def add_message(self, message: Message) -> None:
        """Append a message to the history log. Thread-safe."""
        with self._lock:
            self._messages.append(message)

    def get_messages(self) -> List[Message]:
        """Return a copy of the message history. Thread-safe."""
        with self._lock:
            return list(self._messages)


class MessageBroker:
    """
    Central coordinator for the pub/sub system.

    Manages topics, routes published messages to subscriber callbacks, and
    supports two delivery modes:

    * ``DeliveryMode.SYNCHRONOUS``  — callbacks are invoked inline in the
      publisher's thread before ``publish()`` returns.
    * ``DeliveryMode.ASYNCHRONOUS`` — (message, callback) pairs are enqueued
      and executed by a single background daemon thread.  Call ``shutdown()``
      for a clean exit.

    At-least-once delivery: if a callback raises, ``_deliver`` retries up to
    ``max_retries`` additional times before silently giving up so that one
    faulty subscriber cannot crash the broker.
    """

    def __init__(
        self,
        delivery_mode: DeliveryMode = DeliveryMode.SYNCHRONOUS,
        max_retries: int = 3,
    ) -> None:
        self._topics: Dict[str, Topic] = {}
        self._delivery_mode: DeliveryMode = delivery_mode
        self._max_retries: int = max_retries
        # RLock so that broker methods can safely call other broker methods
        # without deadlocking (e.g. a callback that publishes another message).
        self._lock = threading.RLock()
        self._shutdown: bool = False

        if delivery_mode == DeliveryMode.ASYNCHRONOUS:
            self._queue: queue.Queue = queue.Queue()
            self._worker = threading.Thread(
                target=self._async_worker, daemon=True, name="pub-sub-worker"
            )
            self._worker.start()

    # ------------------------------------------------------------------
    # Topic management
    # ------------------------------------------------------------------

    def create_topic(self, name: str) -> None:
        """Create a new topic. No-op if it already exists. Thread-safe."""
        with self._lock:
            if name not in self._topics:
                self._topics[name] = Topic(name)

    def delete_topic(self, name: str) -> None:
        """
        Delete a topic and stop all future deliveries to it.

        Raises:
            TopicNotFoundError: if the topic does not exist.
        """
        with self._lock:
            if name not in self._topics:
                raise TopicNotFoundError(
                    f"Topic {name!r} not found — cannot delete."
                )
            del self._topics[name]

    # ------------------------------------------------------------------
    # Core pub/sub
    # ------------------------------------------------------------------

    def publish(self, publisher_id: str, topic: str, payload: Any) -> Message:
        """
        Publish a message to *topic*.

        Creates a ``Message``, records it in the topic's history, then
        dispatches it to every current subscriber (synchronously or via the
        async queue, depending on delivery mode).

        Returns:
            The ``Message`` object that was created.

        Raises:
            TopicNotFoundError: if *topic* does not exist.
        """
        with self._lock:
            if topic not in self._topics:
                raise TopicNotFoundError(
                    f"Topic {topic!r} not found — cannot publish."
                )
            t = self._topics[topic]

        message = Message(topic=topic, payload=payload, publisher_id=publisher_id)
        t.add_message(message)

        # Take a snapshot so the lock is not held while invoking callbacks.
        subscribers = t.get_subscribers()
        for callback in subscribers.values():
            if self._delivery_mode == DeliveryMode.SYNCHRONOUS:
                self._deliver(message, callback)
            else:
                self._queue.put((message, callback))

        return message

    def subscribe(
        self,
        subscriber_id: str,
        topic: str,
        callback: Callable[[Message], None],
    ) -> None:
        """
        Subscribe *subscriber_id* to *topic* with the given *callback*.

        Raises:
            TopicNotFoundError: if *topic* does not exist.
        """
        with self._lock:
            if topic not in self._topics:
                raise TopicNotFoundError(
                    f"Topic {topic!r} not found — cannot subscribe."
                )
            t = self._topics[topic]
        t.add_subscriber(subscriber_id, callback)

    def unsubscribe(self, subscriber_id: str, topic: str) -> None:
        """
        Unsubscribe *subscriber_id* from *topic*.

        Raises:
            TopicNotFoundError: if *topic* does not exist.
        """
        with self._lock:
            if topic not in self._topics:
                raise TopicNotFoundError(
                    f"Topic {topic!r} not found — cannot unsubscribe."
                )
            t = self._topics[topic]
        t.remove_subscriber(subscriber_id)

    def get_messages(self, topic: str) -> List[Message]:
        """
        Return all messages ever published to *topic* (oldest first).

        Raises:
            TopicNotFoundError: if *topic* does not exist.
        """
        with self._lock:
            if topic not in self._topics:
                raise TopicNotFoundError(
                    f"Topic {topic!r} not found — cannot get messages."
                )
            t = self._topics[topic]
        return t.get_messages()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def shutdown(self) -> None:
        """
        Cleanly shut down the async worker thread (if running).

        Sends a ``None`` sentinel to the queue so the worker loop exits, then
        waits up to 3 seconds for the thread to finish.  For a synchronous
        broker this is a no-op.
        """
        self._shutdown = True
        if hasattr(self, "_queue"):
            self._queue.put(None)  # sentinel to unblock the worker
            self._worker.join(timeout=3)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _deliver(self, message: Message, callback: Callable[[Message], None]) -> None:
        """
        Invoke *callback* with *message*, retrying on failure.

        Attempts: 1 initial + up to ``_max_retries`` additional tries.
        After all attempts are exhausted the failure is silently absorbed so
        that one broken subscriber cannot disrupt the broker or other
        subscribers.
        """
        for attempt in range(self._max_retries + 1):
            try:
                callback(message)
                return  # success — stop retrying
            except Exception:
                if attempt == self._max_retries:
                    # All retries exhausted — give up silently.
                    break
                # Otherwise loop to retry.

    def _async_worker(self) -> None:
        """
        Background thread: drain the async queue and deliver messages.

        Exits when it dequeues the ``None`` sentinel placed by ``shutdown()``.
        """
        while True:
            item = self._queue.get()
            if item is None:
                break  # sentinel received — clean exit
            message, callback = item
            self._deliver(message, callback)
