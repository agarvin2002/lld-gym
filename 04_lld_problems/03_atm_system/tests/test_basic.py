"""Basic tests for ATM System."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision
from starter import ATM, Card, Account, ATMState, InvalidStateError, CashDispenser


def make_atm():
    atm = ATM(CashDispenser(10_000))
    card = Card("4111-1111-1111-1111", "ACC001")
    account = Account("ACC001", balance=1000.0, pin="1234")
    atm.add_account(card, account)
    return atm, card, account


class TestATMStates:
    def test_atm_starts_in_idle_state(self):
        atm, _, _ = make_atm()
        assert atm.state == ATMState.IDLE

    def test_insert_card_transitions_to_card_inserted(self):
        atm, card, _ = make_atm()
        atm.insert_card(card)
        assert atm.state == ATMState.CARD_INSERTED

    def test_correct_pin_transitions_to_pin_verified(self):
        atm, card, _ = make_atm()
        atm.insert_card(card)
        result = atm.enter_pin("1234")
        assert result is True
        assert atm.state == ATMState.PIN_VERIFIED

    def test_wrong_pin_stays_in_card_inserted(self):
        atm, card, _ = make_atm()
        atm.insert_card(card)
        result = atm.enter_pin("0000")
        assert result is False
        assert atm.state == ATMState.CARD_INSERTED

    def test_eject_card_returns_to_idle(self):
        atm, card, _ = make_atm()
        atm.insert_card(card)
        atm.eject_card()
        assert atm.state == ATMState.IDLE


class TestTransactions:
    def test_get_balance_returns_correct_amount(self):
        atm, card, _ = make_atm()
        atm.insert_card(card)
        atm.enter_pin("1234")
        assert atm.get_balance() == 1000.0

    def test_withdraw_reduces_balance(self):
        atm, card, account = make_atm()
        atm.insert_card(card)
        atm.enter_pin("1234")
        atm.withdraw(200.0)
        assert account.balance == 800.0

    def test_deposit_increases_balance(self):
        atm, card, account = make_atm()
        atm.insert_card(card)
        atm.enter_pin("1234")
        atm.deposit(500.0)
        assert account.balance == 1500.0
