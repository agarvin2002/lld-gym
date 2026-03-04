"""
Extended tests for LRU Cache — Problem 12.
Tests LFU cache behaviour including frequency tracking and tie-breaking.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
from starter import LFUCache


class TestLFUCache:

    def test_lfu_evicts_least_frequently_used(self) -> None:
        """The item with the lowest access frequency should be evicted first."""
        cache = LFUCache(2)
        cache.put(1, 1)   # freq[1]=1
        cache.put(2, 2)   # freq[2]=1
        cache.get(1)      # freq[1]=2
        cache.put(3, 3)   # evicts key 2 (freq=1), freq[3]=1
        assert cache.get(2) == -1
        assert cache.get(1) == 1
        assert cache.get(3) == 3

    def test_lfu_tie_evicts_lru(self) -> None:
        """On frequency tie, the least recently used key should be evicted."""
        cache = LFUCache(2)
        cache.put(1, 1)   # freq[1]=1
        cache.put(2, 2)   # freq[2]=1
        cache.get(1)      # freq[1]=2, key 2 is LRU at freq=1
        cache.get(2)      # freq[2]=2, now both at freq=2; key 1 was accessed first so is LRU
        cache.put(3, 3)   # tie at freq=2; key 1 was LRU among them, evict key 1
        assert cache.get(1) == -1
        assert cache.get(2) == 2
        assert cache.get(3) == 3

    def test_lfu_get_returns_minus_one_for_missing(self) -> None:
        """get on a non-existent key should return -1."""
        cache = LFUCache(3)
        assert cache.get(42) == -1

    def test_lfu_put_updates_existing_key(self) -> None:
        """Updating an existing key should increment its frequency."""
        cache = LFUCache(2)
        cache.put(1, 1)   # freq[1]=1
        cache.put(2, 2)   # freq[2]=1
        cache.put(1, 100) # update key 1, freq[1]=2
        cache.put(3, 3)   # evicts key 2 (freq=1)
        assert cache.get(1) == 100
        assert cache.get(2) == -1
        assert cache.get(3) == 3

    def test_lfu_capacity_one(self) -> None:
        """LFU with capacity=1 should always evict the only item to make room."""
        cache = LFUCache(1)
        cache.put(1, 10)
        assert cache.get(1) == 10
        cache.put(2, 20)
        assert cache.get(1) == -1
        assert cache.get(2) == 20

    def test_lfu_full_sequence_from_problem_statement(self) -> None:
        """Reproduce the exact LFU sequence from the problem statement."""
        cache = LFUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1   # freq[1]=2
        cache.put(3, 3)            # evicts key 2 (freq=1)
        assert cache.get(2) == -1
        assert cache.get(3) == 3   # freq[3]=2
        cache.put(4, 4)            # both freq=2; key 1 is LRU, evict key 1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

    def test_lfu_high_frequency_key_survives_many_evictions(self) -> None:
        """A frequently accessed key should survive many evictions of others."""
        cache = LFUCache(3)
        cache.put(1, 1)
        for _ in range(10):
            cache.get(1)   # freq[1] = 11
        cache.put(2, 2)
        cache.put(3, 3)
        cache.put(4, 4)    # evicts key 2 (freq=1)
        assert cache.get(1) == 1   # key 1 still alive
        assert cache.get(2) == -1
