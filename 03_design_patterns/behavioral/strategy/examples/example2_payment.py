# Advanced topic — injecting payment strategies into a shopping cart so the cart never needs to change when a new method is added
"""
Strategy Pattern — Example 2: Payment Processing
=================================================
A checkout system supports multiple payment methods.
Each method is a strategy — the cart doesn't care which one is used.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    message: str
    transaction_id: str = ""


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResult: ...

    @abstractmethod
    def get_name(self) -> str: ...


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str) -> None:
        self._card = card_number[-4:]   # store only last 4 digits
        self._cvv = cvv

    def pay(self, amount: float) -> PaymentResult:
        print(f"Charging ₹{amount:.2f} to card ending in {self._card}")
        return PaymentResult(True, "Approved", f"CC-{self._card}-{int(amount)}")

    def get_name(self) -> str:
        return f"Credit Card (****{self._card})"


class UPIPayment(PaymentStrategy):
    def __init__(self, vpa: str) -> None:
        self._vpa = vpa  # e.g. user@paytm

    def pay(self, amount: float) -> PaymentResult:
        print(f"UPI: collecting ₹{amount:.2f} from {self._vpa}")
        return PaymentResult(True, "UPI approved", f"UPI-{hash(self._vpa)}")

    def get_name(self) -> str:
        return f"UPI ({self._vpa})"


class NetBankingPayment(PaymentStrategy):
    def __init__(self, bank_code: str) -> None:
        self._bank = bank_code

    def pay(self, amount: float) -> PaymentResult:
        print(f"Net Banking [{self._bank}]: processing ₹{amount:.2f}")
        return PaymentResult(True, "Net Banking approved", f"NB-{self._bank}-{int(amount)}")

    def get_name(self) -> str:
        return f"Net Banking ({self._bank})"


class ShoppingCart:
    """Context — delegates payment to whatever strategy is set."""
    def __init__(self) -> None:
        self._items: list[tuple[str, float]] = []
        self._payment: PaymentStrategy | None = None

    def add_item(self, name: str, price: float) -> None:
        self._items.append((name, price))

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._payment = strategy

    def checkout(self) -> PaymentResult:
        if not self._payment:
            raise ValueError("No payment strategy set")
        total = sum(price for _, price in self._items)
        print(f"\nCart total: ₹{total:.2f}")
        print(f"Paying with: {self._payment.get_name()}")
        return self._payment.pay(total)


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item("Laptop", 55000.00)
    cart.add_item("Mouse", 1500.00)

    # Pay with credit card
    cart.set_payment_strategy(CreditCardPayment("4111111111111234", "123"))
    result = cart.checkout()
    print(f"Result: {result.message} (ID: {result.transaction_id})\n")

    # Switch to UPI — zero changes to cart
    cart.set_payment_strategy(UPIPayment("user@paytm"))
    result = cart.checkout()
    print(f"Result: {result.message}\n")
