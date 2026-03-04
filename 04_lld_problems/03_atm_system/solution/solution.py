"""
ATM System — Reference Solution

Patterns: State (ATM lifecycle), Strategy (extensible for different dispensing)
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
        if self.is_locked:
            return False
        if entered_pin == self.pin:
            self.failed_attempts = 0
            return True
        self.failed_attempts += 1
        if self.failed_attempts >= 3:
            self.is_locked = True
        return False

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds: balance={self.balance:.2f}, requested={amount:.2f}")
        self.balance -= amount


@dataclass
class Card:
    card_number: str
    account_id: str


class CashDispenser:
    DENOMINATIONS = [100, 50, 20]

    def __init__(self, initial_cash: float = 10_000) -> None:
        self.available_cash = initial_cash

    def dispense(self, amount: float) -> dict[int, int]:
        if amount > self.available_cash:
            raise ValueError(f"ATM has insufficient cash: {self.available_cash}")
        amount_int = int(amount)
        result: dict[int, int] = {}
        remaining = amount_int
        for denom in self.DENOMINATIONS:
            count = remaining // denom
            if count > 0:
                result[denom] = count
                remaining -= denom * count
        if remaining != 0:
            raise ValueError(f"Cannot dispense ${amount} with available denominations {self.DENOMINATIONS}")
        self.available_cash -= amount
        return result


class InvalidStateError(Exception):
    pass


class ATM:
    def __init__(self, cash_dispenser: CashDispenser | None = None) -> None:
        self.state = ATMState.IDLE
        self.current_card: Card | None = None
        self.current_account: Account | None = None
        self.cash_dispenser = cash_dispenser or CashDispenser()
        self._accounts: dict[str, tuple[Card, Account]] = {}

    def add_account(self, card: Card, account: Account) -> None:
        self._accounts[card.card_number] = (card, account)

    def _require_state(self, *states: ATMState) -> None:
        if self.state not in states:
            raise InvalidStateError(
                f"Operation not valid in state {self.state.value}. "
                f"Required: {[s.value for s in states]}"
            )

    def insert_card(self, card: Card) -> None:
        self._require_state(ATMState.IDLE)
        if card.card_number not in self._accounts:
            raise ValueError(f"Card not recognized: {card.card_number}")
        _, account = self._accounts[card.card_number]
        self.current_card = card
        self.current_account = account
        self.state = ATMState.CARD_INSERTED

    def enter_pin(self, pin: str) -> bool:
        self._require_state(ATMState.CARD_INSERTED)
        assert self.current_account is not None
        success = self.current_account.verify_pin(pin)
        if success:
            self.state = ATMState.PIN_VERIFIED
        elif self.current_account.is_locked:
            self.eject_card()
        return success

    def get_balance(self) -> float:
        self._require_state(ATMState.PIN_VERIFIED)
        assert self.current_account is not None
        return self.current_account.balance

    def withdraw(self, amount: float) -> dict[int, int]:
        self._require_state(ATMState.PIN_VERIFIED)
        assert self.current_account is not None
        self.current_account.withdraw(amount)  # raises if insufficient
        self.state = ATMState.DISPENSING
        result = self.cash_dispenser.dispense(amount)
        self.state = ATMState.IDLE
        return result

    def deposit(self, amount: float) -> None:
        self._require_state(ATMState.PIN_VERIFIED)
        assert self.current_account is not None
        self.current_account.deposit(amount)

    def eject_card(self) -> None:
        self.current_card = None
        self.current_account = None
        self.state = ATMState.IDLE
