"""
Strategy Pattern — Example 1: Sorting Algorithms
==================================================
Different sort strategies are injected into a Sorter.
Switching algorithm requires zero changes to Sorter.
"""
from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...


class BubbleSort(SortStrategy):
    """O(n²) — educational, not for production."""
    def sort(self, data: list) -> list:
        data = list(data)
        n = len(data)
        for i in range(n):
            for j in range(n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data


class QuickSort(SortStrategy):
    """O(n log n) average — fast in practice."""
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return list(data)
        pivot = data[len(data) // 2]
        left  = [x for x in data if x < pivot]
        mid   = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)


class PythonBuiltinSort(SortStrategy):
    """Timsort — what Python uses under the hood."""
    def sort(self, data: list) -> list:
        return sorted(data)


class Sorter:
    """Context — uses a SortStrategy, never knows which one."""
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Swap algorithm at runtime."""
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)


if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    sorter = Sorter(BubbleSort())
    print(f"BubbleSort:  {sorter.sort(data)}")

    sorter.set_strategy(QuickSort())
    print(f"QuickSort:   {sorter.sort(data)}")

    sorter.set_strategy(PythonBuiltinSort())
    print(f"BuiltinSort: {sorter.sort(data)}")
