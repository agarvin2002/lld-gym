"""
Composite Pattern — Example 2: Restaurant Menu
===============================================

A restaurant menu naturally forms a tree:

- MenuComponent  — shared ABC (Component)
- MenuItem       — Leaf: a single dish with a fixed price
- Menu           — Composite: a named category containing other components
                   (items or sub-menus)

Because both leaf and composite implement price(), you can ask any node for
its total price without caring about the depth of nesting.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component (abstract base)
# ---------------------------------------------------------------------------

class MenuComponent(ABC):
    """Shared interface for both menu items and menu categories."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def price(self) -> float:
        """Return the price (leaf) or total price (composite)."""
        ...

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Return a human-readable representation of this node."""
        ...


# ---------------------------------------------------------------------------
# Leaf
# ---------------------------------------------------------------------------

class MenuItem(MenuComponent):
    """A single dish — leaf node with its own price."""

    def __init__(self, name: str, description: str, price_val: float) -> None:
        self._name = name
        self._description = description
        self._price_val = price_val

    @property
    def name(self) -> str:
        return self._name

    def price(self) -> float:
        return self._price_val

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return (
            f"{prefix}{self._name}  ${self._price_val:.2f}\n"
            f"{prefix}  {self._description}"
        )


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------

class Menu(MenuComponent):
    """A named menu category that groups MenuComponents."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._components: list[MenuComponent] = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, component: MenuComponent) -> "Menu":
        """Add a child component (fluent — returns self for chaining)."""
        self._components.append(component)
        return self

    def price(self) -> float:
        """Total price of all items in this category (recursively)."""
        return sum(c.price() for c in self._components)

    def display(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}=== {self._name} === (subtotal: ${self.price():.2f})"]
        for component in self._components:
            lines.append(component.display(indent + 1))
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def build_full_menu() -> Menu:
    """
    All Day Menu
    ├── Breakfast
    │   ├── Pancakes          $8.99
    │   ├── Omelette          $10.50
    │   └── Avocado Toast     $12.00
    └── Lunch
        ├── Caesar Salad      $11.00
        ├── Grilled Salmon    $18.50
        └── Veggie Burger     $13.75
    """
    # Breakfast items
    pancakes       = MenuItem("Pancakes",       "Fluffy buttermilk pancakes with maple syrup",    8.99)
    omelette       = MenuItem("Omelette",       "Three-egg omelette with cheese and vegetables", 10.50)
    avocado_toast  = MenuItem("Avocado Toast",  "Sourdough with smashed avocado and poached egg",12.00)

    breakfast = Menu("Breakfast").add(pancakes).add(omelette).add(avocado_toast)

    # Lunch items
    caesar  = MenuItem("Caesar Salad",   "Romaine, parmesan, croutons, caesar dressing",  11.00)
    salmon  = MenuItem("Grilled Salmon", "Atlantic salmon with seasonal vegetables",        18.50)
    veggie  = MenuItem("Veggie Burger",  "Black-bean patty with house-made aioli",          13.75)

    lunch = Menu("Lunch").add(caesar).add(salmon).add(veggie)

    all_day = Menu("All Day Menu").add(breakfast).add(lunch)
    return all_day


if __name__ == "__main__":
    menu = build_full_menu()

    print("=== Restaurant Menu ===")
    print(menu.display())

    print()

    # Uniform price() call on different node types
    breakfast_menu = menu._components[0]
    caesar_salad   = menu._components[1]._components[0]

    nodes: list[MenuComponent] = [menu, breakfast_menu, caesar_salad]
    print("=== Prices (uniform interface) ===")
    for node in nodes:
        print(f"  {node.name:20s}  ${node.price():.2f}")

    print()

    # Verify arithmetic
    expected_total = 8.99 + 10.50 + 12.00 + 11.00 + 18.50 + 13.75
    assert abs(menu.price() - expected_total) < 0.001, (
        f"Expected {expected_total:.2f}, got {menu.price():.2f}"
    )
    print(f"Total menu price: ${menu.price():.2f}  (verified correct)")
