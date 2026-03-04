"""Vending Machine — Reference Solution."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class InvalidStateError(Exception):
    pass


class VendingMachineState(Enum):
    IDLE             = auto()
    COIN_INSERTED    = auto()
    PRODUCT_SELECTED = auto()
    DISPENSING       = auto()


@dataclass
class Product:
    code: str
    name: str
    price: float
    quantity: int


class VendingMachine:
    def __init__(self, products: dict[str, tuple[str, float, int]]) -> None:
        self._products: dict[str, Product] = {
            code: Product(code=code, name=name, price=price, quantity=qty)
            for code, (name, price, qty) in products.items()
        }
        self._state = VendingMachineState.IDLE
        self._balance = 0.0
        self._selected: Product | None = None

    def _require_state(self, *allowed: VendingMachineState) -> None:
        if self._state not in allowed:
            raise InvalidStateError(
                f"Cannot perform this action in state {self._state.name}."
            )

    def insert_coin(self, amount: float) -> None:
        self._require_state(VendingMachineState.IDLE, VendingMachineState.COIN_INSERTED)
        self._balance += amount
        self._state = VendingMachineState.COIN_INSERTED

    def select_product(self, code: str) -> str:
        self._require_state(VendingMachineState.COIN_INSERTED)
        if code not in self._products:
            return f"Product {code!r} not found."
        product = self._products[code]
        if product.quantity == 0:
            return "Out of stock."
        if self._balance < product.price:
            return (
                f"Insufficient funds. "
                f"Price: ${product.price:.2f}, Balance: ${self._balance:.2f}"
            )
        self._selected = product
        self._state = VendingMachineState.PRODUCT_SELECTED
        return f"Selected: {product.name}. Please dispense."

    def dispense(self) -> str:
        self._require_state(VendingMachineState.PRODUCT_SELECTED)
        product = self._selected
        change = round(self._balance - product.price, 2)
        product.quantity -= 1
        self._balance = 0.0
        self._selected = None
        self._state = VendingMachineState.IDLE
        return f"Dispensed: {product.name}. Change: ${change:.2f}"

    def refund(self) -> float:
        self._require_state(
            VendingMachineState.COIN_INSERTED,
            VendingMachineState.PRODUCT_SELECTED,
        )
        amount = self._balance
        self._balance = 0.0
        self._selected = None
        self._state = VendingMachineState.IDLE
        return amount

    def restock(self, code: str, quantity: int) -> None:
        self._require_state(VendingMachineState.IDLE)
        if code not in self._products:
            raise ValueError(f"Unknown product code {code!r}.")
        self._products[code].quantity += quantity

    @property
    def current_state(self) -> VendingMachineState:
        return self._state

    @property
    def balance(self) -> float:
        return self._balance
