# Advanced topic — FilteredIterator: iterating a large collection with lazy filtering and pagination.
"""
Iterator Pattern — Example 2: Filtered and Paginated Iterator

A FilteredIterator wraps any iterable and yields only items that pass a
predicate — without loading the full collection into memory first.
A PagedIterator slices results into fixed-size pages, one page at a time.

Real-world use: Flipkart search filters (only show items under ₹500, in stock).
The database cursor streams rows; the filtered iterator selects matching ones.

Run:
    python3 examples/example2_filtered_paged_iterator.py
"""
from __future__ import annotations
from typing import Iterator, Callable, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# FilteredIterator
# ---------------------------------------------------------------------------

class FilteredIterator:
    """Wraps an iterable; yields only items where predicate(item) is True."""

    def __init__(self, source, predicate: Callable) -> None:
        self._source = iter(source)
        self._predicate = predicate

    def __iter__(self) -> FilteredIterator:
        return self

    def __next__(self):
        while True:
            item = next(self._source)  # raises StopIteration when exhausted
            if self._predicate(item):
                return item


# ---------------------------------------------------------------------------
# PagedIterator
# ---------------------------------------------------------------------------

class PagedIterator:
    """Yields items from source in fixed-size pages (lists)."""

    def __init__(self, source, page_size: int) -> None:
        self._source = iter(source)
        self._page_size = page_size

    def __iter__(self) -> PagedIterator:
        return self

    def __next__(self) -> list:
        page = []
        for _ in range(self._page_size):
            try:
                page.append(next(self._source))
            except StopIteration:
                break
        if not page:
            raise StopIteration
        return page


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    products = [
        {"name": "Phone",   "price": 12000, "in_stock": True},
        {"name": "Charger", "price": 499,   "in_stock": True},
        {"name": "Cable",   "price": 199,   "in_stock": False},
        {"name": "Case",    "price": 349,   "in_stock": True},
        {"name": "Earbuds", "price": 1500,  "in_stock": True},
    ]

    print("=== Products under ₹500 and in stock ===")
    cheap_in_stock = FilteredIterator(
        products,
        predicate=lambda p: p["price"] < 500 and p["in_stock"]
    )
    for p in cheap_in_stock:
        print(f"  {p['name']} — ₹{p['price']}")

    print("\n=== Paged (2 per page) ===")
    for page_num, page in enumerate(PagedIterator(products, page_size=2), start=1):
        names = [p["name"] for p in page]
        print(f"  Page {page_num}: {names}")
