# Explanation: LSP Payment Hierarchy

## The Key Design Decision: Split the Interface

The naive approach:
```python
class PaymentMethod(ABC):
    def process(amount): ...
    def refund(transaction_id): ...  # GiftCard can't do this!
```

GiftCard would be forced to implement `refund()` — either with `pass` (silently does nothing) or `raise NotImplementedError` (surprise exception). Both violate LSP.

## The LSP-Compliant Fix
```python
class PaymentMethod(ABC):
    def process(amount): ...          # ALL methods can process

class RefundablePayment(PaymentMethod, ABC):
    def refund(transaction_id): ...   # Only some methods can refund
```

Now:
- `GiftCard(PaymentMethod)` — can process, can't refund, and that's explicit in the type
- `CreditCard(RefundablePayment)` — can process AND refund
- Code that needs refunds accepts `RefundablePayment` (not just `PaymentMethod`)

## Substitution in Practice
```python
def charge(method: PaymentMethod, amount):  # accepts any payment method
    return method.process(amount)

def issue_refund(method: RefundablePayment, tid):  # only refundable types
    return method.refund(tid)

# GiftCard works for charge() but can't be passed to issue_refund()
# This is CORRECT behavior, enforced by the type system
```

## Connection to ISP
This solution also demonstrates ISP: we split the fat interface into smaller ones (`PaymentMethod` and `RefundablePayment`), so clients only depend on what they need.
