# Module 02 — SOLID Principles

## Overview

SOLID is an acronym for five foundational object-oriented design principles introduced by Robert C. Martin (Uncle Bob). These principles guide developers toward writing software that is easier to maintain, extend, and test — especially as systems grow in complexity.

In the context of Low-Level Design (LLD), SOLID principles are not abstract theory. They are practical tools that determine the quality of your class hierarchies, service layers, and module boundaries. Interviewers at top tech companies evaluate SOLID fluency as a proxy for design maturity.

---

## Why SOLID Matters for LLD

When you design a system at the class and interface level, every design decision compounds. A violation of one principle today means:

- **Hard-to-test code** — you cannot unit test a class that hardcodes its own dependencies
- **Fragile extensions** — adding a feature breaks existing, working functionality
- **Unreliable hierarchies** — a subclass that surprises callers destroys trust in your API
- **Unnecessary coupling** — one change ripples through unrelated modules
- **Difficult onboarding** — god classes with hundreds of lines are impossible to reason about quickly

SOLID gives you a vocabulary and a checklist for avoiding these problems.

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
├── theory.md                  # Deep-dive explanation with analogies and Python-specific guidance
├── examples/
│   ├── example1_violation.py  # Shows the anti-pattern clearly with comments
│   └── example2_refactored.py # Shows the correct approach
└── exercises/
    ├── problem.md             # Exercise description
    ├── starter.py             # Skeleton code to fill in
    ├── tests.py               # Tests that must pass with your solution
    └── solution/
        ├── solution.py        # Complete working solution
        └── explanation.md     # Explanation of design decisions
```

---

## How the Five Principles Work Together

SOLID principles are not independent silos — they reinforce each other:

**SRP + ISP** work together on the *granularity* dimension. SRP tells you to break apart classes with multiple responsibilities. ISP tells you to break apart interfaces that are too fat. Both reduce coupling and increase cohesion.

**OCP + LSP** work together on the *extension* dimension. OCP tells you to design so new behavior can be added without changing existing code. LSP tells you that any extension via inheritance must be a true behavioral substitute — otherwise your OCP extension breaks existing callers.

**DIP + SRP** work together on the *dependency* dimension. DIP tells you that high-level modules should depend on abstractions. SRP ensures those abstractions stay focused — a fat interface used as an abstraction still causes problems.

**DIP + OCP** are deeply linked. To make a class open for extension, you typically inject dependencies via interfaces (DIP). Then new behavior is added by providing new implementations of those interfaces — the existing class never changes.

A practical mental model:

```
SRP  → "What does this class do?" (answer should be one thing)
OCP  → "How do I add new behavior?" (answer: extend, don't modify)
LSP  → "Can I trust this subtype?" (answer should always be yes)
ISP  → "What does this interface expose?" (answer: only what the client needs)
DIP  → "Who creates dependencies?" (answer: the caller, via injection)
```

---

## Recommended Study Order

1. Start with **SRP** — it is the most intuitive and sets the foundation for all others
2. Move to **OCP** — you will naturally use polymorphism, which sets up LSP
3. Study **LSP** — understand what correct inheritance looks like
4. Study **ISP** — learn to design focused, composable interfaces
5. Finish with **DIP** — bring it all together with dependency injection

Each principle builds on the vocabulary and patterns introduced before it.

---

## Quick Reference: Violation Smells

| Principle | Code Smell / Symptom |
|-----------|----------------------|
| SRP | Class name contains "And"; methods that don't use instance data; 200+ line classes |
| OCP | `if/elif` chains that grow with every new feature type |
| LSP | Overriding a method to raise `NotImplementedError`; empty overrides |
| ISP | Implementing a method with `pass` to satisfy an interface |
| DIP | `self.db = MySQLDatabase()` inside `__init__`; impossible to unit test without infrastructure |

---

## Prerequisites

- Python 3.10+
- Understanding of classes, inheritance, and abstract base classes
- Familiarity with `abc.ABC` and `abc.abstractmethod`
- Module 01 (OOP Fundamentals) recommended but not required
