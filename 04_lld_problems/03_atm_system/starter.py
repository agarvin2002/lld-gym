"""
ATM System — Starter

Implement a state-machine-based ATM.
Fill in the TODOs. Test with: pytest tests/ -v
"""
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field


class ATMState(Enum):
    IDLE = "IDLE"
    CARD_INSERTED = "CARD_INSERTED"
    PIN_VERIFIED = "PIN_VERIFIED"
    DISPENSING = "DISPENSING"


@dataclass
class Account:
    account_id: str
    balance: float
    pin: str
    is_locked: bool = False
    failed_attempts: int = 0

    def verify_pin(self, entered_pin: str) -> bool:
        # TODO: if locked, return False
        # TODO: if pin matches, reset failed_attempts, return True
        # TODO: else increment failed_attempts, lock if >= 3, return False
        pass

    def deposit(self, amount: float) -> None:
        # TODO: add amount to balance (validate > 0)
        pass

    def withdraw(self, amount: float) -> None:
        # TODO: raise ValueError if amount > balance or amount <= 0
        # TODO: subtract from balance
        pass


@dataclass
class Card:
    card_number: str
    account_id: str


class CashDispenser:
    """Dispenses cash in $100, $50, $20 denominations."""

    DENOMINATIONS = [100, 50, 20]

    def __init__(self, initial_cash: float = 10_000) -> None:
        # TODO: store available_cash
        pass

    def dispense(self, amount: float) -> dict[int, int]:
        """
        Dispense given amount using largest denominations first.

        Returns:
            dict mapping denomination to count, e.g. {100: 1, 50: 1, 20: 2}

        Raises:
            ValueError: if amount not dispensable or insufficient cash
        """
        # TODO: check available_cash >= amount
        # TODO: greedy algorithm: for each denomination, take as many as possible
        # TODO: if remainder > 0 after all denominations, raise ValueError
        # TODO: deduct from available_cash, return denomination dict
        pass


class InvalidStateError(Exception):
    """Raised when operation is not valid in current ATM state."""
    pass


class ATM:
    """
    ATM state machine.

    Operations only valid in certain states — raise InvalidStateError otherwise.
    """

    def __init__(self, cash_dispenser: CashDispenser | None = None) -> None:
        # TODO: initialize state = ATMState.IDLE
        # TODO: initialize current_card = None, current_account = None
        # TODO: store cash_dispenser (default to CashDispenser())
        # TODO: initialize _accounts: dict[str, Account] = {}
        pass

    def add_account(self, card: Card, account: Account) -> None:
        """Register card→account mapping (bank setup, not ATM operation)."""
        # TODO: store in _accounts by card_number
        pass

    def insert_card(self, card: Card) -> None:
        """
        Insert card into ATM.
        Only valid in IDLE state.
        """
        # TODO: raise InvalidStateError if not IDLE
        # TODO: set current_card = card
        # TODO: look up account, raise ValueError if not found
        # TODO: set current_account, transition to CARD_INSERTED
        pass

    def enter_pin(self, pin: str) -> bool:
        """
        Enter PIN.
        Only valid in CARD_INSERTED state.

        Returns:
            True if correct, False if wrong
        """
        # TODO: raise InvalidStateError if not CARD_INSERTED
        # TODO: verify pin via account.verify_pin()
        # TODO: if correct: transition to PIN_VERIFIED, return True
        # TODO: if wrong: if account locked, eject card; return False
        pass

    def get_balance(self) -> float:
        """
        Get account balance.
        Only valid in PIN_VERIFIED state.
        """
        # TODO: raise InvalidStateError if not PIN_VERIFIED
        # TODO: return current_account.balance
        pass

    def withdraw(self, amount: float) -> dict[int, int]:
        """
        Withdraw cash.
        Only valid in PIN_VERIFIED state.

        Returns:
            denomination dict from CashDispenser
        """
        # TODO: raise InvalidStateError if not PIN_VERIFIED
        # TODO: call account.withdraw(amount) — raises if insufficient funds
        # TODO: call cash_dispenser.dispense(amount)
        # TODO: transition state to DISPENSING then back to IDLE
        pass

    def deposit(self, amount: float) -> None:
        """
        Deposit cash.
        Only valid in PIN_VERIFIED state.
        """
        # TODO: raise InvalidStateError if not PIN_VERIFIED
        # TODO: call account.deposit(amount)
        # TODO: stay in PIN_VERIFIED state (more transactions allowed)
        pass

    def eject_card(self) -> None:
        """Return card and reset to IDLE. Valid from any state."""
        # TODO: reset current_card, current_account to None
        # TODO: transition to IDLE
        pass
