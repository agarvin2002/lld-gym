# Explanation: Strategy Pattern — Discount System

## The Core Inversion

Without Strategy:
```python
def final_price(self):
    if self.discount_type == "percent":
        return self.total * (1 - self.percent / 100)
    elif self.discount_type == "fixed":
        return max(0, self.total - self.amount)
    elif ...   # grows forever
```

With Strategy:
```python
def final_price(self):
    return self._discount.apply(self.total)  # one line, forever
```

## Why `Order` doesn't need to change

Adding `LoyaltyDiscount` required zero changes to `Order`. The OCP is satisfied — `Order` is open for extension (via new strategies) but closed for modification.

## Testability

Each strategy is tested independently:
```python
assert PercentageDiscount(20).apply(100.0) == 80.0  # no Order needed
```

And `Order` is tested with a mock:
```python
class MockDiscount(DiscountStrategy):
    def apply(self, total): return total * 0.5

order = Order(100.0, MockDiscount())
assert order.final_price() == 50.0
```

## Key Design Details

**`apply()` is pure**: No side effects. Same input → same output. Strategies are stateless (after construction) and safe to reuse or share.

**Validation in `__init__`**: Invalid inputs raise `ValueError` at construction time, not later when `apply()` is called. Fail fast.

**`Order.total` is immutable from `apply()`'s perspective**: `apply()` receives the total, computes a new value, returns it. Never stores or mutates anything on the Order.
