"""
Iterator Pattern — Example 1: NumberRange

Demonstrates three equivalent ways to iterate over a numeric range:
  1. Class-based iterator with __iter__ / __next__
  2. Generator function
  3. Verification that both produce identical output

Run:
    python3 examples/example1_number_range.py
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Approach 1: Class-based iterator
# ---------------------------------------------------------------------------

class NumberRangeIterator:
    """Stateful iterator returned by NumberRange.__iter__."""

    def __init__(self, start: int, stop: int, step: int) -> None:
        self._current = start
        self._stop = stop
        self._step = step

    def __iter__(self) -> NumberRangeIterator:
        # An iterator must also be iterable (return itself).
        return self

    def __next__(self) -> int:
        if (self._step > 0 and self._current >= self._stop) or \
           (self._step < 0 and self._current <= self._stop):
            raise StopIteration
        value = self._current
        self._current += self._step
        return value


class NumberRange:
    """
    An iterable range of numbers from `start` (inclusive) to `stop`
    (exclusive) with a configurable `step`.

    Unlike Python's built-in range(), this class wraps arbitrary numeric
    types and demonstrates the iterable/iterator split: the collection
    (NumberRange) and the cursor (NumberRangeIterator) are separate objects,
    so multiple independent iterations can run simultaneously.
    """

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("step must not be zero")
        self._start = start
        self._stop = stop
        self._step = step

    def __repr__(self) -> str:
        return f"NumberRange(start={self._start}, stop={self._stop}, step={self._step})"

    def __iter__(self) -> NumberRangeIterator:
        # Each call creates a FRESH iterator — so you can loop twice.
        return NumberRangeIterator(self._start, self._stop, self._step)


# ---------------------------------------------------------------------------
# Approach 2: Generator function
# ---------------------------------------------------------------------------

def number_range_gen(start: int, stop: int, step: int = 1):
    """
    Equivalent generator function.  Python automatically gives generators
    both __iter__ and __next__, making them iterators.
    """
    if step == 0:
        raise ValueError("step must not be zero")
    current = start
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current += step


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== NumberRange (class-based iterator) ===")
    nr = NumberRange(1, 10, 2)
    print(f"Object: {nr!r}")

    # for loop
    print("for loop:", end=" ")
    for n in nr:
        print(n, end=" ")
    print()

    # list() — proves iterable is re-usable (creates a new iterator each time)
    print("list()  :", list(nr))

    # Two simultaneous iterations share NO state
    it1 = iter(nr)
    it2 = iter(nr)
    print(f"next(it1)={next(it1)}, next(it2)={next(it2)}, next(it1)={next(it1)}")

    print()
    print("=== number_range_gen (generator function) ===")
    gen_values = list(number_range_gen(1, 10, 2))
    print("list()  :", gen_values)

    print()
    print("=== Counting down (negative step) ===")
    countdown = NumberRange(10, 0, -2)
    print(f"Object: {countdown!r}")
    print("list()  :", list(countdown))

    print()
    print("=== Identical output? ===")
    class_output = list(NumberRange(0, 20, 3))
    gen_output = list(number_range_gen(0, 20, 3))
    print(f"Class  : {class_output}")
    print(f"Generator: {gen_output}")
    print(f"Match  : {class_output == gen_output}")


if __name__ == "__main__":
    main()
