# Template Method Pattern

## What Is It?

The Template Method pattern defines the **skeleton of an algorithm** in a base class method, deferring certain steps to subclasses. The base class calls abstract "hook" methods at specific points; subclasses override those hooks to supply concrete behaviour — but they never change the overall flow.

The key distinction: **the base class controls *when* steps happen; subclasses control *what* those steps do.**

```python
class Base:
    def template_method(self):        # ← the skeleton (usually final)
        self.step_one()               # ← called in order
        self.step_two()
        self.step_three()

    @abstractmethod
    def step_one(self): ...           # ← subclass fills in

    @abstractmethod
    def step_two(self): ...

    def step_three(self):             # ← optional: default implementation
        print("default step 3")
```

A subclass that inherits `Base` only overrides the abstract steps — it never redefines the order they are called.

---

## Analogy

Think of a **recipe card** with printed instructions and blank lines:

```
1. Preheat oven to _____°C.          ← subclass fills in temperature
2. Mix ________________ ingredients. ← subclass fills in list
3. Bake for _____ minutes.           ← subclass fills in time
4. Let cool, then serve.             ← fixed step (base class default)
```

Every baker follows steps 1-4 in order. The recipe card (base class) owns the structure. Each specific recipe (subclass) fills in the blanks differently.

Without Template Method you would copy steps 1–4 into every recipe class, creating duplication and the risk of diverging logic.

---

## Why It Matters

### The Problem It Solves: Algorithmic Duplication

Consider generating a report in three formats. Without Template Method:

```python
class CSVReport:
    def generate(self, data):
        output = "Name,Category,Price\n"   # header
        for row in data:
            output += f"{row['name']},{row['category']},{row['price']}\n"
        output += f"Total rows: {len(data)}\n"
        return output

class HTMLReport:
    def generate(self, data):
        output = "<table><tr><th>Name</th>...</tr>\n"  # header (different)
        for row in data:                                # loop (SAME)
            output += f"<tr><td>{row['name']}</td>...</tr>\n"
        output += f"</table><p>Total: {len(data)}</p>"  # footer (different)
        return output
```

The `for` loop appears in every class. If the loop logic changes (e.g., filter empty rows), you must update every class.

### The Solution: Extract the Invariant

```python
class ReportGenerator(ABC):
    def generate(self, data: list[dict]) -> str:    # invariant skeleton
        parts = [self.format_header()]
        for row in data:
            parts.append(self.format_row(row))      # variant step
        parts.append(self.format_footer(len(data)))
        return "".join(parts)

    @abstractmethod
    def format_header(self) -> str: ...

    @abstractmethod
    def format_row(self, row: dict) -> str: ...

    @abstractmethod
    def format_footer(self, total: int) -> str: ...
```

Now the loop lives in one place. Adding a new format means writing a new subclass — the `generate()` method never changes.

---

## Python-Specific Notes

### Use ABC + @abstractmethod
Python does not have `final` (though `typing.final` exists), so the convention is to document the template method as "do not override" and enforce the abstract steps with `@abstractmethod`:

```python
from abc import ABC, abstractmethod

class Pipeline(ABC):

    def run(self) -> None:
        """Template method — do not override."""
        self._before()
        self._execute()
        self._after()

    @abstractmethod
    def _execute(self) -> None: ...

    def _before(self) -> None:
        """Optional hook — subclasses may override."""
        pass

    def _after(self) -> None:
        """Optional hook — subclasses may override."""
        pass
```

### Naming Conventions
- Template method: usually a **public** method like `generate()`, `run()`, `process()`.
- Primitive operations (abstract hooks): often **prefixed with `_`** to signal "internal, override me" — e.g., `_format_header()`.
- Optional hooks (concrete defaults): same prefix, but not abstract — subclasses may override but don't have to.

### Abstract vs Concrete Hooks

| Hook type | Decorator | Subclass must override? |
|-----------|-----------|------------------------|
| Primitive operation | `@abstractmethod` | Yes — Python raises `TypeError` if not |
| Optional hook | none (has default body) | No — default is used if not overridden |

### @dataclass Usage
Subclasses that carry configuration (e.g., a title string, a separator character) can use `@dataclass` to avoid writing `__init__`:

```python
from dataclasses import dataclass

@dataclass
class CSVReport(ReportGenerator):
    separator: str = ","

    def format_header(self) -> str:
        return f"Name{self.separator}Price\n"
```

---

## When to Use

- You have multiple classes that share the same algorithmic **structure** but differ in specific **steps**.
- You want to guarantee a fixed execution order (e.g., open → process → close) while letting subclasses specialise each step.
- You want a single place to update the overall flow without touching subclasses.
- You are building frameworks: the framework owns the template method and calls hooks that application code fills in.

## When to Avoid

