# Advanced topic — shows how a Facade coordinates multiple backend services in the correct order, with fail-fast error handling before payment is charged.
"""
Facade Pattern — Example 2: E-Commerce Order Processing

An order on Flipkart/Amazon touches five backend services in sequence.
The OrderFacade exposes one method — place_order — so every entry point
(web, mobile, batch) shares the same workflow.
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
        self._stock: dict[str, int] = {
            "SKU-001": 50,
            "SKU-002": 3,
            "SKU-999": 0,  # out of stock
        }

    def check_stock(self, sku: str) -> bool:
        available = self._stock.get(sku, 0)
        in_stock = available > 0
        print(f"[Inventory] {sku}: {'available' if in_stock else 'OUT OF STOCK'} ({available} units).")
        return in_stock

    def reserve(self, sku: str, qty: int) -> None:
        self._stock[sku] = self._stock.get(sku, 0) - qty
        print(f"[Inventory] Reserved {qty}x {sku}. Remaining: {self._stock[sku]}.")


class PaymentGateway:
    """Processes card payments and returns a receipt ID."""

    def charge(self, amount: float, card_token: str) -> str:
        receipt = f"RCPT-{uuid.uuid4().hex[:8].upper()}"
        print(f"[Payment] Charged ₹{amount:.2f} to card ...{card_token[-4:]}. Receipt: {receipt}.")
        return receipt


class ShippingService:
    """Creates shipping labels and schedules carrier pickup."""

    def create_label(self, address: str) -> str:
        label = f"SHIP-{uuid.uuid4().hex[:10].upper()}"
        print(f"[Shipping] Label {label} created for: {address}.")
        return label

    def schedule_pickup(self, label: str) -> None:
        print(f"[Shipping] Pickup scheduled for {label}: tomorrow 9am–1pm.")


class NotificationService:
    """Sends transactional emails."""

    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"[Notification] Email → {to} | '{subject}'.")


class AuditLogger:
    """Appends immutable audit records for compliance."""

    def log(self, event: str) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[Audit] {ts} — {event}")


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

class OrderFacade:
    """
    Single entry point for placing an order.

    Sequence: inventory check → payment → shipping → notification → audit.
    Raises ValueError if the item is out of stock (before charging the card).
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
        """Place a complete order. Returns dict with success, receipt, label."""
        print(f"\n=== Placing order: {qty}x {sku} ===")

        # Fail fast before touching payment
        if not self._inventory.check_stock(sku):
            self._audit.log(f"Order FAILED — {sku} out of stock.")
            raise ValueError(f"SKU '{sku}' is out of stock.")
        self._inventory.reserve(sku, qty)

        receipt = self._payment.charge(amount, card_token)
        label = self._shipping.create_label(address)
        self._shipping.schedule_pickup(label)
        self._notification.send_email(email, "Your order is confirmed!", f"Receipt: {receipt}.")
        self._audit.log(f"Order SUCCESS — SKU={sku} receipt={receipt} label={label}.")

        print("=== Order complete ===\n")
        return {"success": True, "receipt": receipt, "label": label}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    facade = OrderFacade(
        InventoryService(), PaymentGateway(), ShippingService(),
        NotificationService(), AuditLogger(),
    )

    # Successful order
    result = facade.place_order(
        sku="SKU-001", qty=2, amount=499.00,
        card_token="tok_4242424242424242",
        address="42 MG Road, Bengaluru 560001",
        email="alice@example.com",
    )
    print(f"Result: {result}\n")

    # Out-of-stock order
    try:
        facade.place_order(
            sku="SKU-999", qty=1, amount=199.00,
            card_token="tok_1111111111111111",
            address="7 Park Street, Mumbai 400001",
            email="bob@example.com",
        )
    except ValueError as exc:
        print(f"Order rejected: {exc}\n")
