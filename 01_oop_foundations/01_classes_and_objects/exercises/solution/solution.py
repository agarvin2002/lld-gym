"""
solution.py — Reference Implementation: Product and ShoppingCart
----------------------------------------------------------------
This is a complete, production-quality implementation of the exercise.

Design principles applied:
  - Fail fast: validate all inputs in __init__ and method entry points
  - Immutable identity: __eq__ and __hash__ use SKU (the stable identifier)
  - Defensive copying: get_items() returns a copy to prevent state leakage
  - Informative __repr__: shows all state needed for debugging
  - Single responsibility: Product knows about products, Cart knows about the cart
"""

from __future__ import annotations


class Product:
    """
    Represents a purchasable product in an e-commerce system.

    Identity is based on SKU — two products with the same SKU are considered
    the same product regardless of their current price or name.
    """

    def __init__(self, name: str, price: float, quantity: int, sku: str) -> None:
        """
        Initialize a Product with validation.

        Args:
            name:     Human-readable name. Must be a non-empty string.
            price:    Unit price in dollars. Must be strictly > 0.
            quantity: Units in stock. Must be >= 0.
            sku:      Unique stock-keeping identifier. Must be non-empty.

        Raises:
            ValueError: If any argument violates its constraint.
        """
        # Validate before assignment — the object should never exist in an invalid state
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"name must be a non-empty string, got {name!r}.")
        if not isinstance(sku, str) or not sku.strip():
            raise ValueError(f"sku must be a non-empty string, got {sku!r}.")
        if price <= 0:
            raise ValueError(f"price must be strictly positive (> 0), got {price}.")
        if quantity < 0:
            raise ValueError(f"quantity must be >= 0, got {quantity}.")

        self.name: str = name
        self.price: float = float(price)
        self.quantity: int = quantity
        self.sku: str = sku

    # -----------------------------------------------------------------------
    # String representations
    # -----------------------------------------------------------------------

    def __repr__(self) -> str:
        """Developer-facing representation — shows all attributes."""
        return (
            f"Product("
            f"name={self.name!r}, "
            f"price={self.price}, "
            f"quantity={self.quantity}, "
            f"sku={self.sku!r}"
            f")"
        )

    def __str__(self) -> str:
        """Human-readable representation for display."""
        stock_status = f"{self.quantity} in stock" if self.quantity > 0 else "OUT OF STOCK"
        return f"{self.name} (SKU: {self.sku}) — ${self.price:.2f} | {stock_status}"

    # -----------------------------------------------------------------------
    # Equality and hashing
    # -----------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """
        Equality based on SKU.

        Two products are the same product if they share a SKU, regardless of
        name or price (both of which can change over time).
        """
        if not isinstance(other, Product):
            return NotImplemented
        return self.sku == other.sku

    def __hash__(self) -> int:
        """
        Hash based on SKU, consistent with __eq__.

        Allows Product instances to be used as dict keys and stored in sets.
        Only immutable fields (sku never changes after creation) should be hashed.
        """
        return hash(self.sku)

    # -----------------------------------------------------------------------
    # Business logic methods
    # -----------------------------------------------------------------------

    def is_in_stock(self) -> bool:
        """Return True if at least one unit is available."""
        return self.quantity > 0

    def apply_discount(self, percent: float) -> None:
        """
        Reduce price by the given percentage.

        Args:
            percent: Discount percentage. Must be in range (0, 100].

        Raises:
            ValueError: If percent is not in (0, 100].
        """
        if percent <= 0 or percent > 100:
            raise ValueError(
                f"Discount percent must be in range (0, 100], got {percent}."
            )
        discount_amount = self.price * percent / 100
        self.price -= discount_amount


class ShoppingCart:
    """
    A shopping cart that tracks which products a customer wants to purchase
    and in what quantities.

    Internal storage: dict[Product, int] where the value is the cart quantity
    (how many units the customer wants), not the product's stock quantity.
    """

    def __init__(self) -> None:
        """Initialize an empty shopping cart."""
        # Using dict rather than list because:
        # 1. O(1) lookup to check if a product is already in the cart
        # 2. O(1) access to the quantity for a given product
        # 3. Natural deduplication — same product can only appear once as a key
        self._items: dict[Product, int] = {}

    # -----------------------------------------------------------------------
    # Core cart operations
    # -----------------------------------------------------------------------

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """
        Add units of a product to the cart.

        If the product is already in the cart, its quantity is increased.
        If not, it is added fresh with the given quantity.

        Args:
            product:  The Product to add.
            quantity: Number of units. Must be >= 1.

        Raises:
            ValueError: If quantity < 1.
        """
        if quantity < 1:
            raise ValueError(
                f"Quantity must be at least 1, got {quantity}."
            )
        # dict.get(key, default) returns the existing value or the default.
        # This avoids a separate "if product in self._items" check.
        self._items[product] = self._items.get(product, 0) + quantity

    def remove_item(self, product: Product) -> None:
        """
        Remove a product entirely from the cart.

        Args:
            product: The Product to remove.

        Raises:
            ValueError: If the product is not in the cart.
        """
        if product not in self._items:
            raise ValueError(
                f"Product {product.name!r} (SKU: {product.sku}) is not in the cart."
            )
        del self._items[product]

    def get_total(self) -> float:
        """
        Calculate the total cost of all items in the cart.

        Returns:
            sum(product.price * cart_quantity) for all items.
        """
        return sum(product.price * qty for product, qty in self._items.items())

    def get_item_count(self) -> int:
        """
        Return the total number of individual units in the cart.

        E.g., 2 laptops + 3 mice = 5 total units.
        """
        return sum(self._items.values())

    def is_empty(self) -> bool:
        """Return True if the cart contains no items."""
        return len(self._items) == 0

    def get_items(self) -> dict[Product, int]:
        """
        Return a copy of the internal items dict.

        Returns a copy so external callers cannot mutate the cart's internal state.
        This is an example of defensive copying — a key encapsulation technique.
        """
        return dict(self._items)

    # -----------------------------------------------------------------------
    # Dunder methods
    # -----------------------------------------------------------------------

    def __repr__(self) -> str:
        """Developer-facing representation showing cart summary."""
        distinct = len(self._items)
        total_units = self.get_item_count()
        total_price = self.get_total()
        return (
            f"ShoppingCart("
            f"distinct_products={distinct}, "
            f"total_units={total_units}, "
            f"total=${total_price:.2f}"
            f")"
        )

    def __len__(self) -> int:
        """Return the total number of units in the cart. Enables: len(cart)."""
        return self.get_item_count()

    def __contains__(self, product: Product) -> bool:
        """Return True if the product is in the cart. Enables: product in cart."""
        return product in self._items


# =============================================================================
# Quick smoke test — runs when executed directly, not when imported by pytest
# =============================================================================

if __name__ == "__main__":
    print("=== Product ===")
    laptop = Product("Laptop Pro", 999.99, 10, "SKU-LAPTOP-001")
    mouse = Product("Wireless Mouse", 29.99, 50, "SKU-MOUSE-001")
    keyboard = Product("Mechanical Keyboard", 79.99, 25, "SKU-KB-001")

    print(repr(laptop))
    print(str(laptop))

    laptop.apply_discount(10)
    print(f"After 10% discount: {laptop.price:.2f}")  # 899.991

    print("\n=== ShoppingCart ===")
    cart = ShoppingCart()
    print(f"Empty cart: {cart.is_empty()}")

    cart.add_item(laptop, 1)
    cart.add_item(mouse, 2)
    cart.add_item(keyboard, 1)

    print(repr(cart))
    print(f"len(cart): {len(cart)}")           # 4
    print(f"Total: ${cart.get_total():.2f}")
    print(f"laptop in cart: {laptop in cart}")  # True

    cart.remove_item(mouse)
    print(f"\nAfter removing mouse:")
    print(repr(cart))

    # Demonstrate error handling
    try:
        cart.remove_item(mouse)
    except ValueError as e:
        print(f"Expected error: {e}")
