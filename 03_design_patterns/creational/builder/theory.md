# Builder Pattern

## What is Builder?

Builder is a **creational design pattern** that separates the construction of a complex object from its representation. Instead of a single enormous constructor call, you build an object step by step using a dedicated builder object, then call `build()` to get the finished product.

---

## Real-World Analogy: Sandwich Shop

Picture yourself ordering at a sandwich counter:

1. You pick the bread
2. You choose a protein
3. You add condiments, one by one
4. You decide on extras (toasted? extra cheese?)
5. The worker hands you the finished sandwich

You don't pass every decision in a single breath. You build the order incrementally, and the result is only produced at the end. The Builder pattern works exactly the same way.

---

## The Telescoping Constructor Problem

Without Builder, complex objects force you into one of two bad options:

**Option A — Telescoping constructors** (many overloads):
```python
# Painful: which positional arg is which?
Pizza("large", "thin", "tomato", [], False)
Pizza("medium", "thick", "pesto", ["mushrooms", "olives"], True)
```

**Option B — Huge keyword-argument soup**:
```python
Pizza(size="large", crust="thin", sauce="tomato",
      toppings=[], extra_cheese=False, gluten_free=False,
      delivery_notes="", loyalty_points=0, ...)
```

Both options break down as the number of optional/mandatory parameters grows. Builder solves this elegantly.

---

## Why Builder Matters

| Problem | Builder Solution |
|---|---|
| Too many constructor parameters | Fluent setters, one concern at a time |
| Optional vs. mandatory fields | `build()` validates mandatory fields |
| Object assembled over many steps | Builder accumulates state; call `build()` when ready |
| Readable construction code | Method chaining reads like English |
| Multiple representations | Different Director configurations, same builder |

---

## Python Specifics

### Method Chaining (Fluent Interface)
Every setter returns `self`, enabling chaining:

```python
resume = (ResumeBuilder()
          .contact("Alice", "alice@example.com")
          .summary("Senior engineer with 10 years experience")
          .add_skill("Python")
          .add_skill("System Design")
          .build())
```

### Quick Snippet — QueryBuilder
```python
class QueryBuilder:
    def __init__(self):
        self._table = ""
        self._conditions = []
        self._limit = None

    def table(self, name: str) -> "QueryBuilder":
        self._table = name
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def build(self) -> str:
        if not self._table:
            raise ValueError("Table name is required")
        sql = f"SELECT * FROM {self._table}"
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        if self._limit is not None:
            sql += f" LIMIT {self._limit}"
        return sql

# Usage
query = QueryBuilder().table("users").where("age > 18").limit(10).build()
```

### `@dataclass` vs Builder — When Does Builder Win?

| Scenario | Use |
|---|---|
| Simple value objects, all fields known upfront | `@dataclass` |
| Some fields optional, sensible defaults | `@dataclass` with defaults |
| **Mandatory fields that need runtime validation** | Builder |
| **Object assembled across multiple steps / method calls** | Builder |
| **Multiple preset configurations (Director pattern)** | Builder |
| **Immutable product with mutable construction process** | Builder |

`**kwargs` and `@dataclass` are fine for simple cases. Use Builder when the construction *process itself* has logic, or when missing fields should raise an error only at `build()` time.

---

## The Director (Optional Add-On)

A **Director** class encodes common configurations. It takes a builder and calls the right setters in the right order:

```python
class SandwichDirector:
    def __init__(self, builder: SandwichBuilder):
        self._builder = builder

    def club_sandwich(self) -> Sandwich:
        return (self._builder
                .bread("white")
                .protein("turkey")
                .add_condiment("mayo")
                .add_condiment("mustard")
                .toasted(True)
                .build())
```

The Director is optional — clients can also drive the builder directly for custom configurations.

---

## When to Use Builder

- Object has **4+ parameters**, especially optional ones
- Construction involves **validation** (mandatory fields, value constraints)
- You want to produce **multiple representations** of the same kind of object
- The object must be **immutable** once created but assembled over many steps
- You want to provide **named presets** (Director) alongside custom builds

## When to Avoid Builder

- Object is simple (2–3 always-required fields) — `@dataclass` is cleaner
- Construction never varies — a plain factory function suffices
- You control the call site and keyword args are readable enough

---

## Common Mistakes

1. **Forgetting to call `build()`**
   ```python
   resume = ResumeBuilder().contact("Alice", "alice@example.com")
   # resume is a ResumeBuilder, NOT a Resume — easy bug
   ```

2. **Mutable default arguments in the builder's `__init__`**
   ```python
   # WRONG — all instances share the same list object
   class ResumeBuilder:
       def __init__(self):
           self._skills = []   # fine here — assigned in __init__, not as a default arg

   # This is the real danger:
   def __init__(self, skills=[]):   # NEVER do this
       self._skills = skills
   ```

3. **Not copying mutable fields in `build()`**
   ```python
   # WRONG — caller could mutate the builder's list after build()
   return Resume(skills=self._skills)

   # CORRECT — snapshot at build time
   return Resume(skills=list(self._skills))
   ```

4. **Builder that can be built multiple times with shared state**
   Consider resetting the builder or returning a fresh builder after each `build()` call if reuse is intended.

5. **Missing validation in `build()`**
   Setters are individual; `build()` is the single place to enforce invariants across all fields together.
