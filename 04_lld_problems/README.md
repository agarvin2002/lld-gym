# LLD Problems — Practice Set

This section contains 15 Low-Level Design problems organized into three difficulty tiers. Each problem follows a consistent structure so you can focus on thinking, not on navigating files.

---

## How to Use Each Problem (6-Step Framework)

Follow these six steps for every problem:

```
Step 1 — READ      Read problem.md fully. Answer every clarifying question yourself before reading the answers.
Step 2 — DESIGN    On paper (or a whiteboard), draw your class diagram before opening design.md.
Step 3 — COMPARE   Open design.md and compare your design. Note every difference and ask why.
Step 4 — CODE      Open starter.py. Fill in every TODO. Do not look at solution/ yet.
Step 5 — TEST      Run tests level by level: test_basic → test_extended → test_edge.
Step 6 — REVEAL    Only after all tests pass (or you are stuck for >30 min), open solution/solution.py.
```

Running tests:

```bash
# From the problem directory (e.g., 01_parking_lot/)
python -m pytest tests/test_basic.py -v
python -m pytest tests/test_extended.py -v
python -m pytest tests/test_edge.py -v
python -m pytest tests/ -v          # all at once
```

---

## Problem Tiers

### Tier 1 — Foundational (Problems 01–05)
Core OOP patterns. Focus on clean class hierarchies and single responsibility. Expected interview time: 30–40 minutes.

### Tier 2 — Intermediate (Problems 06–10)
Multiple interacting subsystems. Introduces behavioral patterns (Strategy, Observer, State). Expected interview time: 40–50 minutes.

### Tier 3 — Advanced (Problems 11–15)
Distributed-adjacent problems with concurrency, caching, and complex state management. Expected interview time: 50–60 minutes.

---

## Problem Table

| # | Problem | Tier | Key Patterns | Core Challenge |
|---|---------|------|--------------|----------------|
| 01 | Parking Lot | 1 | Strategy, Hierarchy | Spot-vehicle compatibility + fees |
| 02 | Elevator System | 1 | State, Strategy | Scheduling algorithm |
| 03 | ATM System | 1 | State | Lifecycle state machine |
| 04 | Library Management | 1 | Observer | Reservations + notifications |
| 05 | Vending Machine | 1 | State | Inventory + change dispensing |
| 06 | Hotel Booking | 2 | Strategy, Builder | Room search + pricing |
| 07 | Chess Game | 2 | Strategy | Move validation per piece |
| 08 | Ride Sharing | 2 | Observer, Strategy | Driver matching |
| 09 | Food Delivery | 2 | Observer, Chain of Resp. | Order lifecycle |
| 10 | Online Shopping Cart | 2 | Strategy, Decorator | Discounts + checkout |
| 11 | Rate Limiter | 3 | Strategy | Token bucket / sliding window |
| 12 | Cache System (LRU) | 3 | — | Eviction policies |
| 13 | Pub/Sub System | 3 | Observer | Topic routing + subscriptions |
| 14 | Splitwise | 3 | Strategy | Expense splitting algorithms |
| 15 | Movie Ticket Booking | 3 | Strategy, State | Seat locking + concurrency |

---

## Directory Structure

```
04_lld_problems/
├── README.md                    ← you are here
├── 01_parking_lot/
│   ├── problem.md               ← requirements + clarifying questions
│   ├── design.md                ← class diagram + design decisions
│   ├── starter.py               ← fill this in (Step 4)
│   ├── tests/
│   │   ├── test_basic.py
│   │   ├── test_extended.py
│   │   └── test_edge.py
│   └── solution/
│       ├── solution.py          ← open only after Step 5
│       └── explanation.md       ← design rationale
├── 02_elevator_system/
│   └── ... (same structure)
├── 03_atm_system/
│   └── ... (same structure)
└── ...
```

---

## Key Design Patterns Reference

| Pattern | When to Reach For It | Problems |
|---------|---------------------|----------|
| **Strategy** | Interchangeable algorithms (fee calculation, scheduling) | 01, 02, 06, 08 |
| **State** | Object lifecycle with well-defined states | 02, 03, 05 |
| **Observer** | One event triggers multiple reactions | 04, 08, 09 |
| **Factory** | Creating objects without specifying exact class | 01, 03 |
| **Singleton** | One instance needed system-wide | 01, 03 |
| **Decorator** | Adding behavior dynamically | 10 |

---

## Interview Tips

1. **Always clarify before coding.** Spend 3–5 minutes on clarifying questions. Interviewers reward this.
2. **Start with entities, not methods.** List nouns first (Car, Spot, Ticket), then verbs (park, unpark).
3. **Draw the class diagram first.** Code should follow the design, not the other way around.
4. **Think about extensibility.** "How would you add a new vehicle type?" should have a clean answer.
5. **Mention concurrency.** Even if not asked, note where thread safety matters and how you'd handle it.
6. **Know the trade-offs.** For every design decision, know what you gave up.
