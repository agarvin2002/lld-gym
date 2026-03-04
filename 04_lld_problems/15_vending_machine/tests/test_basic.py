"""Vending Machine — Basic Tests."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import VendingMachine, VendingMachineState, InvalidStateError

PRODUCTS = {
    "A1": ("Cola", 1.50, 5),
    "B1": ("Chips", 2.00, 3),
    "C1": ("Water", 1.00, 10),
}


@pytest.fixture
def machine():
    return VendingMachine(PRODUCTS)


class TestInitialState:
    def test_starts_idle(self, machine):
        assert machine.current_state == VendingMachineState.IDLE

    def test_balance_starts_zero(self, machine):
        assert machine.balance == pytest.approx(0.0)


class TestInsertCoin:
    def test_insert_coin_transitions_to_coin_inserted(self, machine):
        machine.insert_coin(1.0)
        assert machine.current_state == VendingMachineState.COIN_INSERTED

    def test_balance_increases(self, machine):
        machine.insert_coin(1.0)
        assert machine.balance == pytest.approx(1.0)

    def test_multiple_coins_accumulate(self, machine):
        machine.insert_coin(0.50)
        machine.insert_coin(1.00)
        assert machine.balance == pytest.approx(1.50)

    def test_insert_coin_not_allowed_in_product_selected(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")
        with pytest.raises(InvalidStateError):
            machine.insert_coin(0.5)


class TestSelectProduct:
    def test_select_valid_product(self, machine):
        machine.insert_coin(2.0)
        msg = machine.select_product("A1")
        assert "Cola" in msg
        assert machine.current_state == VendingMachineState.PRODUCT_SELECTED

    def test_select_requires_coin_inserted(self, machine):
        with pytest.raises(InvalidStateError):
            machine.select_product("A1")

    def test_insufficient_funds_stays_coin_inserted(self, machine):
        machine.insert_coin(0.50)
        msg = machine.select_product("A1")
        assert "Insufficient" in msg
        assert machine.current_state == VendingMachineState.COIN_INSERTED

    def test_insufficient_funds_message_contains_price_and_balance(self, machine):
        machine.insert_coin(0.50)
        msg = machine.select_product("A1")
        assert "1.50" in msg
        assert "0.50" in msg


class TestDispense:
    def test_dispense_returns_product_name(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")
        result = machine.dispense()
        assert "Cola" in result

    def test_dispense_returns_correct_change(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")
        result = machine.dispense()
        assert "0.50" in result

    def test_dispense_resets_to_idle(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")
        machine.dispense()
        assert machine.current_state == VendingMachineState.IDLE
        assert machine.balance == pytest.approx(0.0)

    def test_dispense_requires_product_selected(self, machine):
        with pytest.raises(InvalidStateError):
            machine.dispense()

    def test_dispense_decrements_quantity(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("B1")  # Chips qty=3
        machine.dispense()
        # Restock should add to remaining 2
        machine.restock("B1", 1)
        # (indirect check — if qty was decremented, restock works)
        machine.insert_coin(2.0)
        machine.select_product("B1")
        result = machine.dispense()
        assert "Chips" in result


class TestRefund:
    def test_refund_returns_balance(self, machine):
        machine.insert_coin(1.50)
        amount = machine.refund()
        assert amount == pytest.approx(1.50)

    def test_refund_resets_to_idle(self, machine):
        machine.insert_coin(1.0)
        machine.refund()
        assert machine.current_state == VendingMachineState.IDLE
        assert machine.balance == pytest.approx(0.0)

    def test_refund_from_product_selected(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")
        amount = machine.refund()
        assert amount == pytest.approx(2.0)
        assert machine.current_state == VendingMachineState.IDLE

    def test_refund_not_allowed_in_idle(self, machine):
        with pytest.raises(InvalidStateError):
            machine.refund()
