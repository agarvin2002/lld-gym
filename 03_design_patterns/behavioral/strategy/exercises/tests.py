"""Tests for Strategy Pattern — Order Discount System."""
import sys, os
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    NoDiscount, PercentageDiscount, FixedDiscount,
    BuyOneGetOneFree, LoyaltyDiscount, Order, DiscountStrategy,
)


class TestNoDiscount:
    def test_returns_original_total(self):
        assert NoDiscount().apply(100.0) == pytest.approx(100.0)

    def test_returns_zero_total_unchanged(self):
        assert NoDiscount().apply(0.0) == pytest.approx(0.0)


class TestPercentageDiscount:
    def test_20_percent_off_100(self):
        assert PercentageDiscount(20).apply(100.0) == pytest.approx(80.0)

    def test_0_percent_returns_unchanged(self):
        assert PercentageDiscount(0).apply(100.0) == pytest.approx(100.0)

    def test_100_percent_returns_zero(self):
        assert PercentageDiscount(100).apply(100.0) == pytest.approx(0.0)

    def test_negative_percent_raises(self):
        with pytest.raises(ValueError):
            PercentageDiscount(-1)

    def test_over_100_raises(self):
        with pytest.raises(ValueError):
            PercentageDiscount(101)

    def test_is_discount_strategy(self):
        assert issubclass(PercentageDiscount, DiscountStrategy)


class TestFixedDiscount:
    def test_subtracts_amount(self):
        assert FixedDiscount(15).apply(100.0) == pytest.approx(85.0)

    def test_clamps_to_zero(self):
        assert FixedDiscount(200).apply(100.0) == pytest.approx(0.0)

    def test_exact_match_gives_zero(self):
        assert FixedDiscount(50).apply(50.0) == pytest.approx(0.0)

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError):
            FixedDiscount(-10)

    def test_zero_amount_is_valid(self):
        assert FixedDiscount(0).apply(100.0) == pytest.approx(100.0)


class TestBuyOneGetOneFree:
    def test_halves_total(self):
        assert BuyOneGetOneFree().apply(80.0) == pytest.approx(40.0)

    def test_odd_total(self):
        assert BuyOneGetOneFree().apply(99.0) == pytest.approx(49.5)


class TestLoyaltyDiscount:
    def test_silver_5_percent(self):
        assert LoyaltyDiscount("silver").apply(100.0) == pytest.approx(95.0)

    def test_gold_10_percent(self):
        assert LoyaltyDiscount("gold").apply(100.0) == pytest.approx(90.0)

    def test_platinum_15_percent(self):
        assert LoyaltyDiscount("platinum").apply(100.0) == pytest.approx(85.0)

    def test_invalid_tier_raises(self):
        with pytest.raises(ValueError):
            LoyaltyDiscount("bronze")


class TestOrder:
    def test_final_price_applies_discount(self):
        order = Order(100.0, PercentageDiscount(10))
        assert order.final_price() == pytest.approx(90.0)

    def test_total_not_mutated(self):
        order = Order(100.0, PercentageDiscount(50))
        order.final_price()
        assert order.total == pytest.approx(100.0)

    def test_zero_or_negative_total_raises(self):
        with pytest.raises(ValueError):
            Order(0.0, NoDiscount())
        with pytest.raises(ValueError):
            Order(-10.0, NoDiscount())

    def test_set_discount_changes_result(self):
        order = Order(100.0, NoDiscount())
        assert order.final_price() == pytest.approx(100.0)
        order.set_discount(PercentageDiscount(25))
        assert order.final_price() == pytest.approx(75.0)

    def test_all_strategies_interchangeable(self):
        strategies = [
            (NoDiscount(), 100.0),
            (PercentageDiscount(20), 80.0),
            (FixedDiscount(30), 70.0),
            (BuyOneGetOneFree(), 50.0),
            (LoyaltyDiscount("gold"), 90.0),
        ]
        for strategy, expected in strategies:
            order = Order(100.0, strategy)
            assert order.final_price() == pytest.approx(expected), \
                f"Failed for {type(strategy).__name__}"
