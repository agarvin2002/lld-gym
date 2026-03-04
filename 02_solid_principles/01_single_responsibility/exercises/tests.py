"""
SRP Exercise Tests
==================
These tests verify that each refactored class has the correct responsibility
and that the OrderService orchestrator works correctly end-to-end.

Run with:
    python tests.py

All tests must pass before you submit.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)

from starter import (
    OrderValidator,
    DiscountCalculator,
    PaymentProcessor,
    EmailNotifier,
    InventoryUpdater,
    OrderService,
)


# =============================================================================
# Test Helpers
# =============================================================================

def run_test(test_name: str, test_fn) -> bool:
    """Run a single test and report pass/fail."""
    try:
        test_fn()
        print(f"  PASS  {test_name}")
        return True
    except AssertionError as e:
        print(f"  FAIL  {test_name}")
        print(f"        AssertionError: {e}")
        return False
    except NotImplementedError:
        print(f"  SKIP  {test_name} (not implemented yet)")
        return False
    except Exception as e:
        print(f"  ERROR {test_name}")
        print(f"        {type(e).__name__}: {e}")
        return False


def make_valid_order(**overrides) -> dict:
    """Factory for creating a valid order dict, with optional overrides."""
    base = {
        "order_id": "ORD-TEST",
        "customer_email": "customer@example.com",
        "membership": "none",
        "payment_method": "credit_card",
        "coupon_code": None,
        "items": [
            {"product_id": "P001", "name": "Widget A", "quantity": 2, "unit_price": 25.00},
        ],
    }
    base.update(overrides)
    return base


def make_inventory() -> dict:
    return {"P001": 100, "P002": 50, "P003": 25}


def make_service(inventory: dict | None = None) -> OrderService:
    if inventory is None:
        inventory = make_inventory()
    return OrderService(
        validator=OrderValidator(),
        discount_calculator=DiscountCalculator(),
        payment_processor=PaymentProcessor(),
        email_notifier=EmailNotifier(),
        inventory_updater=InventoryUpdater(inventory),
    )


# =============================================================================
# OrderValidator Tests
# =============================================================================

def test_validator_accepts_valid_order():
    validator = OrderValidator()
    order = make_valid_order()
    is_valid, errors = validator.validate(order)
    assert is_valid is True, f"Expected valid order to pass, got errors: {errors}"
    assert errors == [], f"Expected no errors, got: {errors}"


def test_validator_rejects_missing_email():
    validator = OrderValidator()
    order = make_valid_order(customer_email="")
    is_valid, errors = validator.validate(order)
    assert is_valid is False, "Order with empty email should be invalid"
    assert len(errors) > 0, "Should return at least one error message"


def test_validator_rejects_invalid_email():
    validator = OrderValidator()
    order = make_valid_order(customer_email="not-an-email")
    is_valid, errors = validator.validate(order)
    assert is_valid is False, "Order with email missing '@' should be invalid"


def test_validator_rejects_empty_items():
    validator = OrderValidator()
    order = make_valid_order(items=[])
    is_valid, errors = validator.validate(order)
    assert is_valid is False, "Order with empty items list should be invalid"


def test_validator_rejects_zero_quantity():
    validator = OrderValidator()
    order = make_valid_order(items=[
        {"product_id": "P001", "name": "Widget A", "quantity": 0, "unit_price": 25.00},
    ])
    is_valid, errors = validator.validate(order)
    assert is_valid is False, "Item with quantity 0 should be invalid"


def test_validator_rejects_negative_quantity():
    validator = OrderValidator()
    order = make_valid_order(items=[
        {"product_id": "P001", "name": "Widget A", "quantity": -1, "unit_price": 25.00},
    ])
    is_valid, errors = validator.validate(order)
    assert is_valid is False, "Item with negative quantity should be invalid"


def test_validator_rejects_missing_payment_method():
    validator = OrderValidator()
    order = make_valid_order(payment_method="")
    is_valid, errors = validator.validate(order)
    assert is_valid is False, "Order without payment method should be invalid"


def test_validator_returns_multiple_errors():
    validator = OrderValidator()
    order = make_valid_order(customer_email="bad", items=[])
    is_valid, errors = validator.validate(order)
    assert is_valid is False
    assert len(errors) >= 2, f"Expected at least 2 errors, got {len(errors)}: {errors}"


# =============================================================================
# DiscountCalculator Tests
# =============================================================================

def test_discount_no_membership_no_coupon():
    calc = DiscountCalculator()
    order = make_valid_order(membership="none", coupon_code=None)
    # subtotal = 2 * 25.00 = 50.00, no discount
    discount = calc.calculate(order)
    assert discount == 0.0, f"Expected 0.0 discount, got {discount}"


def test_discount_silver_membership():
    calc = DiscountCalculator()
    order = make_valid_order(
        membership="silver",
        coupon_code=None,
        items=[{"product_id": "P001", "name": "W", "quantity": 4, "unit_price": 25.00}]
    )
    # subtotal = 100.00, silver = 5% = 5.00
    discount = calc.calculate(order)
    assert discount == 5.0, f"Expected 5.0, got {discount}"


def test_discount_gold_membership():
    calc = DiscountCalculator()
    order = make_valid_order(
        membership="gold",
        coupon_code=None,
        items=[{"product_id": "P001", "name": "W", "quantity": 4, "unit_price": 25.00}]
    )
    # subtotal = 100.00, gold = 10% = 10.00
    discount = calc.calculate(order)
    assert discount == 10.0, f"Expected 10.0, got {discount}"


def test_discount_platinum_membership():
    calc = DiscountCalculator()
    order = make_valid_order(
        membership="platinum",
        coupon_code=None,
        items=[{"product_id": "P001", "name": "W", "quantity": 4, "unit_price": 25.00}]
    )
    # subtotal = 100.00, platinum = 15% = 15.00
    discount = calc.calculate(order)
    assert discount == 15.0, f"Expected 15.0, got {discount}"


def test_discount_bulk_threshold():
    calc = DiscountCalculator()
    order = make_valid_order(
        membership="none",
        coupon_code=None,
        items=[{"product_id": "P001", "name": "W", "quantity": 10, "unit_price": 25.00}]
    )
    # subtotal = 250.00 (> 200), bulk = 5% = 12.50
    discount = calc.calculate(order)
    assert discount == 12.5, f"Expected 12.5, got {discount}"


def test_discount_coupon_save10():
    calc = DiscountCalculator()
    order = make_valid_order(membership="none", coupon_code="SAVE10")
    # subtotal = 50.00, coupon SAVE10 = $10.00
    discount = calc.calculate(order)
    assert discount == 10.0, f"Expected 10.0, got {discount}"


def test_discount_combined_membership_and_coupon():
    calc = DiscountCalculator()
    order = make_valid_order(
        membership="gold",
        coupon_code="SAVE10",
        items=[{"product_id": "P001", "name": "W", "quantity": 4, "unit_price": 25.00}]
    )
    # subtotal = 100.00, gold = 10% = 10.00, coupon = 10.00, total = 20.00
    discount = calc.calculate(order)
    assert discount == 20.0, f"Expected 20.0, got {discount}"


def test_discount_invalid_coupon_ignored():
    calc = DiscountCalculator()
    order = make_valid_order(membership="none", coupon_code="FAKECODE")
    discount = calc.calculate(order)
    assert discount == 0.0, f"Invalid coupon should give no discount, got {discount}"


# =============================================================================
# PaymentProcessor Tests
# =============================================================================

def test_payment_credit_card_success():
    processor = PaymentProcessor()
    order = make_valid_order(payment_method="credit_card")
    success, transaction_id = processor.charge(order, 45.00)
    assert success is True, "Credit card payment should succeed"
    assert transaction_id.startswith("CC-"), f"Credit card txn ID should start with 'CC-', got {transaction_id}"
    assert len(transaction_id) > 3, "Transaction ID should be non-trivial"


def test_payment_paypal_success():
    processor = PaymentProcessor()
    order = make_valid_order(payment_method="paypal")
    success, transaction_id = processor.charge(order, 45.00)
    assert success is True, "PayPal payment should succeed"
    assert transaction_id.startswith("PP-"), f"PayPal txn ID should start with 'PP-', got {transaction_id}"


def test_payment_unknown_method_fails():
    processor = PaymentProcessor()
    order = make_valid_order(payment_method="bitcoin")
    success, transaction_id = processor.charge(order, 45.00)
    assert success is False, "Unknown payment method should fail"
    assert transaction_id == "", f"Failed payment should return empty transaction_id, got '{transaction_id}'"


def test_payment_generates_unique_transaction_ids():
    processor = PaymentProcessor()
    order = make_valid_order(payment_method="credit_card")
    _, txn1 = processor.charge(order, 10.00)
    _, txn2 = processor.charge(order, 10.00)
    assert txn1 != txn2, "Each charge should produce a unique transaction ID"


# =============================================================================
# EmailNotifier Tests
# =============================================================================

def test_email_notifier_returns_true(capsys=None):
    notifier = EmailNotifier()
    order = make_valid_order()
    result = notifier.send_confirmation(order, 40.00, "CC-ABC123")
    assert result is True, "send_confirmation should return True on success"


# =============================================================================
# InventoryUpdater Tests
# =============================================================================

def test_inventory_updates_correctly():
    inventory = {"P001": 100, "P002": 50}
    updater = InventoryUpdater(inventory)
    order = make_valid_order(items=[
        {"product_id": "P001", "name": "Widget A", "quantity": 3, "unit_price": 25.00},
    ])
    result = updater.update(order)
    assert result is True, "update() should return True"
    assert inventory["P001"] == 97, f"Expected P001 stock 97, got {inventory['P001']}"


def test_inventory_updates_multiple_items():
    inventory = {"P001": 100, "P002": 50}
    updater = InventoryUpdater(inventory)
    order = make_valid_order(items=[
        {"product_id": "P001", "name": "Widget A", "quantity": 5, "unit_price": 25.00},
        {"product_id": "P002", "name": "Widget B", "quantity": 10, "unit_price": 50.00},
    ])
    updater.update(order)
    assert inventory["P001"] == 95, f"Expected P001=95, got {inventory['P001']}"
    assert inventory["P002"] == 40, f"Expected P002=40, got {inventory['P002']}"


def test_inventory_skips_unknown_products():
    inventory = {"P001": 100}
    updater = InventoryUpdater(inventory)
    order = make_valid_order(items=[
        {"product_id": "UNKNOWN", "name": "Ghost", "quantity": 5, "unit_price": 10.00},
    ])
    result = updater.update(order)
    # Should not crash — just skip unknown products
    assert result is True
    assert inventory["P001"] == 100  # unchanged


# =============================================================================
# OrderService End-to-End Tests
# =============================================================================

def test_service_successful_order():
    inventory = make_inventory()
    service = make_service(inventory)
    order = make_valid_order(
        membership="gold",
        coupon_code="SAVE10",
        items=[
            {"product_id": "P001", "name": "Widget A", "quantity": 2, "unit_price": 25.00},
            {"product_id": "P002", "name": "Widget B", "quantity": 1, "unit_price": 50.00},
        ],
    )
    result = service.process_order(order)
    assert result["success"] is True, f"Expected success, got: {result}"
    assert result["transaction_id"] is not None
    assert result["transaction_id"].startswith("CC-")
    assert result["errors"] == []
    # Verify inventory was updated
    assert inventory["P001"] == 98
    assert inventory["P002"] == 49


def test_service_invalid_order_returns_errors():
    service = make_service()
    order = make_valid_order(customer_email="not-valid", items=[])
    result = service.process_order(order)
    assert result["success"] is False
    assert len(result["errors"]) > 0
    assert result["transaction_id"] is None


def test_service_invalid_order_does_not_charge():
    """If validation fails, payment should NOT be attempted."""
    inventory = make_inventory()
    service = make_service(inventory)
    order = make_valid_order(customer_email="bad-email")
    result = service.process_order(order)
    assert result["success"] is False
    assert result["transaction_id"] is None
    # Inventory should NOT have changed
    assert inventory["P001"] == 100


def test_service_discount_reflected_in_result():
    service = make_service()
    order = make_valid_order(
        membership="gold",
        items=[{"product_id": "P001", "name": "Widget A", "quantity": 4, "unit_price": 25.00}],
        coupon_code=None,
    )
    # subtotal = 100, gold = 10% = 10
    result = service.process_order(order)
    assert result["success"] is True
    assert result["discount"] == 10.0, f"Expected discount 10.0, got {result['discount']}"


def test_service_paypal_order():
    service = make_service()
    order = make_valid_order(payment_method="paypal")
    result = service.process_order(order)
    assert result["success"] is True
    assert result["transaction_id"].startswith("PP-")


def test_service_no_discount_for_no_membership_no_coupon():
    service = make_service()
    order = make_valid_order(membership="none", coupon_code=None)
    result = service.process_order(order)
    assert result["success"] is True
    assert result["discount"] == 0.0


# =============================================================================
# Test Runner
# =============================================================================

def main():
    all_tests = [
        # OrderValidator
        ("OrderValidator: accepts valid order", test_validator_accepts_valid_order),
        ("OrderValidator: rejects missing email", test_validator_rejects_missing_email),
        ("OrderValidator: rejects invalid email (no @)", test_validator_rejects_invalid_email),
        ("OrderValidator: rejects empty items", test_validator_rejects_empty_items),
        ("OrderValidator: rejects zero quantity", test_validator_rejects_zero_quantity),
        ("OrderValidator: rejects negative quantity", test_validator_rejects_negative_quantity),
        ("OrderValidator: rejects missing payment method", test_validator_rejects_missing_payment_method),
        ("OrderValidator: returns multiple errors", test_validator_returns_multiple_errors),
        # DiscountCalculator
        ("DiscountCalculator: no membership, no coupon = 0", test_discount_no_membership_no_coupon),
        ("DiscountCalculator: silver = 5%", test_discount_silver_membership),
        ("DiscountCalculator: gold = 10%", test_discount_gold_membership),
        ("DiscountCalculator: platinum = 15%", test_discount_platinum_membership),
        ("DiscountCalculator: bulk > $200 = 5%", test_discount_bulk_threshold),
        ("DiscountCalculator: coupon SAVE10 = $10", test_discount_coupon_save10),
        ("DiscountCalculator: membership + coupon combined", test_discount_combined_membership_and_coupon),
        ("DiscountCalculator: invalid coupon = $0", test_discount_invalid_coupon_ignored),
        # PaymentProcessor
        ("PaymentProcessor: credit card succeeds", test_payment_credit_card_success),
        ("PaymentProcessor: paypal succeeds", test_payment_paypal_success),
        ("PaymentProcessor: unknown method fails", test_payment_unknown_method_fails),
        ("PaymentProcessor: unique transaction IDs", test_payment_generates_unique_transaction_ids),
        # EmailNotifier
        ("EmailNotifier: returns True on success", test_email_notifier_returns_true),
        # InventoryUpdater
        ("InventoryUpdater: decrements correctly", test_inventory_updates_correctly),
        ("InventoryUpdater: handles multiple items", test_inventory_updates_multiple_items),
        ("InventoryUpdater: skips unknown products", test_inventory_skips_unknown_products),
        # OrderService
        ("OrderService: successful end-to-end order", test_service_successful_order),
        ("OrderService: invalid order returns errors", test_service_invalid_order_returns_errors),
        ("OrderService: invalid order does not charge", test_service_invalid_order_does_not_charge),
        ("OrderService: discount reflected in result", test_service_discount_reflected_in_result),
        ("OrderService: PayPal order works", test_service_paypal_order),
        ("OrderService: no discount when not applicable", test_service_no_discount_for_no_membership_no_coupon),
    ]

    print("=" * 60)
    print("SRP Exercise — Test Suite")
    print("=" * 60)

    passed = 0
    failed = 0
    skipped = 0

    for name, fn in all_tests:
        result = run_test(name, fn)
        if result:
            passed += 1
        else:
            # Distinguish between failures and skips
            try:
                fn()
                passed += 1
            except NotImplementedError:
                skipped += 1
            except Exception:
                failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} not yet implemented")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
