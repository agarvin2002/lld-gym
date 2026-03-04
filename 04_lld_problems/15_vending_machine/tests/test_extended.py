"""Vending Machine — Extended Tests."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import VendingMachine, VendingMachineState, InvalidStateError

PRODUCTS = {
    "A1": ("Cola", 1.50, 2),
    "B1": ("Chips", 2.00, 1),
    "C1": ("Water", 1.00, 0),   # out of stock
}


@pytest.fixture
def machine():
    return VendingMachine(PRODUCTS)


class TestOutOfStock:
    def test_out_of_stock_message(self, machine):
        machine.insert_coin(2.0)
        msg = machine.select_product("C1")
        assert "stock" in msg.lower()

    def test_out_of_stock_stays_coin_inserted(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("C1")
        assert machine.current_state == VendingMachineState.COIN_INSERTED

    def test_balance_retained_after_out_of_stock(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("C1")
        assert machine.balance == pytest.approx(2.0)


class TestRestock:
    def test_restock_increases_quantity(self, machine):
        machine.restock("C1", 5)
        machine.insert_coin(2.0)
        msg = machine.select_product("C1")
        assert machine.current_state == VendingMachineState.PRODUCT_SELECTED

    def test_restock_invalid_code_raises(self, machine):
        with pytest.raises(ValueError):
            machine.restock("Z9", 10)

    def test_restock_not_allowed_when_not_idle(self, machine):
        machine.insert_coin(1.0)
        with pytest.raises(InvalidStateError):
            machine.restock("A1", 5)


class TestExactChange:
    def test_exact_payment_change_zero(self, machine):
        machine.insert_coin(1.50)
        machine.select_product("A1")
        result = machine.dispense()
        assert "0.00" in result

    def test_overpayment_gives_correct_change(self, machine):
        machine.insert_coin(2.00)
        machine.select_product("A1")
        result = machine.dispense()
        assert "0.50" in result


class TestSelectDifferentProduct:
    def test_can_change_selection_by_refunding(self, machine):
        machine.insert_coin(2.0)
        machine.select_product("A1")  # selected Cola
        machine.refund()
        machine.insert_coin(2.0)
        machine.select_product("B1")  # select Chips instead
        result = machine.dispense()
        assert "Chips" in result

    def test_last_product_depleted(self, machine):
        """After buying the last unit, product shows out-of-stock."""
        machine.insert_coin(2.0)
        machine.select_product("B1")  # qty=1
        machine.dispense()
        machine.insert_coin(2.0)
        msg = machine.select_product("B1")
        assert "stock" in msg.lower()

    def test_full_purchase_cycle(self, machine):
        """Complete happy-path: insert → select → dispense → idle."""
        assert machine.current_state == VendingMachineState.IDLE
        machine.insert_coin(1.00)
        machine.insert_coin(0.50)
        assert machine.balance == pytest.approx(1.50)
        msg = machine.select_product("A1")
        assert machine.current_state == VendingMachineState.PRODUCT_SELECTED
        result = machine.dispense()
        assert "Cola" in result
        assert machine.current_state == VendingMachineState.IDLE
        assert machine.balance == pytest.approx(0.0)
