"""
starter.py — Classes and Objects Exercise
-----------------------------------------
Your task: Implement the Product and ShoppingCart classes.

Instructions:
  1. Read problem.md carefully before starting.
  2. Fill in every method marked with TODO.
  3. Do not change method signatures or class names.
  4. Run tests with: pytest tests.py -v

Type hints are already provided — keep them.
Docstrings describe the expected behavior — implement exactly that.
"""


class Product:
    """
    Represents a purchasable product in an e-commerce system.

    Attributes:
        name (str):     Human-readable product name. Non-empty.
        price (float):  Unit price in dollars. Must be > 0.
        quantity (int): Number of units available in stock. Must be >= 0.
        sku (str):      Stock Keeping Unit — unique identifier. Non-empty.
    """

    def __init__(self, name: str, price: float, quantity: int, sku: str) -> None:
        """
        Initialize a Product with validation.

        Raises:
            ValueError: If name or sku are empty strings.
            ValueError: If price is not strictly positive (> 0).
            ValueError: If quantity is negative.
        """
        # TODO: Validate name — must be a non-empty string
        # TODO: Validate price — must be strictly greater than 0
        # TODO: Validate quantity — must be >= 0
        # TODO: Validate sku — must be a non-empty string
        # TODO: Assign all validated values to instance attributes
        pass

    def __repr__(self) -> str:
        """
        Return a developer-friendly string representation.

        Example:
            Product(name='Laptop Pro', price=999.99, quantity=10, sku='SKU-LAPTOP-001')
        """
        # TODO: Return a string in the format shown in the docstring example
        pass

    def __str__(self) -> str:
        """
        Return a human-readable string representation.

        Example:
            Laptop Pro (SKU: SKU-LAPTOP-001) — $999.99 | 10 in stock
        """
        # TODO: Return a user-friendly string describing the product
        pass

    def __eq__(self, other: object) -> bool:
        """
        Two Products are equal if they have the same SKU.

        Note: equality is based on sku, not name or price (which can change).

        Returns:
            NotImplemented if other is not a Product.
            True if self.sku == other.sku.
            False otherwise.
        """
        # TODO: Check if other is a Product instance
        # TODO: Return NotImplemented if not
        # TODO: Compare by sku
        pass

    def __hash__(self) -> int:
        """
        Return a hash based on sku (consistent with __eq__).

        This allows Products to be used as dict keys and in sets.
        """
        # TODO: Return hash(self.sku)
        pass

    def is_in_stock(self) -> bool:
        """
        Return True if there is at least one unit available in stock.

        Returns:
            True if self.quantity > 0, False otherwise.
        """
        # TODO: Return True if quantity > 0
        pass

    def apply_discount(self, percent: float) -> None:
        """
        Reduce the product's price by a given percentage.

        Args:
            percent: The discount percentage. Must be in range (0, 100].
                     e.g., percent=10 reduces a $100 item to $90.

        Raises:
            ValueError: If percent is not in range (0, 100].
        """
        # TODO: Validate that percent is in range (0, 100]
        # TODO: Calculate the discount amount: price * percent / 100
        # TODO: Subtract the discount from self.price
        pass

class ShoppingCart:
    """
    A shopping cart that holds a collection of Products.

    Internally, stores items as a dict mapping Product -> cart_quantity,
    where cart_quantity is how many units the customer wants to buy
    (distinct from the product's stock quantity).
    """

    def __init__(self) -> None:
        """
        Initialize an empty shopping cart.

        Internal state:
            _items (dict[Product, int]): maps each product to its cart quantity.
        """
        # TODO: Initialize self._items as an empty dict
        pass

    def add_item(self, product: "Product", quantity: int = 1) -> None:
        """
        Add one or more units of a product to the cart.

        If the product is already in the cart, increase its cart quantity.
        If the product is not yet in the cart, add it with the given quantity.

        Args:
            product:  The Product to add.
            quantity: Number of units to add. Must be >= 1.

        Raises:
            ValueError: If quantity < 1.
        """
        # TODO: Validate that quantity >= 1
        # TODO: If product already in cart, increase quantity
        # TODO: If product not in cart, add with given quantity
        pass

    def remove_item(self, product: "Product") -> None:
        """
        Remove a product entirely from the cart.

        Args:
            product: The Product to remove.

        Raises:
            ValueError: If the product is not in the cart.
        """
        # TODO: Check if product is in _items
        # TODO: Raise ValueError with a descriptive message if not found
        # TODO: Delete the product from _items
        pass

    def get_total(self) -> float:
        """
        Calculate the total price of all items in the cart.

        Total = sum(product.price * cart_quantity) for each item.

        Returns:
            The total cost as a float.
        """
        # TODO: Iterate over _items.items() and sum price * quantity for each
        pass

    def get_item_count(self) -> int:
        """
        Return the total number of individual units in the cart.

        E.g., if cart has 1 laptop and 2 mice, count is 3.

        Returns:
            Sum of all cart quantities.
        """
        # TODO: Return sum of all values in _items
        pass

    def is_empty(self) -> bool:
        """
        Return True if the cart has no items.

        Returns:
            True if _items is empty, False otherwise.
        """
        # TODO: Return True if _items is empty
        pass

    def get_items(self) -> dict:
        """
        Return a copy of the internal items dict.

        Returns a copy to prevent external mutation of internal state.

        Returns:
            dict[Product, int]: copy of _items
        """
        # TODO: Return a copy of _items (use dict(...) or .copy())
        pass

    def __repr__(self) -> str:
        """
        Return a developer-friendly string representation.

        Example:
            ShoppingCart(items=3, distinct_products=2, total=1059.97)
        """
        # TODO: Show number of distinct products, total item count, and total price
        pass

    def __len__(self) -> int:
        """
        Return the total number of individual units in the cart.

        Enables: len(cart)
        """
        # TODO: Return self.get_item_count()
        pass

    def __contains__(self, product: "Product") -> bool:
        """
        Return True if the product is in the cart.

        Enables: product in cart
        """
        # TODO: Return True if product is a key in _items
        pass
