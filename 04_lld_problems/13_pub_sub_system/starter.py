"""
Pub/Sub Messaging System — Starter File
==========================================
Your task: Implement a publish-subscribe messaging broker.

Read problem.md and design.md before starting.

Design decisions:
  - Topic: manages subscriber registry and message history; thread-safe with a Lock
    - get_subscribers() and get_messages() return COPIES (snapshot pattern)
  - MessageBroker: manages topics; supports SYNCHRONOUS and ASYNCHRONOUS delivery
    - SYNCHRONOUS: callbacks invoked inline before publish() returns
    - ASYNCHRONOUS: (message, callback) put in a queue; background daemon thread drains it
    - At-least-once: _deliver() retries failed callbacks up to max_retries times
    - shutdown() sends a sentinel None to the queue to stop the worker thread
  - Use uuid.uuid4() for message IDs, time.time() for timestamps
"""
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
    SYNCHRONOUS  = "synchronous"
    ASYNCHRONOUS = "asynchronous"


class Message:
    """Represents a single message published to a topic."""

    def __init__(self, topic: str, payload: Any, publisher_id: str) -> None:
        # TODO: Set message_id = str(uuid.uuid4())
        # TODO: Store topic, payload, publisher_id
        # TODO: Set timestamp = time.time()
        pass

    def __repr__(self) -> str:
        return (
            f"Message(id={self.message_id!r}, topic={self.topic!r}, "
            f"payload={self.payload!r})"
        )


class Topic:
    """A named channel with a subscriber registry and message history.

    Use a threading.Lock to protect _subscribers and _messages.
    get_subscribers() and get_messages() must return copies (snapshot pattern).
    """

    def __init__(self, name: str) -> None:
        # TODO: Store name
        # TODO: Create _subscribers: Dict[str, Callable[[Message], None]] = {}
        # TODO: Create _messages: List[Message] = []
        # TODO: Create _lock = threading.Lock()
        pass

    def add_subscriber(
        self, subscriber_id: str, callback: Callable[[Message], None]
    ) -> None:
        # TODO: Under _lock, add subscriber_id → callback to _subscribers
        pass

    def remove_subscriber(self, subscriber_id: str) -> None:
        # TODO: Under _lock, pop subscriber_id from _subscribers (no error if missing)
        pass

    def get_subscribers(self) -> Dict[str, Callable[[Message], None]]:
        # TODO: Under _lock, return dict(_subscribers) — a snapshot copy
        pass

    def add_message(self, message: Message) -> None:
        # TODO: Under _lock, append message to _messages
        pass

    def get_messages(self) -> List[Message]:
        # TODO: Under _lock, return list(_messages) — a snapshot copy
        pass


class MessageBroker:
    """Central coordinator for the pub/sub system."""

    def __init__(
        self,
        delivery_mode: DeliveryMode = DeliveryMode.SYNCHRONOUS,
        max_retries: int = 3,
    ) -> None:
        # TODO: Store _delivery_mode and _max_retries
        # TODO: Create _topics: Dict[str, Topic] = {}
        # TODO: Create _lock = threading.RLock() (reentrant — callbacks may call broker)
        # TODO: Set _shutdown = False
        # TODO: If ASYNCHRONOUS: create _queue = queue.Queue() and start _async_worker thread
        #       (daemon=True, name="pub-sub-worker")
        pass

    # ------------------------------------------------------------------
    # Topic management
    # ------------------------------------------------------------------

    def create_topic(self, name: str) -> None:
        """Create a new topic. No-op if already exists (thread-safe).

        TODO: Under _lock, add Topic(name) to _topics if not present.
        """
        pass

    def delete_topic(self, name: str) -> None:
        """Delete a topic (thread-safe).

        TODO:
            - Under _lock: raise TopicNotFoundError if not found
            - Delete from _topics
        """
        pass

    # ------------------------------------------------------------------
    # Core pub/sub
    # ------------------------------------------------------------------

    def publish(self, publisher_id: str, topic: str, payload: Any) -> Message:
        """Publish a message to a topic. Returns the created Message.

        TODO:
            - Under _lock: raise TopicNotFoundError if topic not found; get topic ref
            - Create Message(topic, payload, publisher_id)
            - Call t.add_message(message)
            - Get snapshot of subscribers (t.get_subscribers())
            - For each callback:
              - SYNCHRONOUS: call _deliver(message, callback)
              - ASYNCHRONOUS: put (message, callback) in _queue
            - Return message
        """
        pass

    def subscribe(
        self,
        subscriber_id: str,
        topic: str,
        callback: Callable[[Message], None],
    ) -> None:
        """Subscribe to a topic (thread-safe).

        TODO:
            - Under _lock: raise TopicNotFoundError if topic not found
            - Call t.add_subscriber(subscriber_id, callback)
        """
        pass

    def unsubscribe(self, subscriber_id: str, topic: str) -> None:
        """Unsubscribe from a topic (thread-safe).

        TODO:
            - Under _lock: raise TopicNotFoundError if topic not found
            - Call t.remove_subscriber(subscriber_id)
        """
        pass

    def get_messages(self, topic: str) -> List[Message]:
        """Return all messages published to a topic.

        TODO:
            - Under _lock: raise TopicNotFoundError if topic not found
            - Return t.get_messages()
        """
        pass

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def shutdown(self) -> None:
        """Cleanly shut down the async worker thread (no-op for synchronous broker).

        TODO:
            - Set _shutdown = True
            - If async: put None sentinel in _queue; join worker thread (timeout=3)
        """
        pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _deliver(self, message: Message, callback: Callable[[Message], None]) -> None:
        """Invoke callback with message, retrying on failure.

        TODO:
            - Try callback(message) up to (max_retries + 1) total attempts
            - On success: return immediately
            - After all retries exhausted: silently absorb the failure
        """
        pass

    def _async_worker(self) -> None:
        """Background thread: drain the async queue and deliver messages.

        TODO:
            - Loop: dequeue item from _queue
            - If item is None (sentinel): break and exit
            - Otherwise: unpack (message, callback) and call _deliver(message, callback)
        """
        pass
