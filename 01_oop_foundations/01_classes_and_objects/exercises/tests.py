"""
tests.py — pytest tests for the Classes and Objects exercise.

Run with:
    pytest tests.py -v
    pytest tests.py -v --tb=short   (shorter tracebacks on failure)

These tests import from starter.py by default.
To test the solution instead, change the import line to:
    from solution.solution import Product, ShoppingCart
"""

import sys
import os
import pytest

# ---------------------------------------------------------------------------
# Import configuration
# ---------------------------------------------------------------------------
# Add the directory containing this file to sys.path so we can import
# starter.py regardless of where pytest is invoked from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)

# To run tests against your starter (in-progress) implementation:
from starter import Product, ShoppingCart

# To run tests against the reference solution, comment out the line above
# and uncomment the line below:
# from solution.solution import Product, ShoppingCart


# ===========================================================================
# Product Tests
# ===========================================================================

class TestProductCreation:
    """Tests for Product.__init__ validation and attribute assignment."""

    def test_product_creation_with_valid_data(self):
        """A Product with valid arguments should be created without errors."""
        p = Product("Laptop Pro", 999.99, 10, "SKU-001")
        assert p.name == "Laptop Pro"
        assert p.price == 999.99
        assert p.quantity == 10
        assert p.sku == "SKU-001"

    def test_product_raises_on_negative_price(self):
        """A negative price should raise ValueError."""
        with pytest.raises(ValueError, match="price"):
            Product("Widget", -10.0, 5, "SKU-002")

    def test_product_raises_on_zero_price(self):
        """A zero price should raise ValueError (price must be strictly positive)."""
        with pytest.raises(ValueError):
            Product("Widget", 0.0, 5, "SKU-003")

    def test_product_raises_on_negative_quantity(self):
        """A negative quantity should raise ValueError."""
        with pytest.raises(ValueError, match="quantity"):
            Product("Widget", 9.99, -1, "SKU-004")

    def test_product_zero_quantity_is_valid(self):
        """quantity=0 is valid (item is out of stock, but still a valid product)."""
        p = Product("Widget", 9.99, 0, "SKU-005")
        assert p.quantity == 0

    def test_product_raises_on_empty_name(self):
        """An empty name should raise ValueError."""
        with pytest.raises(ValueError):
            Product("", 9.99, 5, "SKU-006")

    def test_product_raises_on_empty_sku(self):
        """An empty SKU should raise ValueError."""
        with pytest.raises(ValueError):
            Product("Widget", 9.99, 5, "")


class TestProductMethods:
    """Tests for Product's instance methods."""

    def test_product_is_in_stock_true(self):
        """is_in_stock returns True when quantity > 0."""
        p = Product("Widget", 9.99, 5, "SKU-007")
        assert p.is_in_stock() is True

    def test_product_is_in_stock_false(self):
        """is_in_stock returns False when quantity == 0."""
        p = Product("Widget", 9.99, 0, "SKU-008")
        assert p.is_in_stock() is False

    def test_product_apply_discount_reduces_price(self):
        """Applying a 10% discount to a $100 product should make it $90."""
        p = Product("Widget", 100.0, 5, "SKU-009")
        p.apply_discount(10)
        assert abs(p.price - 90.0) < 0.001  # floating point tolerance

    def test_product_apply_discount_100_percent(self):
        """A 100% discount should make the price 0."""
        p = Product("Widget", 100.0, 5, "SKU-010")
        p.apply_discount(100)
        assert p.price == pytest.approx(0.0)

    def test_product_apply_discount_invalid_zero_raises(self):
        """A 0% discount should raise ValueError."""
        p = Product("Widget", 100.0, 5, "SKU-011")
        with pytest.raises(ValueError):
            p.apply_discount(0)

    def test_product_apply_discount_invalid_negative_raises(self):
        """A negative discount should raise ValueError."""
        p = Product("Widget", 100.0, 5, "SKU-012")
        with pytest.raises(ValueError):
            p.apply_discount(-5)

    def test_product_apply_discount_over_100_raises(self):
        """A discount greater than 100% should raise ValueError."""
        p = Product("Widget", 100.0, 5, "SKU-013")
        with pytest.raises(ValueError):
            p.apply_discount(110)


class TestProductDunders:
    """Tests for Product's dunder methods."""

    def test_product_repr_contains_name_and_price(self):
        """__repr__ should contain the product name and price."""
        p = Product("Laptop Pro", 999.99, 10, "SKU-LAPTOP")
        r = repr(p)
        assert "Laptop Pro" in r
        assert "999.99" in r

    def test_product_repr_contains_sku(self):
        """__repr__ should contain the SKU."""
        p = Product("Widget", 9.99, 5, "SKU-WIDGET")
        assert "SKU-WIDGET" in repr(p)

    def test_product_equality_by_sku(self):
        """Two Products with the same SKU should be equal, regardless of other fields."""
        p1 = Product("Widget v1", 9.99, 10, "SKU-SAME")
        p2 = Product("Widget v2", 19.99, 5, "SKU-SAME")
        assert p1 == p2

    def test_product_inequality_different_sku(self):
        """Two Products with different SKUs should not be equal."""
        p1 = Product("Widget", 9.99, 10, "SKU-AAA")
        p2 = Product("Widget", 9.99, 10, "SKU-BBB")
        assert p1 != p2

    def test_product_hashable(self):
        """Products should be usable as dict keys and in sets."""
        p1 = Product("Widget", 9.99, 10, "SKU-AAA")
        p2 = Product("Gadget", 19.99, 5, "SKU-BBB")
        product_set = {p1, p2}
        assert len(product_set) == 2

    def test_product_hash_consistent_with_eq(self):
        """Two equal products must have the same hash."""
        p1 = Product("Widget v1", 9.99, 10, "SKU-SAME")
        p2 = Product("Widget v2", 19.99, 5, "SKU-SAME")
        assert p1 == p2
        assert hash(p1) == hash(p2)


