# Strategy Pattern

## What is it?
Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from the clients that use it.

## Real-world analogy
A GPS navigation app that can route by fastest time, shortest distance, or avoiding tolls. You switch strategies at runtime — the map UI doesn't change, only the routing algorithm does.

## Why does it matter?
Without Strategy, algorithm selection lives in the calling code as a chain of `if/elif` blocks. Adding a new algorithm means editing existing code (OCP violation). With Strategy, you add a class and inject it.

## Python-specific notes
- Define the strategy interface as an `ABC` with an `@abstractmethod`
- Inject the strategy via `__init__` (constructor injection) — most testable
- Can also use simple callables (functions) as lightweight strategies when the interface is a single method

## When to use
- You have multiple variants of an algorithm and want to swap them at runtime
- You want to eliminate conditionals that select behaviour
- You want to test algorithms independently from the code that uses them

## When to avoid
- Only one algorithm exists and no variation is expected
- The variation is trivial (one line) — a callable/lambda is simpler than a full ABC

## Quick example
```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        data = list(data)
        for i in range(len(data)):
            for j in range(len(data) - i - 1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        mid  = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)

class Sorter:
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)

# Usage
sorter = Sorter(QuickSort())
print(sorter.sort([5, 3, 1, 4, 2]))  # [1, 2, 3, 4, 5]

sorter.set_strategy(BubbleSort())
print(sorter.sort([5, 3, 1, 4, 2]))  # [1, 2, 3, 4, 5]
```

## Common mistakes
- Putting the strategy selection logic back inside the context class (defeats the purpose)
- Making strategies stateful — keep them stateless and reusable
- Over-engineering: if you have two algorithms and they'll never change, just use a function

## Links
- Exercise: `exercises/starter.py` — implement a payment processing system with multiple fee strategies
