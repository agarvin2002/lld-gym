"""
Problem 12: LRU Cache + LFU Cache — Complete Solution
"""

from collections import OrderedDict
from typing import Dict
import threading


class LRUCache:
    """
    Least Recently Used Cache using OrderedDict.
    O(1) get and put.

    OrderedDict maintains insertion order. We use move_to_end() to mark
    items as recently used. The front (first item) is always the LRU.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move to end (most recently used position)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update value and mark as most recently used
            self.cache.move_to_end(key)
            self.cache[key] = value
        else:
            if len(self.cache) >= self.capacity:
                # Evict least recently used (first item)
                self.cache.popitem(last=False)
            self.cache[key] = value


class LFUCache:
    """
    Least Frequently Used Cache.
    O(1) get and put using three hash maps + min_freq tracking.

    Data structures:
      key_to_val:   key -> value
      key_to_freq:  key -> access frequency
      freq_to_keys: frequency -> OrderedDict of keys (ordered by recency)
      min_freq:     current minimum frequency in the cache
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.min_freq: int = 0
        self.key_to_val: Dict[int, int] = {}
        self.key_to_freq: Dict[int, int] = {}
        self.freq_to_keys: Dict[int, OrderedDict[int, None]] = {}

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._increment_freq(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_to_val:
            # Update existing key
            self.key_to_val[key] = value
            self._increment_freq(key)
        else:
            if len(self.key_to_val) >= self.capacity:
                self._evict()
            # Insert new key with frequency 1
            self.key_to_val[key] = value
            self.key_to_freq[key] = 1
            if 1 not in self.freq_to_keys:
                self.freq_to_keys[1] = OrderedDict()
            self.freq_to_keys[1][key] = None
            self.min_freq = 1

    def _increment_freq(self, key: int) -> None:
        """Move key from its current frequency bucket to the next one."""
        freq = self.key_to_freq[key]
        # Remove from current frequency bucket
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq = freq + 1
        # Add to next frequency bucket
        new_freq = freq + 1
        self.key_to_freq[key] = new_freq
        if new_freq not in self.freq_to_keys:
            self.freq_to_keys[new_freq] = OrderedDict()
        self.freq_to_keys[new_freq][key] = None

    def _evict(self) -> None:
        """Evict the LFU key (LRU among ties)."""
        # The LRU key at min_freq bucket is the first item in the OrderedDict
        lfu_keys = self.freq_to_keys[self.min_freq]
        evict_key, _ = lfu_keys.popitem(last=False)
        if not self.freq_to_keys[self.min_freq]:
            del self.freq_to_keys[self.min_freq]
        del self.key_to_val[evict_key]
        del self.key_to_freq[evict_key]


class ThreadSafeLRUCache:
    """
    Thread-safe LRU Cache using a reentrant lock.
    All public operations are protected by the lock.
    """

    def __init__(self, capacity: int) -> None:
        self._cache: LRUCache = LRUCache(capacity)
        self._lock: threading.RLock = threading.RLock()

    def get(self, key: int) -> int:
        with self._lock:
            return self._cache.get(key)

    def put(self, key: int, value: int) -> None:
        with self._lock:
            self._cache.put(key, value)


class ThreadSafeLFUCache:
    """
    Thread-safe LFU Cache using a reentrant lock.
    All public operations are protected by the lock.
    """

    def __init__(self, capacity: int) -> None:
        self._cache: LFUCache = LFUCache(capacity)
        self._lock: threading.RLock = threading.RLock()

    def get(self, key: int) -> int:
        with self._lock:
            return self._cache.get(key)

    def put(self, key: int, value: int) -> None:
        with self._lock:
            self._cache.put(key, value)
