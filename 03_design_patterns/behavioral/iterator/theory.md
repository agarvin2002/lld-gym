# Iterator Pattern

## What is it?
An iterator gives you a way to walk through a collection one item at a time. The caller never needs to know whether the data lives in a list, a file, a database, or a network stream. It just calls `next()` until there's nothing left.

## Analogy
A Spotify playlist queue. You press "next track" and the next song plays. You don't know if the songs are stored in an array, streamed from a server, or generated on the fly. The "next" button is a uniform interface over whatever is underneath.

## Minimal code
```python
class NumberRange:
    """Iterable: creates a fresh iterator on each for-loop."""
    def __init__(self, start: int, stop: int) -> None:
        self._start, self._stop = start, stop

    def __iter__(self):
        return NumberRangeIterator(self._start, self._stop)

class NumberRangeIterator:
    """Iterator: holds traversal state."""
    def __init__(self, current: int, stop: int) -> None:
        self._current, self._stop = current, stop

    def __iter__(self): return self

    def __next__(self) -> int:
        if self._current >= self._stop:
            raise StopIteration
        value = self._current
        self._current += 1
        return value

for n in NumberRange(1, 4):
    print(n)   # 1  2  3
```

## Real-world uses
- Paginated Flipkart search results — each page is fetched only when the user scrolls (lazy)
- Reading a large CSV log file line by line without loading it all into memory
- A database cursor iterating over query results row by row

> The minimal code above uses a fixed list. The real power is lazy evaluation:
> iterators can pull from a database, a network stream, or a generator without
> loading everything into memory. See example2 for a filtered, paginated iterator.

## One mistake
Making the iterable and the iterator the same object (returning `self` from `__iter__`). Once exhausted, a second `for` loop over the same object yields nothing. Separate the two: the collection creates a fresh iterator each time `__iter__` is called.

## What to do next
See `examples/example1_number_range.py` for a full class-based iterator vs. generator comparison.
See `examples/example2_filtered_paged_iterator.py` for a filtered/paginated iterator used in system design.
Then try `exercises/starter.py` — build a Playlist with forward, reverse, and shuffled iteration.