# ===========================================================================
# ShoppingCart Tests
# ===========================================================================

class TestShoppingCartCreation:
    """Tests for ShoppingCart initialization."""

    def test_cart_is_empty_on_init(self):
        """A new cart should be empty."""
        cart = ShoppingCart()
        assert cart.is_empty() is True

    def test_cart_item_count_zero_on_init(self):
        """A new cart should have 0 items."""
        cart = ShoppingCart()
        assert cart.get_item_count() == 0

    def test_cart_total_zero_on_init(self):
        """A new cart should have a total of 0.0."""
        cart = ShoppingCart()
        assert cart.get_total() == pytest.approx(0.0)


class TestShoppingCartAddItem:
    """Tests for ShoppingCart.add_item."""

    def test_cart_add_item_increases_count(self):
        """Adding a product should increase get_item_count by the quantity added."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        cart.add_item(p, 3)
        assert cart.get_item_count() == 3

    def test_cart_is_not_empty_after_add(self):
        """Cart should not be empty after adding a product."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        cart.add_item(p)
        assert cart.is_empty() is False

    def test_cart_add_same_product_accumulates(self):
        """Adding the same product twice should accumulate quantities, not duplicate."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        cart.add_item(p, 2)
        cart.add_item(p, 3)
        assert cart.get_item_count() == 5

    def test_cart_add_item_default_quantity_is_one(self):
        """add_item with no quantity argument should add 1 unit."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        cart.add_item(p)
        assert cart.get_item_count() == 1

    def test_cart_add_item_invalid_quantity_raises(self):
        """Adding a quantity < 1 should raise ValueError."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        with pytest.raises(ValueError):
            cart.add_item(p, 0)


class TestShoppingCartRemoveItem:
    """Tests for ShoppingCart.remove_item."""

    def test_cart_remove_item_decreases_count(self):
        """Removing a product should decrease item count by its cart quantity."""
        cart = ShoppingCart()
        p1 = Product("Widget", 9.99, 10, "SKU-001")
        p2 = Product("Gadget", 19.99, 5, "SKU-002")
        cart.add_item(p1, 2)
        cart.add_item(p2, 1)
        cart.remove_item(p1)
        assert cart.get_item_count() == 1  # only p2 remains

    def test_cart_remove_nonexistent_raises_error(self):
        """Removing a product that isn't in the cart should raise ValueError."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        with pytest.raises(ValueError):
            cart.remove_item(p)

    def test_cart_becomes_empty_after_removing_all(self):
        """Cart should be empty after removing the only item."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        cart.add_item(p)
        cart.remove_item(p)
        assert cart.is_empty() is True


class TestShoppingCartGetTotal:
    """Tests for ShoppingCart.get_total."""

    def test_cart_get_total_calculates_correctly(self):
        """Total should equal sum of (price * quantity) for all items."""
        cart = ShoppingCart()
        p1 = Product("Laptop", 999.99, 5, "SKU-001")
        p2 = Product("Mouse", 29.99, 20, "SKU-002")
        cart.add_item(p1, 1)
        cart.add_item(p2, 2)
        expected = 999.99 * 1 + 29.99 * 2  # 1059.97
        assert cart.get_total() == pytest.approx(expected)

    def test_cart_total_updates_after_remove(self):
        """Total should decrease after removing a product."""
        cart = ShoppingCart()
        p1 = Product("Laptop", 1000.0, 5, "SKU-001")
        p2 = Product("Mouse", 30.0, 20, "SKU-002")
        cart.add_item(p1, 1)
        cart.add_item(p2, 2)
        cart.remove_item(p2)
        assert cart.get_total() == pytest.approx(1000.0)


class TestShoppingCartContains:
    """Tests for ShoppingCart.__contains__ and __len__."""

    def test_product_in_cart_after_add(self):
        """'product in cart' should return True after adding it."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        cart.add_item(p)
        assert p in cart

    def test_product_not_in_cart_initially(self):
        """'product in cart' should return False before adding."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        assert p not in cart

    def test_len_returns_total_unit_count(self):
        """len(cart) should return total number of individual units."""
        cart = ShoppingCart()
        p1 = Product("Widget", 9.99, 10, "SKU-001")
        p2 = Product("Gadget", 19.99, 5, "SKU-002")
        cart.add_item(p1, 3)
        cart.add_item(p2, 2)
        assert len(cart) == 5


class TestShoppingCartGetItems:
    """Tests for ShoppingCart.get_items."""

    def test_get_items_returns_copy(self):
        """Mutating the returned dict should not affect the cart."""
        cart = ShoppingCart()
        p = Product("Widget", 9.99, 10, "SKU-001")
        cart.add_item(p, 2)
        items = cart.get_items()
        items[p] = 999  # mutate the copy
        # The cart's internal state should be unchanged
        assert cart.get_item_count() == 2

    def test_get_items_has_correct_quantities(self):
        """get_items should return the correct product-to-quantity mapping."""
        cart = ShoppingCart()
        p1 = Product("Widget", 9.99, 10, "SKU-001")
        p2 = Product("Gadget", 19.99, 5, "SKU-002")
        cart.add_item(p1, 3)
        cart.add_item(p2, 1)
        items = cart.get_items()
        assert items[p1] == 3
        assert items[p2] == 1
