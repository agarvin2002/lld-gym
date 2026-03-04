"""
SRP Exercise — Complete Solution
=================================
This file contains the full working implementation of the refactored
OrderProcessor system, split into SRP-compliant classes.

Each class has exactly one reason to change:
- OrderValidator    → validation rules change
- DiscountCalculator → discount tiers/rules change
- PaymentProcessor  → payment provider/logic changes
- EmailNotifier     → notification template/provider changes
- InventoryUpdater  → inventory system changes
- OrderService      → orchestration workflow changes
"""

from __future__ import annotations

import uuid
from typing import Any


class OrderValidator:
    """
    Responsibility: Validate that an order has all required fields and valid data.
    Reason to change: ONLY when validation rules change.
    """

    def validate(self, order: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Validate the order for required fields and data integrity.

        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        errors: list[str] = []

        # Validate customer email
        email = order.get("customer_email", "")
        if not email or "@" not in email:
            errors.append("Invalid customer email")

        # Validate items list is non-empty
        items = order.get("items", [])
        if not items:
            errors.append("Order must contain at least one item")

        # Validate each item has a positive quantity
        for item in items:
            if item.get("quantity", 0) <= 0:
                errors.append(f"Invalid quantity for {item.get('name', 'unknown')}")

        # Validate payment method is present
        if not order.get("payment_method"):
            errors.append("Payment method is required")

        is_valid = len(errors) == 0
        return is_valid, errors


class DiscountCalculator:
    """
    Responsibility: Calculate the total discount for an order.
    Reason to change: ONLY when discount rules or tiers change.
    """

    MEMBERSHIP_DISCOUNTS: dict[str, float] = {
        "none": 0.0,
        "silver": 0.05,
        "gold": 0.10,
        "platinum": 0.15,
    }

    BULK_THRESHOLD: float = 200.0
    BULK_DISCOUNT_RATE: float = 0.05

    VALID_COUPONS: dict[str, float] = {
        "SAVE10": 10.0,
        "SAVE20": 20.0,
        "HALFOFF": 50.0,
    }

    def calculate(self, order: dict[str, Any]) -> float:
        """
        Calculate total discount amount.

        Rules applied in order:
        1. Membership percentage discount off subtotal
        2. Bulk discount (5% if subtotal > $200)
        3. Coupon fixed-amount discount

        Returns:
            Total discount amount in dollars
        """
        # Step 1: Calculate order subtotal
        subtotal = sum(
            item["quantity"] * item["unit_price"]
            for item in order.get("items", [])
        )

        discount = 0.0

        # Step 2: Apply membership discount
        membership = order.get("membership", "none")
        membership_rate = self.MEMBERSHIP_DISCOUNTS.get(membership, 0.0)
        discount += subtotal * membership_rate

        # Step 3: Apply bulk discount if applicable
        if subtotal > self.BULK_THRESHOLD:
            discount += subtotal * self.BULK_DISCOUNT_RATE

        # Step 4: Apply coupon if valid
        coupon_code = order.get("coupon_code")
        if coupon_code and coupon_code in self.VALID_COUPONS:
            discount += self.VALID_COUPONS[coupon_code]

        return discount


class PaymentProcessor:
    """
    Responsibility: Charge the customer using their chosen payment method.
    Reason to change: ONLY when payment provider or payment logic changes.
    """

    def charge(self, order: dict[str, Any], amount: float) -> tuple[bool, str]:
        """
        Process the payment for the given amount.

        Returns:
            Tuple of (success, transaction_id)
        """
        payment_method = order.get("payment_method", "")

        if payment_method == "credit_card":
            transaction_id = f"CC-{uuid.uuid4().hex[:8].upper()}"
            print(f"[Payment] Credit card charged ${amount:.2f}. Transaction: {transaction_id}")
            return True, transaction_id

        elif payment_method == "paypal":
            transaction_id = f"PP-{uuid.uuid4().hex[:8].upper()}"
            print(f"[Payment] PayPal charged ${amount:.2f}. Transaction: {transaction_id}")
            return True, transaction_id

        else:
            print(f"[Payment] Unsupported payment method: {payment_method}")
            return False, ""


class EmailNotifier:
    """
    Responsibility: Send order confirmation notification to the customer.
    Reason to change: ONLY when notification logic or template changes.
    """

    def send_confirmation(
        self,
        order: dict[str, Any],
        final_total: float,
        transaction_id: str,
    ) -> bool:
        """
        Send a confirmation email to the customer.

        Returns:
            True if sent successfully
        """
        email = order.get("customer_email", "")
        order_id = order.get("order_id", "UNKNOWN")
        print(
            f"[Email] Sending confirmation to {email}: "
            f"Order {order_id}, Total: ${final_total:.2f}, "
            f"Transaction: {transaction_id}"
        )
        return True


class InventoryUpdater:
    """
    Responsibility: Update stock levels after a successful order.
    Reason to change: ONLY when inventory system or update logic changes.
    """

    def __init__(self, inventory: dict[str, int]) -> None:
        self.inventory = inventory

    def update(self, order: dict[str, Any]) -> bool:
        """
        Decrement inventory for each ordered item.

        Skips items whose product_id is not found in inventory.

        Returns:
            True after attempting all updates
        """
        for item in order.get("items", []):
            product_id = item["product_id"]
            quantity = item["quantity"]

            if product_id in self.inventory:
                self.inventory[product_id] -= quantity
                print(
                    f"[Inventory] {product_id}: stock updated to {self.inventory[product_id]}"
                )
            # Unknown products are silently skipped — could log a warning in production

        return True


class OrderService:
    """
    Responsibility: Orchestrate the order processing workflow.
    Reason to change: ONLY when the high-level workflow steps change.
    """

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
        Process an order through the complete workflow.

        Returns:
            Dict with keys: success, transaction_id, discount, errors
        """
        # Step 1: Validate the order
        is_valid, errors = self.validator.validate(order)
        if not is_valid:
            return {
                "success": False,
                "transaction_id": None,
                "discount": 0.0,
                "errors": errors,
            }

        # Step 2: Calculate discount
        discount = self.discount_calculator.calculate(order)

        # Step 3: Calculate final total
        subtotal = sum(
            item["quantity"] * item["unit_price"]
            for item in order.get("items", [])
        )
        final_total = subtotal - discount

        # Step 4: Charge payment
        payment_success, transaction_id = self.payment_processor.charge(order, final_total)
        if not payment_success:
            return {
                "success": False,
                "transaction_id": None,
                "discount": discount,
                "errors": [f"Payment failed for method: {order.get('payment_method')}"],
            }

        # Step 5: Send confirmation email
        self.email_notifier.send_confirmation(order, final_total, transaction_id)

        # Step 6: Update inventory
        self.inventory_updater.update(order)

        # Step 7: Return success
        return {
            "success": True,
            "transaction_id": transaction_id,
            "discount": discount,
            "errors": [],
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    inventory = {"P001": 100, "P002": 50, "P003": 25}

    service = OrderService(
        validator=OrderValidator(),
        discount_calculator=DiscountCalculator(),
        payment_processor=PaymentProcessor(),
        email_notifier=EmailNotifier(),
        inventory_updater=InventoryUpdater(inventory),
    )

    print("=== Test 1: Valid Gold Member Order with Coupon ===")
    order1 = {
        "order_id": "ORD-001",
        "customer_email": "alice@example.com",
        "membership": "gold",
        "payment_method": "credit_card",
        "coupon_code": "SAVE10",
        "items": [
            {"product_id": "P001", "name": "Widget A", "quantity": 2, "unit_price": 25.00},
            {"product_id": "P002", "name": "Widget B", "quantity": 1, "unit_price": 50.00},
        ],
    }
    result1 = service.process_order(order1)
    print(f"Result: {result1}")
    print()

    print("=== Test 2: Invalid Order (bad email, empty items) ===")
    order2 = {
        "order_id": "ORD-002",
        "customer_email": "not-an-email",
        "membership": "none",
        "payment_method": "credit_card",
        "items": [],
    }
    result2 = service.process_order(order2)
    print(f"Result: {result2}")
    print()

    print("=== Test 3: PayPal Order ===")
    order3 = {
        "order_id": "ORD-003",
        "customer_email": "bob@example.com",
        "membership": "silver",
        "payment_method": "paypal",
        "coupon_code": None,
        "items": [
            {"product_id": "P003", "name": "Widget C", "quantity": 1, "unit_price": 75.00},
        ],
    }
    result3 = service.process_order(order3)
    print(f"Result: {result3}")
    print()

    print(f"Final inventory state: {inventory}")
