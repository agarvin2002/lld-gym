# Design: ATM System

## Clarifying Questions
1. What operations? (balance check, withdraw, deposit, PIN change?)
2. How many PIN attempts before card is locked?
3. Do we need multi-currency or denomination selection?
4. Is cash dispenser in scope?
5. Thread safety — can multiple sessions run concurrently?

**Decisions**: Support balance, withdraw, deposit. Lock after 3 failed PIN attempts. CashDispenser with greedy denomination algorithm. Single-session model (one card at a time per ATM).

## Core Entities

| Entity | Responsibility |
|--------|---------------|
| `ATM` | Orchestrates the session lifecycle; enforces state guards |
| `ATMState` | Enum: IDLE / CARD_INSERTED / PIN_VERIFIED / DISPENSING |
| `Card` | Maps card number → account ID |
| `Account` | Holds balance, PIN, lock status, failed attempt counter |
| `CashDispenser` | Tracks cash inventory; dispenses using greedy algorithm |
| `InvalidStateError` | Raised when an operation is called in the wrong state |

## State Machine

```
         insert_card()
  IDLE ──────────────────► CARD_INSERTED
   ▲                              │
   │ eject_card()          enter_pin() ✓
   │◄─────────────────────────────┤
   │                              ▼
   │                        PIN_VERIFIED
   │                        │           │
   │            withdraw()  │           │ get_balance() / deposit()
   │                        ▼           │ (stay in PIN_VERIFIED)
   │                   DISPENSING       │
   │                        │           │
   └────────────────────────┴───────────┘
              eject_card() / session complete
```

## ASCII Class Diagram

```
┌─────────────────────────┐        ┌─────────────────┐
│           ATM           │        │   CashDispenser  │
│  - state: ATMState      │        │  - _cash: int    │
│  - _current_card: Card  │        │  - _denoms: list │
│  - _accounts: dict      │        ├─────────────────┤
│  - _dispenser           │───────►│ + dispense(amt) │
├─────────────────────────┤        │ + can_dispense() │
│ + insert_card(card)     │        └─────────────────┘
│ + enter_pin(pin) → bool │
│ + get_balance() → float │        ┌─────────────────┐
│ + withdraw(amount)      │        │     Account      │
│ + deposit(amount)       │        │  - balance       │
│ + eject_card()          │        │  - pin           │
│ - _require_state(state) │        │  - is_locked     │
└─────────────────────────┘        │  - failed_tries  │
                                   ├─────────────────┤
┌─────────────────┐                │ + verify_pin()   │
│      Card       │                └─────────────────┘
│  - card_number  │
│  - account_id   │
└─────────────────┘
```

## Key Design Decisions

**`_require_state()` guard**: Every public method calls `self._require_state(ATMState.X)` first. This keeps state validation DRY — one line per method instead of repeated `if` blocks.

**Account locking**: After 3 failed PIN attempts, `account.is_locked = True`. Subsequent `verify_pin()` calls return `False` immediately regardless of PIN.

**Greedy denomination algorithm**: `CashDispenser.dispense(amount)` uses denominations `[100, 50, 20]` in descending order. Raises `ValueError` if the amount can't be made (e.g., $15 with only $20 bills).

**Single-ATM, single-session**: The `_lock` on `ATM` prevents concurrent card insertions. For a network of ATMs, each ATM instance is independent; account state would live in a shared database.

## Extensibility Points
- **New operations**: add method + `_require_state(ATMState.PIN_VERIFIED)` guard
- **Different dispensing logic**: inject a `DispensingStrategy` ABC
- **Network ATM**: replace `_accounts` dict with a `BankService` interface
- **Receipt printing**: add `ReceiptPrinter` observer triggered after transactions
