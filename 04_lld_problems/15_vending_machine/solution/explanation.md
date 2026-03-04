# Vending Machine — Solution Explanation

## State Machine Design

The machine is a Finite State Machine (FSM) with 4 states. Every public method starts by calling `_require_state()`, making illegal transitions impossible without exception handling scattered through client code.

```
IDLE ──insert_coin──→ COIN_INSERTED ──select_product──→ PRODUCT_SELECTED
 ↑                         │  ↑                               │
 └──────refund()────────────┘  └──────── (out-of-stock or     │
 └──────────────────────────────────────  insufficient funds)  │
 └──────────────────────dispense()─────────────────────────────┘
```

## `_require_state` centralizes guard logic

Instead of an `if self._state != X: raise` in every method, one helper handles it:

```python
def _require_state(self, *allowed):
    if self._state not in allowed:
        raise InvalidStateError(...)
```

`insert_coin` accepts `IDLE` or `COIN_INSERTED` (multiple coins), while `dispense` accepts only `PRODUCT_SELECTED`. The allowed states are declared at the call site, making each method's preconditions self-documenting.

## `select_product` returns messages, doesn't raise

Soft failures (out-of-stock, insufficient funds) return descriptive strings and keep the machine in `COIN_INSERTED` so the user can try another product or refund. This is intentional UX — not a bug. The state transition only happens on success.

## Floating-point change with `round()`

```python
change = round(self._balance - product.price, 2)
```

`round(..., 2)` prevents `1.50 - 1.00 = 0.4999999999999998` from appearing as change. A production system would use `Decimal` for financial accuracy.

## Refund resets `_selected`

Even when called from `PRODUCT_SELECTED`, `refund()` clears `self._selected = None`. This prevents a stale reference if `refund` is called mid-selection.

## State pattern vs Enum-based FSM

This solution uses an Enum + `_require_state`. An alternative is the full State pattern (separate class per state, like the design patterns module exercise). The Enum approach is simpler for small FSMs; the class-based State pattern scales better when each state needs significantly different behavior per method.
