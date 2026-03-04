# Python LLD Masterclass

> A complete, hands-on Low-Level Design (LLD) learning resource for FAANG interviews — built with Python.

---

## What is this?

This is a self-contained study + practice setup covering everything you need for LLD interviews:

- Theory with real-world analogies
- Runnable code examples
- Stub-based exercises with test-driven feedback
- 15 full FAANG-style LLD problems
- Cheatsheets for quick revision
- Interview strategy guide

---

## How to Use

### 1. Clone and set up
```bash
git clone https://github.com/agarvin2002/lld-gym.git
cd lld-gym
pip install -r requirements.txt
bash setup_practice.sh   # prevents your starter.py edits from being tracked by git
```

### 2. Pick a module and start reading
Each topic has a `theory.md` — read it first.

### 3. Run the examples
```bash
python 01_oop_foundations/01_classes_and_objects/examples/example1_basic_class.py
```

### 4. Attempt the exercise
Open `exercises/starter.py`, fill in the stubs, then run tests:
```bash
pytest 01_oop_foundations/01_classes_and_objects/exercises/tests.py -v
```

### 5. For LLD problems
```bash
# Read the problem
cat 04_lld_problems/01_parking_lot/problem.md

# Implement your solution in starter.py, then test level by level
pytest 04_lld_problems/01_parking_lot/tests/test_basic.py -v
pytest 04_lld_problems/01_parking_lot/tests/test_extended.py -v
pytest 04_lld_problems/01_parking_lot/tests/test_edge.py -v
```

### 6. Compare with reference solution
Only after you've attempted it:
```bash
cat 04_lld_problems/01_parking_lot/solution/solution.py
cat 04_lld_problems/01_parking_lot/solution/explanation.md
```

---

## Modules

| # | Module | Topics |
|---|--------|--------|
| 01 | [OOP Foundations](01_oop_foundations/) | Classes, Encapsulation, Inheritance, Polymorphism, Abstraction |
| 02 | [SOLID Principles](02_solid_principles/) | SRP, OCP, LSP, ISP, DIP |
| 03 | [Design Patterns](03_design_patterns/) | 13 patterns — Creational, Structural, Behavioral |
| 04 | [LLD Problems](04_lld_problems/) | 15 FAANG-style problems |
| 05 | [Concurrency](05_concurrency/) | Threading, Locks, Thread-safe patterns |
| — | [Cheatsheets](cheatsheets/) | Quick reference for revision |
| — | [Interview Guide](interview_guide/) | How to approach LLD interviews |

---

## Recommended Study Order

```
Week 1-2  → Module 01: OOP Foundations
Week 2-3  → Module 02: SOLID Principles
Week 3-5  → Module 03: Design Patterns
Week 6-9  → Module 04: LLD Problems (Tier 1 first)
Week 10   → Module 05: Concurrency
Week 11+  → Mock interviews using Interview Guide
```

---

## LLD Problems (15 Total)

| Tier | Problem | Key Concepts |
|------|---------|-------------|
| 1 | Parking Lot | Polymorphism, Strategy |
| 1 | Elevator System | State machine, Scheduling |
| 1 | ATM System | State machine, Chain of responsibility |
| 1 | Library Management | CRUD, Relationships |
| 1 | Hotel Booking | Availability, Concurrency |
| 2 | Movie Ticket Booking | Concurrency, Locking |
| 2 | Ride Sharing (Uber) | Real-time matching, Observer |
| 2 | Food Delivery | Order lifecycle, State |
| 2 | Chess | Game loop, OOP modeling |
| 2 | Snake & Ladders | Game engine, Factory |
| 3 | Rate Limiter | Token bucket, Sliding window |
| 3 | LRU Cache | OrderedDict, Eviction |
| 3 | Pub/Sub System | Observer, Threading |
| 3 | Logging Framework | Singleton, Chain of responsibility |
| 3 | Vending Machine | State machine |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — contributions welcome!

---

## License

[MIT](LICENSE)
