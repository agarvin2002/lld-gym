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
        # In reality: call payment gateway API
        print(f"Charging ${amount:.2f} to card ending in {self._card}")
        return PaymentResult(True, "Approved", f"CC-{self._card}-{int(amount)}")

    def get_name(self) -> str:
        return f"Credit Card (****{self._card})"


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str) -> None:
        self._email = email

    def pay(self, amount: float) -> PaymentResult:
        print(f"PayPal: charging ${amount:.2f} to {self._email}")
        return PaymentResult(True, "PayPal approved", f"PP-{hash(self._email)}")

    def get_name(self) -> str:
        return f"PayPal ({self._email})"


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str) -> None:
        self._wallet = wallet_address[:8] + "..."

    def pay(self, amount: float) -> PaymentResult:
        print(f"Crypto: sending ${amount:.2f} worth to {self._wallet}")
        return PaymentResult(True, "Transaction broadcast", f"CRYPTO-{self._wallet}")

    def get_name(self) -> str:
        return f"Crypto ({self._wallet})"


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
        print(f"\nCart total: ${total:.2f}")
        print(f"Paying with: {self._payment.get_name()}")
        return self._payment.pay(total)


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99)

    # Pay with credit card
    cart.set_payment_strategy(CreditCardPayment("4111111111111234", "123"))
    result = cart.checkout()
    print(f"Result: {result.message} (ID: {result.transaction_id})\n")

    # Switch to PayPal — zero changes to cart
    cart.set_payment_strategy(PayPalPayment("user@example.com"))
    result = cart.checkout()
    print(f"Result: {result.message}\n")
