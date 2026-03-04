"""Vending Machine — Edge Cases."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import VendingMachine, VendingMachineState, InvalidStateError

PRODUCTS = {
    "A1": ("Cola", 1.50, 5),
    "B1": ("Chips", 2.00, 3),
}


@pytest.fixture
def machine():
    return VendingMachine(PRODUCTS)


class TestInvalidStateTransitions:
    def test_dispense_from_idle_raises(self, machine):
        with pytest.raises(InvalidStateError):
            machine.dispense()

    def test_dispense_from_coin_inserted_raises(self, machine):
        machine.insert_coin(2.0)
        with pytest.raises(InvalidStateError):
            machine.dispense()

    def test_select_from_idle_raises(self, machine):
        with pytest.raises(InvalidStateError):
            machine.select_product("A1")

    def test_select_from_product_selected_raises(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")
        with pytest.raises(InvalidStateError):
            machine.select_product("B1")

    def test_refund_from_idle_raises(self, machine):
        with pytest.raises(InvalidStateError):
            machine.refund()

    def test_restock_from_coin_inserted_raises(self, machine):
        machine.insert_coin(1.0)
        with pytest.raises(InvalidStateError):
            machine.restock("A1", 5)

    def test_restock_from_product_selected_raises(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")
        with pytest.raises(InvalidStateError):
            machine.restock("A1", 5)


class TestMultiplePurchases:
    def test_two_sequential_purchases(self, machine):
        for _ in range(2):
            machine.insert_coin(2.0)
            machine.select_product("A1")
            result = machine.dispense()
            assert "Cola" in result
        assert machine.current_state == VendingMachineState.IDLE

    def test_balance_reset_after_dispense(self, machine):
        machine.insert_coin(5.0)
        machine.select_product("A1")
        machine.dispense()
        assert machine.balance == pytest.approx(0.0)

    def test_balance_reset_after_refund(self, machine):
        machine.insert_coin(0.50)
        machine.refund()
        assert machine.balance == pytest.approx(0.0)

    def test_machine_reusable_after_refund(self, machine):
        machine.insert_coin(0.50)
        machine.refund()
        machine.insert_coin(2.0)
        machine.select_product("A1")
        result = machine.dispense()
        assert "Cola" in result


class TestBoundaryValues:
    def test_insert_zero_still_transitions(self, machine):
        """Inserting 0.0 is technically valid (edge case)."""
        machine.insert_coin(0.0)
        assert machine.current_state == VendingMachineState.COIN_INSERTED

    def test_unknown_product_code(self, machine):
        machine.insert_coin(5.0)
        msg = machine.select_product("Z9")
        # Should not crash; stays in COIN_INSERTED
        assert machine.current_state == VendingMachineState.COIN_INSERTED
