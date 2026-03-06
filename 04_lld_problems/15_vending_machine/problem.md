# Problem 15: Vending Machine

## Problem Statement

Design a vending machine that accepts coins, lets users select products, dispenses them, and gives change. The machine must enforce valid state transitions and handle edge cases like insufficient funds and out-of-stock items.

---

## States

```
IDLE → COIN_INSERTED → PRODUCT_SELECTED → DISPENSING → IDLE
         ↑                    |
         └────────────────────┘  (select different product)
```

| State | Description |
|-------|-------------|
| `IDLE` | Waiting for coins |
| `COIN_INSERTED` | Has credit, awaiting product selection |
| `PRODUCT_SELECTED` | Product chosen, ready to dispense |
| `DISPENSING` | Dispensing product + change |

---

## API

```python
class VendingMachine:
    def insert_coin(self, amount: float) -> None
    def select_product(self, code: str) -> str   # returns status message
    def dispense(self) -> str                     # returns "Dispensed: {name}. Change: ${x:.2f}"
    def refund(self) -> float                     # returns amount refunded, resets to IDLE
    def restock(self, code: str, quantity: int) -> None
    def current_state(self) -> VendingMachineState
    def balance(self) -> float
```

---

## Product Catalog

Products are loaded at construction time as `dict[code, (name, price, quantity)]`.

Example:
```python
products = {
    "A1": ("Cola", 1.50, 5),
    "B1": ("Chips", 2.00, 3),
    "C1": ("Water", 1.00, 10),
}
machine = VendingMachine(products)
```

---

## Rules

- `insert_coin` only allowed in `IDLE` or `COIN_INSERTED` states
- `select_product` only allowed in `COIN_INSERTED` state
- `dispense` only allowed in `PRODUCT_SELECTED` state
- `refund` allowed in `COIN_INSERTED` or `PRODUCT_SELECTED` states
- `restock` allowed in `IDLE` state only
- Calling a method in the wrong state raises `InvalidStateError`
- Selecting an out-of-stock product returns a message and stays in `COIN_INSERTED`
- Selecting a product with insufficient funds returns a message and stays in `COIN_INSERTED`
- Successful `dispense` gives change and returns to `IDLE`

---

## Error

```python
class InvalidStateError(Exception):
    pass
```

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **State** | `VendingMachineState`: IDLE → COIN_INSERTED → PRODUCT_SELECTED → DISPENSING → IDLE |
| **Guard clauses** | `_require_state()` raises `InvalidStateError` when an operation is called in the wrong state |
| **SRP** | `Product` is data; `VendingMachine` manages state transitions and inventory |

**See also:** Module 03 → [State](../../03_design_patterns/behavioral/state/), also compare with [ATM System](../03_atm_system/) which uses the same `_require_state()` guard pattern
