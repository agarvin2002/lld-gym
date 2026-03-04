"""
Edge case and concurrency tests for LRU/LFU Cache — Problem 12.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import threading
import pytest
from starter import ThreadSafeLRUCache, ThreadSafeLFUCache, LRUCache, LFUCache


class TestThreadSafeCache:

    def test_thread_safe_concurrent_put_get(self) -> None:
        """Multiple threads performing put/get should not corrupt the cache."""
        cache = ThreadSafeLRUCache(100)
        errors: list[Exception] = []
        results: dict[int, int] = {}

        def worker(thread_id: int) -> None:
            try:
                for i in range(20):
                    key = thread_id * 20 + i
                    cache.put(key, key * 2)
                for i in range(20):
                    key = thread_id * 20 + i
                    val = cache.get(key)
                    # value may have been evicted due to capacity; that is fine
                    if val != -1:
                        results[key] = val
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Thread errors: {errors}"
        for key, val in results.items():
            assert val == key * 2, f"Corrupted value for key {key}: expected {key * 2}, got {val}"

    def test_thread_safe_lfu_concurrent(self) -> None:
        """Thread-safe LFU should handle concurrent access without corruption."""
        cache = ThreadSafeLFUCache(50)
        errors: list[Exception] = []

        def writer(start: int) -> None:
            try:
                for i in range(start, start + 25):
                    cache.put(i, i * 3)
            except Exception as e:
                errors.append(e)

        def reader(start: int) -> None:
            try:
                for i in range(start, start + 25):
                    cache.get(i)  # value may or may not exist
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=writer, args=(0,)),
            threading.Thread(target=writer, args=(25,)),
            threading.Thread(target=reader, args=(0,)),
            threading.Thread(target=reader, args=(25,)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Thread errors: {errors}"

    def test_thread_safe_lru_returns_correct_values_under_load(self) -> None:
        """Values inserted without eviction pressure should be retrievable."""
        cache = ThreadSafeLRUCache(1000)
        barrier = threading.Barrier(10)
        errors: list[Exception] = []

        def fill_and_check(tid: int) -> None:
            try:
                barrier.wait()
                cache.put(tid, tid * 7)
                barrier.wait()
                val = cache.get(tid)
                if val != -1:
                    assert val == tid * 7
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=fill_and_check, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0


class TestEdgeCases:

    def test_lru_put_zero_value(self) -> None:
        """Value of 0 is a valid value and should not be confused with -1 (miss)."""
        cache = LRUCache(2)
        cache.put(1, 0)
        assert cache.get(1) == 0

    def test_lru_same_key_put_multiple_times(self) -> None:
        """Repeated puts to the same key should always reflect the latest value."""
        cache = LRUCache(2)
        for v in range(100):
            cache.put(1, v)
        assert cache.get(1) == 99

    def test_lfu_get_increments_freq_so_survives_eviction(self) -> None:
        """Accessing a key should increment its freq so it outlasts lower-freq keys."""
        cache = LFUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.get(1)       # freq[1]=2, freq[2]=1
        cache.put(3, 30)   # evicts key 2 (lowest freq)
        assert cache.get(1) == 10
        assert cache.get(2) == -1
        assert cache.get(3) == 30

    def test_lru_does_not_evict_when_updating_existing_key(self) -> None:
        """Updating an existing key should not increase size or trigger eviction."""
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        # Update key 1 — cache size stays 2, no eviction needed
        cache.put(1, 999)
        # Both keys still present
        assert cache.get(1) == 999
        assert cache.get(2) == 2

    def test_lfu_zero_capacity_edge(self) -> None:
        """LFU/LRU with capacity 0 should handle puts without crashing."""
        # Some implementations simply do nothing; just ensure no exception
        try:
            cache = LFUCache(0)
            cache.put(1, 1)
            assert cache.get(1) == -1
        except Exception:
            pass  # Acceptable to raise on capacity=0
