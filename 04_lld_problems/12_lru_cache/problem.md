# Problem 12: LRU Cache (+ LFU Cache)

## Problem Statement

Design and implement a **Least Recently Used (LRU) Cache** that supports O(1) get and put operations. Additionally, implement a **Least Frequently Used (LFU) Cache** with eviction based on access frequency. Both must have thread-safe variants.

---

## Requirements

### LRUCache

- `LRUCache(capacity: int)` — initialize with a fixed capacity
- `get(key: int) -> int` — return the value if key exists (and mark as recently used), else return -1
- `put(key: int, value: int) -> None` — insert or update the key. If at capacity, evict the **Least Recently Used** item first.

### LFUCache

- `LFUCache(capacity: int)` — initialize with a fixed capacity
- `get(key: int) -> int` — return the value if key exists (and increment frequency), else return -1
- `put(key: int, value: int) -> None` — insert or update the key. If at capacity, evict the **Least Frequently Used** item. On frequency tie, evict the **Least Recently Used** among them.

### Thread-Safe Variants

- `ThreadSafeLRUCache(capacity: int)` — thread-safe LRU
- `ThreadSafeLFUCache(capacity: int)` — thread-safe LFU

---

## Constraints

- `1 <= capacity <= 10^6`
- `0 <= key <= 10^5`
- `0 <= value <= 10^9`
- Both `get` and `put` must run in **O(1)** average time for LRU
- LFU `get` and `put` must run in **O(log n)** or better

---

## Examples

### LRU Cache

```
cache = LRUCache(2)
cache.put(1, 1)    # cache: {1:1}
cache.put(2, 2)    # cache: {1:1, 2:2}
cache.get(1)       # returns 1, cache order: {2, 1} (1 most recent)
cache.put(3, 3)    # evicts key 2, cache: {1:1, 3:3}
cache.get(2)       # returns -1 (evicted)
cache.get(3)       # returns 3
cache.put(4, 4)    # evicts key 1, cache: {3:3, 4:4}
cache.get(1)       # returns -1 (evicted)
cache.get(3)       # returns 3
cache.get(4)       # returns 4
```

### LFU Cache

```
cache = LFUCache(2)
cache.put(1, 1)    # freq: {1:1}
cache.put(2, 2)    # freq: {1:1, 2:1}
cache.get(1)       # returns 1, freq: {1:2, 2:1}
cache.put(3, 3)    # evicts key 2 (lower freq), freq: {1:2, 3:1}
cache.get(2)       # returns -1 (evicted)
cache.get(3)       # returns 3, freq: {1:2, 3:2}
cache.put(4, 4)    # both have freq 2, evict LRU (key 1 was accessed before 3), freq: {3:2, 4:1}
cache.get(1)       # returns -1 (evicted)
cache.get(3)       # returns 3
cache.get(4)       # returns 4
```

---

## Follow-up Questions

1. How would you implement a distributed LRU cache?
2. What if keys had TTL (time-to-live) expiry?
3. How would you persist the cache to disk efficiently?
4. Can you implement LRU with only O(1) extra space (no extra data structures)?

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **Strategy** | `LRUCache` and `LFUCache` are interchangeable eviction strategies with the same interface |
| **Proxy** | `ThreadSafeLRUCache` / `ThreadSafeLFUCache` wrap base caches adding `threading.Lock` |
| **Decorator** | Thread-safe wrappers add behaviour (locking) without changing the cache interface |
| **SRP** | `DoublyLinkedList` / `Node` handle ordering; cache classes handle eviction policy |

**See also:** Module 03 → [Strategy](../../03_design_patterns/behavioral/strategy/), [Proxy](../../03_design_patterns/structural/proxy/), [Decorator](../../03_design_patterns/structural/decorator/)
