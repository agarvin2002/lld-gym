"""
Vending Machine — Starter File
=================================
Your task: Implement a vending machine with a state machine.

Read problem.md and design.md before starting.

Design decisions:
  - VendingMachineState Enum: IDLE → COIN_INSERTED → PRODUCT_SELECTED → DISPENSING → IDLE
  - _require_state() enforces valid states; raise InvalidStateError if violated
  - insert_coin() accumulates balance and transitions to COIN_INSERTED
    (can be called multiple times in COIN_INSERTED state to add more coins)
  - select_product() validates code, quantity, and funds; returns descriptive string
  - dispense() completes the transaction: deducts price, resets state, returns change message
  - refund() returns all inserted coins from COIN_INSERTED or PRODUCT_SELECTED state
  - restock() adds quantity to a product (only valid in IDLE state)
"""
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
        """Initialize the vending machine with a product catalog.

        Args:
            products: dict mapping product code → (name, price, quantity)

        TODO:
            - Build _products: dict[str, Product] from the input dict
              Hint: for code, (name, price, qty) in products.items()
            - Set _state = VendingMachineState.IDLE
            - Set _balance = 0.0
            - Set _selected: Product | None = None
        """
        pass

    def _require_state(self, *allowed: VendingMachineState) -> None:
        """Raise InvalidStateError if current state is not in allowed.

        TODO:
            - If _state not in allowed: raise InvalidStateError
              with message mentioning the current state name
        """
        pass

    def insert_coin(self, amount: float) -> None:
        """Insert coins into the machine.

        TODO:
            - Require IDLE or COIN_INSERTED state
            - Add amount to _balance
            - Set state to COIN_INSERTED
        """
        pass

    def select_product(self, code: str) -> str:
        """Select a product by code. Returns a status message string.

        TODO:
            - Require COIN_INSERTED state
            - If code not in _products: return f"Product {code!r} not found."
            - If product.quantity == 0: return "Out of stock."
            - If _balance < product.price: return insufficient funds message
              Format: f"Insufficient funds. Price: ${product.price:.2f}, Balance: ${self._balance:.2f}"
            - Set _selected = product, transition to PRODUCT_SELECTED
            - Return f"Selected: {product.name}. Please dispense."
        """
        pass

    def dispense(self) -> str:
        """Dispense the selected product and return change as a message string.

        TODO:
            - Require PRODUCT_SELECTED state
            - Calculate change = round(_balance - _selected.price, 2)
            - Decrement _selected.quantity by 1
            - Reset: _balance = 0.0, _selected = None, state = IDLE
            - Return f"Dispensed: {product.name}. Change: ${change:.2f}"
        """
        pass

    def refund(self) -> float:
        """Refund all inserted coins and reset to IDLE.

        TODO:
            - Require COIN_INSERTED or PRODUCT_SELECTED state
            - Capture current _balance
            - Reset: _balance = 0.0, _selected = None, state = IDLE
            - Return the captured amount
        """
        pass

    def restock(self, code: str, quantity: int) -> None:
        """Restock a product (admin operation).

        TODO:
            - Require IDLE state
            - Raise ValueError if code not in _products
            - Add quantity to _products[code].quantity
        """
        pass

    @property
    def current_state(self) -> VendingMachineState:
        return self._state

    @property
    def balance(self) -> float:
        return self._balance
