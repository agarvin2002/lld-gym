"""
SRP Exercise — Starter File
============================
The OrderProcessor god class below violates SRP by handling five
distinct responsibilities in one class.

Your task: Refactor this into the classes defined below the god class.
Fill in each class's methods. The tests in tests.py will verify your work.

Order dict structure:
{
    "order_id": "ORD-001",
    "customer_email": "customer@example.com",
    "membership": "gold",          # "none", "silver", "gold", "platinum"
    "payment_method": "credit_card", # "credit_card" or "paypal"
    "coupon_code": "SAVE10",       # optional, may be absent or None
    "items": [
        {"product_id": "P001", "name": "Widget A", "quantity": 2, "unit_price": 25.00},
        {"product_id": "P002", "name": "Widget B", "quantity": 1, "unit_price": 50.00},
    ]
}
"""

from __future__ import annotations

import uuid
from typing import Any


# =============================================================================
# GOD CLASS — violates SRP (study this, then refactor below)
# =============================================================================

class OrderProcessor:
    """
    GOD CLASS: handles validation, discounts, payment, email, and inventory.

    This class has FIVE reasons to change:
    1. Validation rules change
    2. Discount logic changes
    3. Payment provider changes
    4. Email template/provider changes
    5. Inventory system changes

    Do NOT modify this class. Study it and implement the refactored classes below.
    """

    # Simulated in-memory inventory
    INVENTORY: dict[str, int] = {
        "P001": 100,
        "P002": 50,
        "P003": 25,
    }

    # Simulated valid coupon codes and their discount amounts
    COUPONS: dict[str, float] = {
        "SAVE10": 10.0,
        "SAVE20": 20.0,
        "HALFOFF": 50.0,
    }

    def process_order(self, order: dict[str, Any]) -> dict[str, Any]:
        errors: list[str] = []

        # --- RESPONSIBILITY 1: Validation ---
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

        # --- RESPONSIBILITY 2: Discount Calculation ---
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
            discount += subtotal * 0.05  # Bulk discount

        coupon = order.get("coupon_code")
        if coupon and coupon in self.COUPONS:
            discount += self.COUPONS[coupon]

        # --- RESPONSIBILITY 3: Payment ---
        payment_method = order["payment_method"]
        transaction_id = None
        payment_success = False

        if payment_method == "credit_card":
            # Simulate credit card charge
            transaction_id = f"CC-{uuid.uuid4().hex[:8].upper()}"
            payment_success = True
            print(f"[Payment] Credit card charged. Transaction: {transaction_id}")
        elif payment_method == "paypal":
            # Simulate PayPal charge
            transaction_id = f"PP-{uuid.uuid4().hex[:8].upper()}"
            payment_success = True
            print(f"[Payment] PayPal charged. Transaction: {transaction_id}")
        else:
            errors.append(f"Unsupported payment method: {payment_method}")
            return {"success": False, "errors": errors, "transaction_id": None, "discount": discount}

        # --- RESPONSIBILITY 4: Email Notification ---
        email = order["customer_email"]
        final_total = subtotal - discount
        print(f"[Email] Sending confirmation to {email}: Order {order['order_id']}, Total: ${final_total:.2f}")

        # --- RESPONSIBILITY 5: Inventory Update ---
        for item in order["items"]:
            product_id = item["product_id"]
            qty = item["quantity"]
            if product_id in self.INVENTORY:
                self.INVENTORY[product_id] -= qty
                print(f"[Inventory] {product_id}: stock updated to {self.INVENTORY[product_id]}")

        return {
            "success": True,
            "errors": [],
            "transaction_id": transaction_id,
            "discount": discount,
        }


# =============================================================================
# YOUR TASK: Implement the refactored classes below
# =============================================================================

