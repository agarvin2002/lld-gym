"""
Starter: Polymorphic Discount System
=====================================

Complete all the TODOs below.

Run the tests with:
    pytest tests.py -v

The test file imports from this module, so keep all class names exactly
as they are defined here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Step 1: Define the Discount interface
# ---------------------------------------------------------------------------

class Discount(ABC):
    """
    Abstract base for all discount types.

    Every discount must implement apply(), which takes a price and returns
    the discounted price.

    Why ABC here?
    - Makes the interface explicit and enforced by Python
    - Instantiating Discount directly raises TypeError
    - Type checkers (mypy, pyright) understand the relationship

    Alternative: typing.Protocol (no inheritance required — see example2)
    """

    @abstractmethod
    def apply(self, price: float) -> float:
        """
        Apply this discount to the given price.

        Args:
            price: The original price (must be >= 0).

        Returns:
            The price after discount (must be >= 0).
        """
        # TODO: This is an abstract method — no implementation needed here
        ...


# ---------------------------------------------------------------------------
# Step 2: NoDiscount
# ---------------------------------------------------------------------------

class NoDiscount(Discount):
    """
    A discount that changes nothing.

    This is the Null Object pattern applied to discounts. Instead of
    checking 'if discount is None' everywhere, use NoDiscount() as the
    default — the interface remains consistent.
    """

    def apply(self, price: float) -> float:
        # TODO: Return the price unchanged
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 3: PercentageDiscount
# ---------------------------------------------------------------------------

class PercentageDiscount(Discount):
    """
    Reduces the price by a given percentage.

    Example:
        PercentageDiscount(20).apply(100.0) → 80.0
        PercentageDiscount(0).apply(100.0)  → 100.0
        PercentageDiscount(100).apply(50.0) → 0.0
    """

    def __init__(self, percent: float) -> None:
        """
        Args:
            percent: The discount percentage (0 to 100 inclusive).
        """
        # TODO: Validate that percent is between 0 and 100 (inclusive).
        # Raise ValueError if it is out of range.
        # Store the percent value.
        raise NotImplementedError

    def apply(self, price: float) -> float:
        # TODO: Calculate and return (price * (1 - percent/100))
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 4: FixedDiscount
# ---------------------------------------------------------------------------

class FixedDiscount(Discount):
    """
    Subtracts a fixed dollar amount from the price.

    The result is clamped to 0.0 — it can never go negative.

    Example:
        FixedDiscount(10).apply(50.0) → 40.0
        FixedDiscount(10).apply(8.0)  → 0.0   (not -2.0)
        FixedDiscount(10).apply(10.0) → 0.0
    """

    def __init__(self, amount: float) -> None:
        """
        Args:
            amount: The fixed amount to subtract (must be >= 0).
        """
        # TODO: Validate that amount is non-negative.
        # Raise ValueError if amount < 0.
        # Store the amount value.
        raise NotImplementedError

    def apply(self, price: float) -> float:
        # TODO: Subtract self.amount from price, but never go below 0.
        # Hint: max(0.0, price - self.amount)
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 5: BuyOneGetOneDiscount
# ---------------------------------------------------------------------------

class BuyOneGetOneDiscount(Discount):
    """
    Buy-one-get-one-free: the customer pays half price.

    Think of it as: you buy 2 items but pay for 1.
    So the per-item price is halved.

    Example:
        BuyOneGetOneDiscount().apply(60.0) → 30.0
        BuyOneGetOneDiscount().apply(99.0) → 49.5
    """

    def apply(self, price: float) -> float:
        # TODO: Return price / 2
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 6: Order
# ---------------------------------------------------------------------------

class Order:
    """
    Represents a customer order with a price and a discount strategy.

    The Order does not know (or care) which specific Discount is applied.
    It just calls discount.apply(price) — that is polymorphism in action.
    """

    def __init__(self, price: float, discount: Discount) -> None:
        """
        Args:
            price:    The original price of the order (must be > 0).
            discount: Any Discount implementation to apply.
        """
        # TODO: Validate that price > 0. Raise ValueError if not.
        # TODO: Store price and discount as instance attributes.
        raise NotImplementedError

    def final_price(self) -> float:
        """
        Apply the current discount to the original price.

        Returns:
            The price after discount.
        """
        # TODO: Return self.discount.apply(self.price)
        # No isinstance() allowed here!
        raise NotImplementedError

    def apply_discount(self, new_discount: Discount) -> None:
        """
        Replace the current discount strategy.

        This is the Strategy pattern: swap the algorithm at runtime.

        Args:
            new_discount: The new Discount to use going forward.
        """
        # TODO: Replace self.discount with new_discount
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"Order(price={self.price}, "
            f"discount={type(self.discount).__name__}, "
            f"final={self.final_price():.2f})"
        )
