# Exercise: Vending Machine (State Pattern)

## Problem

Implement a vending machine using the State pattern. The machine has 4 states and transitions based on user actions.

## State Machine

```
         insert_coin()
  IDLE ──────────────────► HAS_MONEY
   ▲                          │  │
   │ refund()                 │  │ select_product(code)
   │◄─────────────────────────┘  │
   │                             │ [product available]
   │                             ▼
   │                        DISPENSING
   │                             │
   │◄────────────────────────────┘
   │         dispense() done
   │
   │  [stock = 0]
   └─────────────────────────────► OUT_OF_STOCK
```

## Classes to implement

### `VendingMachineState(Enum)`
Values: `IDLE`, `HAS_MONEY`, `DISPENSING`, `OUT_OF_STOCK`

### `VendingMachine`
| Method | Description |
|--------|-------------|
| `__init__(products: dict[str, tuple[float, int]])` | `products` maps code → `(price, quantity)`. e.g. `{"A1": (1.50, 5)}` |
| `insert_coin(amount: float)` | Accepted in IDLE or HAS_MONEY. Accumulates `_balance`. |
| `select_product(code: str) -> str` | In HAS_MONEY: if enough balance and stock, move to DISPENSING. Returns product name. |
| `dispense() -> str` | In DISPENSING: reduces stock, deducts price from balance, returns to IDLE. Returns product name. |
| `refund() -> float` | In HAS_MONEY: returns `_balance` and goes to IDLE. |
| `restock(code: str, quantity: int)` | Adds stock; if was OUT_OF_STOCK, returns to IDLE. |

### Transitions
- Any method called in wrong state raises `InvalidStateError`
- After last item of any product is dispensed AND no products have stock, go to `OUT_OF_STOCK`

## Starter File
Edit `starter.py`. Run tests with:
```bash
pytest tests.py -v
```
