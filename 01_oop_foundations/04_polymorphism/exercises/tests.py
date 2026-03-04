"""
Tests for the Polymorphic Discount System
==========================================

Run with:
    pytest tests.py -v
    pytest tests.py -v --tb=short   (shorter tracebacks)

All tests import from starter.py in the same directory.
"""

from __future__ import annotations

import sys
import os

# Make starter.py importable when running from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)

import pytest
from starter import (
    BuyOneGetOneDiscount,
    Discount,
    FixedDiscount,
    NoDiscount,
    Order,
    PercentageDiscount,
)


# ---------------------------------------------------------------------------
# NoDiscount
# ---------------------------------------------------------------------------

class TestNoDiscount:
    def test_no_discount_returns_original_price(self) -> None:
        """NoDiscount must leave the price completely unchanged."""
        discount = NoDiscount()
        assert discount.apply(100.0) == 100.0

    def test_no_discount_works_with_zero_price(self) -> None:
        """NoDiscount should handle a zero price without error."""
        discount = NoDiscount()
        assert discount.apply(0.0) == 0.0

    def test_no_discount_works_with_fractional_price(self) -> None:
        """NoDiscount should preserve fractional prices exactly."""
        discount = NoDiscount()
        assert discount.apply(49.99) == 49.99


# ---------------------------------------------------------------------------
# PercentageDiscount
# ---------------------------------------------------------------------------

class TestPercentageDiscount:
    def test_percentage_discount_reduces_price(self) -> None:
        """20% off $100 should be $80."""
        discount = PercentageDiscount(20)
        assert discount.apply(100.0) == pytest.approx(80.0)

    def test_percentage_discount_with_zero_percent(self) -> None:
        """0% discount should leave price unchanged."""
        discount = PercentageDiscount(0)
        assert discount.apply(100.0) == pytest.approx(100.0)

    def test_percentage_discount_with_100_percent(self) -> None:
        """100% discount should reduce price to 0."""
        discount = PercentageDiscount(100)
        assert discount.apply(100.0) == pytest.approx(0.0)

    def test_percentage_discount_with_fractional_percent(self) -> None:
        """15% off $200 = $170."""
        discount = PercentageDiscount(15)
        assert discount.apply(200.0) == pytest.approx(170.0)

    def test_percentage_discount_negative_percent_raises_error(self) -> None:
        """Negative percent is invalid and should raise ValueError."""
        with pytest.raises(ValueError):
            PercentageDiscount(-5)

    def test_percentage_discount_over_100_raises_error(self) -> None:
        """Percent greater than 100 is invalid and should raise ValueError."""
        with pytest.raises(ValueError):
            PercentageDiscount(101)

    def test_percentage_discount_is_discount_subtype(self) -> None:
        """PercentageDiscount must be a subclass of Discount (ABC contract)."""
        assert issubclass(PercentageDiscount, Discount)


# ---------------------------------------------------------------------------
# FixedDiscount
# ---------------------------------------------------------------------------

class TestFixedDiscount:
    def test_fixed_discount_reduces_price(self) -> None:
        """$10 off a $50 item should be $40."""
        discount = FixedDiscount(10)
        assert discount.apply(50.0) == pytest.approx(40.0)

    def test_fixed_discount_never_goes_below_zero(self) -> None:
        """Discount larger than price should clamp to 0, not go negative."""
        discount = FixedDiscount(20)
        assert discount.apply(15.0) == pytest.approx(0.0)

    def test_fixed_discount_exact_match_gives_zero(self) -> None:
        """Discount equal to price should give exactly 0."""
        discount = FixedDiscount(50)
        assert discount.apply(50.0) == pytest.approx(0.0)

    def test_fixed_discount_with_small_price(self) -> None:
        """$10 off $8 should clamp to 0."""
        discount = FixedDiscount(10)
        assert discount.apply(8.0) == pytest.approx(0.0)

    def test_fixed_discount_negative_amount_raises_error(self) -> None:
        """Negative fixed discount amount is invalid."""
        with pytest.raises(ValueError):
            FixedDiscount(-5)

    def test_fixed_discount_zero_amount_is_valid(self) -> None:
        """A FixedDiscount of $0 is allowed and leaves price unchanged."""
        discount = FixedDiscount(0)
        assert discount.apply(100.0) == pytest.approx(100.0)


# ---------------------------------------------------------------------------
# BuyOneGetOneDiscount
# ---------------------------------------------------------------------------

