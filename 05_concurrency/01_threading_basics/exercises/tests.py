"""Tests for BoundedBuffer (thread-safe producer-consumer buffer)."""

import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import BoundedBuffer


class TestInitialState:
    def test_initial_state(self):
        buf = BoundedBuffer(5)
        assert buf.size == 0
        assert buf.capacity == 5
        assert buf.is_empty() is True
        assert buf.is_full() is False

    def test_capacity_is_preserved(self):
        for cap in (1, 10, 100):
            buf = BoundedBuffer(cap)
            assert buf.capacity == cap


class TestBasicPutGet:
    def test_put_and_get_single_item(self):
        buf = BoundedBuffer(3)
        buf.put(42)
        assert buf.get() == 42

    def test_fifo_order(self):
        buf = BoundedBuffer(5)
        for item in ('A', 'B', 'C'):
            buf.put(item)
        assert buf.get() == 'A'
        assert buf.get() == 'B'
        assert buf.get() == 'C'

    def test_size_increases_on_put(self):
        buf = BoundedBuffer(5)
        for i in range(3):
            buf.put(i)
            assert buf.size == i + 1

    def test_size_decreases_on_get(self):
        buf = BoundedBuffer(5)
        for i in range(3):
            buf.put(i)
        for remaining in (2, 1, 0):
            buf.get()
            assert buf.size == remaining

    def test_multiple_item_types(self):
        buf = BoundedBuffer(5)
        items = [1, 'hello', None, 3.14, [1, 2, 3]]
        for item in items:
            buf.put(item)
        for expected in items:
            assert buf.get() == expected


class TestFullAndEmpty:
    def test_is_full_when_capacity_reached(self):
        buf = BoundedBuffer(3)
        assert buf.is_full() is False
        buf.put(1)
        buf.put(2)
        assert buf.is_full() is False
        buf.put(3)
        assert buf.is_full() is True

    def test_is_empty_after_all_items_removed(self):
        buf = BoundedBuffer(3)
        buf.put('x')
        buf.put('y')
        buf.get()
        buf.get()
        assert buf.is_empty() is True

    def test_not_empty_after_put(self):
        buf = BoundedBuffer(3)
        buf.put('item')
        assert buf.is_empty() is False


class TestBlocking:
    def test_put_blocks_when_full(self):
        """A put() call on a full buffer must block until a consumer reads."""
        buf = BoundedBuffer(2)
        buf.put('a')
        buf.put('b')  # buffer is now full

        blocker = threading.Thread(target=buf.put, args=('c',), daemon=True)
        blocker.start()
        time.sleep(0.05)  # give the thread time to run

        # Thread should still be alive because no consumer has called get()
        assert blocker.is_alive(), "put() should block when the buffer is full"

        # Unblock: consume one item so the blocked put() can proceed
        buf.get()
        blocker.join(timeout=1.0)
        assert not blocker.is_alive(), "put() should unblock once space is available"

    def test_get_blocks_when_empty(self):
        """A get() call on an empty buffer must block until a producer writes."""
        buf = BoundedBuffer(2)

        result = []
        def consumer():
            result.append(buf.get())

        t = threading.Thread(target=consumer, daemon=True)
        t.start()
        time.sleep(0.05)

        assert t.is_alive(), "get() should block when the buffer is empty"

        buf.put('item')
        t.join(timeout=1.0)
        assert not t.is_alive(), "get() should unblock once an item is available"
        assert result == ['item']


class TestConcurrency:
    def test_concurrent_producers_consumers(self):
        """5 producers x 10 items each, 5 consumers x 10 items each — no loss."""
        buf = BoundedBuffer(5)
        num_producers = 5
        items_each = 10
        total = num_producers * items_each

        produced = []
        consumed = []
        lock = threading.Lock()

        def producer(start):
            for i in range(start, start + items_each):
                buf.put(i)
                with lock:
                    produced.append(i)

        def consumer():
            for _ in range(items_each):
                item = buf.get()
                with lock:
                    consumed.append(item)

        producers = [
            threading.Thread(target=producer, args=(i * items_each,))
            for i in range(num_producers)
        ]
        consumers = [
            threading.Thread(target=consumer)
            for _ in range(num_producers)
        ]

        for t in producers + consumers:
            t.start()
        for t in producers + consumers:
            t.join(timeout=10.0)

        assert len(produced) == total, "all items should have been produced"
        assert len(consumed) == total, "all items should have been consumed"
        assert sorted(consumed) == sorted(produced), (
            "consumed items must match produced items exactly (no loss/duplication)"
        )

    def test_capacity_one(self):
        """With capacity=1 every put must wait for a corresponding get."""
        buf = BoundedBuffer(1)
        results = []

        def producer():
            for i in range(5):
                buf.put(i)

        def consumer():
            for _ in range(5):
                results.append(buf.get())

        p = threading.Thread(target=producer)
        c = threading.Thread(target=consumer)
        p.start()
        c.start()
        p.join(timeout=5.0)
        c.join(timeout=5.0)

        assert not p.is_alive(), "producer thread should have finished"
        assert not c.is_alive(), "consumer thread should have finished"
        assert results == list(range(5)), "items must arrive in FIFO order"

    def test_many_threads_stress(self):
        """Stress test: 10 producers and 10 consumers, 20 items each."""
        buf = BoundedBuffer(4)
        n_threads = 10
        items_each = 20
        total = n_threads * items_each

        counter = {'produced': 0, 'consumed': 0}
        lock = threading.Lock()

        def producer():
            for _ in range(items_each):
                buf.put(1)
                with lock:
                    counter['produced'] += 1

        def consumer():
            for _ in range(items_each):
                buf.get()
                with lock:
                    counter['consumed'] += 1

        threads = (
            [threading.Thread(target=producer) for _ in range(n_threads)]
            + [threading.Thread(target=consumer) for _ in range(n_threads)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=15.0)

        assert counter['produced'] == total
        assert counter['consumed'] == total
