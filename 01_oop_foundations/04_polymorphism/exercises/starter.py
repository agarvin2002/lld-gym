"""
WHAT YOU'RE BUILDING
--------------------
You are building a discount system for an online shop.

There are different types of discounts:
  NoDiscount            — price stays the same
  PercentageDiscount    — e.g. 20% off → ₹100 becomes ₹80
  FixedDiscount         — e.g. ₹10 off → ₹50 becomes ₹40 (never goes below ₹0)
  BuyOneGetOneDiscount  — pay for one, get one free → price is halved

An Order holds a price and a discount. You call order.final_price() and it applies
whichever discount is set — WITHOUT checking the type using if/elif.

TIP: This is the Strategy Pattern. You'll use it in every LLD problem where
the behaviour can change at runtime. Example: hotel pricing (peak vs off-peak),
payment gateways (Razorpay vs Paytm), vehicle fee calculation.

HOW TO RUN TESTS
    pytest tests.py -v
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# The common interface — every discount must implement apply()
# ---------------------------------------------------------------------------

class Discount(ABC):
    """
    Abstract base for all discount types.
    Every discount must implement apply(price) → discounted_price.
    """

    @abstractmethod
    def apply(self, price: float) -> float:
        """
        Apply this discount to the given price.
        Returns the price after discount (never negative).
        """
        ...


# ---------------------------------------------------------------------------
# NoDiscount — price does not change
# ---------------------------------------------------------------------------

class NoDiscount(Discount):
    """Use this when there is no discount. Returns price unchanged."""

    def apply(self, price: float) -> float:
        # No discount — return the price as-is
        return price


# ---------------------------------------------------------------------------
# PercentageDiscount — e.g. 20% off
# ---------------------------------------------------------------------------

class PercentageDiscount(Discount):
    """
    Reduces the price by a percentage.

    Example:
        PercentageDiscount(20).apply(100.0) → 80.0
        PercentageDiscount(0).apply(100.0)  → 100.0
        PercentageDiscount(100).apply(50.0) → 0.0
    """

    def __init__(self, percent: float) -> None:
        # percent must be between 0 and 100 (inclusive)
        if not 0 <= percent <= 100:
            raise ValueError(
                f"percent must be between 0 and 100, got {percent}"
            )
        self.percent = percent

    def apply(self, price: float) -> float:
        # Formula: price × (1 - percent/100)
        return price * (1 - self.percent / 100)


# ---------------------------------------------------------------------------
# FixedDiscount — e.g. ₹10 off, but never below ₹0
# ---------------------------------------------------------------------------

class FixedDiscount(Discount):
    """
    Subtracts a fixed amount from the price.
    Result is clamped to 0 — price never goes negative.

    Example:
        FixedDiscount(10).apply(50.0) → 40.0
        FixedDiscount(10).apply(8.0)  → 0.0   (not -2.0)
    """

    def __init__(self, amount: float) -> None:
        # amount must be >= 0
        if amount < 0:
            raise ValueError(f"amount must be >= 0, got {amount}")
        self.amount = amount

    def apply(self, price: float) -> float:
        # Subtract amount but never go below 0
        return max(0.0, price - self.amount)


# ---------------------------------------------------------------------------
# BuyOneGetOneDiscount — pay for one, get one free
# ---------------------------------------------------------------------------

class BuyOneGetOneDiscount(Discount):
    """
    Buy one get one free: customer pays for 1, gets 2.
    So the effective price per item is halved.

    Example:
        BuyOneGetOneDiscount().apply(60.0) → 30.0
    """

    def apply(self, price: float) -> float:
        return price / 2


# ---------------------------------------------------------------------------
# Order — holds a price and a discount strategy
# ---------------------------------------------------------------------------

class Order:
    """
    An order with a price and a discount.

    TIP: Order does NOT know which Discount type it has.
    It just calls discount.apply(price). This is polymorphism.
    No isinstance() checks. No if/elif chains.
    """

    def __init__(self, price: float, discount: Discount) -> None:
        # price must be > 0
        if price <= 0:
            raise ValueError(f"price must be > 0, got {price}")
        self.price = price
        self.discount = discount

    def final_price(self) -> float:
        """Apply the current discount and return the final price."""
        # TIP: this is the key line — one call, works for ALL discount types
        return self.discount.apply(self.price)

    def apply_discount(self, new_discount: Discount) -> None:
        """Change the discount. The price itself does not change."""
        self.discount = new_discount

    def __repr__(self) -> str:
        return (
            f"Order(price={self.price}, "
            f"discount={type(self.discount).__name__}, "
            f"final={self.final_price():.2f})"
        )


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/04_polymorphism/exercises/tests.py -v
#
# Run all OOP exercises at once:
#   /tmp/lld_venv/bin/pytest 01_oop_foundations/ -v
# =============================================================================