class TestBuyOneGetOneDiscount:
    def test_bogo_discount_halves_price(self) -> None:
        """BOGO should return exactly half the price."""
        discount = BuyOneGetOneDiscount()
        assert discount.apply(60.0) == pytest.approx(30.0)

    def test_bogo_discount_with_odd_price(self) -> None:
        """BOGO with $99 price should give $49.50."""
        discount = BuyOneGetOneDiscount()
        assert discount.apply(99.0) == pytest.approx(49.5)

    def test_bogo_discount_with_fractional_price(self) -> None:
        """BOGO with $33.33 should give $16.665."""
        discount = BuyOneGetOneDiscount()
        assert discount.apply(33.33) == pytest.approx(16.665)


# ---------------------------------------------------------------------------
# Order
# ---------------------------------------------------------------------------

class TestOrder:
    def test_order_applies_discount_correctly(self) -> None:
        """Order.final_price() should apply the discount to the original price."""
        order = Order(price=100.0, discount=PercentageDiscount(10))
        assert order.final_price() == pytest.approx(90.0)

    def test_order_with_no_discount(self) -> None:
        """Order with NoDiscount should return original price."""
        order = Order(price=75.0, discount=NoDiscount())
        assert order.final_price() == pytest.approx(75.0)

    def test_order_can_swap_discount_strategy(self) -> None:
        """apply_discount() should swap the strategy; final_price() should reflect the change."""
        order = Order(price=100.0, discount=NoDiscount())
        assert order.final_price() == pytest.approx(100.0)

        order.apply_discount(PercentageDiscount(50))
        assert order.final_price() == pytest.approx(50.0)

        order.apply_discount(FixedDiscount(10))
        assert order.final_price() == pytest.approx(90.0)

    def test_order_with_fixed_discount(self) -> None:
        """Order with FixedDiscount should subtract fixed amount."""
        order = Order(price=80.0, discount=FixedDiscount(15))
        assert order.final_price() == pytest.approx(65.0)

    def test_order_with_bogo_discount(self) -> None:
        """Order with BOGO should halve the price."""
        order = Order(price=120.0, discount=BuyOneGetOneDiscount())
        assert order.final_price() == pytest.approx(60.0)

    def test_order_original_price_not_mutated(self) -> None:
        """Applying a discount should not change order.price."""
        order = Order(price=200.0, discount=PercentageDiscount(25))
        order.final_price()
        assert order.price == 200.0

    def test_order_invalid_price_raises_error(self) -> None:
        """Order with zero or negative price should raise ValueError."""
        with pytest.raises(ValueError):
            Order(price=0.0, discount=NoDiscount())

        with pytest.raises(ValueError):
            Order(price=-10.0, discount=NoDiscount())

    def test_order_swap_to_fixed_discount_clamping(self) -> None:
        """After swapping to FixedDiscount, clamping should still work."""
        order = Order(price=5.0, discount=NoDiscount())
        order.apply_discount(FixedDiscount(100))
        assert order.final_price() == pytest.approx(0.0)

    def test_order_swap_multiple_times(self) -> None:
        """Swapping discount multiple times should always use the latest one."""
        order = Order(price=100.0, discount=NoDiscount())
        order.apply_discount(PercentageDiscount(10))
        order.apply_discount(PercentageDiscount(20))
        order.apply_discount(PercentageDiscount(30))
        assert order.final_price() == pytest.approx(70.0)


# ---------------------------------------------------------------------------
# Polymorphism: same interface, interchangeable types
# ---------------------------------------------------------------------------

class TestPolymorphism:
    """
    These tests verify the core polymorphic property:
    any Discount can be used wherever a Discount is expected.
    """

    def test_all_discounts_satisfy_the_interface(self) -> None:
        """All discount types must implement apply() correctly."""
        discounts: list[Discount] = [
            NoDiscount(),
            PercentageDiscount(10),
            FixedDiscount(5),
            BuyOneGetOneDiscount(),
        ]
        price = 100.0
        for discount in discounts:
            result = discount.apply(price)
            assert isinstance(result, float), (
                f"{type(discount).__name__}.apply() must return a float"
            )
            assert result >= 0.0, (
                f"{type(discount).__name__}.apply() returned a negative price"
            )

    def test_cannot_instantiate_abstract_discount(self) -> None:
        """The Discount ABC cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Discount()  # type: ignore[abstract]

    def test_order_works_with_any_discount_type(self) -> None:
        """Order should produce correct results regardless of discount type."""
        test_cases: list[tuple[Discount, float]] = [
            (NoDiscount(), 100.0),
            (PercentageDiscount(25), 75.0),
            (FixedDiscount(30), 70.0),
            (BuyOneGetOneDiscount(), 50.0),
        ]
        for discount, expected in test_cases:
            order = Order(price=100.0, discount=discount)
            assert order.final_price() == pytest.approx(expected), (
                f"Failed for {type(discount).__name__}"
            )
