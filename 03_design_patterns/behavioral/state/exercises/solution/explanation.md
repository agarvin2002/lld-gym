# Explanation: State Pattern — Vending Machine

## Why State (not if/elif chains)?

Without State, every method looks like:
```python
def insert_coin(self, amount):
    if self.state == "IDLE" or self.state == "HAS_MONEY":
        self._balance += amount
        self.state = "HAS_MONEY"
    elif self.state == "DISPENSING":
        raise InvalidStateError(...)
    elif self.state == "OUT_OF_STOCK":
        raise InvalidStateError(...)
```

With 4 states × 6 methods = 24 branches, all tangled in one class. Adding a 5th state (e.g. `MAINTENANCE`) requires editing all 6 methods.

## The `_require_state()` pattern

Every public method starts with one line:
```python
self._require_state(VendingMachineState.HAS_MONEY)
```

This replaces all the defensive `if self.state != X` checks. Single responsibility: the method does its job; `_require_state` enforces preconditions.

## State transition map

```
insert_coin()  → IDLE/HAS_MONEY → HAS_MONEY
select()       → HAS_MONEY      → DISPENSING
dispense()     → DISPENSING     → IDLE (or OUT_OF_STOCK)
refund()       → HAS_MONEY      → IDLE
restock()      → any            → IDLE (if was OUT_OF_STOCK)
```

## Key detail: `_check_out_of_stock()`

Called after `dispense()` and in `__init__`. Keeps the OUT_OF_STOCK transition in one place rather than scattered through every method that decrements stock.

## This exercise vs full State objects

This solution uses an Enum + guard methods (simpler, faster to write in an interview). The alternative — one class per state — is better when:
- Each state has >3-4 unique method implementations
- States need to hold their own data
- You want to add states without touching the context class at all

For a vending machine in an interview, the Enum approach wins on clarity and speed.
