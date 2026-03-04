# Exercise: Payment Method Hierarchy (LSP)

## Problem

You're building a payment system. The base class `PaymentMethod` has a `process(amount)` method and a `refund(amount)` method. A naive design puts both methods on every payment type — but **gift cards can't be refunded** (the balance is consumed).

A violation of LSP would be:
```python
class GiftCard(PaymentMethod):
    def refund(self, amount):
        raise NotImplementedError("Gift cards cannot be refunded")  # ❌ violates LSP
```

Calling code that does `for payment in payments: payment.refund(100)` would crash.

## Your Task

Design a hierarchy that obeys LSP:

1. `PaymentMethod` — abstract base with only `process(amount) → bool`
2. `RefundablePayment(PaymentMethod)` — abstract mixin that adds `refund(amount) → bool`
3. Implement:
   - `CreditCard(RefundablePayment)` — both process and refund work
   - `DebitCard(RefundablePayment)` — both process and refund work
   - `GiftCard(PaymentMethod)` — only process (no refund method at all)

## Constraints
- `GiftCard` must NOT have a `refund()` method — not even one that raises
- Code that only uses `PaymentMethod` must work safely with all three types
- Code that uses `RefundablePayment` can call `refund()` safely

## Starter File
Edit `starter.py`. Run tests with:
```bash
pytest tests.py -v
```
