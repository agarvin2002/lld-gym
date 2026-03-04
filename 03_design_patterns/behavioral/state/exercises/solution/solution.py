"""State Pattern Exercise — Vending Machine Reference Solution."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class VendingMachineState(Enum):
    IDLE = "IDLE"
    HAS_MONEY = "HAS_MONEY"
    DISPENSING = "DISPENSING"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class InvalidStateError(Exception):
    pass


@dataclass
class Product:
    name: str
    price: float
    quantity: int


class VendingMachine:
    def __init__(self, products: dict[str, tuple[str, float, int]]) -> None:
        self._products: dict[str, Product] = {
            code: Product(name, price, qty)
            for code, (name, price, qty) in products.items()
        }
        self._balance: float = 0.0
        self._selected: str | None = None
        self.state = VendingMachineState.IDLE
        self._check_out_of_stock()

    def _require_state(self, *states: VendingMachineState) -> None:
        if self.state not in states:
            allowed = ", ".join(s.value for s in states)
            raise InvalidStateError(
                f"Operation requires state {allowed}, current state is {self.state.value}"
            )

    def _check_out_of_stock(self) -> None:
        if all(p.quantity == 0 for p in self._products.values()):
            self.state = VendingMachineState.OUT_OF_STOCK

    def insert_coin(self, amount: float) -> None:
        self._require_state(VendingMachineState.IDLE, VendingMachineState.HAS_MONEY)
        self._balance += amount
        self.state = VendingMachineState.HAS_MONEY

    def select_product(self, code: str) -> str:
        self._require_state(VendingMachineState.HAS_MONEY)
        if code not in self._products:
            raise ValueError(f"Unknown product code: {code!r}")
        product = self._products[code]
        if product.quantity == 0:
            raise ValueError(f"Product {code!r} is out of stock")
        if self._balance < product.price:
            raise ValueError(
                f"Insufficient balance: have ${self._balance:.2f}, need ${product.price:.2f}"
            )
        self._selected = code
        self.state = VendingMachineState.DISPENSING
        return product.name

    def dispense(self) -> str:
        self._require_state(VendingMachineState.DISPENSING)
        product = self._products[self._selected]
        self._balance -= product.price
        product.quantity -= 1
        name = product.name
        self._selected = None
        self.state = VendingMachineState.IDLE
        self._check_out_of_stock()
        return name

    def refund(self) -> float:
        self._require_state(VendingMachineState.HAS_MONEY)
        amount = self._balance
        self._balance = 0.0
        self.state = VendingMachineState.IDLE
        return amount

    def restock(self, code: str, quantity: int) -> None:
        if code not in self._products:
            raise ValueError(f"Unknown product code: {code!r}")
        self._products[code].quantity += quantity
        if self.state == VendingMachineState.OUT_OF_STOCK:
            self.state = VendingMachineState.IDLE

    @property
    def balance(self) -> float:
        return self._balance
