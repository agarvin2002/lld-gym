"""
Iterator Pattern — Example 1: NumberRange

Shows two equivalent ways to walk a numeric range:
  1. Class-based iterator with __iter__ / __next__
  2. Generator function (Python's shortcut for the same protocol)

Real-world use: Paginated API responses use the same idea — a cursor object
fetches the next page only when asked, just like __next__ is called on demand.

Run:
    python3 examples/example1_number_range.py
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Approach 1: Class-based iterator
# ---------------------------------------------------------------------------

class NumberRangeIterator:
    """Stateful cursor returned by NumberRange.__iter__."""

    def __init__(self, start: int, stop: int, step: int) -> None:
        self._current = start
        self._stop = stop
        self._step = step

    def __iter__(self) -> NumberRangeIterator:
        return self  # iterator is also iterable

    def __next__(self) -> int:
        if (self._step > 0 and self._current >= self._stop) or \
           (self._step < 0 and self._current <= self._stop):
            raise StopIteration
        value = self._current
        self._current += self._step
        return value


class NumberRange:
    """
    Iterable range from start (inclusive) to stop (exclusive).

    NumberRange is the *iterable*; NumberRangeIterator is the *iterator*.
    Separating them means each for-loop gets a fresh cursor — you can loop
    over the same NumberRange twice without resetting anything manually.
    """

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("step must not be zero")
        self._start = start
        self._stop = stop
        self._step = step

    def __repr__(self) -> str:
        return f"NumberRange({self._start}, {self._stop}, step={self._step})"

    def __iter__(self) -> NumberRangeIterator:
        # Each call returns a FRESH iterator — safe to loop twice.
        return NumberRangeIterator(self._start, self._stop, self._step)


# ---------------------------------------------------------------------------
# Approach 2: Generator function (same result, less boilerplate)
# ---------------------------------------------------------------------------

def number_range_gen(start: int, stop: int, step: int = 1):
    """Generator equivalent — Python gives it __iter__ and __next__ for free."""
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
    nr = NumberRange(1, 10, 2)
    print("Class-based:", list(nr))          # [1, 3, 5, 7, 9]
    print("Loop again :", list(nr))          # [1, 3, 5, 7, 9]  — still works

    # Two independent cursors over the same collection
    it1, it2 = iter(nr), iter(nr)
    print(f"it1={next(it1)}, it2={next(it2)}, it1={next(it1)}")  # 1, 1, 3

    print("Generator  :", list(number_range_gen(1, 10, 2)))      # [1, 3, 5, 7, 9]
    print("Countdown  :", list(NumberRange(10, 0, -2)))           # [10, 8, 6, 4, 2]

    # Both approaches produce identical output
    assert list(NumberRange(0, 20, 3)) == list(number_range_gen(0, 20, 3))
    print("Class and generator match: True")


if __name__ == "__main__":
    main()
