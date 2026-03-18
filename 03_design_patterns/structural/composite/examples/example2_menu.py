# Advanced topic — building a nested restaurant menu as a composite tree
"""
Composite Pattern — Example 2: Restaurant Menu

A restaurant menu naturally forms a tree.

- MenuComponent  — shared ABC (Component)
- MenuItem       — Leaf: a single dish with a fixed price
- Menu           — Composite: a named category containing items or sub-menus

Calling price() on any node works uniformly — no need to know whether you
are asking a single dish or an entire category section.

Real-world use: Swiggy/Zomato menus with nested categories (Starters →
Veg Starters → specific items) where the app calculates sub-totals at any level.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class MenuComponent(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def price(self) -> float: ...

    @abstractmethod
    def display(self, indent: int = 0) -> str: ...


class MenuItem(MenuComponent):
    """Leaf — a single dish with its own price."""

    def __init__(self, name: str, price_val: float) -> None:
        self._name = name
        self._price_val = price_val

    @property
    def name(self) -> str:
        return self._name

    def price(self) -> float:
        return self._price_val

    def display(self, indent: int = 0) -> str:
        return "  " * indent + f"{self._name}  ₹{self._price_val:.0f}"


class Menu(MenuComponent):
    """Composite — a category that groups MenuComponents."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._components: list[MenuComponent] = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, component: MenuComponent) -> "Menu":
        """Add a child. Returns self for fluent chaining."""
        self._components.append(component)
        return self

    def price(self) -> float:
        """Subtotal — recursively sums all items below this node."""
        return sum(c.price() for c in self._components)

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}=== {self._name} === (subtotal: ₹{self.price():.0f})"]
        for component in self._components:
            lines.append(component.display(indent + 1))
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    breakfast = (
        Menu("Breakfast")
        .add(MenuItem("Masala Dosa",   80))
        .add(MenuItem("Idli Sambar",   60))
        .add(MenuItem("Aloo Paratha", 100))
    )

    lunch = (
        Menu("Lunch")
        .add(MenuItem("Dal Makhani",  180))
        .add(MenuItem("Paneer Tikka", 220))
        .add(MenuItem("Naan",          40))
    )

    full_menu = Menu("Today's Menu").add(breakfast).add(lunch)

    print(full_menu.display())

    print()
    # Uniform price() call — no isinstance() needed
    for node in [full_menu, breakfast, lunch, breakfast._components[0]]:
        print(f"  {node.name:20s}  ₹{node.price():.0f}")
