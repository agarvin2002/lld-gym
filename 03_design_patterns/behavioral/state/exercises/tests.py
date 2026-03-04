"""Tests for State Pattern — Vending Machine."""
import sys, os
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import VendingMachine, VendingMachineState, InvalidStateError


def make_machine():
    return VendingMachine({
        "A1": ("Cola", 1.50, 3),
        "B2": ("Water", 1.00, 2),
        "C3": ("Chips", 2.00, 1),
    })


class TestInitialState:
    def test_starts_idle(self):
        vm = make_machine()
        assert vm.state == VendingMachineState.IDLE

    def test_starts_out_of_stock_when_empty(self):
        vm = VendingMachine({"A1": ("Cola", 1.50, 0)})
        assert vm.state == VendingMachineState.OUT_OF_STOCK

    def test_balance_starts_at_zero(self):
        vm = make_machine()
        assert vm.balance == pytest.approx(0.0)


class TestInsertCoin:
    def test_insert_coin_transitions_to_has_money(self):
        vm = make_machine()
        vm.insert_coin(1.00)
        assert vm.state == VendingMachineState.HAS_MONEY

    def test_insert_accumulates_balance(self):
        vm = make_machine()
        vm.insert_coin(1.00)
        vm.insert_coin(0.50)
        assert vm.balance == pytest.approx(1.50)

    def test_insert_in_wrong_state_raises(self):
        vm = make_machine()
        vm.insert_coin(2.00)
        vm.select_product("A1")
        with pytest.raises(InvalidStateError):
            vm.insert_coin(1.00)


class TestSelectProduct:
    def test_select_transitions_to_dispensing(self):
        vm = make_machine()
        vm.insert_coin(2.00)
        vm.select_product("A1")
        assert vm.state == VendingMachineState.DISPENSING

    def test_select_invalid_code_raises(self):
        vm = make_machine()
        vm.insert_coin(2.00)
        with pytest.raises(ValueError):
            vm.select_product("ZZ")

    def test_select_insufficient_balance_raises(self):
        vm = make_machine()
        vm.insert_coin(0.50)
        with pytest.raises(ValueError):
            vm.select_product("A1")  # costs 1.50

    def test_select_without_money_raises(self):
        vm = make_machine()
        with pytest.raises(InvalidStateError):
            vm.select_product("A1")


class TestDispense:
    def test_dispense_returns_product_name(self):
        vm = make_machine()
        vm.insert_coin(2.00)
        vm.select_product("A1")
        name = vm.dispense()
        assert name == "Cola"

    def test_dispense_deducts_price(self):
        vm = make_machine()
        vm.insert_coin(2.00)
        vm.select_product("A1")  # costs 1.50
        vm.dispense()
        assert vm.balance == pytest.approx(0.50)  # 2.00 - 1.50

    def test_dispense_returns_to_idle(self):
        vm = make_machine()
        vm.insert_coin(2.00)
        vm.select_product("A1")
        vm.dispense()
        assert vm.state == VendingMachineState.IDLE

    def test_dispense_without_selecting_raises(self):
        vm = make_machine()
        with pytest.raises(InvalidStateError):
            vm.dispense()

    def test_dispense_to_out_of_stock_when_last_item(self):
        vm = VendingMachine({"A1": ("Cola", 1.00, 1)})
        vm.insert_coin(1.00)
        vm.select_product("A1")
        vm.dispense()
        assert vm.state == VendingMachineState.OUT_OF_STOCK


class TestRefund:
    def test_refund_returns_balance(self):
        vm = make_machine()
        vm.insert_coin(1.50)
        refunded = vm.refund()
        assert refunded == pytest.approx(1.50)

    def test_refund_returns_to_idle(self):
        vm = make_machine()
        vm.insert_coin(1.00)
        vm.refund()
        assert vm.state == VendingMachineState.IDLE

    def test_refund_zeroes_balance(self):
        vm = make_machine()
        vm.insert_coin(1.00)
        vm.refund()
        assert vm.balance == pytest.approx(0.0)

    def test_refund_in_wrong_state_raises(self):
        vm = make_machine()
        with pytest.raises(InvalidStateError):
            vm.refund()


class TestRestock:
    def test_restock_from_out_of_stock_returns_to_idle(self):
        vm = VendingMachine({"A1": ("Cola", 1.00, 0)})
        assert vm.state == VendingMachineState.OUT_OF_STOCK
        vm.restock("A1", 5)
        assert vm.state == VendingMachineState.IDLE

    def test_restock_invalid_code_raises(self):
        vm = make_machine()
        with pytest.raises(ValueError):
            vm.restock("ZZ", 5)

    def test_full_flow(self):
        vm = make_machine()
        vm.insert_coin(2.00)
        vm.select_product("B2")  # Water, $1.00
        name = vm.dispense()
        assert name == "Water"
        assert vm.state == VendingMachineState.IDLE
        assert vm.balance == pytest.approx(1.00)  # change remaining
