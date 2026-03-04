"""
test_edge.py — Pub/Sub Messaging System
========================================
Edge-case tests: error conditions, retry-on-failure, and concurrent publishing.
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
# TestErrors
# ---------------------------------------------------------------------------

class TestErrors:

    def test_publish_to_nonexistent_topic_raises(self) -> None:
        """publish() to a topic that was never created must raise TopicNotFoundError."""
        broker = MessageBroker()
        with pytest.raises(TopicNotFoundError):
            broker.publish("pub1", "does-not-exist", "payload")

    def test_subscribe_to_nonexistent_topic_raises(self) -> None:
        """subscribe() to a topic that does not exist must raise TopicNotFoundError."""
        broker = MessageBroker()
        with pytest.raises(TopicNotFoundError):
            broker.subscribe("sub1", "does-not-exist", lambda m: None)

    def test_unsubscribe_from_nonexistent_topic_raises(self) -> None:
        """unsubscribe() from a topic that does not exist must raise TopicNotFoundError."""
        broker = MessageBroker()
        with pytest.raises(TopicNotFoundError):
            broker.unsubscribe("sub1", "does-not-exist")

    def test_delete_nonexistent_topic_raises(self) -> None:
        """delete_topic() on a topic that does not exist must raise TopicNotFoundError."""
        broker = MessageBroker()
        with pytest.raises(TopicNotFoundError):
            broker.delete_topic("phantom")

    def test_get_messages_nonexistent_topic_raises(self) -> None:
        """get_messages() for a topic that does not exist must raise TopicNotFoundError."""
        broker = MessageBroker()
        with pytest.raises(TopicNotFoundError):
            broker.get_messages("missing")

    def test_error_message_mentions_topic_name(self) -> None:
        """TopicNotFoundError should include the topic name for debuggability."""
        broker = MessageBroker()
        topic_name = "vanished-topic"
        with pytest.raises(TopicNotFoundError, match=topic_name):
            broker.publish("pub1", topic_name, "data")


# ---------------------------------------------------------------------------
# TestRetryOnFailure
# ---------------------------------------------------------------------------

class TestRetryOnFailure:

    def _make_flaky_callback(self, fail_times: int, received: list) -> callable:
        """Return a callback that raises Exception for the first `fail_times` calls."""
        call_count = [0]

        def callback(msg: Message) -> None:
            call_count[0] += 1
            if call_count[0] <= fail_times:
                raise RuntimeError(f"Simulated failure #{call_count[0]}")
            received.append(msg)

        return callback

    def test_retry_succeeds_when_max_retries_sufficient(self) -> None:
        """With max_retries >= fail_count, message must eventually arrive."""
        fail_times = 2
        # max_retries=2 means 3 total attempts (0, 1, 2) — should succeed on attempt 3
        broker = MessageBroker(max_retries=2)
        broker.create_topic("flaky-topic")
        received: list = []
        flaky = self._make_flaky_callback(fail_times=fail_times, received=received)
        broker.subscribe("sub1", "flaky-topic", flaky)
        broker.publish("pub1", "flaky-topic", "retry-payload")
        assert len(received) == 1
        assert received[0].payload == "retry-payload"

    def test_retry_gives_up_when_max_retries_insufficient(self) -> None:
        """With max_retries < fail_count, the broker gives up and does not crash."""
        fail_times = 5
        # max_retries=2 means only 3 total attempts — all will fail
        broker = MessageBroker(max_retries=2)
        broker.create_topic("always-fails")
        received: list = []
        flaky = self._make_flaky_callback(fail_times=fail_times, received=received)
        broker.subscribe("sub1", "always-fails", flaky)
        # Must not raise — broker absorbs the failure after exhausting retries
        broker.publish("pub1", "always-fails", "lost-payload")
        assert len(received) == 0

    def test_retry_does_not_affect_other_subscribers(self) -> None:
        """A failing callback must not prevent delivery to other subscribers."""
        broker = MessageBroker(max_retries=0)  # zero retries = fail immediately
        broker.create_topic("mixed")
        received_good: list = []

        def bad_callback(msg: Message) -> None:
            raise RuntimeError("always fails")

        broker.subscribe("bad-sub", "mixed", bad_callback)
        broker.subscribe("good-sub", "mixed", lambda m: received_good.append(m))
        broker.publish("pub1", "mixed", "data")
        # good subscriber must still receive the message
        assert len(received_good) == 1


# ---------------------------------------------------------------------------
# TestConcurrentPublish
# ---------------------------------------------------------------------------

class TestConcurrentPublish:

    def test_10_threads_5_messages_each_all_received(self) -> None:
        """10 threads each publishing 5 messages must result in 50 deliveries."""
        broker = MessageBroker()
        broker.create_topic("concurrent-topic")

        counter_lock = threading.Lock()
        received_count = [0]

        def on_message(msg: Message) -> None:
            with counter_lock:
                received_count[0] += 1

        broker.subscribe("counter-sub", "concurrent-topic", on_message)

        def publish_batch(thread_id: int) -> None:
            for i in range(5):
                broker.publish(f"pub-{thread_id}", "concurrent-topic", f"t{thread_id}-m{i}")

        threads = [
            threading.Thread(target=publish_batch, args=(tid,))
            for tid in range(10)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert received_count[0] == 50, (
            f"Expected 50 messages but received {received_count[0]}"
        )

    def test_concurrent_publish_all_messages_stored_in_history(self) -> None:
        """50 concurrent messages must all appear in the topic history."""
        broker = MessageBroker()
        broker.create_topic("history-concurrent")

        def publish_batch(thread_id: int) -> None:
            for i in range(5):
                broker.publish(f"pub-{thread_id}", "history-concurrent", f"t{thread_id}-m{i}")

        threads = [
            threading.Thread(target=publish_batch, args=(tid,))
            for tid in range(10)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        history = broker.get_messages("history-concurrent")
        assert len(history) == 50, (
            f"Expected 50 messages in history but found {len(history)}"
        )

    def test_concurrent_subscribe_and_publish_no_crash(self) -> None:
        """Concurrent subscribe and publish operations must not raise exceptions."""
        broker = MessageBroker()
        broker.create_topic("race-topic")
        errors: list = []
        lock = threading.Lock()

        def subscriber_thread(sid: str) -> None:
            try:
                broker.subscribe(sid, "race-topic", lambda m: None)
            except Exception as e:
                with lock:
                    errors.append(str(e))

        def publisher_thread(pid: str) -> None:
            try:
                for _ in range(3):
                    broker.publish(pid, "race-topic", "data")
            except Exception as e:
                with lock:
                    errors.append(str(e))

        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=subscriber_thread, args=(f"sub-{i}",)))
        for i in range(5):
            threads.append(threading.Thread(target=publisher_thread, args=(f"pub-{i}",)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Unexpected errors during concurrent operations: {errors}"


# ---------------------------------------------------------------------------
# TestShutdown
# ---------------------------------------------------------------------------

class TestShutdown:

    def test_sync_broker_shutdown_does_not_raise(self) -> None:
        """shutdown() on a synchronous broker must complete without raising."""
        broker = MessageBroker(delivery_mode=DeliveryMode.SYNCHRONOUS)
        broker.create_topic("t")
        broker.shutdown()  # should not raise

    def test_async_broker_shutdown_joins_worker(self) -> None:
        """shutdown() on async broker must complete within a reasonable time."""
        broker = MessageBroker(delivery_mode=DeliveryMode.ASYNCHRONOUS)
        broker.create_topic("t")
        broker.publish("pub1", "t", "msg")
        start = time.time()
        broker.shutdown()
        elapsed = time.time() - start
        assert elapsed < 5.0, f"shutdown() took {elapsed:.2f}s — too slow"
