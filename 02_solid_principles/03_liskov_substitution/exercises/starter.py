"""
Exercise: Payment Processing Hierarchy (LSP)

Design a payment hierarchy where every subtype is truly substitutable.
The tricky part: GiftCard cannot be refunded — design accordingly.

Fill in the TODOs. Run: pytest tests.py -v
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
    Note: NOT all payment methods support refunds (see RefundablePayment).
    """

    @abstractmethod
    def process(self, amount: float) -> TransactionResult:
        """
        Process a payment of the given amount.

        Args:
            amount: positive float representing amount to charge

        Returns:
            TransactionResult with success=True on success
        """
        ...

    @abstractmethod
    def get_payment_type(self) -> str:
        """Return a human-readable name for this payment type."""
        ...


class RefundablePayment(PaymentMethod, ABC):
    """
    Extended interface for payment methods that support refunds.
    Only inherit from this if refunds are genuinely supported.
    """

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """
        Refund a previous transaction.

        Returns:
            True if refund was successful, False otherwise
        """
        ...


class CreditCard(RefundablePayment):
    """Credit card supports both payment and refunds."""

    def __init__(self, card_number: str, holder_name: str) -> None:
        # TODO: store card_number, holder_name
        pass

    def process(self, amount: float) -> TransactionResult:
        # TODO: return TransactionResult(success=True, transaction_id="CC-{amount}", amount=amount)
        pass

    def refund(self, transaction_id: str) -> bool:
        # TODO: return True (simulate successful refund)
        pass

    def get_payment_type(self) -> str:
        # TODO: return "CreditCard"
        pass


class DebitCard(RefundablePayment):
    """Debit card supports both payment and refunds."""

    def __init__(self, card_number: str) -> None:
        # TODO: store card_number
        pass

    def process(self, amount: float) -> TransactionResult:
        # TODO: return TransactionResult(success=True, transaction_id="DC-{amount}", amount=amount)
        pass

    def refund(self, transaction_id: str) -> bool:
        # TODO: return True
        pass

    def get_payment_type(self) -> str:
        # TODO: return "DebitCard"
        pass


class GiftCard(PaymentMethod):
    """
    Gift card can process payments but CANNOT be refunded.
    Correctly inherits PaymentMethod only — NOT RefundablePayment.
    This is the LSP-compliant design.
    """

    def __init__(self, card_code: str, balance: float) -> None:
        # TODO: store card_code, balance
        pass

    def process(self, amount: float) -> TransactionResult:
        # TODO: check if balance >= amount
        # If yes: deduct from balance, return success TransactionResult
        # If no: return TransactionResult(success=False, ...)
        pass

    def get_payment_type(self) -> str:
        # TODO: return "GiftCard"
        pass