- The "algorithm" is only one step — there is nothing to template.
- The variations are so different that forcing them into a shared skeleton produces an awkward `if isinstance(...)` smell.
- The skeleton needs to vary too — if the order of steps must change per subclass, **Strategy** is more appropriate (inject the whole algorithm, don't inherit it).
- You want to compose behaviours at runtime — Template Method uses compile-time inheritance; for runtime composition use **Strategy** or **Decorator**.

---

## Quick Example

```python
from abc import ABC, abstractmethod

class DataMigrator(ABC):
    """Template: connect → extract → transform → load → disconnect."""

    def migrate(self) -> None:
        """Template method — fixed sequence."""
        conn = self._connect()
        try:
            raw = self._extract(conn)
            transformed = self._transform(raw)
            self._load(transformed)
        finally:
            self._disconnect(conn)

    @abstractmethod
    def _connect(self) -> object: ...

    @abstractmethod
    def _extract(self, conn: object) -> list: ...

    @abstractmethod
    def _transform(self, data: list) -> list: ...

    @abstractmethod
    def _load(self, data: list) -> None: ...

    def _disconnect(self, conn: object) -> None:
        """Default: do nothing (override if needed)."""
        pass


class CSVToDBMigrator(DataMigrator):
    def _connect(self) -> object:
        return open("data.csv")

    def _extract(self, conn) -> list:
        return [line.split(",") for line in conn]

    def _transform(self, data: list) -> list:
        return [{"name": row[0], "value": int(row[1])} for row in data]

    def _load(self, data: list) -> None:
        print(f"Inserting {len(data)} rows …")

    def _disconnect(self, conn) -> None:
        conn.close()
```

---

## Template Method vs Strategy

Both patterns handle algorithmic variation.  The difference is **how** they vary:

| Aspect | Template Method | Strategy |
|--------|----------------|----------|
| Mechanism | Inheritance | Composition |
| Variation point | Individual steps | Entire algorithm |
| Relationship | IS-A (subclass) | HAS-A (injected object) |
| Runtime swap | No | Yes |
| Testability | Subclass per variant | Inject mock strategy |
| Hollywood Principle | Yes ("don't call us, we'll call you") | No |

**Rule of thumb**: use Template Method when the skeleton is fixed and variants differ in a few well-defined steps. Use Strategy when you need to swap the whole algorithm at runtime or inject from outside.

---

## Template Method vs Decorator

| Aspect | Template Method | Decorator |
|--------|----------------|-----------|
| Mechanism | Inheritance | Wrapping |
| Adds behaviour | At compile time (subclass) | At runtime (wrap) |
| Multiple additions | Multiple subclasses | Nest wrappers |

Decorators are better when you want to add behaviour to an existing object at runtime without subclassing.

---

## Common Mistakes

1. **Overriding the template method itself**: The template method is the part that should *not* change. If a subclass overrides `generate()` instead of `format_header()`, it defeats the entire pattern.

2. **Too many abstract steps**: If the base class has 10 abstract methods, subclasses become burdensome to write. Consider default (optional) hooks for steps that most subclasses handle the same way.

3. **Steps that are too coarse**: If `_process()` does everything, the template is useless. Break into meaningful atomic steps that genuinely vary.

4. **Steps that are too fine-grained**: If `_add_comma()` and `_add_newline()` are separate abstract methods, the template becomes more complex than the subclasses. Find the right granularity.

5. **Calling abstract steps with incompatible arguments**: The base class must call each hook with exactly the arguments the subclass signature expects. Changing the signature later breaks every subclass.

6. **Forgetting to call `super().__init__()`**: If the base class stores state in `__init__`, subclasses that define their own `__init__` must call `super().__init__()` or they inherit a broken state.

7. **Mutable default arguments in hooks**: `def format_row(self, row: dict = {})` — the `{}` default is shared across all calls. Always use `None` and replace inside the body.

---

## Summary

```
Abstract Base Class
    ├── template_method()          ← owns the algorithm skeleton (do not override)
    │       calls:
    │       ├── step_one()         ← abstract — MUST override
    │       ├── step_two()         ← abstract — MUST override
    │       └── optional_step()    ← concrete default — MAY override
    │
    ├── ConcreteClassA(Base)       ← fills in step_one, step_two
    └── ConcreteClassB(Base)       ← fills in step_one, step_two differently
```

The Hollywood Principle in action: *"Don't call us, we'll call you."*
The base class calls the subclass's methods — not the other way around.

---

## LLD Problems That Use This Pattern

| Problem | Template method | Abstract steps |
|---------|----------------|----------------|
| [14 Logging Framework](../../../04_lld_problems/14_logging_framework/) | `LogHandler.handle()` — filter → format → emit | `emit()` differs per handler: Console prints, Memory stores, File writes |
| [09 Chess](../../../04_lld_problems/09_chess/) | `Game.make_move()` — validate → execute → detect check/checkmate | Each `Piece.get_valid_moves()` is a per-piece-type hook |

**Best example:** Logging Framework — study `LogHandler` after completing the exercise. The `handle()` template is inherited by every handler; only `emit()` is overridden.