class OrderValidator:
    """
    Responsibility: Validate that an order has all required fields and valid data.
    Reason to change: ONLY when validation rules change.
    """

    def validate(self, order: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Validate the order.

        Args:
            order: Raw order dictionary

        Returns:
            Tuple of (is_valid, list_of_error_messages)
            If is_valid is True, the error list will be empty.
        """
        # TODO: Implement validation logic
        # Check: customer_email exists and contains "@"
        # Check: items list is non-empty
        # Check: each item has quantity > 0
        # Check: payment_method is present
        raise NotImplementedError("Implement OrderValidator.validate()")


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
        Calculate total discount amount for the order.

        Discount rules:
        - Membership discount: silver=5%, gold=10%, platinum=15% of subtotal
        - Bulk discount: 5% of subtotal if subtotal > $200
        - Coupon: fixed amount off (see VALID_COUPONS)

        Args:
            order: Raw order dictionary

        Returns:
            Total discount amount in dollars (float)
        """
        # TODO: Implement discount calculation
        # Step 1: Calculate subtotal = sum(quantity * unit_price for each item)
        # Step 2: Apply membership discount based on order["membership"]
        # Step 3: Apply bulk discount if subtotal > BULK_THRESHOLD
        # Step 4: Apply coupon if order["coupon_code"] is in VALID_COUPONS
        raise NotImplementedError("Implement DiscountCalculator.calculate()")


class PaymentProcessor:
    """
    Responsibility: Charge the customer using their chosen payment method.
    Reason to change: ONLY when payment provider or payment logic changes.
    """

    def charge(self, order: dict[str, Any], amount: float) -> tuple[bool, str]:
        """
        Process the payment for the given amount.

        Supported payment methods: "credit_card", "paypal"

        Args:
            order: Raw order dictionary (contains payment_method)
            amount: Final amount to charge (after discounts)

        Returns:
            Tuple of (success, transaction_id)
            On failure, transaction_id will be an empty string.
        """
        # TODO: Implement payment logic
        # For "credit_card": generate transaction_id starting with "CC-"
        # For "paypal": generate transaction_id starting with "PP-"
        # For unknown methods: return (False, "")
        # Use uuid.uuid4().hex[:8].upper() for the random part of transaction_id
        raise NotImplementedError("Implement PaymentProcessor.charge()")


class EmailNotifier:
    """
    Responsibility: Send order confirmation notification to the customer.
    Reason to change: ONLY when notification logic or template changes.
    """

    def send_confirmation(self, order: dict[str, Any], final_total: float, transaction_id: str) -> bool:
        """
        Send a confirmation email to the customer.

        Args:
            order: Raw order dictionary (contains customer_email, order_id)
            final_total: The final charged amount
            transaction_id: The transaction ID from payment processing

        Returns:
            True if sent successfully
        """
        # TODO: Implement notification logic
        # Print: "[Email] Sending confirmation to {email}: Order {order_id}, Total: ${final_total:.2f}"
        # Return True
        raise NotImplementedError("Implement EmailNotifier.send_confirmation()")


class InventoryUpdater:
    """
    Responsibility: Update stock levels after a successful order.
    Reason to change: ONLY when inventory system or update logic changes.
    """

    def __init__(self, inventory: dict[str, int]) -> None:
        """
        Args:
            inventory: A reference to the inventory dict {product_id: stock_count}
        """
        self.inventory = inventory

    def update(self, order: dict[str, Any]) -> bool:
        """
        Decrement inventory for each ordered item.

        Args:
            order: Raw order dictionary (contains items list)

        Returns:
            True if all items were updated successfully
        """
        # TODO: Implement inventory update logic
        # For each item in order["items"]:
        #   If product_id in self.inventory, decrement by quantity
        #   Print: "[Inventory] {product_id}: stock updated to {new_stock}"
        # Return True
        raise NotImplementedError("Implement InventoryUpdater.update()")


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
        Process an order end-to-end.

        Workflow:
        1. Validate the order → if invalid, return early with errors
        2. Calculate discount
        3. Calculate final total (subtotal - discount)
        4. Charge payment → if fails, return error
        5. Send confirmation email
        6. Update inventory
        7. Return success result

        Args:
            order: Raw order dictionary

        Returns:
            Dict with keys: success (bool), transaction_id (str|None),
                           discount (float), errors (list[str])
        """
        # TODO: Implement the orchestration workflow
        # Step 1: Use self.validator.validate(order)
        # Step 2: Use self.discount_calculator.calculate(order)
        # Step 3: Calculate subtotal and final_total = subtotal - discount
        # Step 4: Use self.payment_processor.charge(order, final_total)
        # Step 5: Use self.email_notifier.send_confirmation(order, final_total, transaction_id)
        # Step 6: Use self.inventory_updater.update(order)
        # Step 7: Return result dict
        raise NotImplementedError("Implement OrderService.process_order()")


# =============================================================================
# QUICK MANUAL TEST (run this file directly to check your work)
# =============================================================================

if __name__ == "__main__":
    # Sample inventory
    inventory = {"P001": 100, "P002": 50, "P003": 25}

    # Wire up all components
    service = OrderService(
        validator=OrderValidator(),
        discount_calculator=DiscountCalculator(),
        payment_processor=PaymentProcessor(),
        email_notifier=EmailNotifier(),
        inventory_updater=InventoryUpdater(inventory),
    )

    # Valid order
    order = {
        "order_id": "ORD-001",
        "customer_email": "customer@example.com",
        "membership": "gold",
        "payment_method": "credit_card",
        "coupon_code": "SAVE10",
        "items": [
            {"product_id": "P001", "name": "Widget A", "quantity": 2, "unit_price": 25.00},
            {"product_id": "P002", "name": "Widget B", "quantity": 1, "unit_price": 50.00},
        ],
    }

    print("Processing order...")
    result = service.process_order(order)
    print(f"Result: {result}")
    print(f"Updated inventory: {inventory}")
