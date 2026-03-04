# Composite Pattern

## What Is It?

The **Composite** pattern lets you treat individual objects (leaves) and
compositions of objects (composites) **uniformly** through a shared interface.
Client code calls the same methods regardless of whether it is talking to a
single item or an entire tree of items.

## Real-World Analogy

Think of a company **org chart**.

- An **Employee** (leaf) has a salary. Ask them `get_salary()` → returns their own pay.
- A **Department** (composite) contains employees *and* sub-departments.
  Ask it `get_salary()` → it asks every child and sums the results.

The caller does not need to know whether it is talking to a person or an entire
division. Both answer the same question.

Other examples: file systems (File vs Directory), GUI widgets (Button vs Panel),
restaurant menus (MenuItem vs Menu category).

## Why It Matters

Recursive tree structures appear everywhere in software. Without Composite you
end up writing `if isinstance(node, Leaf): … else: …` branches everywhere.
With Composite, recursion is *encoded in the tree itself* — the composite
delegates to its children, and each child does the same.

## Python Specifics

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def operation(self) -> int: ...   # leaf returns scalar, composite sums children

class Leaf(Component):
    def __init__(self, name: str, value: int) -> None:
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    def operation(self) -> int:
        return self._value            # base case

class Composite(Component):
    def __init__(self, name: str) -> None:
        self._name = name
        self._children: list[Component] = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, child: Component) -> None:
        self._children.append(child)

    def operation(self) -> int:
        return sum(c.operation() for c in self._children)   # recursive case
```

## When to Use

- You need to represent **part-whole hierarchies** (trees, nested structures).
- Client code should be able to ignore the difference between leaf and composite.
- You want to **add new node types** without modifying existing client code
  (Open/Closed Principle).

## When to Avoid

- Leaf and composite behaviours diverge so much that a shared interface becomes
  misleading or forces empty/unsupported methods on leaves.
- The hierarchy is guaranteed to be only one level deep — a plain list suffices.
- You need strict type safety at the API level: exposing `add_child` only on
  Composite (the "safety" variant) means clients must downcast, which can be
  awkward.

## Transparency vs Safety

Two flavours exist:

| Variant | `add_child` on | Trade-off |
|---------|---------------|-----------|
| **Transparent** | `Component` ABC | Uniform interface; leaf must raise or no-op |
| **Safety** | `Composite` only | Type-safe; client must know node type |

Python codebases usually prefer **safety** — keep `add_child` on `Composite`,
and rely on duck-typing when the caller already has a `Composite` reference.

## Common Mistakes

- Calling `add_child()` on a `Leaf` — either guard with `NotImplementedError`
  or keep `add_child` off the base ABC entirely.
- Forgetting the **base case**: a leaf's method must return a concrete value,
  not delegate further.
- Storing children as a `tuple` (immutable) when the tree needs to grow at
  runtime — use a `list`.
- Making `display()` print directly instead of returning a `str`; returning a
  string makes testing straightforward.
