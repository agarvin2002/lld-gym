# Explanation: ATM System

## State Pattern
The ATM's behavior depends entirely on its current state. The `_require_state()` helper enforces valid transitions:

```python
def withdraw(self, amount):
    self._require_state(ATMState.PIN_VERIFIED)  # guard
    ...
```

This means any operation called in the wrong state raises `InvalidStateError` — the caller knows exactly what went wrong.

## State Transition Table

| Current State | Operation | Next State |
|--------------|-----------|------------|
| IDLE | insert_card | CARD_INSERTED |
| CARD_INSERTED | enter_pin (correct) | PIN_VERIFIED |
| CARD_INSERTED | enter_pin (wrong x3) | IDLE (ejected) |
| PIN_VERIFIED | get_balance | PIN_VERIFIED |
| PIN_VERIFIED | withdraw | DISPENSING → IDLE |
| PIN_VERIFIED | deposit | PIN_VERIFIED |
| Any | eject_card | IDLE |

## Cash Dispenser — Greedy Algorithm
Uses largest denominations first:
```python
for denom in [100, 50, 20]:
    count = remaining // denom
    remaining -= denom * count
```
If remainder ≠ 0 after all denominations, the amount can't be dispensed (e.g., $15 with only $20 bills).

## Security Considerations
- PIN failures tracked per account, not per session
- Card locked after 3 failures — persists even if ATM is reset
- Account is locked at the `Account` level, not just the ATM

## Full GoF State Pattern Alternative
A more complete implementation would use State objects instead of enum + conditionals:
```python
class IdleState(ATMState):
    def insert_card(self, atm, card): ...
    def enter_pin(self, atm, pin): raise InvalidStateError(...)
```
This is cleaner for complex state machines (5+ states with many transitions) but overkill here.
