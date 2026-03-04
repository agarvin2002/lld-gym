# Solution Explanation: Polymorphic Discount System

## What Just Happened?

You built a system where an `Order` applies discounts without knowing which type
of discount it has. This is the core of polymorphism: **one interface, many behaviors**.

---

## The Key Insight: No `isinstance()` in Order

Look at `Order.final_price()`:

```python
def final_price(self) -> float:
    return self.discount.apply(self.price)
```

That is the entire method. No `if`, no `elif`, no `isinstance()`. It does not
matter whether `self.discount` is a `NoDiscount`, `PercentageDiscount`,
`FixedDiscount`, or something you write tomorrow. The call `discount.apply(price)`
always does the right thing for the type behind it.

Compare what this would look like *without* polymorphism:

```python
def final_price(self) -> float:
    if isinstance(self.discount, NoDiscount):
        return self.price
    elif isinstance(self.discount, PercentageDiscount):
        return self.price * (1 - self.discount.percent / 100)
    elif isinstance(self.discount, FixedDiscount):
        return max(0.0, self.price - self.discount.amount)
    elif isinstance(self.discount, BuyOneGetOneDiscount):
        return self.price / 2
    else:
        raise ValueError(f"Unknown discount: {type(self.discount)}")
```

Every new discount type requires editing `Order`. The `isinstance` version
violates the **Open/Closed Principle**: Order is not closed for modification.

---

## The Strategy Pattern

What you built is called the **Strategy pattern**:

- The *context* (`Order`) has a goal: calculate a final price.
- The *strategy* (`Discount`) defines how to achieve it.
- The context delegates to the strategy: `discount.apply(price)`.
- The strategy can be swapped at runtime: `apply_discount(new_discount)`.

```
Order ──delegates──▶ Discount (interface)
                         ▲
              ┌──────────┼──────────┬────────────┐
         NoDiscount  Percentage  Fixed       BOGO
```

This pattern appears constantly in real codebases:
- Sorting algorithms (QuickSort, MergeSort as strategies)
- Compression algorithms (gzip, brotli, lzma as strategies)
- Authentication methods (JWT, session, OAuth as strategies)
- Payment gateways (Stripe, PayPal, Crypto as strategies)

---

## Why ABC Instead of Protocol?

The `Discount` base class uses `abc.ABC`. An alternative is `typing.Protocol`:

```python
from typing import Protocol

class Discount(Protocol):
    def apply(self, price: float) -> float: ...
```

### ABC approach (chosen here):
- Python **enforces** the contract: instantiating a class without `apply()`
  raises `TypeError` at object creation time.
- `isinstance(obj, Discount)` works natively.
- Explicit class hierarchy — you can see the relationship in the code.
- Best when: you control all the implementations.

### Protocol approach:
- No inheritance required. Any class with `apply()` satisfies it.
- Allows third-party classes to be used as discounts without modification.
- Type checkers (mypy/pyright) enforce the contract at analysis time.
- Best when: you need to work with external code you cannot inherit from.

For this exercise, ABC is the right choice because we own all the discount
classes and want Python to enforce the contract at runtime.

---

## The Null Object Pattern: `NoDiscount`

`NoDiscount` is more than just the trivial case. It is an implementation of
the **Null Object pattern**: instead of `None`, we use an object that has the
right interface but does nothing.

Without it, every place that uses `Order` might need:

```python
if order.discount is not None:
    price = order.discount.apply(price)
else:
    price = order.price
```

With `NoDiscount`, the caller never needs this check. The interface is always
consistent. `NoDiscount().apply(100)` just returns `100` — no special casing.

---

## Edge Case: Clamping in `FixedDiscount`

```python
def apply(self, price: float) -> float:
    return max(0.0, price - self.amount)
```

Using `max(0.0, ...)` is a pattern called **clamping**. It enforces a lower
bound. This is a business rule: a discount cannot make you profit from a
customer. The invariant (`result >= 0`) is encoded once, in one place,
inside `FixedDiscount`. The caller (`Order`) does not need to check for it.

---

## Extensibility: Adding TieredDiscount

The solution includes `TieredDiscount` as a bonus:

```python
class TieredDiscount(Discount):
    def apply(self, price: float) -> float:
        if price > 100:
            return price * 0.80
        elif price > 50:
            return price * 0.90
        else:
            return price
```

Notice: `Order` does not change at all. `NoDiscount`, `PercentageDiscount`,
and `FixedDiscount` do not change. Tests for existing classes do not change.
You only add one new class. This is the **Open/Closed Principle** working in
your favor.

---

## Testing Insight

The test file includes a `TestPolymorphism` class that treats all discounts
uniformly:

```python
discounts: list[Discount] = [
    NoDiscount(),
    PercentageDiscount(10),
    FixedDiscount(5),
    BuyOneGetOneDiscount(),
]
for discount in discounts:
    result = discount.apply(price)
    assert result >= 0.0
```

This kind of **contract test** verifies that all implementations satisfy the
shared invariant (`result >= 0`). If you add a new discount type, you just
add it to this list — the test structure does not change.

---

## Summary

| Concept | Where it appears |
|---|---|
| Polymorphism | `Order.final_price()` calls `discount.apply()` without knowing the type |
| Strategy pattern | `apply_discount()` swaps the algorithm at runtime |
| Null Object pattern | `NoDiscount` eliminates `if discount is None` checks |
| Open/Closed Principle | Adding `TieredDiscount` requires zero changes to existing code |
| Clamping invariant | `FixedDiscount` owns the "no negative price" rule |
| Contract tests | `TestPolymorphism` verifies all types satisfy the interface |

The next step in your LLD journey: the **Strategy pattern** you built here is
one of the original Gang of Four design patterns. You will see it again (with
more context) in the design patterns module.
