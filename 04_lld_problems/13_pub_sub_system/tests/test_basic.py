"""
test_basic.py — Pub/Sub Messaging System
=========================================
Basic / happy-path tests. These should pass with a minimal correct implementation.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
import time
from starter import Message, Topic, MessageBroker, DeliveryMode, TopicNotFoundError


# ---------------------------------------------------------------------------
# TestMessage
# ---------------------------------------------------------------------------

class TestMessage:

    def test_message_id_is_non_empty_string(self) -> None:
        """message_id must be a non-empty string (e.g. a UUID)."""
        msg = Message(topic="news", payload="hello", publisher_id="pub1")
        assert isinstance(msg.message_id, str)
        assert len(msg.message_id) > 0

    def test_message_topic_matches(self) -> None:
        """topic attribute must equal the value passed in."""
        msg = Message(topic="orders", payload=42, publisher_id="pub2")
        assert msg.topic == "orders"

    def test_message_payload_matches(self) -> None:
        """payload attribute must equal the value passed in."""
        payload = {"key": "value", "count": 7}
        msg = Message(topic="events", payload=payload, publisher_id="pub3")
        assert msg.payload == payload

    def test_message_timestamp_is_positive_float(self) -> None:
        """timestamp must be a positive float (unix epoch)."""
        before = time.time()
        msg = Message(topic="t", payload=None, publisher_id="pub4")
        after = time.time()
        assert isinstance(msg.timestamp, float)
        assert msg.timestamp > 0
        assert before <= msg.timestamp <= after

    def test_message_publisher_id_matches(self) -> None:
        """publisher_id must equal the value passed in."""
        msg = Message(topic="t", payload=None, publisher_id="publisher-xyz")
        assert msg.publisher_id == "publisher-xyz"

    def test_two_messages_have_different_ids(self) -> None:
        """Each Message must receive a unique message_id."""
        msg1 = Message(topic="t", payload=1, publisher_id="p")
        msg2 = Message(topic="t", payload=2, publisher_id="p")
        assert msg1.message_id != msg2.message_id


# ---------------------------------------------------------------------------
# TestTopic
# ---------------------------------------------------------------------------

class TestTopic:

    def test_topic_name_is_correct(self) -> None:
        """Topic name attribute must match the value passed to __init__."""
        t = Topic("my-topic")
        assert t.name == "my-topic"

    def test_new_topic_has_no_subscribers(self) -> None:
        """A freshly created Topic should have an empty subscriber mapping."""
        t = Topic("empty")
        assert len(t.get_subscribers()) == 0

    def test_add_subscriber_registers_callback(self) -> None:
        """add_subscriber must make the callback retrievable via get_subscribers."""
        t = Topic("events")
        cb = lambda msg: None
        t.add_subscriber("sub1", cb)
        subs = t.get_subscribers()
        assert "sub1" in subs
        assert subs["sub1"] is cb

    def test_remove_subscriber_deregisters_callback(self) -> None:
        """remove_subscriber must remove the subscriber from the mapping."""
        t = Topic("events")
        t.add_subscriber("sub1", lambda msg: None)
        t.remove_subscriber("sub1")
        assert "sub1" not in t.get_subscribers()

    def test_get_subscribers_returns_copy(self) -> None:
        """Mutating the dict returned by get_subscribers must not affect the Topic."""
        t = Topic("events")
        t.add_subscriber("sub1", lambda msg: None)
        snapshot = t.get_subscribers()
        snapshot["injected"] = lambda msg: None  # mutate the snapshot
        # The topic itself must not be affected
        assert "injected" not in t.get_subscribers()

    def test_add_message_stores_message(self) -> None:
        """add_message must make the message retrievable via get_messages."""
        t = Topic("news")
        msg = Message(topic="news", payload="p", publisher_id="pub")
        t.add_message(msg)
        history = t.get_messages()
        assert len(history) == 1
        assert history[0] is msg

    def test_get_messages_returns_copy(self) -> None:
        """Mutating the list returned by get_messages must not affect the Topic."""
        t = Topic("news")
        msg = Message(topic="news", payload="p", publisher_id="pub")
        t.add_message(msg)
        history = t.get_messages()
        history.clear()
        assert len(t.get_messages()) == 1


# ---------------------------------------------------------------------------
# TestMessageBrokerBasic
# ---------------------------------------------------------------------------

class TestMessageBrokerBasic:

    def test_create_topic_succeeds(self) -> None:
        """create_topic must not raise for a new topic name."""
        broker = MessageBroker()
        broker.create_topic("alpha")  # should not raise

    def test_create_topic_is_idempotent(self) -> None:
        """Calling create_topic twice with the same name must not raise."""
        broker = MessageBroker()
        broker.create_topic("alpha")
        broker.create_topic("alpha")  # no-op, should not raise

    def test_publish_to_existing_topic_returns_message(self) -> None:
        """publish() must return a Message object."""
        broker = MessageBroker()
        broker.create_topic("news")
        msg = broker.publish("pub1", "news", "headline")
        assert isinstance(msg, Message)

    def test_published_message_payload_matches(self) -> None:
        """The returned Message's payload must match what was published."""
        broker = MessageBroker()
        broker.create_topic("news")
        payload = {"headline": "LLD is fun"}
        msg = broker.publish("pub1", "news", payload)
        assert msg.payload == payload

    def test_subscribe_receives_message_via_callback(self) -> None:
        """A subscribed callback must be called when a message is published."""
        broker = MessageBroker()
        broker.create_topic("orders")
        received: list = []
        broker.subscribe("sub1", "orders", lambda m: received.append(m))
        broker.publish("pub1", "orders", "order-data")
        assert len(received) == 1
        assert received[0].payload == "order-data"

    def test_unsubscribe_stops_delivery(self) -> None:
        """After unsubscribe, the callback must no longer receive messages."""
        broker = MessageBroker()
        broker.create_topic("orders")
        received: list = []
        broker.subscribe("sub1", "orders", lambda m: received.append(m))
        broker.unsubscribe("sub1", "orders")
        broker.publish("pub1", "orders", "should-not-arrive")
        assert len(received) == 0

    def test_get_messages_returns_published_messages(self) -> None:
        """get_messages must return the list of all messages published to a topic."""
        broker = MessageBroker()
        broker.create_topic("log")
        broker.publish("pub1", "log", "msg-1")
        broker.publish("pub1", "log", "msg-2")
        history = broker.get_messages("log")
        assert len(history) == 2
        assert history[0].payload == "msg-1"
        assert history[1].payload == "msg-2"
