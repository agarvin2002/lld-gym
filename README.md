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

## Recommended Study Path

The material is designed for a 12-week sprint from zero to FAANG-ready. Follow the tiers in order — each tier builds directly on the previous one.

---

### Tier 1 — Foundations (Weeks 1–5)

Master these before touching the LLD problems.

| Week | Module | What to do | Goal |
|------|--------|-----------|------|
| 1 | [01 OOP Foundations](01_oop_foundations/) | Read all 5 theory files → run examples → complete exercises | Fluent in classes, encapsulation, inheritance, polymorphism, abstraction |
| 2 | [02 SOLID Principles](02_solid_principles/) | Read all 5 theory files → run examples → complete exercises | Can identify SOLID violations and apply fixes |
| 3–4 | [03 Design Patterns — Creational + Structural](03_design_patterns/) | Singleton, Factory Method, Abstract Factory, Builder, Decorator, Proxy, Facade, Adapter | Know 8 patterns cold |
| 5 | [03 Design Patterns — Behavioral (part 1)](03_design_patterns/) | Strategy, Observer, State | The 3 most common FAANG patterns |

**Tier 1 LLD Problems** — attempt after Week 5:

| # | Problem | Patterns to apply | Tests |
|---|---------|-------------------|-------|
| 01 | [Parking Lot](04_lld_problems/01_parking_lot/) | Strategy, Polymorphism, threading.Lock | test_basic → extended → edge |
| 02 | [Elevator System](04_lld_problems/02_elevator_system/) | Strategy (dispatch), State machine | test_basic → extended → edge |
| 03 | [ATM System](04_lld_problems/03_atm_system/) | State, guard clauses | test_basic → extended → edge |
| 04 | [Library Management](04_lld_problems/04_library_management/) | Observer, Strategy (fines) | test_basic → extended → edge |
| 05 | [Hotel Booking](04_lld_problems/05_hotel_booking/) | Strategy (pricing), State | test_basic → extended → edge |

---

### Tier 2 — Intermediate (Weeks 6–9)

Add the remaining behavioral patterns, then tackle more complex LLD problems.

| Week | Module | What to do | Goal |
|------|--------|-----------|------|
| 6 | [03 Behavioral Patterns (part 2)](03_design_patterns/) | Command, Iterator, Template Method, Chain of Responsibility | Complete the behavioral patterns set |
| 7–9 | [04 LLD Problems — Tier 2](04_lld_problems/) | Work through problems 06–10 below | Multi-entity designs with concurrent access |

**Tier 2 LLD Problems:**

| # | Problem | Patterns to apply | Difficulty notes |
|---|---------|-------------------|-----------------|
| 06 | [Movie Ticket Booking](04_lld_problems/06_movie_ticket_booking/) | State (seat), Facade | Seat locking under concurrency |
| 07 | [Ride Sharing](04_lld_problems/07_ride_sharing/) | State (driver + trip), Strategy (fare) | Two parallel state machines |
| 08 | [Food Delivery](04_lld_problems/08_food_delivery/) | State, Strategy, Observer | Long order lifecycle pipeline |
| 09 | [Chess](04_lld_problems/09_chess/) | Polymorphism (pieces), Command | Move validation per piece type |
| 10 | [Snake & Ladders](04_lld_problems/10_snake_and_ladders/) | Strategy (dice), State (game) | Simplest game engine to model cleanly |

---

### Tier 3 — Advanced (Weeks 10–12)

System-design-adjacent problems that require concurrency, algorithm knowledge, and careful API design.

| Week | Module | What to do | Goal |
|------|--------|-----------|------|
| 10 | [05 Concurrency](05_concurrency/) | Threading basics → Locks & Semaphores → Thread-safe patterns | Understand `threading.Lock`, `Condition`, `Semaphore` |
| 11 | [04 LLD Problems — Tier 3](04_lld_problems/) | Work through problems 11–15 | Deliver thread-safe, algorithm-correct designs |
| 12 | [Interview Guide](interview_guide/) | Practice verbal walkthroughs + mock sessions | Interview-ready |

**Tier 3 LLD Problems:**

| # | Problem | Patterns to apply | Key challenge |
|---|---------|-------------------|--------------|
| 11 | [Rate Limiter](04_lld_problems/11_rate_limiter/) | Strategy (algorithm), Proxy | Token Bucket vs Sliding Window; thread safety |
| 12 | [LRU Cache](04_lld_problems/12_lru_cache/) | Strategy (eviction), Proxy (thread-safe) | O(1) get+put with LFU variant |
| 13 | [Pub/Sub System](04_lld_problems/13_pub_sub_system/) | Observer, async delivery | Concurrent publish; snapshot isolation |
| 14 | [Logging Framework](04_lld_problems/14_logging_framework/) | Chain of Responsibility, Strategy, Template Method, Singleton | Handler chain with filter+format+emit |
| 15 | [Vending Machine](04_lld_problems/15_vending_machine/) | State, Strategy (payment) | Full state machine with guard clauses |

---

### Quick-revision Cheatsheets

Use these when revising before an interview:

- [OOP Cheatsheet](cheatsheets/oop_cheatsheet.md)
- [SOLID Cheatsheet](cheatsheets/solid_cheatsheet.md)
- [Design Patterns Cheatsheet](cheatsheets/design_patterns_cheatsheet.md)
- [LLD Interview Cheatsheet](cheatsheets/lld_interview_cheatsheet.md)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — contributions welcome!

---

## License

[MIT](LICENSE)
