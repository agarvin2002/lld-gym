# LLD Problem: ATM System

## Problem Summary

Design an ATM that handles card operations, PIN verification, and banking transactions using a state machine.

## Clarifying Questions to Ask

1. What transaction types are supported? (balance inquiry, withdraw, deposit)
2. What happens after 3 wrong PINs?
3. Do we need multiple accounts per card?
4. What denominations does the ATM dispense?
5. Is there a daily withdrawal limit?

**Assumptions:**
- Transactions: balance inquiry, withdraw, deposit
- 3 wrong PINs → card locked
- One account per card (simplicity)
- Denominations: $100, $50, $20
- No daily limit for this exercise

## State Machine

```
IDLE ──────────────────────── (insert_card) ──────────────────────→ CARD_INSERTED
CARD_INSERTED ─────────────── (enter_pin correct) ────────────────→ PIN_VERIFIED
CARD_INSERTED ─────────────── (enter_pin wrong x3) ───────────────→ IDLE (card locked)
PIN_VERIFIED ──────────────── (select balance) ────────────────────→ IDLE (show balance)
PIN_VERIFIED ──────────────── (select withdraw) ───────────────────→ DISPENSING
PIN_VERIFIED ──────────────── (select deposit) ────────────────────→ IDLE (deposit done)
DISPENSING ────────────────── (dispense complete) ─────────────────→ IDLE
Any state ─────────────────── (cancel / eject_card) ──────────────→ IDLE
```

## Key Design Decisions

- **State Pattern**: each ATM state is a class that handles allowed operations
- **Account** class holds balance and PIN
- **CashDispenser** handles denomination logic

## Entities

```
ATM
├── state: ATMState
├── card: Card | None
├── account: Account | None
└── cash_dispenser: CashDispenser

ATMState (Enum): IDLE, CARD_INSERTED, PIN_VERIFIED, DISPENSING

Card: card_number, pin_hash
Account: account_id, balance, is_locked
CashDispenser: available_cash, dispense(amount) → dict[int, int]
```

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **State** | ATM behavior governed by `ATMState` enum (IDLE → CARD_INSERTED → PIN_VERIFIED → DISPENSING) |
| **Strategy** | Cash dispenser uses a greedy denomination algorithm |
| **SRP** | `Account` holds balance/PIN; `ATM` manages session state; `CashDispenser` manages physical cash |
| **Guard clauses** | `_require_state()` enforces valid transitions at method entry |

**See also:** Module 03 → [State](../../03_design_patterns/behavioral/state/), [Strategy](../../03_design_patterns/behavioral/strategy/)
