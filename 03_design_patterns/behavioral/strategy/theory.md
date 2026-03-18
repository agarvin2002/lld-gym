# Strategy Pattern

## What is it?
Define a family of algorithms, wrap each one in its own class, and make them
interchangeable. The object that uses them (the "context") doesn't care which
one is plugged in — it just calls the same method.
Swapping behaviour at runtime requires no changes to the context class.

## Analogy
Swiggy lets you sort restaurants by Rating, Distance, or Delivery Time.
The app screen (context) doesn't change. Only the sorting algorithm (strategy)
swaps out when you pick a different option.

## Minimal code
```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float: ...

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class TenPercent(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.9

class Order:
    def __init__(self, total: float, discount: DiscountStrategy):
        self.total = total
        self._discount = discount

    def final_price(self) -> float:
        return self._discount.apply(self.total)

    def set_discount(self, d: DiscountStrategy) -> None:
        self._discount = d

order = Order(500.0, NoDiscount())
print(order.final_price())         # 500.0
order.set_discount(TenPercent())
print(order.final_price())         # 450.0
```

## Real-world uses
- Razorpay/Paytm: Credit Card, UPI, and Net Banking are swappable payment strategies
- Flipkart: flat, percentage, and BOGO discount strategies on checkout
- Rate limiters: Token Bucket vs Fixed Window vs Sliding Window — same interface, different algorithm

## One mistake
Putting the strategy selection logic back inside the context class. If `Order`
has `if discount_type == "percent": ...` it defeats the entire point — you are
back to a chain of conditionals.

## What to do next
See `examples/example1_sorting.py` for a classic sorting demo and
`examples/example2_payment.py` for a checkout system with multiple payment methods.
Then try `exercises/starter.py` — build a discount engine for an order system.
