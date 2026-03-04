"""Solution: LSP Payment Hierarchy"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid


@dataclass
class TransactionResult:
    success: bool
    transaction_id: str
    amount: float
    message: str = ""


class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> TransactionResult: ...

    @abstractmethod
    def get_payment_type(self) -> str: ...


class RefundablePayment(PaymentMethod, ABC):
    @abstractmethod
    def refund(self, transaction_id: str) -> bool: ...


class CreditCard(RefundablePayment):
    def __init__(self, card_number: str, holder_name: str) -> None:
        self.card_number = card_number
        self.holder_name = holder_name

    def process(self, amount: float) -> TransactionResult:
        tid = f"CC-{amount}-{uuid.uuid4().hex[:6]}"
        return TransactionResult(success=True, transaction_id=tid, amount=amount)

    def refund(self, transaction_id: str) -> bool:
        return True

    def get_payment_type(self) -> str:
        return "CreditCard"


class DebitCard(RefundablePayment):
    def __init__(self, card_number: str) -> None:
        self.card_number = card_number

    def process(self, amount: float) -> TransactionResult:
        tid = f"DC-{amount}-{uuid.uuid4().hex[:6]}"
        return TransactionResult(success=True, transaction_id=tid, amount=amount)

    def refund(self, transaction_id: str) -> bool:
        return True

    def get_payment_type(self) -> str:
        return "DebitCard"


class GiftCard(PaymentMethod):
    def __init__(self, card_code: str, balance: float) -> None:
        self.card_code = card_code
        self.balance = balance

    def process(self, amount: float) -> TransactionResult:
        if self.balance >= amount:
            self.balance -= amount
            tid = f"GC-{amount}-{uuid.uuid4().hex[:6]}"
            return TransactionResult(success=True, transaction_id=tid, amount=amount)
        return TransactionResult(
            success=False, transaction_id="", amount=amount,
            message=f"Insufficient balance: {self.balance:.2f}"
        )

    def get_payment_type(self) -> str:
        return "GiftCard"
