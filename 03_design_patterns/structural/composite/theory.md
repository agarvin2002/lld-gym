# Composite Pattern

## What is it?
The Composite pattern lets you treat a single object and a group of objects the same way.
You define one shared interface. Both the individual item and the container implement it.
The container just delegates to its children — no special-casing needed by the caller.

## Analogy
Think of a Zomato order. A single dish has a price. A combo meal also has a price — it adds up the prices of its dishes.
You call `.price()` on either one. You do not need to know whether it is a single item or a combo.

## Minimal code
```python
from abc import ABC, abstractmethod

class OrderItem(ABC):
    @abstractmethod
    def price(self) -> float: ...

class Dish(OrderItem):
    def __init__(self, name: str, cost: float) -> None:
        self._cost = cost

    def price(self) -> float:
        return self._cost          # leaf: return own value

class Combo(OrderItem):
    def __init__(self) -> None:
        self._items: list[OrderItem] = []

    def add(self, item: OrderItem) -> None:
        self._items.append(item)

    def price(self) -> float:
        return sum(i.price() for i in self._items)  # composite: delegate to children
        # Each child may itself be a Combo — the recursion goes as deep as needed.

biryani = Dish("Biryani", 180)
raita   = Dish("Raita",    40)
meal    = Combo()
meal.add(biryani)
meal.add(raita)
print(meal.price())   # 220 — no isinstance() anywhere
```

## Real-world uses
- File system: a `File` returns its own size; a `Directory` sums the sizes of everything inside it
- Org chart: an `Employee` returns their own salary; a `Department` sums salaries of all members
- Flipkart cart: individual products and bundled packs both expose a `total_price()` method

## One mistake
Putting `add_child()` on the base interface (ABC) instead of only on the composite class.
Leaf nodes cannot have children, so calling `add_child()` on a leaf should be impossible or raise immediately.
Keep `add_child()` on the composite only — callers that have a composite reference already know what they have.

## What to do next
- Read `examples/example1_filesystem.py` to see a full file-system tree.
- Read `examples/example2_menu.py` to see a restaurant menu built as a composite tree.
- Then open `exercises/starter.py` and build your own org chart.
