# Solution Explanation: LRU Cache + LFU Cache

## LRU Cache

### Core Insight: OrderedDict

Python's `collections.OrderedDict` is a dictionary that remembers insertion order. It exposes two key operations used here:

- `move_to_end(key)` — O(1), moves an existing key to the end (most-recent position)
- `popitem(last=False)` — O(1), removes and returns the first (least-recent) item

By treating the **front** as LRU and the **back** as MRU, both `get` and `put` reduce to O(1) dictionary + linked-list operations (OrderedDict is implemented in C as a doubly linked list backed by a hash table).

### Manual Alternative (without OrderedDict)

If implementing from scratch you would maintain:
1. A **doubly linked list** where the head is LRU and the tail is MRU
2. A **hash map** mapping keys to list nodes

Every get/put touches the hash map (O(1)) and re-links list pointers (O(1)), giving overall O(1).

```
HashMap: {1 -> Node1, 2 -> Node2}
List:    HEAD <-> [Node1: k=1,v=10] <-> [Node2: k=2,v=20] <-> TAIL
                   (LRU)                                   (MRU)
```

---

## LFU Cache

### O(1) Approach — Three Hash Maps + min_freq

Naive LFU uses a min-heap, giving O(log n) per operation. The O(1) approach uses:

| Structure | Type | Purpose |
|---|---|---|
| `key_to_val` | `dict[int, int]` | key → value |
| `key_to_freq` | `dict[int, int]` | key → current access count |
| `freq_to_keys` | `dict[int, OrderedDict]` | frequency → ordered set of keys (by recency) |
| `min_freq` | `int` | current minimum frequency |

**Why `min_freq` is maintainable in O(1):**
- When we add a new key, its frequency is always 1 → `min_freq = 1`
- When we increment a key's frequency from `f` to `f+1` and the bucket at `f` becomes empty, `min_freq` can only increase to `f+1` (the smallest bucket that could exist after the increment)
- So `min_freq` never needs to be recomputed from scratch

**Why `OrderedDict` inside `freq_to_keys`:**
- Keys at the same frequency are ordered by recency (insertion/access order)
- `popitem(last=False)` removes the LRU key among equal-frequency keys in O(1)

### Walkthrough

```
capacity=2, initial state: empty

put(1, 1):
  key_to_val = {1: 1}
  key_to_freq = {1: 1}
  freq_to_keys = {1: OrderedDict([(1, None)])}
  min_freq = 1

put(2, 2):
  key_to_val = {1: 1, 2: 2}
  key_to_freq = {1: 1, 2: 1}
  freq_to_keys = {1: OrderedDict([(1, None), (2, None)])}
  min_freq = 1

get(1):  → returns 1, _increment_freq(1)
  freq[1]: 1 → 2
  freq_to_keys[1] = OrderedDict([(2, None)])  (1 removed)
  freq_to_keys[2] = OrderedDict([(1, None)])
  min_freq = 1  (freq_to_keys[1] still has key 2)

put(3, 3):  capacity full → evict
  evict: min_freq=1, LRU at freq=1 is key 2 → evict key 2
  Insert 3: freq[3]=1, min_freq=1
  freq_to_keys[1] = OrderedDict([(3, None)])
```

---

## Thread Safety

Using `threading.RLock` (reentrant lock):
- `with self._lock:` ensures only one thread executes the critical section
- Reentrant so the same thread can acquire it multiple times without deadlock
- Wrapper pattern keeps the base classes simple and single-responsibility

---

## Complexity Summary

| Cache | get | put | Space |
|-------|-----|-----|-------|
| LRU (OrderedDict) | O(1) amortized | O(1) amortized | O(n) |
| LFU (three maps) | O(1) | O(1) | O(n) |
| Thread-safe variants | same + lock overhead | same + lock overhead | O(n) |

---

## Design Patterns Used

- **Composition** (ThreadSafe* wraps base cache): separates concurrency from logic
- **Strategy** (could inject eviction policy): LRU vs LFU as interchangeable strategies
