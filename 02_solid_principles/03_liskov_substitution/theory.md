# Liskov Substitution Principle

## What is it?

If `B` is a subtype of `A`, you should be able to use `B` wherever `A` is expected without breaking anything. A subclass must honor the same behavioral contract as its parent. Callers should not need to check which specific subtype they have.

## Analogy

A Zomato delivery partner and a Swiggy delivery partner both deliver food. You should be able to swap one for the other without changing how the order system works. If swapping breaks the flow, the "is-a delivery partner" claim is false.

## Minimal code

```python
# Violation — Square breaks Rectangle's contract
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = self.height = w  # breaks the contract!
    def set_height(self, h):
        self.width = self.height = h

r = Square(1, 1)
r.set_width(5)
r.set_height(4)
print(r.area())  # prints 16, not 20 — LSP violated

# Fix — separate classes with a shared interface
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Rectangle(Shape):
    def __init__(self, w, h): self.width = w; self.height = h
    def area(self): return self.width * self.height

class Square(Shape):
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2
```

## Real-world uses

- **Payment methods**: `CreditCard` and `GiftCard` both process payments. But `GiftCard` cannot be refunded, so it should NOT inherit from a `RefundablePayment` base — only from `PaymentMethod`.
- **Vehicle types**: `Car` and `Bicycle` are both vehicles. `Bicycle` cannot accelerate on a highway lane, so they share a `Vehicle` base but the highway planner only works with `MotorVehicle`.
- **Notification senders**: `SMSSender` and `EmailSender` are both senders. Swapping one for the other in a notification service should require no code changes in the caller.

## One mistake

Making `GiftCard` extend `RefundablePayment` and raising `NotImplementedError` in `refund()`. Now callers who call `refund()` on a `PaymentMethod` variable get a surprise runtime error. The contract was broken silently.

## Composition over inheritance

When a class cannot fully honor the parent's contract, use composition instead of inheritance. A `GiftCard` that "has a" balance and "has a" payment processor is cleaner than a `GiftCard` that "is a" `RefundablePayment` but secretly can't refund. Use inheritance only when the subtype is truly a safe substitute for the parent in every situation.

## What to do next

- See `examples/example1_classic_rectangle.py` for the rectangle-square violation and fix.
- See `examples/example2_correct_hierarchy.py` for a hierarchy with no forced empty methods.
- Open `exercises/starter.py` and implement the payment hierarchy where `GiftCard` only inherits `PaymentMethod`.
