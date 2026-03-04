"""
Tests for Thread-safe EventBus
================================
Run with:
    /tmp/lld_venv/bin/pytest 05_concurrency/03_thread_safe_patterns/exercises/tests.py -v
"""

import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import EventBus


# ---------------------------------------------------------------------------
# Basic behaviour
# ---------------------------------------------------------------------------

class TestSubscribeAndPublish:
    def test_subscribe_and_publish(self):
        """A single subscribed handler is called with the correct data."""
        bus = EventBus()
        received = []

        bus.subscribe("click", lambda data: received.append(data))
        count = bus.publish("click", "button_id=42")

        assert count == 1
        assert received == ["button_id=42"]

    def test_multiple_subscribers_same_event(self):
        """Both handlers are called when two handlers are registered for the same event."""
        bus = EventBus()
        calls = []

        bus.subscribe("login", lambda d: calls.append(("h1", d)))
        bus.subscribe("login", lambda d: calls.append(("h2", d)))
        count = bus.publish("login", "user=alice")

        assert count == 2
        assert ("h1", "user=alice") in calls
        assert ("h2", "user=alice") in calls

    def test_different_event_types_isolated(self):
        """Publishing 'click' must not trigger handlers registered for 'hover'."""
        bus = EventBus()
        hover_calls = []

        bus.subscribe("hover", lambda d: hover_calls.append(d))
        count = bus.publish("click", "button")

        assert count == 0
        assert hover_calls == []

    def test_publish_unknown_event_returns_zero(self):
        """Publishing to an event type with no subscribers returns 0."""
        bus = EventBus()
        count = bus.publish("nonexistent_event", "data")
        assert count == 0


# ---------------------------------------------------------------------------
# Unsubscribe
# ---------------------------------------------------------------------------

class TestUnsubscribe:
    def test_unsubscribe_removes_handler(self):
        """After unsubscribing, the handler is not called on the next publish."""
        bus = EventBus()
        calls = []
        handler = lambda d: calls.append(d)

        bus.subscribe("resize", handler)
        bus.unsubscribe("resize", handler)
        bus.publish("resize", "1920x1080")

        assert calls == []

    def test_unsubscribe_nonexistent_is_noop(self):
        """Unsubscribing a handler that was never registered must not raise."""
        bus = EventBus()

        def never_registered(data):
            pass

        # Should not raise any exception
        bus.unsubscribe("scroll", never_registered)
        bus.unsubscribe("nonexistent_event", never_registered)

    def test_unsubscribe_only_removes_one_handler(self):
        """Unsubscribing one handler does not affect other handlers for the same event."""
        bus = EventBus()
        calls = []

        handler_a = lambda d: calls.append(("a", d))
        handler_b = lambda d: calls.append(("b", d))

        bus.subscribe("keypress", handler_a)
        bus.subscribe("keypress", handler_b)
        bus.unsubscribe("keypress", handler_a)
        bus.publish("keypress", "Enter")

        assert ("b", "Enter") in calls
        assert ("a", "Enter") not in calls


# ---------------------------------------------------------------------------
# Return values and counts
# ---------------------------------------------------------------------------

class TestReturnValues:
    def test_publish_returns_handler_count(self):
        """publish() returns the exact number of handlers that were called."""
        bus = EventBus()

        bus.subscribe("event", lambda d: None)
        bus.subscribe("event", lambda d: None)
        bus.subscribe("event", lambda d: None)

        assert bus.publish("event") == 3

    def test_subscriber_count_correct(self):
        """subscriber_count() reflects the current number of registered handlers."""
        bus = EventBus()
        assert bus.subscriber_count("evt") == 0

        bus.subscribe("evt", lambda d: None)
        assert bus.subscriber_count("evt") == 1

        bus.subscribe("evt", lambda d: None)
        assert bus.subscriber_count("evt") == 2

    def test_subscriber_count_decreases_after_unsubscribe(self):
        """subscriber_count() decreases by one after a successful unsubscribe."""
        bus = EventBus()
        h = lambda d: None

        bus.subscribe("evt", h)
        assert bus.subscriber_count("evt") == 1
        bus.unsubscribe("evt", h)
        assert bus.subscriber_count("evt") == 0


# ---------------------------------------------------------------------------
# Deadlock prevention
# ---------------------------------------------------------------------------

class TestDeadlockPrevention:
    def test_handler_can_publish(self):
        """A handler that calls bus.publish() must not cause a deadlock."""
        bus = EventBus()
        secondary_calls = []

        def primary_handler(data):
            # This publish happens while the bus lock is NOT held — no deadlock.
            bus.publish("secondary", data + "_processed")

        bus.subscribe("primary", primary_handler)
        bus.subscribe("secondary", lambda d: secondary_calls.append(d))

        # If there is a deadlock this test will hang; pytest-timeout (or the
        # test runner's own timeout) will catch it.
        bus.publish("primary", "payload")

        assert secondary_calls == ["payload_processed"]

    def test_handler_can_subscribe(self):
        """A handler that calls bus.subscribe() must not cause a deadlock."""
        bus = EventBus()
        late_calls = []

        def self_subscribing_handler(data):
            bus.subscribe("late_event", lambda d: late_calls.append(d))

        bus.subscribe("setup", self_subscribing_handler)
        bus.publish("setup", None)
        bus.publish("late_event", "hello")

        assert late_calls == ["hello"]


# ---------------------------------------------------------------------------
# Thread-safety (concurrent access)
# ---------------------------------------------------------------------------

class TestConcurrency:
    def test_concurrent_subscribe_publish(self):
        """5 threads subscribe while 5 other threads publish — no crash, all handled."""
        bus = EventBus()
        call_count = 0
        lock = threading.Lock()

        def subscriber_thread():
            for _ in range(10):
                bus.subscribe("load", lambda d, _l=lock, _c=call_count: None)
                time.sleep(0.0005)

        def publisher_thread():
            for _ in range(100):
                received = []
                bus.subscribe("tick", lambda d: received.append(d))
                bus.publish("tick", 1)

        sub_threads = [threading.Thread(target=subscriber_thread) for _ in range(5)]
        pub_threads = [threading.Thread(target=publisher_thread) for _ in range(5)]

        all_threads = sub_threads + pub_threads
        for t in all_threads:
            t.start()
        for t in all_threads:
            t.join(timeout=10)

        # Primary assertion: no exception was raised and all threads completed
        assert all(not t.is_alive() for t in all_threads), "Some threads did not finish"

    def test_concurrent_subscribe_unsubscribe(self):
        """Threads adding and removing handlers concurrently must not crash."""
        bus = EventBus()
        errors = []

        def toggle_handler():
            handler = lambda d: None
            try:
                for _ in range(50):
                    bus.subscribe("event", handler)
                    bus.unsubscribe("event", handler)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=toggle_handler) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        assert errors == [], f"Exceptions raised during concurrent access: {errors}"

    def test_all_publishes_reach_subscribers_under_concurrency(self):
        """Every published event must reach every subscriber that was registered before publish."""
        bus = EventBus()
        received = []
        lock = threading.Lock()

        # Register 10 handlers upfront (before concurrent publishing begins)
        for _ in range(10):
            bus.subscribe("data", lambda d: (lock.acquire(), received.append(d), lock.release()))

        publish_count = 20

        def publish_thread():
            for i in range(publish_count):
                bus.publish("data", i)

        threads = [threading.Thread(target=publish_thread) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        # 5 threads * 20 publishes * 10 handlers = 1000 calls
        expected = 5 * publish_count * 10
        assert len(received) == expected, f"Expected {expected} calls, got {len(received)}"
