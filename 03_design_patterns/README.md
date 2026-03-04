# Design Patterns

## What Are Design Patterns?

Design patterns are **reusable solutions to commonly occurring problems** in software design. They are not finished code you can copy-paste — they are templates, blueprints, or descriptions of how to solve a problem that can be applied in many different situations.

Think of patterns as vocabulary. When an experienced engineer says "use a Singleton here" or "this calls for a Strategy pattern," everyone on the team immediately understands the intent, the structure, and the trade-offs. Patterns are a communication shortcut.

### A Brief History: The Gang of Four

In 1994, four authors — Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides — published **"Design Patterns: Elements of Reusable Object-Oriented Software."** They became known as the **Gang of Four (GoF)**, and the book catalogued 23 fundamental patterns observed across successful object-oriented codebases.

The book was written in C++ and Smalltalk, but the patterns transcend any language. Python, Java, Go — the same structural problems recur.

> Important caveat: patterns describe *solutions to problems*. If you don't have the problem, don't apply the pattern. Pattern misuse is a real and painful thing.

---

## The 3 Categories of Design Patterns

GoF organized the 23 patterns into three categories based on their *purpose*:

### 1. Creational Patterns
Concerned with **how objects are created**. They abstract the instantiation process, making systems independent of how their objects are created, composed, and represented.

**Problem they solve:** `SomeClass()` scattered everywhere makes code rigid. Creational patterns centralize and control object creation.

### 2. Structural Patterns
Concerned with **how objects are composed** into larger structures. They use inheritance and composition to assemble objects and classes into larger structures while keeping those structures flexible and efficient.

**Problem they solve:** How do you combine classes and objects into larger structures without making a mess of dependencies?

### 3. Behavioral Patterns
Concerned with **how objects communicate and assign responsibilities**. They describe not just patterns of objects or classes but also the patterns of communication between them.

**Problem they solve:** Who does what? How do objects collaborate without becoming tightly coupled?

---

## Patterns in This Module

This module covers **13 patterns** — a curated selection of the most practically useful GoF patterns for modern software engineers. They are organized by category.

### Creational Patterns (4 covered)

| # | Pattern | Location | One-Line Description |
|---|---------|----------|----------------------|
| 1 | **Singleton** | `creational/singleton/` | Ensure only one instance of a class exists and provide a global access point |
| 2 | **Factory Method** | `creational/factory/` | Define an interface for creating objects; let subclasses decide which class to instantiate |
| 3 | **Abstract Factory** | `creational/abstract_factory/` | Create families of related objects without specifying their concrete classes |
| 4 | **Builder** | `creational/builder/` | Construct complex objects step by step, separating construction from representation |

### Structural Patterns (5 covered)

| # | Pattern | Location | One-Line Description |
|---|---------|----------|----------------------|
| 5 | **Adapter** | `structural/adapter/` | Convert one interface into another that clients expect — a translator |
| 6 | **Decorator** | `structural/decorator/` | Add responsibilities to objects dynamically without subclassing |
| 7 | **Facade** | `structural/facade/` | Provide a simplified interface to a complex subsystem |
| 8 | **Proxy** | `structural/proxy/` | Provide a surrogate that controls access to another object |
| 9 | **Composite** | `structural/composite/` | Compose objects into tree structures to represent part-whole hierarchies |

### Behavioral Patterns (4 covered)

| # | Pattern | Location | One-Line Description |
|---|---------|----------|----------------------|
| 10 | **Strategy** | `behavioral/strategy/` | Define a family of algorithms, encapsulate each one, and make them interchangeable |
| 11 | **Observer** | `behavioral/observer/` | Define a one-to-many dependency so that when one object changes state, all dependents are notified |
| 12 | **Command** | `behavioral/command/` | Encapsulate a request as an object, allowing undo, queuing, and logging |
| 13 | **Template Method** | `behavioral/template_method/` | Define the skeleton of an algorithm; let subclasses fill in the steps |

---

## How Patterns Relate to SOLID Principles

Design patterns and SOLID principles are deeply intertwined. Patterns are often the *concrete expression* of SOLID principles:

### Single Responsibility Principle (SRP)
**"A class should have only one reason to change."**

- **Builder** separates the *construction logic* of a complex object from the *object itself* — two separate reasons to change, two separate classes.
- **Factory Method** moves object-creation responsibility out of the client class into a dedicated creator hierarchy.

### Open/Closed Principle (OCP)
**"Open for extension, closed for modification."**

- **Strategy** lets you add new algorithms without touching existing code — swap in a new strategy class.
- **Factory Method** lets you add new product types (new subclasses) without modifying the factory interface.
- **Decorator** adds behavior to objects by wrapping them, not by editing their source code.

### Liskov Substitution Principle (LSP)
**"Subtypes must be substitutable for their base types."**

- All creational patterns depend on LSP. A `RoadLogistics` factory must be substitutable for `LogisticsCompany`. A `DarkButton` must be substitutable for `Button`.
- Patterns break badly when LSP is violated — if a subclass can't be used like its parent, the pattern's polymorphism collapses.

### Interface Segregation Principle (ISP)
**"Clients should not be forced to depend on interfaces they don't use."**

- **Abstract Factory** defines narrow, focused product interfaces. Clients only see `Button`, not all the machinery behind it.
- **Facade** hides a bloated subsystem behind a lean interface, so clients only depend on what they need.

### Dependency Inversion Principle (DIP)
**"Depend on abstractions, not concretions."**

- **Factory Method** and **Abstract Factory** are the canonical implementations of DIP for object creation. Client code depends on the `Creator` abstract class or `Factory` interface — never on `MySQLConnection` or `WindowsButton` directly.
- **Strategy** and **Observer** similarly ensure client code depends on the strategy/observer *interface*, not on specific implementations.

---

## How to Use This Module

Each pattern directory contains:

```
pattern_name/
├── theory.md              # Concept, analogy, when to use, trade-offs
├── examples/
│   ├── example1_*.py      # Simpler example with heavy comments
│   └── example2_*.py      # More realistic, applied example
└── exercises/
    ├── problem.md          # Exercise description and requirements
    ├── starter.py          # Skeleton code with stubs
    ├── tests.py            # Test suite (run against your solution)
    └── solution/
        ├── solution.py     # Complete working solution
        └── explanation.md  # Why the solution is structured this way
```

**Recommended approach:**
1. Read `theory.md` first. Understand the *problem* the pattern solves before looking at the solution.
2. Run and read `example1_*.py`. Understand the mechanics.
3. Read `example2_*.py` — this shows the pattern in a more realistic context.
4. Attempt `exercises/starter.py` using only `problem.md` as guidance.
5. Run `tests.py` against your solution. Debug until all tests pass.
6. Compare with `solution/solution.py` and read `solution/explanation.md`.

Start with the creational patterns: **Singleton → Factory Method → Abstract Factory → Builder**.
