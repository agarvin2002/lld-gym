# Exercise 04: Polymorphic Discount System

## Goal

Build a flexible discount system using polymorphism. By the end you will
have practiced: defining a shared interface, implementing it multiple ways,
and writing code that works with any discount type without `isinstance()` chains.

---

## Background

An e-commerce platform needs to support multiple discount strategies:
- No discount (default)
- Percentage-based discount (e.g. 20% off)
- Fixed-amount discount (e.g. $10 off)
- Buy-one-get-one (half price)

The `Order` class should accept *any* discount object and apply it without
knowing which specific discount type it is.

---

## What to Build

### 1. `Discount` base class (or Protocol)

Define a base class with one method:

```python
def apply(self, price: float) -> float:
    """Return the discounted price."""
```

You may use either:
- An `ABC` with `@abstractmethod`
- A `typing.Protocol`

Both approaches are valid. Consider what the tradeoffs are.

---

### 2. `NoDiscount`

- `apply(price)` returns `price` unchanged.
- Useful as a default — avoids `if discount is None` checks everywhere.

---

### 3. `PercentageDiscount(percent: float)`

- Stores the percentage (e.g. `20.0` means 20%).
- `apply(price)` reduces the price by that percentage.
- Example: `PercentageDiscount(25).apply(100.0)` → `75.0`
- Edge case: 0% returns original price. 100% returns 0.

---

### 4. `FixedDiscount(amount: float)`

- Stores a fixed dollar amount to deduct.
- `apply(price)` subtracts the amount from the price.
- **Constraint:** The result must never go below `0.0`.
- Example: `FixedDiscount(10).apply(8.0)` → `0.0` (not `-2.0`)

---

### 5. `BuyOneGetOneDiscount`

- Represents a buy-one-get-one-free deal.
- `apply(price)` returns half the price (customer pays for one, gets two).
- Example: `BuyOneGetOneDiscount().apply(60.0)` → `30.0`

---

### 6. `Order(price: float, discount: Discount)`

- Stores the original price and a discount object.
- `final_price()` applies the discount and returns the result.
- `apply_discount(new_discount: Discount)` swaps the discount strategy.

```python
order = Order(price=100.0, discount=NoDiscount())
order.final_price()          # → 100.0

order.apply_discount(PercentageDiscount(20))
order.final_price()          # → 80.0
```

---

## Constraints

- `FixedDiscount` result must never be negative (clamp to 0.0).
- `PercentageDiscount` percent must be between 0 and 100 (inclusive).
- `Order.price` must be positive.
- No `isinstance()` checks in `Order`.

---

## Hints

1. Start with the `Discount` interface. Decide: ABC or Protocol? Both work — think about when each is better.

2. Implement `NoDiscount` first — it is the simplest and sets the pattern.

3. `FixedDiscount`: use `max(0.0, price - self.amount)` to prevent negative results.

4. `BuyOneGetOneDiscount`: just `price / 2` — no stored state needed.

5. `Order.apply_discount()` replaces the internal discount. This is the **Strategy pattern** — swapping an algorithm at runtime.

6. After implementing, ask yourself: what would you need to add a `TieredDiscount` that gives 10% off above $50 and 20% off above $100? The answer should be: *just a new class, no changes to Order*.

---

## What You Will Practice

- Defining a polymorphic interface
- Implementing the same interface multiple ways
- Writing code that is open to extension (new discount types) without modification
- The Strategy pattern (runtime algorithm swapping)
- Edge case handling within each implementation

---

## Files

| File | Purpose |
|---|---|
| `starter.py` | Stubs with TODOs — start here |
| `tests.py` | pytest tests — run with `pytest tests.py` |
| `solution/solution.py` | Full working solution (peek only after trying!) |
| `solution/explanation.md` | Detailed explanation of design decisions |
