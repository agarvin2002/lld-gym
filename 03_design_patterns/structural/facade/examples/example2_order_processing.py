"""
Facade Pattern — Example 2: E-Commerce Order Processing

An e-commerce order touches five independent backend services:
  1. InventoryService  — check stock and reserve units
  2. PaymentGateway    — charge the customer's card
  3. ShippingService   — create a shipping label and schedule pickup
  4. NotificationService — send a confirmation email
  5. AuditLogger       — record the event for compliance

Without a Facade, every entry point in the application (web controller,
mobile API, batch job) must orchestrate all five services in the right order.
The OrderFacade encapsulates that sequence behind a single `place_order` call.
"""

from __future__ import annotations

import uuid
from datetime import datetime


# ---------------------------------------------------------------------------
# Subsystem classes
# ---------------------------------------------------------------------------

class InventoryService:
    """Tracks stock levels and reserves units for an order."""

    def __init__(self) -> None:
        # Seed some stock for the demo
        self._stock: dict[str, int] = {
            "SKU-001": 50,
            "SKU-002": 3,
            "SKU-999": 0,  # out of stock
        }

    def check_stock(self, sku: str) -> bool:
        available = self._stock.get(sku, 0)
        in_stock = available > 0
        print(f"[Inventory] Stock check for {sku}: {'available' if in_stock else 'OUT OF STOCK'} ({available} units).")
        return in_stock

    def reserve(self, sku: str, qty: int) -> None:
        self._stock[sku] = self._stock.get(sku, 0) - qty
        print(f"[Inventory] Reserved {qty} unit(s) of {sku}. Remaining: {self._stock[sku]}.")


class PaymentGateway:
    """Processes card payments and returns a receipt ID."""

    def charge(self, amount: float, card_token: str) -> str:
        receipt = f"RCPT-{uuid.uuid4().hex[:8].upper()}"
        print(f"[Payment] Charged ${amount:.2f} to card ending in ...{card_token[-4:]}. Receipt: {receipt}.")
        return receipt


class ShippingService:
    """Creates shipping labels and schedules carrier pickup."""

    def create_label(self, address: str) -> str:
        label = f"SHIP-{uuid.uuid4().hex[:10].upper()}"
        print(f"[Shipping] Label {label} created for: {address}.")
        return label

    def schedule_pickup(self, label: str) -> None:
        pickup_time = "tomorrow between 9am–1pm"
        print(f"[Shipping] Pickup scheduled for label {label}: {pickup_time}.")


class NotificationService:
    """Sends transactional emails."""

    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"[Notification] Email sent to {to} | Subject: '{subject}'.")
        # (body is not printed to keep the output concise)


class AuditLogger:
    """Appends immutable audit records for compliance."""

    def log(self, event: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[Audit] {timestamp} — {event}")


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

class OrderFacade:
    """
    Single entry point for placing an order.

    Orchestrates: inventory check -> payment -> shipping -> notification -> audit.
    Raises ValueError if the item is out of stock (before charging the customer).
    """

    def __init__(
        self,
        inventory: InventoryService,
        payment: PaymentGateway,
        shipping: ShippingService,
        notification: NotificationService,
        audit: AuditLogger,
    ) -> None:
        self._inventory = inventory
        self._payment = payment
        self._shipping = shipping
        self._notification = notification
        self._audit = audit

    def place_order(
        self,
        sku: str,
        qty: int,
        amount: float,
        card_token: str,
        address: str,
        email: str,
    ) -> dict:
        """
        Place a complete order.

        Returns:
            dict with keys: success (bool), receipt (str), label (str)

        Raises:
            ValueError: if the SKU is out of stock.
        """
        print(f"\n=== Placing order: {qty}x {sku} ===")

        # 1. Check and reserve inventory (fail fast before touching payment)
        if not self._inventory.check_stock(sku):
            self._audit.log(f"Order FAILED — {sku} out of stock.")
            raise ValueError(f"SKU '{sku}' is out of stock.")
        self._inventory.reserve(sku, qty)

        # 2. Charge payment
        receipt = self._payment.charge(amount, card_token)

        # 3. Create shipping label and schedule pickup
        label = self._shipping.create_label(address)
        self._shipping.schedule_pickup(label)

        # 4. Notify customer
        self._notification.send_email(
            to=email,
            subject="Your order is confirmed!",
            body=f"Order for {sku} confirmed. Receipt: {receipt}. Label: {label}.",
        )

        # 5. Audit log
        self._audit.log(f"Order SUCCESS — SKU={sku} qty={qty} receipt={receipt} label={label}.")

        print("=== Order complete ===\n")
        return {"success": True, "receipt": receipt, "label": label}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Wire up subsystems
    inventory = InventoryService()
    payment = PaymentGateway()
    shipping = ShippingService()
    notification = NotificationService()
    audit = AuditLogger()

    facade = OrderFacade(inventory, payment, shipping, notification, audit)

    # Scenario 1: Successful order
    result = facade.place_order(
        sku="SKU-001",
        qty=2,
        amount=49.99,
        card_token="tok_visa_4242424242424242",
        address="42 Elm Street, Springfield, IL 62701",
        email="alice@example.com",
    )
    print(f"Result: {result}\n")

    # Scenario 2: Out-of-stock order
    try:
        facade.place_order(
            sku="SKU-999",
            qty=1,
            amount=19.99,
            card_token="tok_visa_1111111111111111",
            address="7 Oak Ave, Portland, OR 97201",
            email="bob@example.com",
        )
    except ValueError as exc:
        print(f"Order rejected: {exc}\n")
