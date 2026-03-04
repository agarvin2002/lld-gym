"""
Example 1: Abstraction with abc.ABC
=====================================

This example demonstrates Python's abc module for defining enforced abstract
interfaces. We build a payment gateway abstraction with multiple concrete
implementations.

Key ideas demonstrated:
- PaymentGateway(ABC) as an enforced interface
- Abstract methods: charge(), refund(), get_transaction_status()
- Abstract property: currency_code
- Attempting to instantiate ABC raises TypeError
- Code depending on PaymentGateway works with any implementation
- Dependency injection: passing the gateway in rather than creating it inside
"""

from __future__ import annotations

import random
import string
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Supporting types
# ---------------------------------------------------------------------------

class TransactionStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


@dataclass
class Transaction:
    """Record of a payment transaction."""
    transaction_id: str
    amount: float
    currency: str
    status: TransactionStatus
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


@dataclass
class RefundResult:
    success: bool
    refund_id: Optional[str] = None
    error_message: Optional[str] = None


# ---------------------------------------------------------------------------
# Abstract base class — defines the interface
# ---------------------------------------------------------------------------

class PaymentGateway(ABC):
    """
    Abstract interface for payment gateways.

    This class defines WHAT a payment gateway must do.
    Concrete subclasses define HOW each gateway does it.

    Business logic (OrderProcessor, etc.) depends only on this class.
    It never imports StripeGateway or PayPalGateway directly.

    Abstract members:
    - charge()                   → initiate a payment
    - refund()                   → reverse a payment
    - get_transaction_status()   → query a transaction
    - currency_code (property)   → the primary currency supported
    """

    @property
    @abstractmethod
    def currency_code(self) -> str:
        """
        The primary currency this gateway operates in.

        Subclasses MUST define this as a property.
        Note: abc.abstractproperty is deprecated — use @property + @abstractmethod.
        """
        ...

    @abstractmethod
    def charge(self, amount: float, description: str = "") -> Transaction:
        """
        Charge the customer.

        Args:
            amount:      The amount to charge (in the gateway's currency).
            description: Human-readable description of the charge.

        Returns:
            A Transaction record with status SUCCESS or FAILED.
        """
        ...

    @abstractmethod
    def refund(self, transaction_id: str, amount: Optional[float] = None) -> RefundResult:
        """
        Refund a previous transaction.

        Args:
            transaction_id: The ID returned by charge().
            amount:         Amount to refund. If None, refunds the full amount.

        Returns:
            RefundResult indicating success or failure.
        """
        ...

    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> TransactionStatus:
        """
        Query the current status of a transaction.

        Args:
            transaction_id: The ID returned by charge().

        Returns:
            Current TransactionStatus.
        """
        ...

    # Concrete method on the ABC — shared by all implementations
    def generate_transaction_id(self) -> str:
        """
        Generate a unique transaction ID.

        This is a concrete helper method on the abstract class — subclasses
        inherit it and can use it or override it. It is NOT abstract.
        """
        return str(uuid.uuid4())

    def __repr__(self) -> str:
        return f"{type(self).__name__}(currency={self.currency_code})"


# ---------------------------------------------------------------------------
# Concrete Implementation 1: Stripe
# ---------------------------------------------------------------------------

class StripeGateway(PaymentGateway):
    """
    Simulated Stripe payment gateway.

    In production this would call stripe.PaymentIntent.create(), etc.
    Here we simulate with in-memory storage and 90% success rate.
    """

    def __init__(self, api_key: str, success_rate: float = 0.9) -> None:
        self._api_key = api_key
        self._success_rate = success_rate
        self._transactions: dict[str, Transaction] = {}

    @property
    def currency_code(self) -> str:
        return "USD"

    def charge(self, amount: float, description: str = "") -> Transaction:
        txn_id = self.generate_transaction_id()
        # Simulate network call
        success = random.random() < self._success_rate
        status = TransactionStatus.SUCCESS if success else TransactionStatus.FAILED

        txn = Transaction(
            transaction_id=txn_id,
            amount=amount,
            currency=self.currency_code,
            status=status,
            metadata={"gateway": "stripe", "description": description},
        )
        self._transactions[txn_id] = txn
        print(f"  [Stripe] charge ${amount:.2f} → {status.value} (txn: {txn_id[:8]}...)")
        return txn

    def refund(self, transaction_id: str, amount: Optional[float] = None) -> RefundResult:
        if transaction_id not in self._transactions:
            return RefundResult(success=False, error_message="Transaction not found")

        txn = self._transactions[transaction_id]
        if txn.status != TransactionStatus.SUCCESS:
            return RefundResult(
                success=False,
                error_message=f"Cannot refund transaction in status: {txn.status.value}"
            )

        refund_amount = amount or txn.amount
        refund_id = "re_" + "".join(random.choices(string.ascii_lowercase, k=8))
        txn.status = TransactionStatus.REFUNDED
        print(f"  [Stripe] refund ${refund_amount:.2f} → {refund_id}")
        return RefundResult(success=True, refund_id=refund_id)

    def get_transaction_status(self, transaction_id: str) -> TransactionStatus:
        if transaction_id not in self._transactions:
            return TransactionStatus.FAILED
        return self._transactions[transaction_id].status


