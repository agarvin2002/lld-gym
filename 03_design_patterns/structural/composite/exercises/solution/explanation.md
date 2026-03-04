# Composite Pattern — Explanation

## The Core Idea: Uniform Treatment

The whole point of Composite is that **caller code never needs to know**
whether it is dealing with a leaf or a composite.  In this exercise, you can
call `total_salary()` on an individual `Employee`, a `Department` containing
employees, or a `Department` containing sub-departments — the same method
signature works everywhere.

```python
nodes: list[OrgNode] = [
    Employee("Diana", "CEO", 200_000),
    Department("Engineering"),   # contains employees
]

for node in nodes:
    print(node.total_salary())  # same call, no isinstance() check
```

This is enforced by the `OrgNode` ABC: both `Employee` and `Department` must
implement every abstract method or Python raises `TypeError` at instantiation.

---

## Why Recursion Is the Secret

The beauty of Composite is that complex aggregation collapses into two trivial
lines:

```python
# Department.total_salary
def total_salary(self) -> float:
    return sum(m.total_salary() for m in self._members)

# Employee.total_salary (base case)
def total_salary(self) -> float:
    return self._salary
```

When you call `company.total_salary()`, the call stack unwinds the entire tree
automatically:

```
company.total_salary()
  └─ diana.total_salary()       → 200_000
  └─ eng.total_salary()
       └─ alice.total_salary()  → 120_000
       └─ backend.total_salary()
            └─ bob.total_salary() → 140_000
```

No loops, no bookkeeping, no `isinstance`.  The structure of the data drives
the computation.

---

## Open/Closed Principle

Adding a new kind of node — say, `Contractor(OrgNode)` with a daily rate and
no benefits — only requires:

1. Create `Contractor` implementing `OrgNode`.
2. Implement `total_salary()`, `headcount()`, `display()`.

You do **not** touch `Department`, the tests, or any existing code.  The tree
naturally delegates to whatever `OrgNode` you add.

---

## Transparency vs Safety

The classic Composite debate:

| Variant | Where does `add_member` live? | Trade-off |
|---------|------------------------------|-----------|
| **Transparent** | On `OrgNode` ABC | Fully uniform API; leaves must raise `NotImplementedError` for `add_member` |
| **Safety** (this solution) | On `Department` only | Type-safe; callers must know they have a `Department` to add children |

This solution uses **safety**: `add_member` is not on `OrgNode`.  If you try
to call `add_member` on an `Employee` you get an `AttributeError` immediately
— a clear, honest error rather than a silent no-op.

The trade-off: if you have an `OrgNode` reference and want to add a child, you
must downcast (`assert isinstance(node, Department)`).  For most real codebases
that is fine because you usually know the concrete type at the point where you
build the tree.

---

## display() — Depth-First Traversal Emerges Naturally

```python
# Department.display
def display(self, indent: int = 0) -> str:
    lines = ["  " * indent + f"[{self._name}]"]
    for member in self._members:
        lines.append(member.display(indent + 1))  # <-- recursive call
    return "\n".join(lines)
```

Each `display()` call passes `indent + 1` to its children.  The result is a
perfectly indented tree printed in **pre-order depth-first** order (parent
before children) — without any explicit traversal algorithm.

---

## Common Mistakes to Avoid

1. **Returning `None` from `display()`** — always `return` a string; do not
   `print` directly inside the method.  Returning a string makes the method
   testable and composable.

2. **Calling `add_member` on `Employee`** — `Employee` has no children and no
   `add_member`.  Keep it that way; adding child management to a leaf muddies
   the model.

3. **Forgetting the base case** — `Employee.total_salary()` must return
   `self._salary` (a concrete number), not delegate further.  If it delegates
   to an empty list you get `0` silently, which is wrong.

4. **Mutable default argument for children list** — never write
   `def __init__(self, members=[])`.  Always initialise with
   `self._members = []` inside `__init__`.
