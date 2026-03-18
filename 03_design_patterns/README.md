# Design Patterns

## What Are Design Patterns?

Design patterns are reusable solutions to common problems in software design.
They are not finished code you copy and paste.
They are templates — descriptions of how to solve a problem that applies in many situations.

Think of patterns as vocabulary.
When an engineer says "use a Strategy here" or "this needs a Facade," everyone on the team understands the intent and the trade-offs immediately.

> Patterns describe *solutions to problems*. If you do not have the problem, do not apply the pattern.

---

## The 3 Categories

### 1. Creational Patterns
Concerned with **how objects are created**.
They abstract object construction so the rest of the code does not depend on specific classes.

### 2. Structural Patterns
Concerned with **how objects are composed** into larger structures.
They use inheritance and composition to build flexible, maintainable systems.

### 3. Behavioral Patterns
Concerned with **how objects communicate** and assign responsibilities.
They describe how objects collaborate without becoming tightly coupled.

---

## Patterns in This Module

This module covers **13 patterns** — a curated selection of the most useful GoF patterns for modern systems.

### Creational (4)

| # | Pattern | Location | What it does |
|---|---------|----------|--------------|
| 1 | **Singleton** | `creational/singleton/` | Ensures only one instance of a class exists |
| 2 | **Factory Method** | `creational/factory/` | Delegates object creation to subclasses or a registry |
| 3 | **Abstract Factory** | `creational/abstract_factory/` | Creates families of related objects without naming concrete classes |
| 4 | **Builder** | `creational/builder/` | Constructs complex objects step by step with a fluent interface |

### Structural (5)

| # | Pattern | Location | What it does |
|---|---------|----------|--------------|
| 5 | **Adapter** | `structural/adapter/` | Converts one interface into another that callers expect |
| 6 | **Decorator** | `structural/decorator/` | Adds behaviour to objects by wrapping them, not by subclassing |
| 7 | **Facade** | `structural/facade/` | Provides a simple interface to a complex subsystem |
| 8 | **Proxy** | `structural/proxy/` | Controls access to another object (caching, logging, protection) |
| 9 | **Composite** | `structural/composite/` | Composes objects into trees so individual items and groups are treated the same way |

### Behavioral (4)

| # | Pattern | Location | What it does |
|---|---------|----------|--------------|
| 10 | **Strategy** | `behavioral/strategy/` | Swaps algorithms at runtime without changing the caller |
| 11 | **Observer** | `behavioral/observer/` | Notifies subscribers automatically when an object changes state |
| 12 | **Command** | `behavioral/command/` | Encapsulates a request as an object — enables undo, queuing, and logging |
| 13 | **Template Method** | `behavioral/template_method/` | Defines an algorithm's skeleton; subclasses fill in the steps |

---

## How Patterns Relate to SOLID Principles

Patterns are often the concrete expression of SOLID principles.

| SOLID Principle | Patterns that express it |
|----------------|--------------------------|
| **Single Responsibility** | Builder (separates construction from the object), Factory Method (moves creation out of the client) |
| **Open/Closed** | Strategy (add algorithms without changing callers), Decorator (add behaviour without editing source), Factory Method (add products via new subclasses) |
| **Liskov Substitution** | All creational patterns depend on this — concrete products must be substitutable for their base types |
| **Interface Segregation** | Abstract Factory (narrow product interfaces), Facade (lean interface hides a bloated subsystem) |
| **Dependency Inversion** | Factory Method and Abstract Factory (client depends on the factory interface, not `MySQLConnection`), Strategy and Observer (client depends on the interface, not the concrete implementation) |

---

## How to Use This Module

Each pattern directory contains:

```
pattern_name/
├── theory.md              # Concept, analogy, when to use, trade-offs
├── examples/
│   ├── example1_*.py      # Simple example with explanatory comments
│   └── example2_*.py      # More realistic, system-design-oriented example
└── exercises/
    ├── problem.md          # Exercise description and requirements
    ├── starter.py          # Skeleton code — edit this
    ├── tests.py            # Test suite — run against your implementation
    └── solution/
        ├── solution.py     # Complete working solution
        └── explanation.md  # Why the solution is structured this way
```

**Recommended approach:**
1. Read `theory.md`. Understand the problem the pattern solves before looking at any code.
2. Run `example1_*.py`. Follow the mechanics in the comments.
3. Read `example2_*.py`. This shows the pattern applied in a realistic context.
4. Attempt `exercises/starter.py` using only `problem.md` as guidance.
5. Run `tests.py` against your implementation. Debug until all tests pass.
6. Compare with `solution/solution.py` and read `solution/explanation.md`.

**Learning goals:**
- Identify which pattern solves a given design problem
- Implement each pattern from scratch in Python
- Recognise how patterns enforce SOLID principles
- Compose multiple patterns together (e.g. Proxy wrapping a Facade)

Start with the creational patterns: **Singleton → Factory Method → Abstract Factory → Builder**.
