"""Edge case tests for ATM System."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision
from starter import ATM, Card, Account, ATMState, CashDispenser, InvalidStateError


class TestCashDispenser:
    def test_dispense_100(self):
        d = CashDispenser(1000)
        result = d.dispense(100)
        assert result.get(100, 0) == 1

    def test_dispense_170(self):
        d = CashDispenser(1000)
        result = d.dispense(170)
        total = sum(k * v for k, v in result.items())
        assert total == 170

    def test_dispense_reduces_available_cash(self):
        d = CashDispenser(1000)
        d.dispense(200)
        assert d.available_cash == 800

    def test_dispense_exceeds_available_cash_raises(self):
        d = CashDispenser(50)
        with pytest.raises(ValueError):
            d.dispense(100)

    def test_undispensable_amount_raises(self):
        d = CashDispenser(1000)
        with pytest.raises(ValueError):
            d.dispense(15)  # not divisible by $20


class TestATMEdgeCases:
    def test_eject_from_idle_does_not_raise(self):
        atm = ATM()
        atm.eject_card()  # should be safe no-op

    def test_unknown_card_raises_error(self):
        atm = ATM()
        with pytest.raises(ValueError):
            atm.insert_card(Card("UNKNOWN", "NO_ACCOUNT"))
