"""
test_extended.py — Pub/Sub Messaging System
============================================
Extended tests: multiple subscribers, multiple topics, message history,
async delivery, and multi-message ordering.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
import threading
import time
from starter import Message, Topic, MessageBroker, DeliveryMode, TopicNotFoundError


# ---------------------------------------------------------------------------
# TestMultipleSubscribers
# ---------------------------------------------------------------------------

class TestMultipleSubscribers:

    def test_two_subscribers_both_receive_message(self) -> None:
        """Both subscribers must receive the message when one is published."""
        broker = MessageBroker()
        broker.create_topic("broadcast")

        received_a: list = []
        received_b: list = []
        broker.subscribe("sub-a", "broadcast", lambda m: received_a.append(m))
        broker.subscribe("sub-b", "broadcast", lambda m: received_b.append(m))

        broker.publish("pub1", "broadcast", "hello-all")

        assert len(received_a) == 1
        assert len(received_b) == 1
        assert received_a[0].payload == "hello-all"
        assert received_b[0].payload == "hello-all"

    def test_unsubscribe_one_leaves_other_active(self) -> None:
        """Removing one subscriber must not affect the other."""
        broker = MessageBroker()
        broker.create_topic("stream")

        received_a: list = []
        received_b: list = []
        broker.subscribe("sub-a", "stream", lambda m: received_a.append(m))
        broker.subscribe("sub-b", "stream", lambda m: received_b.append(m))

        broker.unsubscribe("sub-a", "stream")
        broker.publish("pub1", "stream", "still-live")

        assert len(received_a) == 0   # unsubscribed
        assert len(received_b) == 1   # still active
        assert received_b[0].payload == "still-live"

    def test_three_subscribers_all_receive(self) -> None:
        """Three subscribers on the same topic all receive the message."""
        broker = MessageBroker()
        broker.create_topic("multi")
        buckets: dict = {"s1": [], "s2": [], "s3": []}
        for sid, bucket in buckets.items():
            broker.subscribe(sid, "multi", lambda m, b=bucket: b.append(m))
        broker.publish("pub1", "multi", "ping")
        for sid, bucket in buckets.items():
            assert len(bucket) == 1, f"Subscriber {sid} did not receive message"


# ---------------------------------------------------------------------------
# TestMultipleTopics
# ---------------------------------------------------------------------------

class TestMultipleTopics:

    def test_message_on_topic_a_not_delivered_to_topic_b_subscriber(self) -> None:
        """Publishing to topic A must not deliver to a subscriber of topic B."""
        broker = MessageBroker()
        broker.create_topic("topic-a")
        broker.create_topic("topic-b")

        received_b: list = []
        broker.subscribe("sub-b", "topic-b", lambda m: received_b.append(m))

        broker.publish("pub1", "topic-a", "only-for-a")
        assert len(received_b) == 0

    def test_each_topic_receives_only_its_messages(self) -> None:
        """Subscribers on different topics receive only their own messages."""
        broker = MessageBroker()
        broker.create_topic("sports")
        broker.create_topic("finance")

        sports_received: list = []
        finance_received: list = []
        broker.subscribe("sports-sub", "sports", lambda m: sports_received.append(m))
        broker.subscribe("finance-sub", "finance", lambda m: finance_received.append(m))

        broker.publish("pub1", "sports", "goal!")
        broker.publish("pub2", "finance", "stock up")

        assert len(sports_received) == 1
        assert sports_received[0].payload == "goal!"
        assert len(finance_received) == 1
        assert finance_received[0].payload == "stock up"

    def test_same_subscriber_on_multiple_topics(self) -> None:
        """A single subscriber_id can subscribe to multiple topics independently."""
        broker = MessageBroker()
        broker.create_topic("alpha")
        broker.create_topic("beta")

        received: list = []
        broker.subscribe("omni-sub", "alpha", lambda m: received.append(("alpha", m.payload)))
        broker.subscribe("omni-sub", "beta", lambda m: received.append(("beta", m.payload)))

        broker.publish("pub1", "alpha", "a-msg")
        broker.publish("pub1", "beta", "b-msg")

        assert ("alpha", "a-msg") in received
        assert ("beta", "b-msg") in received


# ---------------------------------------------------------------------------
# TestMessageHistory
# ---------------------------------------------------------------------------

class TestMessageHistory:

    def test_get_messages_returns_all_messages_in_order(self) -> None:
        """get_messages must return messages in publish order."""
        broker = MessageBroker()
        broker.create_topic("log")
        payloads = ["first", "second", "third"]
        for p in payloads:
            broker.publish("pub1", "log", p)
        history = broker.get_messages("log")
        assert [m.payload for m in history] == payloads

    def test_get_messages_after_subscriber_added(self) -> None:
        """Messages published before a subscriber subscribed must still be in history."""
        broker = MessageBroker()
        broker.create_topic("audit")
        broker.publish("pub1", "audit", "early-event")
        # Subscribe after the publish
        broker.subscribe("late-sub", "audit", lambda m: None)
        history = broker.get_messages("audit")
        assert len(history) == 1
        assert history[0].payload == "early-event"

    def test_delete_topic_removes_it(self) -> None:
        """After delete_topic, publishing to that topic raises TopicNotFoundError."""
        broker = MessageBroker()
        broker.create_topic("temp")
        broker.publish("pub1", "temp", "before-delete")
        broker.delete_topic("temp")
        with pytest.raises(TopicNotFoundError):
            broker.publish("pub1", "temp", "after-delete")

    def test_delete_topic_prevents_subscribe(self) -> None:
        """After delete_topic, subscribing raises TopicNotFoundError."""
        broker = MessageBroker()
        broker.create_topic("ephemeral")
        broker.delete_topic("ephemeral")
        with pytest.raises(TopicNotFoundError):
            broker.subscribe("sub1", "ephemeral", lambda m: None)

    def test_delete_topic_prevents_get_messages(self) -> None:
        """After delete_topic, get_messages raises TopicNotFoundError."""
        broker = MessageBroker()
        broker.create_topic("gone")
        broker.delete_topic("gone")
        with pytest.raises(TopicNotFoundError):
            broker.get_messages("gone")


# ---------------------------------------------------------------------------
# TestAsyncDelivery
# ---------------------------------------------------------------------------

class TestAsyncDelivery:

    def test_async_broker_delivers_message_to_subscriber(self) -> None:
        """Async broker must eventually call subscriber callback after publish."""
        broker = MessageBroker(delivery_mode=DeliveryMode.ASYNCHRONOUS)
        try:
            broker.create_topic("async-topic")
            event = threading.Event()
            received: list = []

            def on_message(m: Message) -> None:
                received.append(m)
                event.set()

            broker.subscribe("async-sub", "async-topic", on_message)
            broker.publish("pub1", "async-topic", "async-payload")

            delivered = event.wait(timeout=2.0)
            assert delivered, "Async delivery did not fire within 2 seconds"
            assert len(received) == 1
            assert received[0].payload == "async-payload"
        finally:
            broker.shutdown()

    def test_async_broker_publish_returns_immediately(self) -> None:
        """publish() in async mode must return before the callback fires."""
        broker = MessageBroker(delivery_mode=DeliveryMode.ASYNCHRONOUS)
        try:
            broker.create_topic("timing-topic")
            callback_called = threading.Event()

            def slow_callback(m: Message) -> None:
                time.sleep(0.2)
                callback_called.set()

            broker.subscribe("sub1", "timing-topic", slow_callback)

            start = time.time()
            broker.publish("pub1", "timing-topic", "data")
            elapsed = time.time() - start

            # publish should return well before the 0.2s sleep in the callback
            assert elapsed < 0.15, (
                f"publish() blocked for {elapsed:.3f}s — expected async return"
            )
            # Wait for callback to confirm delivery
            callback_called.wait(timeout=2.0)
        finally:
            broker.shutdown()

    def test_async_shutdown_does_not_raise(self) -> None:
        """shutdown() on an async broker must complete cleanly."""
        broker = MessageBroker(delivery_mode=DeliveryMode.ASYNCHRONOUS)
        broker.create_topic("shutdown-test")
        broker.publish("pub1", "shutdown-test", "msg")
        broker.shutdown()  # should not raise


# ---------------------------------------------------------------------------
# TestPublishMultipleMessages
# ---------------------------------------------------------------------------

class TestPublishMultipleMessages:

    def test_subscriber_receives_all_five_messages_in_order(self) -> None:
        """Publishing 5 messages must deliver all 5, in order, to the subscriber."""
        broker = MessageBroker()
        broker.create_topic("stream")
        received: list = []
        broker.subscribe("sub1", "stream", lambda m: received.append(m.payload))

        for i in range(5):
            broker.publish("pub1", "stream", f"msg-{i}")

        assert len(received) == 5
        assert received == ["msg-0", "msg-1", "msg-2", "msg-3", "msg-4"]

    def test_get_messages_reflects_all_published(self) -> None:
        """get_messages must return all 5 messages after 5 publishes."""
        broker = MessageBroker()
        broker.create_topic("history-topic")
        for i in range(5):
            broker.publish("pub1", "history-topic", i)
        history = broker.get_messages("history-topic")
        assert len(history) == 5
        assert [m.payload for m in history] == list(range(5))
