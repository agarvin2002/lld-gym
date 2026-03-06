"""
LRU Cache + LFU Cache — Starter File
========================================
Your task: Implement LRU and LFU caches, then wrap them in thread-safe versions.

Read problem.md and design.md before starting.

Design decisions:
  - LRUCache: use collections.OrderedDict (maintains insertion order)
    - get(): move accessed key to end (most recent), return value or -1
    - put(): update/insert key; if over capacity evict the FIRST item (least recent)
  - LFUCache: O(1) get/put using three dicts + min_freq tracking
    - key_to_val, key_to_freq, freq_to_keys (OrderedDict for LRU tie-breaking)
    - On access/update: increment freq; if freq bucket empties and was min, update min_freq
  - ThreadSafeLRUCache / ThreadSafeLFUCache: wrap with threading.RLock
"""

from collections import OrderedDict
from typing import Dict
import threading


class LRUCache:
    """
    Least Recently Used Cache — O(1) get and put.

    Uses OrderedDict: most-recently-used item is always at the END.
    """

    def __init__(self, capacity: int) -> None:
        # TODO: Store capacity
        # TODO: Create cache: OrderedDict[int, int] = OrderedDict()
        pass

    def get(self, key: int) -> int:
        """Return value for key, or -1 if not present.

        TODO:
            - If key not in cache: return -1
            - Move key to end (most recently used): cache.move_to_end(key)
            - Return cache[key]
        """
        pass

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair.

        TODO:
            - If key already exists: move to end, update value
            - If new key:
              - If at capacity: evict LRU item (cache.popitem(last=False))
              - Insert key at end
        """
        pass


class LFUCache:
    """
    Least Frequently Used Cache — O(1) get and put.

    Data structures:
      key_to_val:   key → value
      key_to_freq:  key → access count
      freq_to_keys: freq → OrderedDict of keys (LRU order within same frequency)
      min_freq:     current minimum frequency among all cached keys
    """

    def __init__(self, capacity: int) -> None:
        # TODO: Store capacity and set min_freq = 0
        # TODO: Create key_to_val: Dict[int, int] = {}
        # TODO: Create key_to_freq: Dict[int, int] = {}
        # TODO: Create freq_to_keys: Dict[int, OrderedDict[int, None]] = {}
        pass

    def get(self, key: int) -> int:
        """Return value for key, or -1 if not present.

        TODO:
            - If key not in key_to_val: return -1
            - Call _increment_freq(key) to update frequency tracking
            - Return key_to_val[key]
        """
        pass

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair.

        TODO:
            - If capacity <= 0: return immediately
            - If key already exists: update value, call _increment_freq(key)
            - If new key:
              - If at capacity: call _evict() to remove LFU item
              - Insert key: key_to_val[key] = value, key_to_freq[key] = 1
              - Add to freq_to_keys[1] (create OrderedDict if needed)
              - Set min_freq = 1
        """
        pass

    def _increment_freq(self, key: int) -> None:
        """Move key from its current frequency bucket to the next.

        TODO:
            - Get current freq = key_to_freq[key]
            - Remove key from freq_to_keys[freq]; if bucket empty, delete it
              - If that was min_freq: update min_freq = freq + 1
            - Increment key_to_freq[key]
            - Add key to freq_to_keys[freq+1] (create if needed)
        """
        pass

    def _evict(self) -> None:
        """Evict the LFU key (LRU among ties at min_freq).

        TODO:
            - Get the LRU key from freq_to_keys[min_freq] using popitem(last=False)
            - If that bucket is now empty, delete it from freq_to_keys
            - Remove from key_to_val and key_to_freq
        """
        pass


class ThreadSafeLRUCache:
    """Thread-safe LRU Cache using a reentrant lock."""

    def __init__(self, capacity: int) -> None:
        # TODO: Create self._cache = LRUCache(capacity)
        # TODO: Create self._lock = threading.RLock()
        pass

    def get(self, key: int) -> int:
        # TODO: Under _lock, delegate to self._cache.get(key)
        pass

    def put(self, key: int, value: int) -> None:
        # TODO: Under _lock, delegate to self._cache.put(key, value)
        pass


class ThreadSafeLFUCache:
    """Thread-safe LFU Cache using a reentrant lock."""

    def __init__(self, capacity: int) -> None:
        # TODO: Create self._cache = LFUCache(capacity)
        # TODO: Create self._lock = threading.RLock()
        pass

    def get(self, key: int) -> int:
        # TODO: Under _lock, delegate to self._cache.get(key)
        pass

    def put(self, key: int, value: int) -> None:
        # TODO: Under _lock, delegate to self._cache.put(key, value)
        pass
