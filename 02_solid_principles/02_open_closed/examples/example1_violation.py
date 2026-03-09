"""
OCP Violation: Discount Calculator with if/elif chain
======================================================
Every time the business adds a new discount type, a developer must open
this file and add another elif branch. That is the OCP violation.

Comments like "# ADDED IN SPRINT 4" show how the class grew over time —
each addition modified already-working code.

Real-world use: This pattern appears in e-commerce checkout systems
(Flipkart, Meesho) where discount types start simple and grow rapidly.
The if/elif chain becomes a maintenance burden after a few sprints.
"""

from __future__ import annotations

from datetime import date
from typing import Any


class DiscountCalculator:
    """
    OCP VIOLATION: must be modified for every new discount type.

    Sprint history (each is a violation):
    - Sprint 1: PERCENTAGE
    - Sprint 2: FIXED
    - Sprint 4: BOGO
    - Sprint 7: SEASONAL
    - Sprint 9: ??? (next request will require another modification)
    """

    def calculate(self, order_total: float, discount_type: str, **kwargs: Any) -> float:
        """
        Returns discount amount. Must be MODIFIED for every new type.
        """
        # Sprint 1 — original code
        if discount_type == "PERCENTAGE":
            rate = kwargs.get("rate", 0.0)
            if not 0.0 <= rate <= 1.0:
                raise ValueError(f"Rate must be 0-1, got {rate}")
            return order_total * rate

        # Sprint 2 — first modification
        elif discount_type == "FIXED":
            amount = kwargs.get("amount", 0.0)
            if amount < 0:
                raise ValueError(f"Amount cannot be negative, got {amount}")
            return min(amount, order_total)

        # Sprint 4 — second modification, risk to previous branches
        elif discount_type == "BOGO":
            item_prices = kwargs.get("item_prices", [])
            if item_prices:
                sorted_prices = sorted(item_prices)
                return sum(sorted_prices[i] for i in range(1, len(sorted_prices), 2))
            return order_total * 0.50

        # Sprint 7 — third modification, risk to all previous branches
        elif discount_type == "SEASONAL":
            current_month = kwargs.get("month", date.today().month)
            if current_month in [10, 11, 12]:   # Q4
                rate = 0.25
            elif current_month in [6, 7, 8]:    # Summer
                rate = 0.15
            else:                               # off-season
                rate = 0.10
            return order_total * rate

        # TIP: Adding LOYALTY_POINTS here means opening and editing this file again.
        # Every addition increases regression risk for all previous discount types.

        else:
            raise ValueError(f"Unknown discount type: '{discount_type}'")


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    calculator = DiscountCalculator()
    total = 200.0
    print(f"Order total: ${total:.2f}\n")

    cases = [
        ("PERCENTAGE", {"rate": 0.10}, "10% off"),
        ("FIXED", {"amount": 20.00}, "$20 fixed"),
        ("BOGO", {"item_prices": [30.0, 30.0, 50.0, 20.0]}, "BOGO"),
        ("SEASONAL", {"month": 11}, "Seasonal November (Q4 = 25%)"),
    ]

    for discount_type, kwargs, label in cases:
        discount = calculator.calculate(total, discount_type, **kwargs)
        print(f"  {label}: discount=${discount:.2f}, final=${total - discount:.2f}")

    print("\nVIOLATION: adding a new discount type requires editing this class.")
    print("See example2_with_strategy.py for the OCP-compliant design.")
