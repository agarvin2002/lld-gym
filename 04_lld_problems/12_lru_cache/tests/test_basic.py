"""
Basic tests for LRU Cache — Problem 12.
Tests fundamental put/get operations and LRU eviction.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
from starter import LRUCache


class TestLRUCacheBasic:

    def test_lru_get_returns_minus_one_for_missing(self) -> None:
        """get on a key that was never inserted should return -1."""
        cache = LRUCache(2)
        assert cache.get(1) == -1
        assert cache.get(99) == -1

    def test_lru_put_and_get_basic(self) -> None:
        """put then get should return the stored value."""
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        assert cache.get(1) == 10
        assert cache.get(2) == 20

    def test_lru_evicts_least_recently_used(self) -> None:
        """When capacity is exceeded, the LRU item should be evicted."""
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)   # should evict key 1 (LRU)
        assert cache.get(1) == -1
        assert cache.get(2) == 2
        assert cache.get(3) == 3

    def test_lru_get_updates_recency(self) -> None:
        """Accessing a key via get should promote it to most recently used."""
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.get(1)       # key 1 is now MRU; key 2 is LRU
        cache.put(3, 3)    # should evict key 2 (LRU), not key 1
        assert cache.get(1) == 1
        assert cache.get(2) == -1
        assert cache.get(3) == 3

    def test_lru_put_updates_existing_key(self) -> None:
        """put on an existing key should update the value without changing capacity count."""
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(1, 100)  # update key 1 — should NOT evict key 2
        assert cache.get(1) == 100
        assert cache.get(2) == 2

    def test_lru_capacity_one(self) -> None:
        """Cache with capacity=1 should always hold only the most recently put item."""
        cache = LRUCache(1)
        cache.put(1, 1)
        assert cache.get(1) == 1
        cache.put(2, 2)
        assert cache.get(1) == -1
        assert cache.get(2) == 2
        cache.put(2, 99)
        assert cache.get(2) == 99

    def test_lru_full_sequence_from_problem_statement(self) -> None:
        """Reproduce the exact sequence from the problem statement."""
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)    # evicts key 2
        assert cache.get(2) == -1
        assert cache.get(3) == 3
        cache.put(4, 4)    # evicts key 1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4