# ---------------------------------------------------------------------------
# Concrete Implementation 2: PayPal
# ---------------------------------------------------------------------------

class PayPalGateway(PaymentGateway):
    """
    Simulated PayPal payment gateway.

    Different implementation, same interface.
    In production this would call PayPal's REST API.
    """

    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._transactions: dict[str, Transaction] = {}

    @property
    def currency_code(self) -> str:
        return "USD"  # PayPal supports many; defaulting to USD

    def charge(self, amount: float, description: str = "") -> Transaction:
        # PayPal calls this an "order" + "capture"
        txn_id = "PAY-" + self.generate_transaction_id().upper()[:12]
        # Simulate slightly lower success rate (more fraud checks)
        success = random.random() < 0.85
        status = TransactionStatus.SUCCESS if success else TransactionStatus.FAILED

        txn = Transaction(
            transaction_id=txn_id,
            amount=amount,
            currency=self.currency_code,
            status=status,
            metadata={"gateway": "paypal", "order_description": description},
        )
        self._transactions[txn_id] = txn
        print(f"  [PayPal] capture ${amount:.2f} → {status.value} (order: {txn_id})")
        return txn

    def refund(self, transaction_id: str, amount: Optional[float] = None) -> RefundResult:
        if transaction_id not in self._transactions:
            return RefundResult(success=False, error_message="Order not found")

        txn = self._transactions[transaction_id]
        if txn.status != TransactionStatus.SUCCESS:
            return RefundResult(
                success=False,
                error_message=f"Cannot refund in status: {txn.status.value}"
            )

        refund_amount = amount or txn.amount
        refund_id = "REF-" + self.generate_transaction_id().upper()[:8]
        txn.status = TransactionStatus.REFUNDED
        print(f"  [PayPal] refund ${refund_amount:.2f} → {refund_id}")
        return RefundResult(success=True, refund_id=refund_id)

    def get_transaction_status(self, transaction_id: str) -> TransactionStatus:
        if transaction_id not in self._transactions:
            return TransactionStatus.PENDING
        return self._transactions[transaction_id].status


# ---------------------------------------------------------------------------
# Fake/Test Implementation — no real network calls
# ---------------------------------------------------------------------------

class FakePaymentGateway(PaymentGateway):
    """
    In-memory gateway for testing — always succeeds.

    This is a "test double". Because OrderProcessor depends on
    PaymentGateway (the abstraction), we can inject FakePaymentGateway
    in tests without touching the network.
    """

    def __init__(self) -> None:
        self._transactions: dict[str, Transaction] = {}

    @property
    def currency_code(self) -> str:
        return "USD"

    def charge(self, amount: float, description: str = "") -> Transaction:
        txn_id = "FAKE-" + self.generate_transaction_id()[:8]
        txn = Transaction(
            transaction_id=txn_id,
            amount=amount,
            currency=self.currency_code,
            status=TransactionStatus.SUCCESS,
        )
        self._transactions[txn_id] = txn
        print(f"  [Fake ] charge ${amount:.2f} → SUCCESS (txn: {txn_id})")
        return txn

    def refund(self, transaction_id: str, amount: Optional[float] = None) -> RefundResult:
        if transaction_id in self._transactions:
            self._transactions[transaction_id].status = TransactionStatus.REFUNDED
            return RefundResult(success=True, refund_id="FAKE-REFUND-001")
        return RefundResult(success=False, error_message="Not found")

    def get_transaction_status(self, transaction_id: str) -> TransactionStatus:
        return self._transactions.get(transaction_id, Transaction(
            transaction_id="", amount=0, currency="USD",
            status=TransactionStatus.FAILED
        )).status

    def get_all_transactions(self) -> list[Transaction]:
        return list(self._transactions.values())


