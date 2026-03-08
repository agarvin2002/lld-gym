"""
WHAT YOU'RE BUILDING
--------------------
You are building a simple online shop system with two classes:

  Product     — one item you can sell (name, price, quantity, SKU)
  ShoppingCart — a bag that holds products

This is the same kind of design used in real apps like Flipkart, Amazon, or Meesho.

HOW TO RUN TESTS
    pytest tests.py -v

RULES
  - Do not change method names or class names (tests will break)
  - Type hints are already given — keep them
  - Fill every TODO comment
"""


class Product:
    """
    One product in the shop.

    name     — what the product is called (e.g. "Laptop")
    price    — how much it costs (must be > 0)
    quantity — how many are in stock (must be >= 0)
    sku      — a unique ID code for this product (e.g. "SKU-001")
    """

    def __init__(self, name: str, price: float, quantity: int, sku: str) -> None:
        # TODO: Check that name is not empty. Raise ValueError if it is.
        # HINT: if not name: raise ValueError("name cannot be empty")

        # TODO: Check that price is greater than 0. Raise ValueError if not.

        # TODO: Check that quantity is 0 or more. Raise ValueError if negative.

        # TODO: Check that sku is not empty. Raise ValueError if it is.

        # TODO: Save all four values as self.name, self.price, self.quantity, self.sku
        pass

    def __repr__(self) -> str:
        # TODO: Return a string like this (exactly):
        # Product(name='Laptop Pro', price=999.99, quantity=10, sku='SKU-LAPTOP-001')
        # HINT: use f"Product(name='{self.name}', price={self.price}, ...)"
        pass

    def __str__(self) -> str:
        # TODO: Return a friendly string like this:
        # Laptop Pro (SKU: SKU-LAPTOP-001) — $999.99 | 10 in stock
        pass

    def __eq__(self, other: object) -> bool:
        # TODO: Two products are equal if they have the same SKU (not the same name or price).
        # HINT: first check "if not isinstance(other, Product): return NotImplemented"
        # Then compare self.sku == other.sku
        pass

    def __hash__(self) -> int:
        # TODO: Return hash(self.sku)
        # This lets Product be used as a key in a dict or in a set.
        # TIP: You need __hash__ whenever you define __eq__.
        pass

    def is_in_stock(self) -> bool:
        # TODO: Return True if quantity > 0, False if quantity is 0
        # HINT: one line — return self.quantity > 0
        pass

    def apply_discount(self, percent: float) -> None:
        # TODO: Reduce the price by the given percent.
        # percent must be between 0 and 100 (not including 0, including 100).
        # Raise ValueError if it is out of range.
        # HINT: new_price = self.price * (1 - percent / 100)
        pass


class ShoppingCart:
    """
    A shopping cart. It holds products and how many of each the customer wants.

    Internally it uses a dict:  { product: quantity_in_cart }

    TIP: This same pattern (object → count dict) appears in many LLD problems
    like hotel booking (room type → count) or cinema (seat → booking).
    """

    def __init__(self) -> None:
        # TODO: Create an empty dict and save it as self._items
        # HINT: self._items = {}
        pass

    def add_item(self, product: "Product", quantity: int = 1) -> None:
        # TODO: Add the product to the cart with the given quantity.
        # If the product is already in the cart, add to its existing quantity.
        # quantity must be >= 1. Raise ValueError if not.
        # HINT: use self._items.get(product, 0) to get the current quantity
        pass

    def remove_item(self, product: "Product") -> None:
        # TODO: Remove the product from the cart completely.
        # Raise ValueError if the product is not in the cart.
        # HINT: check "if product not in self._items" first
        pass

    def get_total(self) -> float:
        # TODO: Return the total cost = sum of (price × quantity) for every item
        # HINT: use a loop or sum() over self._items.items()
        pass

    def get_item_count(self) -> int:
        # TODO: Return the total number of individual units in the cart.
        # Example: 1 laptop + 2 pens = 3 total units
        # HINT: sum(self._items.values())
        pass

    def is_empty(self) -> bool:
        # TODO: Return True if the cart has nothing in it
        # HINT: one line — return len(self._items) == 0
        pass

    def get_items(self) -> dict:
        # TODO: Return a COPY of self._items (not the original!)
        # Why a copy? So nobody can change the cart from outside.
        # HINT: return dict(self._items)
        pass

    def __repr__(self) -> str:
        # TODO: Return a string like:
        # ShoppingCart(items=3, distinct_products=2, total=1059.97)
        # HINT: use len(self._items) for distinct_products
        pass

    def __len__(self) -> int:
        # TODO: Return total number of units (same as get_item_count)
        # This lets you do: len(cart)
        pass

    def __contains__(self, product: "Product") -> bool:
        # TODO: Return True if the product is in the cart
        # This lets you do: "if product in cart"
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/01_classes_and_objects/exercises/tests.py -v
#
# Run all OOP exercises at once:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/ -v
# =============================================================================
