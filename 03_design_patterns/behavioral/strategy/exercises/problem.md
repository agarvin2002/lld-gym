# Exercise: Order Discount System (Strategy Pattern)

## Problem

Build an e-commerce discount system where different discount strategies can be applied to an order at checkout.

## What to build

### `DiscountStrategy` (ABC)
- `apply(order_total: float) -> float` — returns the discounted total

### Concrete strategies
| Class | Behaviour |
|-------|-----------|
| `NoDiscount` | Returns total unchanged |
| `PercentageDiscount(percent)` | Reduces total by `percent`%. Validates 0 ≤ percent ≤ 100. |
| `FixedDiscount(amount)` | Subtracts fixed `amount`. Clamps to 0 (never goes negative). |
| `BuyOneGetOneFree` | Halves the total (you pay for every other item) |
| `LoyaltyDiscount(tier)` | `tier="silver"` → 5%, `tier="gold"` → 10%, `tier="platinum"` → 15% |

### `Order`
- `__init__(self, total: float, discount: DiscountStrategy)`
- `final_price() -> float` — applies discount, returns result
- `set_discount(discount: DiscountStrategy)` — swap strategy at runtime

## Constraints
- `Order.total` must not be mutated by `final_price()`
- `PercentageDiscount` with `percent < 0` or `percent > 100` raises `ValueError`
- `FixedDiscount` with `amount < 0` raises `ValueError`

## Run tests
```bash
pytest tests.py -v
```
