# Solution Explanation: Playlist Iterator

## What We Built

A `Playlist` class that acts as a reusable *iterable* over `Song` objects,
supporting three traversal modes: forward, reverse, and shuffled.

---

## Python's Iterator Protocol

Python defines two roles:

| Role | Required methods | Behaviour |
|------|-----------------|-----------|
| **Iterable** | `__iter__` | Returns a (possibly new) iterator. Can be looped over multiple times. |
| **Iterator** | `__iter__` + `__next__` | Maintains a cursor. Single-pass; exhausted after one loop. |

The key insight: `Playlist.__iter__` returns `iter(self._songs)`, which is a
**new** `list_iterator` object each time.  This means:

```python
pl = Playlist()
# ... add songs ...
list(pl)   # works
list(pl)   # works again — Playlist is an iterable, not an iterator
```

If `Playlist` had implemented `__next__` directly and returned `self` from
`__iter__`, the second `list(pl)` would return an empty list because the
internal cursor would already be at the end.

---

## Why `iter()` and `reversed()` Are Idiomatic Here

Python's `list` already implements the full iterator protocol and supports
`__reversed__`.  Wrapping it manually would add complexity without benefit:

```python
# Idiomatic — delegates to list's built-in machinery
def __iter__(self):
    return iter(self._songs)

def reversed(self):
    return reversed(self._songs)
```

Compare with a verbose manual version:
```python
# Verbose — same result, more code
def __iter__(self):
    return PlaylistForwardIterator(self._songs)

class PlaylistForwardIterator:
    def __init__(self, songs):
        self._songs = songs
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index >= len(self._songs):
            raise StopIteration
        val = self._songs[self._index]
        self._index += 1
        return val
```

A custom class would only be warranted if you needed extra behaviour:
pagination, peek-ahead (`peek()` method), pause/resume, or filtering on the fly.

---

## The `shuffled()` Implementation

```python
def shuffled(self):
    songs_copy = list(self._songs)   # snapshot — does not touch self._songs
    random.shuffle(songs_copy)       # shuffle in-place on the copy
    return iter(songs_copy)          # single-pass iterator over the shuffled copy
```

Three decisions explained:

1. **Copy first** — `random.shuffle` mutates in-place.  Without a copy it would
   destroy insertion order every time `shuffled()` was called.

2. **Return `iter(copy)` not `copy`** — returning the list itself would work for
   iteration, but it would also let callers index into it (`result[0]`), which
   is not part of the iterator contract we want to expose.

3. **Each call produces a new shuffle** — because we create a fresh copy and
   shuffle it on every call, two successive `playlist.shuffled()` calls are
   independent and usually differ.

### Generator alternative

```python
def shuffled(self):
    songs_copy = list(self._songs)
    random.shuffle(songs_copy)
    yield from songs_copy        # turns the method into a generator
```

Both produce identical observable behaviour.  The `iter()` version is slightly
more explicit; `yield from` is more Pythonic once you are comfortable with
generators.

---

## Iterable vs. Iterator — When Does the Distinction Matter?

| Scenario | Use an Iterable (class with `__iter__`) | Use an Iterator (class with `__iter__` + `__next__`) |
|----------|-----------------------------------------|------------------------------------------------------|
| Collection you want to loop over multiple times | Yes | No |
| Single-pass data source (file, network stream) | No | Yes |
| Need to pause and resume traversal | No | Yes (save cursor in instance variable) |
| Need `peek()` or `push_back()` | No | Yes (custom state machine) |
| Performance-critical lazy evaluation | Generator (simplest) | Custom iterator (most control) |

`Playlist` fits squarely in the first row: it is a re-usable in-memory
collection.  `Playlist` itself should be an *iterable* (not an iterator), so
multiple for loops work independently.

---

## Common Mistakes to Avoid

1. **`__iter__` returns `self` on a collection class**
   — makes the playlist single-use; the second `for` loop yields nothing.

2. **Shuffling `self._songs` directly**
   — permanently destroys insertion order after the first call to `shuffled()`.

3. **Storing cursor state in the collection**
   — prevents multiple simultaneous iterations (`zip(pl, pl)` would break).

4. **Forgetting `StopIteration` in a manual `__next__`**
   — causes an infinite loop instead of normal loop termination.

5. **Returning a generator object from `__iter__` in a collection class**
   — a generator is single-pass; the collection becomes single-use.
   Solution: call `iter(self._songs)` (returns a fresh iterator from the list)
   rather than `yield from self._songs` (turns `__iter__` into a generator).
