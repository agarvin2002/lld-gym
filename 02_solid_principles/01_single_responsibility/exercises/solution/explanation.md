# SRP Exercise — Solution Explanation

## What We Did

We took a monolithic `OrderProcessor` god class with five distinct responsibilities and split it into six focused classes: five single-responsibility workers and one orchestrator.

---

## Identifying the Responsibilities

The first step was to ask: **"What are the different reasons this class might need to change?"**

For `OrderProcessor`, there were five distinct change vectors:

| # | Change Vector | Who Drives the Change | Class Created |
|---|---|---|---|
| 1 | Validation rules change | Product team / QA | `OrderValidator` |
| 2 | Discount tiers change | Marketing / Finance | `DiscountCalculator` |
| 3 | Payment provider changes | DevOps / Finance | `PaymentProcessor` |
| 4 | Email template or provider changes | Marketing | `EmailNotifier` |
| 5 | Inventory system changes | Warehouse / Backend team | `InventoryUpdater` |

Each of these is driven by a **different organizational stakeholder**. When Marketing updates the email template, they should not need to read code that charges credit cards. The separation makes that possible.

---

## Design Decisions

### 1. Returning Tuples for Rich Results

`OrderValidator.validate()` returns `(bool, list[str])` instead of raising an exception. This is a deliberate design choice:

- Validation failures are **expected** outcomes, not exceptional ones
- Returning a list of errors allows callers to show all problems at once, not just the first one
- This is consistent with how form validation works across most frameworks

```python
is_valid, errors = self.validator.validate(order)
if not is_valid:
    return {"success": False, "errors": errors, ...}
```

### 2. DiscountCalculator Has No External State

The `DiscountCalculator` uses class-level constants (`MEMBERSHIP_DISCOUNTS`, `VALID_COUPONS`) rather than fetching them from a database. This is appropriate for the exercise.

In a production system, these values would likely be injected via a `DiscountRuleRepository` — which would then make `DiscountCalculator` depend on an abstraction (DIP), not a hardcoded dict. But that is a concern for Module 05.

### 3. Skipping Unknown Inventory Items Silently

`InventoryUpdater.update()` skips products not found in the inventory rather than failing. This is a deliberate product decision: an order that was already validated and paid should not fail at the inventory step. In production, this would trigger a monitoring alert, but the order would still succeed.

### 4. OrderService Calculates Subtotal Too

Notice that `OrderService.process_order()` also computes `subtotal` to determine `final_total`. You might ask: is that duplication of `DiscountCalculator`'s subtotal computation?

Yes — and that's intentional. `DiscountCalculator` computes the subtotal *to calculate discounts*. `OrderService` needs the subtotal *to determine what to charge*. These are two different uses of the same number.

An alternative is to have `DiscountCalculator.calculate()` return both the discount amount AND the subtotal. Or to extract a `compute_subtotal()` utility. For this exercise, the simple approach is cleaner.

---

## How SRP Enabled Testability

Before the refactor, testing any single concern required the entire `OrderProcessor` to be instantiated. Changing inventory logic meant risking payment logic. There was no way to test validation without also having an inventory dict present.

After the refactor:

```python
# Test ONLY validation — no database, no payment, no email
def test_invalid_email():
    validator = OrderValidator()
    is_valid, errors = validator.validate({"customer_email": "bad"})
    assert not is_valid

# Test ONLY discount logic — no external dependencies at all
def test_gold_discount():
    calc = DiscountCalculator()
    discount = calc.calculate({"membership": "gold", "items": [...]})
    assert discount == 10.0
```

Each class can be instantiated and tested with zero infrastructure. That is the direct testing benefit of SRP.

---

## What "Reason to Change" Means in Practice

The phrase "reason to change" is more concrete than it sounds. Ask yourself:

> "If I received a Jira ticket to change X, which file would I open?"

- **"Change SAVE10 coupon to give $15 off instead of $10"** → open `DiscountCalculator`
- **"Switch from SMTP to SendGrid for emails"** → open `EmailNotifier`
- **"Add a fraud check before charging payment"** → open `OrderService` (add a step to the workflow)
- **"Require phone number on all orders"** → open `OrderValidator`

If the answer is always "I'd open only one file for each of these tickets," your SRP is working correctly.

---

## What Happens When We Add a New Step

Suppose we need to add a **fraud check** before charging payment. In the god class, we would insert code into the middle of `process_order()` and risk breaking the discount calculation or email logic around it.

In the refactored design:

```python
class FraudDetector:
    def is_suspicious(self, order: dict[str, Any]) -> bool:
        # New class, new responsibility, zero risk to existing code
        ...

class OrderService:
    def __init__(self, ..., fraud_detector: FraudDetector) -> None:
        self.fraud_detector = fraud_detector

    def process_order(self, order):
        is_valid, errors = self.validator.validate(order)
        if not is_valid:
            return ...

        # New step inserted cleanly
        if self.fraud_detector.is_suspicious(order):
            return {"success": False, "errors": ["Order flagged for fraud review"]}

        discount = self.discount_calculator.calculate(order)
        ...
```

The new step is added to the workflow with minimal risk. Each existing class remains unchanged. This is SRP enabling extensibility — which leads naturally to the Open/Closed Principle in Module 02.

---

## Common Mistakes to Avoid

1. **Putting `DiscountCalculator` logic inside `OrderService`**: The orchestrator should not know discount rules. It only knows the sequence of steps.

2. **Making `OrderValidator` raise exceptions instead of returning errors**: Use exceptions for truly unexpected failures. Validation is expected failure handling.

3. **Passing `OrderService` to every class**: Each class should know only what it needs. `PaymentProcessor` does not need `OrderValidator`.

4. **Forgetting that `InventoryUpdater` needs the inventory injected**: The inventory data source is an external dependency. Inject it; don't hardcode it.
