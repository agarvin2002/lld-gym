"""
WHAT YOU'RE BUILDING
====================
A payment hierarchy where every payment type is a safe substitute
for the base PaymentMethod interface.

The key design decision: GiftCard can process payments but CANNOT
be refunded. So GiftCard inherits PaymentMethod only — not RefundablePayment.
This is LSP: never inherit an interface you cannot fully honor.

CreditCard and DebitCard both support refunds, so they inherit
from RefundablePayment (which extends PaymentMethod).

Fill in the TODOs below. Run the tests to verify your work.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TransactionResult:
    success: bool
    transaction_id: str
    amount: float
    message: str = ""


class PaymentMethod(ABC):
    """
    Base interface — ALL payment methods can process a payment.
    Not all payment methods support refunds (see RefundablePayment).
    """

    @abstractmethod
    def process(self, amount: float) -> TransactionResult:
        """Charge the given amount. Return TransactionResult with success=True on success."""
        ...

    @abstractmethod
    def get_payment_type(self) -> str:
        """Return a human-readable name for this payment type (e.g. 'CreditCard')."""
        ...


class RefundablePayment(PaymentMethod, ABC):
    """
    Extended interface for payment methods that support refunds.
    Only inherit from this if refunds are genuinely supported.
    """

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a previous transaction. Return True if successful."""
        ...


class CreditCard(RefundablePayment):
    """Credit card supports both payment and refunds."""

    def __init__(self, card_number: str, holder_name: str) -> None:
        # TODO: Store card_number as self.card_number and holder_name as self.holder_name
        pass

    def process(self, amount: float) -> TransactionResult:
        # TODO: Return TransactionResult(success=True, transaction_id=f"CC-{amount}", amount=amount)
        pass

    def refund(self, transaction_id: str) -> bool:
        # TODO: Return True (simulate a successful refund)
        pass

    def get_payment_type(self) -> str:
        # TODO: Return "CreditCard"
        pass


class DebitCard(RefundablePayment):
    """Debit card supports both payment and refunds."""

    def __init__(self, card_number: str) -> None:
        # TODO: Store card_number as self.card_number
        pass

    def process(self, amount: float) -> TransactionResult:
        # TODO: Return TransactionResult(success=True, transaction_id=f"DC-{amount}", amount=amount)
        pass

    def refund(self, transaction_id: str) -> bool:
        # TODO: Return True
        pass

    def get_payment_type(self) -> str:
        # TODO: Return "DebitCard"
        pass


class GiftCard(PaymentMethod):
    """
    Gift card can process payments but CANNOT be refunded.
    Correctly inherits PaymentMethod only — NOT RefundablePayment.
    This is the LSP-compliant design: don't inherit what you can't honor.
    """

    def __init__(self, card_code: str, balance: float) -> None:
        # TODO: Store card_code as self.card_code and balance as self.balance
        pass

    def process(self, amount: float) -> TransactionResult:
        # TODO: Check if self.balance >= amount
        #   If yes: subtract amount from self.balance, return success TransactionResult
        #           transaction_id=f"GC-{amount}", amount=amount
        #   If no:  return TransactionResult(success=False, transaction_id="", amount=amount,
        #                                    message="Insufficient balance")
        # HINT: This is the only class that needs balance-checking logic.
        pass

    def get_payment_type(self) -> str:
        # TODO: Return "GiftCard"
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/03_liskov_substitution/exercises/tests.py -v
#
# Run all SOLID exercises at once:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/ -v
# =============================================================================
