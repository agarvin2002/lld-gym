"""
OCP Violation Example: Discount Calculator with if/elif Chain
=============================================================
This file demonstrates a clear Open/Closed Principle violation.

The `DiscountCalculator` class below uses an if/elif chain to handle
different discount types. Every time a new discount type is requested
by the business, a developer must:

  1. Open this file (modifying a "closed" class)
  2. Add a new elif branch
  3. Re-test all existing discount types (because we modified their file)
  4. Risk accidentally introducing a bug in existing discount logic

The comment "# NEW: added in sprint X" markers show how the class grew
over time — each addition was a modification to an existing, working class.

The four discount types currently supported:
  - PERCENTAGE: a percentage off the total (e.g., 10% off)
  - FIXED: a fixed dollar amount off (e.g., $20 off)
  - BOGO: Buy One Get One Free (50% off the total)
  - SEASONAL: tiered seasonal discount (10-25% depending on season)

Adding a fifth type (e.g., LOYALTY_POINTS) requires modifying this file.
"""

from __future__ import annotations

from datetime import date
from typing import Any


class DiscountCalculator:
    """
    OCP VIOLATION: This class must be modified for every new discount type.

    History of modifications (each is a violation of OCP):
    - Sprint 1: Added PERCENTAGE discount
    - Sprint 2: Added FIXED discount
    - Sprint 4: Added BOGO (marketing campaign)
    - Sprint 7: Added SEASONAL (Q4 request from sales team)
    - Sprint 9: ??? (next request will require ANOTHER modification)

    Every modification to this class risks breaking existing discount logic.
    A bug fix for SEASONAL discount could accidentally break PERCENTAGE.
    """

    def calculate(self, order_total: float, discount_type: str, **kwargs: Any) -> float:
        """
        Calculate discount amount based on discount type.

        This method must be MODIFIED every time a new discount type is added.
        That is the OCP violation.

        Args:
            order_total: The pre-discount order total
            discount_type: String identifier for the discount type
            **kwargs: Additional parameters specific to each discount type

        Returns:
            Discount amount in dollars
        """

        # --- ORIGINAL CODE (Sprint 1) ---
        if discount_type == "PERCENTAGE":
            # Percentage off the total. kwargs must contain "rate" (0.0 to 1.0)
            rate = kwargs.get("rate", 0.0)
            if not 0.0 <= rate <= 1.0:
                raise ValueError(f"Percentage rate must be between 0 and 1, got {rate}")
            return order_total * rate

        # --- ADDED IN SPRINT 2 (first modification) ---
        elif discount_type == "FIXED":
            # Fixed dollar amount off. kwargs must contain "amount"
            amount = kwargs.get("amount", 0.0)
            if amount < 0:
                raise ValueError(f"Fixed discount amount cannot be negative, got {amount}")
            # Cannot discount more than the order total
            return min(amount, order_total)

        # --- ADDED IN SPRINT 4 (second modification, risk to sprint 1 and 2 code) ---
        elif discount_type == "BOGO":
            # Buy One Get One Free: effectively 50% off the total.
            # If order has odd number of items, the cheaper item is free.
            # For simplicity here, we just use 50% of total.
            # kwargs may contain "item_prices" for exact calculation
            item_prices = kwargs.get("item_prices", [])
            if item_prices:
                # More precise: sum of every other item (sorted ascending)
                sorted_prices = sorted(item_prices)
                # Every second item is free (index 1, 3, 5, ...)
                free_amount = sum(sorted_prices[i] for i in range(1, len(sorted_prices), 2))
                return free_amount
            return order_total * 0.50  # Fallback: simple 50%

        # --- ADDED IN SPRINT 7 (third modification, risk to all previous logic) ---
        elif discount_type == "SEASONAL":
            # Tiered seasonal discount based on current month
            # Q4 (Oct-Dec): 25% off
            # Summer (Jun-Aug): 15% off
            # All other months: 10% off
            current_month = kwargs.get("month", date.today().month)

            if current_month in [10, 11, 12]:  # Q4
                rate = 0.25
            elif current_month in [6, 7, 8]:   # Summer
                rate = 0.15
            else:                               # Off-season
                rate = 0.10

            return order_total * rate

        # --- WHAT HAPPENS WHEN SPRINT 9 ASKS FOR LOYALTY_POINTS DISCOUNT? ---
        # We must add ANOTHER elif here, modifying this already-working class.
        # Every addition increases the risk of breaking existing logic.
        # The developer working on LOYALTY_POINTS has to understand BOGO logic.
        # That is wrong. OCP says: extend, don't modify.

        else:
            raise ValueError(f"Unknown discount type: '{discount_type}'")


class Order:
    """Simple order class to demonstrate the violation in context."""

    def __init__(self, order_id: str, items: list[dict[str, Any]]) -> None:
        self.order_id = order_id
        self.items = items
        self.total = sum(item["price"] * item["quantity"] for item in items)

    def apply_discount(self, calculator: DiscountCalculator, discount_type: str, **kwargs: Any) -> float:
        """Apply a discount and return the final amount."""
        discount = calculator.calculate(self.total, discount_type, **kwargs)
        return self.total - discount


# =============================================================================
# DEMONSTRATION: Shows the violation and why it's a problem
# =============================================================================

if __name__ == "__main__":
    calculator = DiscountCalculator()

    order = Order(
        order_id="ORD-001",
        items=[
            {"name": "Widget A", "price": 30.00, "quantity": 2},
            {"name": "Widget B", "price": 50.00, "quantity": 1},
            {"name": "Widget C", "price": 20.00, "quantity": 3},
        ],
    )
    print(f"Order total: ${order.total:.2f}\n")

    # Test each discount type
    tests = [
        ("PERCENTAGE", {"rate": 0.10}, "10% off"),
        ("FIXED", {"amount": 20.00}, "$20 fixed off"),
        ("BOGO", {"item_prices": [30.00, 30.00, 50.00, 20.00, 20.00, 20.00]}, "BOGO"),
        ("SEASONAL", {"month": 11}, "Seasonal (November = Q4 = 25%)"),
        ("SEASONAL", {"month": 7}, "Seasonal (July = Summer = 15%)"),
        ("SEASONAL", {"month": 3}, "Seasonal (March = Off-season = 10%)"),
    ]

    for discount_type, kwargs, description in tests:
        discount = calculator.calculate(order.total, discount_type, **kwargs)
        final = order.total - discount
        print(f"  {description}:")
        print(f"    Discount: ${discount:.2f}")
        print(f"    Final total: ${final:.2f}")
        print()

    print("=" * 60)
    print("OCP VIOLATION ILLUSTRATED:")
    print("=" * 60)
    print()
    print("When the business asks for a LOYALTY_POINTS discount:")
    print("  1. Developer opens DiscountCalculator (modifying closed code)")
    print("  2. Developer adds elif discount_type == 'LOYALTY_POINTS':")
    print("  3. Developer must understand all 4 existing elif branches")
    print("     to ensure no interference")
    print("  4. All 4 existing tests must be re-run (regression risk)")
    print("  5. Any mistake breaks PERCENTAGE, FIXED, BOGO, or SEASONAL")
    print()
    print("This is the OCP violation. See example2_with_strategy.py")
    print("for the correct design that avoids all of these problems.")
