"""
Solution: Polymorphic Discount System
======================================

This is the complete working solution. Study it after you have attempted
the exercise yourself.

Design decisions explained:
- Discount uses ABC (not Protocol) because we want Python to enforce
  that all subclasses implement apply(). This is a hard contract.
- Each discount class is self-contained: it only knows about itself.
- Order delegates all discount logic to the Discount object — it never
  inspects the type of the discount. This is the key polymorphic insight.
- apply_discount() implements the Strategy pattern: swap the algorithm at runtime.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Discount interface
# ---------------------------------------------------------------------------

class Discount(ABC):
    """
    Abstract base class for all discount strategies.

    Any class that extends Discount MUST implement apply().
    Python will raise TypeError at instantiation if it does not.
    """

    @abstractmethod
    def apply(self, price: float) -> float:
        """
        Apply this discount to the given price.

        Args:
            price: The original price (>= 0).

        Returns:
            The price after discount (>= 0).
        """
        ...


# ---------------------------------------------------------------------------
# NoDiscount — Null Object pattern
# ---------------------------------------------------------------------------

class NoDiscount(Discount):
    """
    A discount that does nothing.

    This is the Null Object pattern: instead of checking
    'if discount is not None' everywhere, callers can always call
    discount.apply() and get a sensible result.

    Use this as the default discount when creating an Order.
    """

    def apply(self, price: float) -> float:
        if price <= 0:
            raise ValueError(f"price should be grater than 0 got {price}")
        return price

    def __repr__(self) -> str:
        return "NoDiscount()"


# ---------------------------------------------------------------------------
# PercentageDiscount
# ---------------------------------------------------------------------------

class PercentageDiscount(Discount):
    """
    Reduces price by a percentage.

    Formula: price * (1 - percent / 100)

    Valid percent range: [0, 100] inclusive.
    """

    def __init__(self, percent: float) -> None:
        if not (0 <= percent <= 100):
            raise ValueError(
                f"percent must be between 0 and 100, got {percent}"
            )
        self.percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)

    def __repr__(self) -> str:
        return f"PercentageDiscount(percent={self.percent})"


# ---------------------------------------------------------------------------
# FixedDiscount
# ---------------------------------------------------------------------------

class FixedDiscount(Discount):
    """
    Subtracts a fixed amount from the price, clamped to 0.

    Using max(0.0, ...) ensures the price never goes negative.
    This is a business invariant: you can never owe the seller money
    because of a discount.
    """

    def __init__(self, amount: float) -> None:
        if amount < 0:
            raise ValueError(
                f"amount must be non-negative, got {amount}"
            )
        self.amount = amount

    def apply(self, price: float) -> float:
        return max(0.0, price - self.amount)

    def __repr__(self) -> str:
        return f"FixedDiscount(amount={self.amount})"


# ---------------------------------------------------------------------------
# BuyOneGetOneDiscount
# ---------------------------------------------------------------------------

class BuyOneGetOneDiscount(Discount):
    """
    Buy-one-get-one-free: pay for one, get two.

    This means the effective per-item price is halved.
    No state required — the calculation is purely a function of price.
    """

    def apply(self, price: float) -> float:
        return price / 2

    def __repr__(self) -> str:
        return "BuyOneGetOneDiscount()"


# ---------------------------------------------------------------------------
# Order — uses any Discount without knowing its type
# ---------------------------------------------------------------------------

class Order:
    """
    Represents a customer order with a price and a discount strategy.

    Key design:
    - Order stores a Discount reference, not a type name or enum value.
    - final_price() delegates to discount.apply() — no isinstance() needed.
    - apply_discount() swaps the strategy at runtime (Strategy pattern).
    - The original price is never mutated — discounts are applied on read.
    """

    def __init__(self, price: float, discount: Discount) -> None:
        if price <= 0:
            raise ValueError(f"price must be positive, got {price}")
        self.price = price
        self.discount = discount

    def final_price(self) -> float:
        """
        Apply the current discount to the original price.

        This is the polymorphic call: we never check what type of
        Discount this is. We just call apply(). Python dispatches
        to the correct implementation at runtime.
        """
        return self.discount.apply(self.price)

    def apply_discount(self, new_discount: Discount) -> None:
        """
        Replace the current discount strategy.

        This implements the Strategy pattern: algorithms (discounts)
        can be swapped at runtime without changing the Order class.
        This is powerful because:
        - New discount types can be added without changing Order
        - Discounts can be changed mid-lifecycle
        - The same order can be previewed with multiple discounts
        """
        self.discount = new_discount

    def __repr__(self) -> str:
        return (
            f"Order(price={self.price}, "
            f"discount={self.discount!r}, "
            f"final={self.final_price():.2f})"
        )


# ---------------------------------------------------------------------------
# Optional: TieredDiscount (bonus — shows extensibility)
# ---------------------------------------------------------------------------

class TieredDiscount(Discount):
    """
    Demonstrates extensibility: a new discount type requires ZERO changes
    to Order, NoDiscount, PercentageDiscount, or FixedDiscount.

    Gives:
    - 10% off for prices above $50
    - 20% off for prices above $100
    - No discount otherwise
    """

    def apply(self, price: float) -> float:
        if price > 100:
            return price * 0.80   # 20% off
        elif price > 50:
            return price * 0.90   # 10% off
        else:
            return price          # no discount

    def __repr__(self) -> str:
        return "TieredDiscount(thresholds=[50→10%, 100→20%])"


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("Polymorphic Discount System — Solution Demo")
    print("=" * 55)

    # All discount types applied to the same price
    price = 100.0
    discounts: list[Discount] = [
        NoDiscount(),
        PercentageDiscount(20),
        FixedDiscount(15),
        BuyOneGetOneDiscount(),
        TieredDiscount(),
    ]

    print(f"\nOriginal price: ${price:.2f}")
    print()
    for discount in discounts:
        result = discount.apply(price)
        print(f"  {discount!r:45} → ${result:.2f}")

    # Order with strategy swapping
    print("\n--- Order with strategy swapping ---")
    order = Order(price=100.0, discount=NoDiscount())
    print(f"Initial:  {order}")

    order.apply_discount(PercentageDiscount(25))
    print(f"After 25% off: {order}")

    order.apply_discount(BuyOneGetOneDiscount())
    print(f"After BOGO: {order}")

    order.apply_discount(FixedDiscount(30))
    print(f"After $30 off: {order}")

    # Edge case: Fixed discount > price
    print("\n--- Edge case: discount exceeds price ---")
    order2 = Order(price=5.0, discount=FixedDiscount(100))
    print(f"$5 item with $100 fixed discount: final = ${order2.final_price():.2f}")

    # Edge case: Tiered discount at different price points
    print("\n--- Tiered discount at various prices ---")
    for test_price in [30.0, 60.0, 120.0]:
        order3 = Order(price=test_price, discount=TieredDiscount())
        print(f"  ${test_price:6.2f} → ${order3.final_price():6.2f}")
