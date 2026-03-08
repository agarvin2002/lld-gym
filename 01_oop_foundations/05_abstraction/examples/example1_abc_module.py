"""
example1_abc_module.py
----------------------
Shows how to use ABC (Abstract Base Class) to define an interface.

We build a payment gateway. Different companies (Razorpay, Paytm) implement
the same interface. The order processing code only talks to the interface —
it doesn't care which company is used.

Real-world use: this pattern is the foundation of clean system design.
  Parking lot:  ABC ParkingSpot → CarSpot, BikeSpot, TruckSpot
  ATM system:   ABC ATMState    → IdleState, CardInsertedState, PinEnteredState
  Hotel system: ABC Room        → SingleRoom, DoubleRoom, Suite

Run this file directly:
    python3 example1_abc_module.py
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Supporting types
# ---------------------------------------------------------------------------

class TransactionStatus(Enum):
    SUCCESS = "success"
    FAILED  = "failed"


@dataclass
class Transaction:
    """A record of one payment."""
    transaction_id: str
    amount: float
    status: TransactionStatus


# ---------------------------------------------------------------------------
# The abstract interface — defines WHAT a payment gateway must do
# ---------------------------------------------------------------------------

class PaymentGateway(ABC):
    """
    Abstract interface for all payment gateways.

    This defines WHAT every gateway must support.
    Subclasses define HOW each one does it.

    You cannot create PaymentGateway() directly — Python will raise TypeError.
    """

    @abstractmethod
    def charge(self, amount: float, description: str = "") -> Transaction:
        """
        Charge the customer.
        Returns a Transaction with status SUCCESS or FAILED.
        """
        ...

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """
        Refund a previous charge. Returns True if successful.
        """
        ...

    def generate_transaction_id(self) -> str:
        """Create a unique ID. This is a shared helper — all gateways inherit it."""
        return str(uuid.uuid4())

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


# ---------------------------------------------------------------------------
# Implementation 1: Razorpay
# ---------------------------------------------------------------------------

class RazorpayGateway(PaymentGateway):
    """Simulated Razorpay gateway. In production, this would call Razorpay's API."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._transactions: dict[str, Transaction] = {}

    def charge(self, amount: float, description: str = "") -> Transaction:
        txn_id = "RZP-" + self.generate_transaction_id()[:8]
        # Simulate: always succeeds for this demo
        txn = Transaction(txn_id, amount, TransactionStatus.SUCCESS)
        self._transactions[txn_id] = txn
        print(f"  [Razorpay] Charged ₹{amount:.2f} → {txn.status.value} (id: {txn_id})")
        return txn

    def refund(self, transaction_id: str) -> bool:
        if transaction_id not in self._transactions:
            print(f"  [Razorpay] Transaction {transaction_id} not found")
            return False
        print(f"  [Razorpay] Refunded transaction {transaction_id}")
        return True


# ---------------------------------------------------------------------------
# Implementation 2: Paytm
# ---------------------------------------------------------------------------

class PaytmGateway(PaymentGateway):
    """Simulated Paytm gateway. Same interface, different implementation."""

    def __init__(self, merchant_id: str) -> None:
        self._merchant_id = merchant_id
        self._transactions: dict[str, Transaction] = {}

    def charge(self, amount: float, description: str = "") -> Transaction:
        txn_id = "PTM-" + self.generate_transaction_id()[:8]
        txn = Transaction(txn_id, amount, TransactionStatus.SUCCESS)
        self._transactions[txn_id] = txn
        print(f"  [Paytm]    Charged ₹{amount:.2f} → {txn.status.value} (id: {txn_id})")
        return txn

    def refund(self, transaction_id: str) -> bool:
        if transaction_id not in self._transactions:
            print(f"  [Paytm] Transaction {transaction_id} not found")
            return False
        print(f"  [Paytm] Refunded transaction {transaction_id}")
        return True


# ---------------------------------------------------------------------------
# Business logic — depends ONLY on PaymentGateway, not on Razorpay or Paytm
# ---------------------------------------------------------------------------

@dataclass
class OrderProcessor:
    """
    Processes orders using any payment gateway.

    TIP: This class only imports PaymentGateway (the abstract class).
    The specific gateway (Razorpay, Paytm, etc.) is passed in from outside.
    This is called "Dependency Injection" — you inject the dependency.

    To switch payment providers: change ONE line at the injection site.
    """

    gateway: PaymentGateway

    def process_order(self, order_id: str, amount: float) -> dict:
        """Charge the customer and return a result summary."""
        print(f"\nProcessing order {order_id} for ₹{amount:.2f} via {self.gateway!r}")
        txn = self.gateway.charge(amount, description=f"Order {order_id}")

        if txn.status == TransactionStatus.SUCCESS:
            return {"order_id": order_id, "success": True, "txn_id": txn.transaction_id}
        else:
            return {"order_id": order_id, "success": False}

    def refund_order(self, transaction_id: str) -> bool:
        """Refund a previous order."""
        print(f"\nRefunding transaction {transaction_id} via {self.gateway!r}")
        return self.gateway.refund(transaction_id)


# ---------------------------------------------------------------------------
# RUN THIS TO SEE IT IN ACTION
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # --- Part 1: Cannot create abstract class directly ---
    print("=== Part 1: Cannot create PaymentGateway directly ===\n")
    try:
        gateway = PaymentGateway()   # type: ignore
    except TypeError as e:
        print(f"Error: {e}")

    # --- Part 2: Use Razorpay ---
    print("\n=== Part 2: OrderProcessor with Razorpay ===")
    rzp = RazorpayGateway(api_key="rzp_test_fake_key")
    processor = OrderProcessor(gateway=rzp)

    result = processor.process_order("ORD-001", 599.0)
    print(f"Result: {result}")

    if result["success"]:
        processor.refund_order(result["txn_id"])

    # --- Part 3: Switch to Paytm — OrderProcessor code does NOT change ---
    print("\n=== Part 3: Same OrderProcessor, now with Paytm ===")
    ptm = PaytmGateway(merchant_id="MERCHANT_FAKE")
    processor2 = OrderProcessor(gateway=ptm)   # one line change — that's all!

    result2 = processor2.process_order("ORD-002", 299.0)
    print(f"Result: {result2}")

    print("\nKey takeaway:")
    print("  OrderProcessor.process_order() never changed.")
    print("  To switch from Razorpay to Paytm: change ONE line.")
