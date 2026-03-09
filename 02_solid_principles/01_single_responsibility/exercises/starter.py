"""
WHAT YOU'RE BUILDING
====================
The OrderProcessor god class below handles five things at once:
validation, discounts, payment, email, and inventory. That's five
reasons for it to change and five ways a bug can spread to unrelated code.

Your task: implement each of the six classes below the god class.
Each class does exactly one job. OrderService wires them all together.

Order dict structure:
{
    "order_id": "ORD-001",
    "customer_email": "customer@example.com",
    "membership": "gold",           # "none", "silver", "gold", "platinum"
    "payment_method": "credit_card", # "credit_card" or "paypal"
    "coupon_code": "SAVE10",        # optional, may be absent or None
    "items": [
        {"product_id": "P001", "name": "Widget A", "quantity": 2, "unit_price": 25.00},
    ]
}
"""

from __future__ import annotations

import uuid
from typing import Any


# =============================================================================
# GOD CLASS — study this, then implement the refactored classes below
# =============================================================================

class OrderProcessor:
    """
    GOD CLASS: handles validation, discounts, payment, email, and inventory.
    Do NOT modify this class. Study it and implement the refactored classes below.
    """

    INVENTORY: dict[str, int] = {"P001": 100, "P002": 50, "P003": 25}
    COUPONS: dict[str, float] = {"SAVE10": 10.0, "SAVE20": 20.0, "HALFOFF": 50.0}

    def process_order(self, order: dict[str, Any]) -> dict[str, Any]:
        errors: list[str] = []

        if not order.get("customer_email") or "@" not in order["customer_email"]:
            errors.append("Invalid customer email")
        if not order.get("items"):
            errors.append("Order must contain at least one item")
        for item in order.get("items", []):
            if item.get("quantity", 0) <= 0:
                errors.append(f"Invalid quantity for {item.get('name', 'unknown')}")
        if not order.get("payment_method"):
            errors.append("Payment method is required")

        if errors:
            return {"success": False, "errors": errors, "transaction_id": None, "discount": 0.0}

        subtotal = sum(i["quantity"] * i["unit_price"] for i in order["items"])
        discount = 0.0
        membership = order.get("membership", "none")
        if membership == "silver":
            discount += subtotal * 0.05
        elif membership == "gold":
            discount += subtotal * 0.10
        elif membership == "platinum":
            discount += subtotal * 0.15
        if subtotal > 200:
            discount += subtotal * 0.05
        coupon = order.get("coupon_code")
        if coupon and coupon in self.COUPONS:
            discount += self.COUPONS[coupon]

        payment_method = order["payment_method"]
        transaction_id = None
        if payment_method == "credit_card":
            transaction_id = f"CC-{uuid.uuid4().hex[:8].upper()}"
            print(f"[Payment] Credit card charged. Transaction: {transaction_id}")
        elif payment_method == "paypal":
            transaction_id = f"PP-{uuid.uuid4().hex[:8].upper()}"
            print(f"[Payment] PayPal charged. Transaction: {transaction_id}")
        else:
            errors.append(f"Unsupported payment method: {payment_method}")
            return {"success": False, "errors": errors, "transaction_id": None, "discount": discount}

        email = order["customer_email"]
        final_total = subtotal - discount
        print(f"[Email] Sending confirmation to {email}: Order {order['order_id']}, Total: ${final_total:.2f}")

        for item in order["items"]:
            product_id = item["product_id"]
            qty = item["quantity"]
            if product_id in self.INVENTORY:
                self.INVENTORY[product_id] -= qty
                print(f"[Inventory] {product_id}: stock updated to {self.INVENTORY[product_id]}")

        return {"success": True, "errors": [], "transaction_id": transaction_id, "discount": discount}


# =============================================================================
# YOUR TASK: implement the six classes below
# =============================================================================

