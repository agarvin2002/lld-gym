"""
WHAT YOU'RE BUILDING
====================
A vending machine with four states:
  - IDLE         — waiting for money
  - HAS_MONEY    — coin inserted, waiting for product selection
  - DISPENSING   — product selected, ready to dispense
  - OUT_OF_STOCK — all products exhausted

Operations: insert_coin, select_product, dispense, refund, restock.
Each operation is only valid in certain states — invalid calls raise
InvalidStateError.

Classes you must implement:
  - VendingMachineState (Enum)
  - InvalidStateError (Exception)
  - Product (dataclass with name, price, quantity)
  - VendingMachine
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


# TODO: Define VendingMachineState as an Enum with four values:
#       IDLE, HAS_MONEY, DISPENSING, OUT_OF_STOCK
class VendingMachineState(Enum):
    pass


# TODO: Define InvalidStateError as a simple Exception subclass
class InvalidStateError(Exception):
    pass


# TODO: Define Product as a dataclass with fields: name (str), price (float), quantity (int)
@dataclass
class Product:
    pass


class VendingMachine:
    """
    A state-driven vending machine.

    Constructor:
        products: dict mapping code (str) → tuple(name, price, quantity)
        Example: {"A1": ("Cola", 1.50, 3)}
    """

    def __init__(self, products: dict[str, tuple[str, float, int]]) -> None:
        # TODO: Build self._products — a dict mapping code → Product instance
        # TODO: Set self._balance = 0.0
        # TODO: Set self._selected = None  (holds the selected product code)
        # TODO: Set self.state = VendingMachineState.IDLE
        # TODO: Call self._check_out_of_stock() to handle an initially empty machine
        pass

    def _require_state(self, *states: VendingMachineState) -> None:
        # TODO: If self.state is NOT in the given states, raise InvalidStateError
        # HINT: Build an error message like "Operation requires state X, current state is Y"
        pass

    def _check_out_of_stock(self) -> None:
        # TODO: If ALL products have quantity == 0, set state to OUT_OF_STOCK
        pass

    def insert_coin(self, amount: float) -> None:
        # TODO: Only valid in IDLE or HAS_MONEY — call _require_state
        # TODO: Add amount to self._balance
        # TODO: Transition to HAS_MONEY
        pass

    def select_product(self, code: str) -> str:
        # TODO: Only valid in HAS_MONEY — call _require_state
        # TODO: Raise ValueError for unknown code, out-of-stock product, or insufficient balance
        # TODO: Store the chosen code in self._selected
        # TODO: Transition to DISPENSING
        # TODO: Return the product name
        # HINT: Check self._balance < product.price to detect insufficient funds
        pass

    def dispense(self) -> str:
        # TODO: Only valid in DISPENSING — call _require_state
        # TODO: Subtract product price from self._balance
        # TODO: Decrement product quantity by 1
        # TODO: Clear self._selected (set back to None)
        # TODO: Transition to IDLE
        # TODO: Call _check_out_of_stock (last item may have just been dispensed)
        # TODO: Return the product name
        # HINT: Save the name before clearing self._selected
        pass

    def refund(self) -> float:
        # TODO: Only valid in HAS_MONEY — call _require_state
        # TODO: Save self._balance, reset it to 0.0, transition to IDLE, return saved amount
        pass

    def restock(self, code: str, quantity: int) -> None:
        # TODO: Raise ValueError for unknown product code
        # TODO: Add quantity to the product's current quantity
        # TODO: If currently OUT_OF_STOCK, transition back to IDLE
        pass

    @property
    def balance(self) -> float:
        # TODO: Return the current balance
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/behavioral/state/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
