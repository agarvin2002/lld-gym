"""Extended tests for ATM System."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision
from starter import ATM, Card, Account, ATMState, InvalidStateError, CashDispenser


def make_atm(balance: float = 1000.0):
    atm = ATM(CashDispenser(10_000))
    card = Card("4111", "ACC001")
    account = Account("ACC001", balance=balance, pin="1234")
    atm.add_account(card, account)
    return atm, card, account


class TestPinLocking:
    def test_three_wrong_pins_locks_account(self):
        atm, card, account = make_atm()
        atm.insert_card(card)
        for _ in range(3):
            atm.enter_pin("9999")
        assert account.is_locked is True

    def test_locked_card_cannot_enter_pin(self):
        atm, card, account = make_atm()
        atm.insert_card(card)
        for _ in range(3):
            atm.enter_pin("9999")
        # After lock, ATM should eject card → IDLE
        assert atm.state == ATMState.IDLE


class TestStateGuards:
    def test_balance_in_wrong_state_raises_error(self):
        atm, card, _ = make_atm()
        with pytest.raises(InvalidStateError):
            atm.get_balance()

    def test_withdraw_in_wrong_state_raises_error(self):
        atm, _, _ = make_atm()
        with pytest.raises(InvalidStateError):
            atm.withdraw(100)

    def test_insert_card_twice_raises_error(self):
        atm, card, _ = make_atm()
        atm.insert_card(card)
        with pytest.raises(InvalidStateError):
            atm.insert_card(card)


class TestWithdraw:
    def test_withdraw_insufficient_funds_raises_error(self):
        atm, card, _ = make_atm(balance=100.0)
        atm.insert_card(card)
        atm.enter_pin("1234")
        with pytest.raises(ValueError):
            atm.withdraw(500.0)

    def test_withdraw_returns_denomination_dict(self):
        atm, card, _ = make_atm()
        atm.insert_card(card)
        atm.enter_pin("1234")
        result = atm.withdraw(200.0)
        assert isinstance(result, dict)
        total = sum(denom * count for denom, count in result.items())
        assert total == 200.0
