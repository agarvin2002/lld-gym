# OOP Foundations Module

## What is Object-Oriented Programming?

Object-Oriented Programming (OOP) is a programming paradigm that organizes code around **objects** — self-contained units that bundle together **data** (attributes) and **behavior** (methods). Instead of writing a sequence of instructions that operate on raw data, you define *types* of things, give them responsibilities, and let them collaborate.

At its core, OOP answers a simple question: *who owns this data, and who is responsible for operating on it?*

---

## Why OOP Matters for Low-Level Design (LLD)

Low-Level Design is about translating a system's requirements into **concrete classes, interfaces, and relationships**. OOP is the primary tool for this translation. Here's why it matters:

- **Modeling the real world**: Production systems and LLD problems ask you to model entities (User, Order, Payment, Vehicle). Classes map naturally to these concepts.
- **Encapsulation enforces contracts**: When a class owns its data and controls how it's modified, you prevent invalid states. A `BankAccount` that validates withdrawals is safer than a raw dict anyone can mutate.
- **Inheritance and polymorphism enable extensibility**: You can add a new `PaymentMethod` without rewriting existing code if your design uses the right abstractions.
- **Design patterns are OOP patterns**: Every GoF pattern (Strategy, Observer, Factory, etc.) is expressed through classes and their relationships. You need fluency with OOP before patterns make sense.

In short: **you cannot do LLD without OOP**. This module builds the foundation everything else rests on.

---

## Module Topics

| # | Topic | Description | Link |
|---|-------|-------------|------|
| 01 | Classes and Objects | Defining classes, creating objects, dunder methods, dataclasses | [01_classes_and_objects/](01_classes_and_objects/) |
| 02 | Encapsulation | Private attributes, properties, validation, information hiding | [02_encapsulation/](02_encapsulation/) |
| 03 | Inheritance | Single inheritance, `super()`, method overriding | [03_inheritance/](03_inheritance/) |
| 04 | Polymorphism | Method overriding, duck typing, abstract base classes | [04_polymorphism/](04_polymorphism/) |
| 05 | Abstraction | Abstract classes, interfaces in Python, designing contracts | [05_abstraction/](05_abstraction/) |

---

## Prerequisites

This module assumes you know:

- **Python basics**: variables, functions, loops, conditionals, lists, dicts
- **How to run Python**: `python3 file.py` or `pytest tests.py`
- **Type hints** (helpful but not required — introduced inline): `def foo(x: int) -> str:`

You do **not** need prior OOP experience. This module starts from scratch.

---

## How to Navigate This Module

Each topic folder has the same structure:

```
01_classes_and_objects/
    theory.md          <- Read this first. Concepts + inline examples.
    examples/
        example1_*.py  <- Runnable, heavily commented code
        example2_*.py  <- More advanced patterns
    exercises/
        problem.md     <- What to build + hints
        starter.py     <- Skeleton code with TODOs
        tests.py       <- pytest tests (run to check your work)
        solution/
            solution.py    <- Reference implementation (read AFTER you try)
            explanation.md <- Why decisions were made
```

### Recommended Workflow

1. Read `theory.md` — understand the concept before writing code
2. Run the examples — read every comment, then experiment with changes
3. Read `exercises/problem.md` — understand what you're building
4. Open `exercises/starter.py` — fill in the TODOs
5. Run `pytest exercises/tests.py` — fix failures until all tests pass
6. Read `solution/solution.py` and `solution/explanation.md` — compare your approach

### Running Tests

```bash
# From the topic directory
cd 01_classes_and_objects
pytest exercises/tests.py -v

# Run a single test
pytest exercises/tests.py::test_cart_get_total_calculates_correctly -v
```

### Running Examples

```bash
python3 01_classes_and_objects/examples/example1_basic_class.py
```

---

## A Note on Scope

This module focuses on the OOP patterns that appear most often in real-world system design:
- Defining clean classes with `__init__`, `__repr__`, and `__str__`
- Using `@property` to validate and protect object state
- Building class hierarchies with `super()` and method overriding
- Designing contracts with `ABC` and `@abstractmethod`

Each topic also includes an advanced example file covering additional Python features (dataclasses, duck typing, mixins) for learners who want to go further.

---

## Module Learning Goals

After completing this module you should be able to:

1. Define a well-structured Python class with appropriate attributes, methods, and dunder methods
2. Use encapsulation to protect object state with properties and validation
3. Build class hierarchies with inheritance and use `super()` correctly
4. Recognize when inheritance is appropriate vs. when composition is better
5. Apply these concepts to the LLD problems in Module 04
