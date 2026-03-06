# Design — Vending Machine

## Clarifying Questions (Interview Simulation)

Before drawing any class diagram, ask these in an interview:

1. What states does the machine go through? → IDLE → COIN_INSERTED → PRODUCT_SELECTED → DISPENSING → IDLE.
2. What happens if you insert coins then select an invalid product? → Return a descriptive string, stay in COIN_INSERTED.
3. Can you insert multiple coins? → Yes, balance accumulates in COIN_INSERTED state.
4. What denominations/currencies? → No denomination tracking; just a float balance.
5. What if a product is out of stock? → Return "Out of stock." string, do not transition.
6. Can you get a refund mid-flow? → Yes, from COIN_INSERTED or PRODUCT_SELECTED state.
7. Can admins restock products? → Yes, but only in IDLE state.
8. Thread safety? → Not required for this scope.

---

## Core Entities

### 1. VendingMachineState (Enum)
IDLE → COIN_INSERTED → PRODUCT_SELECTED → DISPENSING → IDLE.
`_require_state()` enforces transitions and raises `InvalidStateError`.

### 2. Product (Data Class)
Holds code, name, price, and current quantity. Products are stored in a dict by code.

### 3. VendingMachine
The complete state machine. Holds:
- `_products`: catalog
- `_state`: current state
- `_balance`: accumulated coins
- `_selected`: the chosen Product (set in PRODUCT_SELECTED, cleared after dispense/refund)

---

## Class Diagram (ASCII)

```
+------------------------------+
|       VendingMachine         |
+------------------------------+
| - _products: dict[str, Product] |------>  Product (1..*)
| - _state: VendingMachineState   |
| - _balance: float               |
| - _selected: Product | None     |
+------------------------------+
| + insert_coin(amount)        |
| + select_product(code) -> str|
| + dispense() -> str          |
| + refund() -> float          |
| + restock(code, quantity)    |
| - _require_state(*states)    |
| @ current_state (property)   |
| @ balance (property)         |
+------------------------------+

+---------------------------+
|         Product           |
+---------------------------+
| code: str                 |
| name: str                 |
| price: float              |
| quantity: int             |
+---------------------------+
```

---

## State Machine

```
           ┌─────────────────────────────────────────────────────────────┐
           │                                                             │
     ┌─────▼──────┐   insert_coin()   ┌──────────────────┐             │
     │    IDLE    │─────────────────>│  COIN_INSERTED   │             │
     └─────▲──────┘                  └────────┬─────────┘             │
           │                                  │                         │
           │                          select_product()                  │
           │                          (valid product,                   │
           │                           sufficient funds)                │
           │                                  │                         │
     refund()                                 ▼                         │
     dispense()           ┌───────────────────────────────┐            │
           │              │      PRODUCT_SELECTED          │─refund()──>│
           │              └───────────────┬───────────────┘            │
           │                              │                             │
           │                          dispense()                        │
           │                              │                             │
           │              ┌───────────────▼───────────────┐            │
           └──────────────│          DISPENSING            │            │
                          └───────────────────────────────┘            │
                          (transitions back to IDLE immediately)        │
                                                                        │
     restock() ──────────────────────────────────────────────> IDLE only│
                                                                        │
     ────────────────────────────────────────────────────────────────────┘
```

---

## Operation Details

| Operation | Allowed State(s) | Effect |
|-----------|-----------------|--------|
| `insert_coin(amount)` | IDLE, COIN_INSERTED | balance += amount; → COIN_INSERTED |
| `select_product(code)` | COIN_INSERTED | Validates code/stock/funds; → PRODUCT_SELECTED |
| `dispense()` | PRODUCT_SELECTED | Decrements qty, returns change; → IDLE |
| `refund()` | COIN_INSERTED, PRODUCT_SELECTED | Returns balance; → IDLE |
| `restock(code, qty)` | IDLE | Increments product quantity |

---

## select_product() Return Values

| Condition | Return Value |
|-----------|-------------|
| Code not found | `f"Product {code!r} not found."` |
| Out of stock | `"Out of stock."` |
| Insufficient funds | `f"Insufficient funds. Price: ${price:.2f}, Balance: ${balance:.2f}"` |
| Success | `f"Selected: {name}. Please dispense."` |

---

## Design Decisions & Trade-offs

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| State enum + `_require_state()` | Clean guard clauses; clear error messages | More verbose than if-else |
| Return strings from select/dispense | Easy to display to user; testable | Not strongly typed |
| Float balance | Simple; avoids integer penny arithmetic | Float precision edge cases |
| Products as dict by code | O(1) lookup | Assumes unique codes |
| No denomination tracking | Simplifies scope | Can't handle exact change issues |

---

## Extensibility

**Add denomination tracking:**
- Store `_coins: dict[float, int]` (denomination → count).
- `insert_coin()` accepts specific denominations.
- `dispense()` returns change as a denomination dict.

**Add admin interface:**
- Create an `AdminPanel` class that wraps VendingMachine for privileged operations.
- Enables price updates, adding new products, viewing sales history.

**Add multiple payment methods:**
- Introduce a `PaymentStrategy` ABC with `charge(amount) -> bool`.
- Inject into VendingMachine for card, QR code, etc.