# ---------------------------------------------------------------------------
# Business logic — depends only on the abstraction
# ---------------------------------------------------------------------------

@dataclass
class OrderProcessor:
    """
    Processes customer orders using any payment gateway.

    This class ONLY knows about PaymentGateway (the ABC).
    It does NOT import StripeGateway or PayPalGateway.
    The gateway is injected at construction time (dependency injection).

    This means:
    - Tests can inject FakePaymentGateway (fast, no network)
    - Production uses StripeGateway or PayPalGateway
    - Switching gateways requires changing ONE line (the injection site)
    """

    gateway: PaymentGateway

    def process_order(self, order_id: str, amount: float, description: str) -> dict:
        """Process a payment and return a result summary."""
        print(f"\nProcessing order {order_id} for ${amount:.2f}")
        print(f"Using gateway: {self.gateway!r}")

        txn = self.gateway.charge(amount, description)

        if txn.status == TransactionStatus.SUCCESS:
            return {
                "order_id": order_id,
                "success": True,
                "transaction_id": txn.transaction_id,
                "amount_charged": txn.amount,
                "currency": txn.currency,
            }
        else:
            return {
                "order_id": order_id,
                "success": False,
                "error": "Payment declined",
            }

    def process_refund(self, transaction_id: str, amount: Optional[float] = None) -> dict:
        """Process a refund for an existing transaction."""
        print(f"\nProcessing refund for txn {transaction_id[:16]}...")
        result = self.gateway.refund(transaction_id, amount)
        return {
            "success": result.success,
            "refund_id": result.refund_id,
            "error": result.error_message,
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: Abstraction with abc.ABC — Payment Gateway")
    print("=" * 60)

    # --- Part 1: Cannot instantiate the ABC ---
    print("\n[Part 1] Attempting to instantiate PaymentGateway (ABC)")
    print("-" * 50)
    try:
        gateway = PaymentGateway()  # type: ignore[abstract]
        print("ERROR: Should have raised TypeError!")
    except TypeError as e:
        print(f"Correctly raised TypeError: {e}")

    # --- Part 2: Stripe gateway ---
    print("\n[Part 2] OrderProcessor with StripeGateway")
    print("-" * 50)
    stripe = StripeGateway(api_key="sk_test_fake_key")
    processor = OrderProcessor(gateway=stripe)

    result = processor.process_order("ORD-001", 99.99, "Premium subscription")
    print(f"Result: {result}")

    if result["success"]:
        refund_result = processor.process_refund(result["transaction_id"])
        print(f"Refund: {refund_result}")

    # --- Part 3: Same OrderProcessor, different gateway ---
    print("\n[Part 3] Same OrderProcessor switched to PayPalGateway")
    print("-" * 50)
    paypal = PayPalGateway(client_id="client_fake", client_secret="secret_fake")
    processor2 = OrderProcessor(gateway=paypal)

    result2 = processor2.process_order("ORD-002", 49.50, "E-book purchase")
    print(f"Result: {result2}")

    # --- Part 4: Test with FakePaymentGateway ---
    print("\n[Part 4] Testing with FakePaymentGateway (no network)")
    print("-" * 50)
    fake = FakePaymentGateway()
    test_processor = OrderProcessor(gateway=fake)

    test_result = test_processor.process_order("TEST-001", 25.00, "Test charge")
    print(f"Test result: {test_result}")
    print(f"All fake transactions: {[t.transaction_id for t in fake.get_all_transactions()]}")

    # --- Part 5: Abstract property demo ---
    print("\n[Part 5] Abstract property: currency_code")
    print("-" * 50)
    gateways: list[PaymentGateway] = [stripe, paypal, fake]
    for gw in gateways:
        print(f"  {type(gw).__name__:20} currency_code = {gw.currency_code}")

    # --- Part 6: Concrete method inherited from ABC ---
    print("\n[Part 6] Concrete method on ABC: generate_transaction_id()")
    print("-" * 50)
    print(f"Stripe txn ID: {stripe.generate_transaction_id()}")
    print(f"PayPal txn ID: {paypal.generate_transaction_id()}")
    print("Both use the same inherited implementation from PaymentGateway")

    print("\n--- End of demo ---")
    print("\nKey takeaway: OrderProcessor.process_order() never changes.")
    print("Swap the gateway by changing ONE line at the injection site.")
