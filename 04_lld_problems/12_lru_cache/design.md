# Design: LRU Cache + LFU Cache

## Class Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        LRUCache                             │
├─────────────────────────────────────────────────────────────┤
│ - capacity: int                                             │
│ - cache: OrderedDict[int, int]                              │
├─────────────────────────────────────────────────────────────┤
│ + get(key: int) -> int                                      │
│ + put(key: int, value: int) -> None                         │
│ - _evict() -> None                                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       LFUCache                              │
├─────────────────────────────────────────────────────────────┤
│ - capacity: int                                             │
│ - min_freq: int                                             │
│ - key_to_val: Dict[int, int]                                │
│ - key_to_freq: Dict[int, int]                               │
│ - freq_to_keys: Dict[int, OrderedDict[int, None]]           │
├─────────────────────────────────────────────────────────────┤
│ + get(key: int) -> int                                      │
│ + put(key: int, value: int) -> None                         │
│ - _increment_freq(key: int) -> None                         │
│ - _evict() -> None                                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   ThreadSafeLRUCache                        │
├─────────────────────────────────────────────────────────────┤
│ - _lock: threading.RLock                                    │
│ - _cache: LRUCache                                          │
├─────────────────────────────────────────────────────────────┤
│ + get(key: int) -> int      [synchronized]                  │
│ + put(key: int, value: int) [synchronized]                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   ThreadSafeLFUCache                        │
├─────────────────────────────────────────────────────────────┤
│ - _lock: threading.RLock                                    │
│ - _cache: LFUCache                                          │
├─────────────────────────────────────────────────────────────┤
│ + get(key: int) -> int      [synchronized]                  │
│ + put(key: int, value: int) [synchronized]                  │
└─────────────────────────────────────────────────────────────┘
```

---

## LRU Cache — Data Structure

```
OrderedDict (doubly-linked-list + hashmap internally):

  Head ←→ [key=2, val=20] ←→ [key=1, val=10] ←→ Tail
           (LRU / oldest)                        (MRU / newest)

  On get(1):  move key=1 to end  →  [key=2] ←→ [key=1]
  On put(3):  add key=3 to end   →  [key=2] ←→ [key=1] ←→ [key=3]
  On evict:   remove from front  →  [key=1] ←→ [key=3]
```

---

## LFU Cache — Data Structures

```
key_to_val:   { 1: 10, 2: 20, 3: 30 }
key_to_freq:  { 1: 3,  2: 1,  3: 2  }
min_freq:     1

freq_to_keys:
  freq=1 → OrderedDict { 2: None }          ← LRU at this freq
  freq=2 → OrderedDict { 3: None }
  freq=3 → OrderedDict { 1: None }          ← MRU at this freq

On get(2):
  - freq[2]: 1 → 2
  - freq_to_keys[1].remove(2); freq_to_keys[2].add(2)
  - if freq_to_keys[min_freq] is empty → min_freq = 2

On evict (capacity full, put new key):
  - Remove LRU from freq_to_keys[min_freq]
  - Delete from key_to_val and key_to_freq
  - Reset min_freq = 1 (new key always has freq=1)
```

---

## Complexity Analysis

| Operation | LRU Cache | LFU Cache |
|-----------|-----------|-----------|
| get       | O(1)      | O(1)      |
| put       | O(1)      | O(1)      |
| Space     | O(n)      | O(n)      |

---

## Design Decisions

1. **OrderedDict for LRU**: Python's `collections.OrderedDict` maintains insertion order and supports `move_to_end()` in O(1). This replaces the need to manually implement a doubly linked list.

2. **LFU with min_freq tracking**: Instead of a heap (O(log n)), we maintain a `min_freq` counter that we can update in O(1). When we add a new key, its frequency is always 1, so `min_freq = 1`.

3. **Two-level OrderedDict for LFU**: `freq_to_keys[f]` is itself an OrderedDict, giving us O(1) LRU eviction among keys at the same frequency.

4. **RLock for thread safety**: Using a reentrant lock allows the same thread to acquire the lock multiple times without deadlock (useful if internal methods call each other).

5. **Wrapper pattern for thread safety**: Thread-safe classes wrap (compose) the non-thread-safe versions, keeping concerns separated and the base classes clean.
