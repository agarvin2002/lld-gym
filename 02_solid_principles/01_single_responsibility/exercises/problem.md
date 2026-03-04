# Exercise: Refactor the OrderProcessor God Class

## Problem Statement

You are given an `OrderProcessor` class in `starter.py`. This class is a classic god class that handles the entire order lifecycle in one place:

1. **Validates** the order (checks required fields, item quantities, customer info)
2. **Calculates discounts** (membership discounts, bulk discounts, coupon codes)
3. **Charges payment** (processes credit card or PayPal transactions)
4. **Sends confirmation email** (builds and sends the order confirmation)
5. **Updates inventory** (decrements stock levels for each ordered item)

All five of these responsibilities are crammed into a single class with a single `process_order()` method.

## Your Task

Refactor `OrderProcessor` into multiple SRP-compliant classes. Each class should have exactly one reason to change.

### Classes to Create

1. **`OrderValidator`**
   - Validates that all required fields are present
   - Validates that item quantities are positive
   - Validates that the customer email is valid
   - Returns `(is_valid: bool, errors: list[str])`

2. **`DiscountCalculator`**
   - Calculates the appropriate discount based on membership level
   - Applies bulk discount if order total exceeds threshold
   - Applies coupon code if provided
   - Returns the final discount amount (float)

3. **`PaymentProcessor`**
   - Charges the customer via their preferred payment method
   - Handles both "credit_card" and "paypal" methods
   - Returns `(success: bool, transaction_id: str)`

4. **`EmailNotifier`**
   - Builds and sends the order confirmation email
   - Returns `True` if sent successfully

5. **`InventoryUpdater`**
   - Decrements stock for each item in the order
   - Returns `True` if all items were successfully updated

6. **`OrderService`**
   - Orchestrates all the above components
   - Has a `process_order(order: dict) -> dict` method
   - Returns a result dict with keys: `success`, `transaction_id`, `discount`, `errors`

## Constraints

- Use type hints on all methods
- Each class should only know about its own concern
- `OrderService` receives all collaborators via constructor injection
- Look at the starter stubs for the expected method signatures

## What Good Design Looks Like

After your refactoring:
- To change validation rules, you only touch `OrderValidator`
- To change discount logic, you only touch `DiscountCalculator`
- To switch from Stripe to PayPal, you only touch `PaymentProcessor`
- To change the email template, you only touch `EmailNotifier`
- To change the inventory system (e.g., from local dict to API call), you only touch `InventoryUpdater`
- To change the order workflow (e.g., add a fraud check step), you only touch `OrderService`

## Running the Tests

```bash
cd exercises/
python tests.py
```

All tests should pass with your implementation.

## Hints

- Start by identifying what data each class needs. `OrderValidator` needs the raw order dict. `DiscountCalculator` needs the order total and some customer metadata.
- Think about what each class returns. The return value is part of the contract.
- `OrderService` should call each component in the right sequence: validate → calculate discount → charge → notify → update inventory.
- If validation fails, `OrderService` should stop early and return the errors without proceeding to payment.
