# Iterator Pattern

## What Is It?

The **Iterator** pattern provides a way to sequentially access elements of a collection without exposing its underlying representation. You separate the traversal logic from the collection itself, so callers can loop over items using a uniform interface — regardless of whether the data lives in a list, tree, database cursor, or network stream.

**GoF definition**: "Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation."

---

## Real-World Analogy

Think of a **TV remote's channel buttons**. You press "next channel" repeatedly without knowing how the cable box stores its channel list — it could be a sorted array, a linked list, or a favourites ring. The remote gives you a single, consistent interface (`next()`, `prev()`) to traverse whatever structure is underneath.

Similarly, Python's `for` loop doesn't care whether it's walking a `list`, a `dict`, a `set`, a file, or a custom class — as long as the object speaks the iterator protocol.

---

## Why It Matters

| Problem without Iterator | Solution with Iterator |
|--------------------------|------------------------|
| Caller must know internal layout (array index, tree pointer) | Caller only calls `next()` |
| Adding a new collection type breaks all traversal code | Implement the protocol once; callers are untouched |
| Can't have multiple independent traversals simultaneously | Each iterator instance holds its own state |
| Lazy evaluation is hard | Iterators/generators can produce values on demand |

---

## Python Specifics

Python has first-class support for the iterator protocol via two dunder methods:

```python
class CountUp:
    def __init__(self, stop):
        self._stop = stop
        self._current = 0           # mutable state lives here

    def __iter__(self):
        return self                 # the iterator IS the iterable

    def __next__(self):
        if self._current >= self._stop:
            raise StopIteration     # signal exhaustion
        value = self._current
        self._current += 1
        return value

for n in CountUp(5):
    print(n)   # 0 1 2 3 4
```

### Key rules

1. **`__iter__`** must return an object that has `__next__`.
2. **`__next__`** returns the next value or raises `StopIteration`.
3. When the same object is both iterable and iterator (implements both methods with `__iter__` returning `self`), each `for` loop shares state — **you cannot restart it**.
4. To support multiple independent traversals, return a **new** iterator object from `__iter__` (see the collection vs. iterator split below).

### Generator shortcut

A **generator function** (uses `yield`) automatically implements the full iterator protocol:

```python
def count_up(stop):
    current = 0
    while current < stop:
        yield current
        current += 1

list(count_up(5))  # [0, 1, 2, 3, 4]
```

Generators are lazy — they compute the next value only when asked. This makes them ideal for large or infinite sequences.

### Iterable vs. Iterator

| Term | Has `__iter__`? | Has `__next__`? | Re-usable? |
|------|----------------|-----------------|------------|
| **Iterable** | Yes | No | Yes — `__iter__` creates a fresh iterator |
| **Iterator** | Yes (returns `self`) | Yes | No — exhausted after one pass |

`list` is an *iterable*; `list.__iter__()` returns a `list_iterator` which is the *iterator*.

---

## When to Use the Iterator Pattern

**Use it when:**
- You want to hide the internal structure of a collection (linked list, tree, graph, DB cursor).
- You need multiple simultaneous traversal cursors over the same collection.
- You want lazy evaluation (compute values on demand, not all at once).
- You're building a custom data structure and want it to work with Python's `for`, `list()`, `sum()`, etc.

**Avoid it when:**
- Simple indexed access (`collection[i]`) is clearer and the internal layout is already public by design.
- The traversal is trivial (e.g., a flat list) and Python's built-in `iter()` already handles it.

---

## Common Mistakes

1. **Forgetting to reset state**: If `__iter__` returns `self` and `__next__` doesn't reset `_current`, the second `for` loop over the same object yields nothing.

   ```python
   # Bug: shares state
   it = CountUp(3)
   list(it)  # [0, 1, 2]
   list(it)  # [] -- already exhausted!

   # Fix: separate iterable from iterator, or reset in __iter__
   def __iter__(self):
       self._current = 0   # reset on each new iteration
       return self
   ```

2. **Not raising `StopIteration`**: Forgetting the guard causes an infinite loop.

3. **Returning `None` from `__iter__`**: Must return an object with `__next__`.

4. **Mutating the collection during iteration**: Can cause skipped or repeated elements. Either copy first or use a snapshot-based iterator.

5. **Using a generator where re-iteration is needed**: Generators are single-pass; once exhausted they yield nothing. Wrap in a class that creates a fresh generator each time `__iter__` is called.
