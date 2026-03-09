# Module 02 — SOLID Principles

## Overview

SOLID is an acronym for five object-oriented design principles introduced by Robert C. Martin. These principles help you write software that is easier to maintain, extend, and test as systems grow in complexity.

---

## Why SOLID Matters

Every design decision at the class and interface level compounds over time. Violating these principles leads to:

- **Hard-to-test code** — a class that hardcodes its own dependencies cannot be unit tested
- **Fragile extensions** — adding a feature breaks existing, working functionality
- **Unreliable hierarchies** — a subclass that surprises callers destroys trust in your API
- **Unnecessary coupling** — one change ripples through unrelated modules
- **Difficult onboarding** — god classes with hundreds of lines are hard to reason about

---

## Table of Contents

| # | Principle | Short Form | Core Idea |
|---|-----------|------------|-----------|
| 1 | [Single Responsibility Principle](./01_single_responsibility/) | SRP | One class, one reason to change |
| 2 | [Open/Closed Principle](./02_open_closed/) | OCP | Open for extension, closed for modification |
| 3 | [Liskov Substitution Principle](./03_liskov_substitution/) | LSP | Subtypes must be substitutable for base types |
| 4 | [Interface Segregation Principle](./04_interface_segregation/) | ISP | Don't force clients to depend on unused interfaces |
| 5 | [Dependency Inversion Principle](./05_dependency_inversion/) | DIP | Depend on abstractions, not concretions |

---

## Each Principle Directory Contains

```
XX_principle_name/
├── theory.md                  # Explanation with analogy, minimal code, and real-world uses
├── examples/
│   ├── example1_*.py          # Shows the anti-pattern clearly
│   └── example2_*.py          # Advanced topic — shows the correct approach
└── exercises/
    ├── problem.md             # Exercise description
    ├── starter.py             # Skeleton code to fill in
    ├── tests.py               # Tests that must pass
    └── solution/
        ├── solution.py        # Complete working solution
        └── explanation.md     # Explanation of design decisions
```

---

## How the Five Principles Work Together

```
SRP  → "What does this class do?" (answer should be one thing)
OCP  → "How do I add new behavior?" (answer: extend, don't modify)
LSP  → "Can I trust this subtype?" (answer should always be yes)
ISP  → "What does this interface expose?" (answer: only what the client needs)
DIP  → "Who creates dependencies?" (answer: the caller, via injection)
```

**SRP + ISP** both reduce coupling — one at the class level, one at the interface level.
**OCP + LSP** both govern extension — OCP says add without modifying; LSP says extensions must be safe substitutes.
**DIP + OCP** are deeply linked — injecting interfaces (DIP) is how you achieve extensibility (OCP).

---

## Putting It All Together: A Payment Service

Consider designing a payment service that supports Razorpay, Paytm, and UPI.

**SRP** — `PaymentService` only orchestrates. `OrderValidator`, `PaymentLogger`, and each gateway class each have one job. Changing the logging format touches only `PaymentLogger`.

**OCP** — `RazorpayGateway`, `PaytmGateway`, and `UPIGateway` each implement `PaymentGatewayInterface`. Adding a new gateway is a new class — `PaymentService` is never modified.

**LSP** — Every gateway is a safe substitute. Code that calls `gateway.charge(amount)` works correctly for any gateway. No gateway raises `NotImplementedError` for a method it cannot support.

**ISP** — `RefundableGateway` is a separate interface from `PaymentGateway`. UPI (no refunds) implements only `PaymentGateway`. Credit card gateways implement both.

**DIP** — `PaymentService.__init__` accepts `PaymentGatewayInterface`, not a concrete class. Tests inject `MockGateway`. Switching from Razorpay to Paytm requires no change to `PaymentService` — only the injected object changes.

This pattern — one interface, multiple implementations, injected from outside — appears in every real system.

---

## Recommended Study Order

1. **SRP** — most intuitive; sets the foundation
2. **OCP** — introduces polymorphism patterns
3. **LSP** — clarifies what correct inheritance looks like
4. **ISP** — teaches focused, composable interfaces
5. **DIP** — brings it all together with dependency injection

---

## Quick Reference: Violation Smells

| Principle | Code Smell |
|-----------|------------|
| SRP | Class name contains "And"; 200+ line classes |
| OCP | `if/elif` chains that grow with every new type |
| LSP | Overriding a method to raise `NotImplementedError` |
| ISP | Implementing a method with `pass` to satisfy an interface |
| DIP | `self.db = MySQLDatabase()` inside `__init__` |

---

## Prerequisites

- Python 3.10+
- Classes, inheritance, and abstract base classes (`abc.ABC`, `@abstractmethod`)
- Module 01 (OOP Foundations) recommended