class OrderValidator:
    """Validates that an order has all required fields and valid data."""

    def validate(self, order: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Check the order for errors.

        Returns:
            (True, []) if valid.
            (False, ["error1", ...]) if invalid.
        """
        # TODO: Build an errors list, then return (len(errors) == 0, errors)
        # Check 1: customer_email must exist and contain "@"
        # Check 2: items list must be non-empty
        # Check 3: every item must have quantity > 0
        # Check 4: payment_method must be present
        # HINT: Start with errors = [], append strings for each failed check,
        #       return (len(errors) == 0, errors) at the end.
        raise NotImplementedError("Implement OrderValidator.validate()")


class DiscountCalculator:
    """Calculates the total discount amount for an order."""

    MEMBERSHIP_DISCOUNTS: dict[str, float] = {
        "none": 0.0, "silver": 0.05, "gold": 0.10, "platinum": 0.15,
    }
    BULK_THRESHOLD: float = 200.0
    BULK_DISCOUNT_RATE: float = 0.05
    VALID_COUPONS: dict[str, float] = {"SAVE10": 10.0, "SAVE20": 20.0, "HALFOFF": 50.0}

    def calculate(self, order: dict[str, Any]) -> float:
        """
        Return total discount in dollars.

        Rules:
        - Membership: silver=5%, gold=10%, platinum=15% of subtotal
        - Bulk: 5% of subtotal if subtotal > $200
        - Coupon: fixed dollar amount from VALID_COUPONS
        """
        # TODO: Calculate and return the discount as a float
        # Step 1: subtotal = sum(item["quantity"] * item["unit_price"] for item in order["items"])
        # Step 2: membership_rate = self.MEMBERSHIP_DISCOUNTS.get(order.get("membership", "none"), 0.0)
        # Step 3: discount += subtotal * membership_rate
        # Step 4: if subtotal > BULK_THRESHOLD, discount += subtotal * BULK_DISCOUNT_RATE
        # Step 5: if order.get("coupon_code") in VALID_COUPONS, discount += VALID_COUPONS[coupon]
        # HINT: Return the discount as a float (not the final total — just the discount).
        raise NotImplementedError("Implement DiscountCalculator.calculate()")


class PaymentProcessor:
    """Charges the customer using their chosen payment method."""

    def charge(self, order: dict[str, Any], amount: float) -> tuple[bool, str]:
        """
        Process payment and return (success, transaction_id).

        On failure, return (False, "").
        """
        # TODO: Return (True, transaction_id) for supported methods, (False, "") otherwise
        # For "credit_card": transaction_id = f"CC-{uuid.uuid4().hex[:8].upper()}"
        # For "paypal":      transaction_id = f"PP-{uuid.uuid4().hex[:8].upper()}"
        # For anything else: return (False, "")
        raise NotImplementedError("Implement PaymentProcessor.charge()")


class EmailNotifier:
    """Sends order confirmation to the customer."""

    def send_confirmation(self, order: dict[str, Any], final_total: float, transaction_id: str) -> bool:
        """Print confirmation message and return True."""
        # TODO: Print this exact line, then return True:
        # "[Email] Sending confirmation to {email}: Order {order_id}, Total: ${final_total:.2f}"
        raise NotImplementedError("Implement EmailNotifier.send_confirmation()")


class InventoryUpdater:
    """Updates stock levels after a successful order."""

    def __init__(self, inventory: dict[str, int]) -> None:
        self.inventory = inventory

    def update(self, order: dict[str, Any]) -> bool:
        """
        Decrement stock for each ordered item, then return True.
        Only update items whose product_id exists in self.inventory.
        """
        # TODO: For each item in order["items"]:
        #   if item["product_id"] in self.inventory:
        #       subtract item["quantity"] from self.inventory[product_id]
        #       print: "[Inventory] {product_id}: stock updated to {new_stock}"
        # Return True at the end.
        raise NotImplementedError("Implement InventoryUpdater.update()")


class OrderService:
    """Orchestrates the order processing workflow."""

    def __init__(
        self,
        validator: OrderValidator,
        discount_calculator: DiscountCalculator,
        payment_processor: PaymentProcessor,
        email_notifier: EmailNotifier,
        inventory_updater: InventoryUpdater,
    ) -> None:
        self.validator = validator
        self.discount_calculator = discount_calculator
        self.payment_processor = payment_processor
        self.email_notifier = email_notifier
        self.inventory_updater = inventory_updater

    def process_order(self, order: dict[str, Any]) -> dict[str, Any]:
        """
        Process an order end-to-end and return a result dict.

        Returns:
            {"success": bool, "transaction_id": str|None, "discount": float, "errors": list[str]}
        """
        # TODO: Follow these steps in order:
        # 1. is_valid, errors = self.validator.validate(order)
        #    If not is_valid: return {"success": False, "errors": errors, "transaction_id": None, "discount": 0.0}
        # 2. discount = self.discount_calculator.calculate(order)
        # 3. subtotal = sum(i["quantity"] * i["unit_price"] for i in order["items"])
        #    final_total = subtotal - discount
        # 4. success, tx_id = self.payment_processor.charge(order, final_total)
        #    If not success: return {"success": False, "errors": ["Payment failed"], "transaction_id": None, "discount": discount}
        # 5. self.email_notifier.send_confirmation(order, final_total, tx_id)
        # 6. self.inventory_updater.update(order)
        # 7. return {"success": True, "errors": [], "transaction_id": tx_id, "discount": discount}
        # HINT: The workflow is a straight sequence — no branching after step 4 succeeds.
        raise NotImplementedError("Implement OrderService.process_order()")


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/01_single_responsibility/exercises/tests.py -v
#
# Run all SOLID exercises at once:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/ -v
# =============================================================================
