"""
WHAT YOU'RE BUILDING
====================
A discount engine for an order system (think Swiggy/Zomato checkout).

You will implement five discount strategies and an Order class that uses them:

  - NoDiscount          — no discount applied
  - PercentageDiscount  — knock off a percentage (e.g. 20% off)
  - FixedDiscount       — knock off a fixed rupee amount (e.g. ₹50 off)
  - BuyOneGetOneFree    — pay for half (50% off total)
  - LoyaltyDiscount     — tier-based discount (silver 5%, gold 10%, platinum 15%)
  - Order               — holds a total and a strategy; computes the final price

The Order's total must never be mutated — final_price() applies the discount
and returns a new value each time.
"""
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, order_total: float) -> float:
        """Return the price after applying this discount."""
        ...


class NoDiscount(DiscountStrategy):
    # TODO: Return order_total unchanged
    def apply(self, order_total: float) -> float:
        pass


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        # TODO: Raise ValueError if percent is not in the range 0–100 (inclusive)
        # TODO: Store percent for use in apply()
        # HINT: if not (0 <= percent <= 100): raise ValueError(...)
        pass

    def apply(self, order_total: float) -> float:
        # TODO: Return order_total reduced by the stored percentage
        # HINT: order_total * (1 - self._percent / 100)
        pass


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        # TODO: Raise ValueError if amount is negative
        # TODO: Store amount for use in apply()
        pass

    def apply(self, order_total: float) -> float:
        # TODO: Subtract the fixed amount; never return less than 0.0
        # HINT: use max(0.0, order_total - self._amount)
        pass


class BuyOneGetOneFree(DiscountStrategy):
    def apply(self, order_total: float) -> float:
        # TODO: Return half the total (customer pays for one, gets one free)
        pass


class LoyaltyDiscount(DiscountStrategy):
    _TIERS = {"silver": 5, "gold": 10, "platinum": 15}

    def __init__(self, tier: str) -> None:
        # TODO: Raise ValueError for any tier not in _TIERS
        # TODO: Look up the discount percentage for the given tier and store it
        # HINT: if tier not in self._TIERS: raise ValueError(...)
        pass

    def apply(self, order_total: float) -> float:
        # TODO: Apply the tier's percentage discount (same formula as PercentageDiscount)
        pass


class Order:
    def __init__(self, total: float, discount: DiscountStrategy) -> None:
        # TODO: Raise ValueError if total is 0 or negative
        # TODO: Store total as self.total (public attribute — tests read it directly)
        # TODO: Store discount as self._discount (private)
        pass

    def final_price(self) -> float:
        # TODO: Delegate to self._discount.apply(self.total) and return the result
        # HINT: Do NOT modify self.total — tests check it stays unchanged
        pass

    def set_discount(self, discount: DiscountStrategy) -> None:
        # TODO: Replace the current discount strategy
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/behavioral/strategy/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
