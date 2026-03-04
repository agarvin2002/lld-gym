"""
Builder Pattern — Example 1: Pizza Builder

Demonstrates:
- A product class (Pizza) with multiple optional fields
- A PizzaBuilder with fluent setters (each returns self)
- Method chaining to construct two different pizzas
- A PizzaDirector with named convenience methods (margherita, pepperoni)
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

@dataclass
class Pizza:
    """The finished product. Constructed only by PizzaBuilder.build()."""
    size: str
    crust: str
    sauce: str
    toppings: list[str]
    extra_cheese: bool

    def __str__(self) -> str:
        toppings_str = ", ".join(self.toppings) if self.toppings else "none"
        cheese_str = " + extra cheese" if self.extra_cheese else ""
        return (
            f"Pizza [{self.size}] | crust: {self.crust} | sauce: {self.sauce} "
            f"| toppings: {toppings_str}{cheese_str}"
        )


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class PizzaBuilder:
    """
    Fluent builder for Pizza objects.

    Usage:
        pizza = (PizzaBuilder()
                 .size("large")
                 .crust("thin")
                 .sauce("tomato")
                 .add_topping("mushrooms")
                 .extra_cheese()
                 .build())
    """

    def __init__(self) -> None:
        self._size: str = "medium"
        self._crust: str = "regular"
        self._sauce: str = "tomato"
        self._toppings: list[str] = []
        self._extra_cheese: bool = False

    # --- fluent setters ---

    def size(self, s: str) -> PizzaBuilder:
        self._size = s
        return self

    def crust(self, c: str) -> PizzaBuilder:
        self._crust = c
        return self

    def sauce(self, s: str) -> PizzaBuilder:
        self._sauce = s
        return self

    def add_topping(self, t: str) -> PizzaBuilder:
        self._toppings.append(t)
        return self

    def extra_cheese(self) -> PizzaBuilder:
        self._extra_cheese = True
        return self

    # --- terminal step ---

    def build(self) -> Pizza:
        """Construct and return the immutable Pizza product."""
        return Pizza(
            size=self._size,
            crust=self._crust,
            sauce=self._sauce,
            toppings=list(self._toppings),   # snapshot — caller cannot mutate builder's list
            extra_cheese=self._extra_cheese,
        )


# ---------------------------------------------------------------------------
# Director
# ---------------------------------------------------------------------------

class PizzaDirector:
    """
    Encodes well-known pizza configurations.

    The Director owns a builder and calls the right setters in the right order
    so clients don't need to remember each preset's ingredients.
    """

    def __init__(self, builder: PizzaBuilder) -> None:
        self._builder = builder

    def _reset(self) -> None:
        """Re-initialise the builder so presets don't bleed into each other."""
        self._builder = PizzaBuilder()

    def margherita(self) -> Pizza:
        self._reset()
        return (self._builder
                .size("medium")
                .crust("thin")
                .sauce("tomato")
                .add_topping("mozzarella")
                .add_topping("basil")
                .build())

    def pepperoni(self) -> Pizza:
        self._reset()
        return (self._builder
                .size("large")
                .crust("regular")
                .sauce("tomato")
                .add_topping("pepperoni")
                .add_topping("mozzarella")
                .extra_cheese()
                .build())


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Custom pizzas via method chaining ---
    custom_veggie = (PizzaBuilder()
                     .size("small")
                     .crust("whole-wheat")
                     .sauce("pesto")
                     .add_topping("bell peppers")
                     .add_topping("olives")
                     .add_topping("sun-dried tomatoes")
                     .build())

    custom_meat = (PizzaBuilder()
                   .size("large")
                   .crust("stuffed")
                   .sauce("bbq")
                   .add_topping("chicken")
                   .add_topping("bacon")
                   .extra_cheese()
                   .build())

    print("=== Custom Pizzas ===")
    print(custom_veggie)
    print(custom_meat)

    # --- Preset pizzas via Director ---
    director = PizzaDirector(PizzaBuilder())
    margherita = director.margherita()
    pepperoni  = director.pepperoni()

    print("\n=== Director Presets ===")
    print(f"Margherita : {margherita}")
    print(f"Pepperoni  : {pepperoni}")
