# Exercise: Organization Chart

## Problem Statement

Build an organization chart where each node is either an `Employee` (leaf) or
a `Department` (composite).  Both implement the `OrgNode` interface so that
client code never needs to distinguish between them.

## Components to Implement

### `OrgNode` (ABC — do not modify)

Abstract base class with four contract methods:

| Method | Return type | Description |
|--------|-------------|-------------|
| `name` (property) | `str` | Name of this node |
| `total_salary()` | `float` | Sum of all salaries in the subtree |
| `headcount()` | `int` | Number of employees in the subtree |
| `display(indent=0)` | `str` | Human-readable tree representation |

---

### `Employee(name, title, salary)` — Leaf

| Method | Behaviour |
|--------|-----------|
| `name` | Returns the employee's name |
| `total_salary()` | Returns own salary |
| `headcount()` | Returns `1` |
| `display(indent)` | `"  " * indent + f"{name} ({title}) — ${salary:,.0f}"` |

Example output for `Employee("Alice", "Engineer", 120000).display(2)`:

```
    Alice (Engineer) — $120,000
```

---

### `Department(name)` — Composite

| Method | Behaviour |
|--------|-----------|
| `name` | Returns the department name |
| `add_member(node)` | Appends `node` (any `OrgNode`) to internal list |
| `total_salary()` | Sum of `total_salary()` across all members |
| `headcount()` | Sum of `headcount()` across all members |
| `display(indent)` | Department name on its own line, then each member indented by 1 more |

Display format for Department at indent `i`:

```
<i spaces>[Engineering]
<i+1 spaces>Alice (Engineer) — $120,000
<i+1 spaces>[Backend]
<i+2 spaces>Bob (Senior Engineer) — $140,000
```

Department header uses `"  " * indent + f"[{name}]"`.

---

## Example Usage

```python
ceo      = Employee("Diana", "CEO",              200_000)
alice    = Employee("Alice", "Engineer",          120_000)
bob      = Employee("Bob",   "Senior Engineer",   140_000)

backend  = Department("Backend")
backend.add_member(bob)

eng      = Department("Engineering")
eng.add_member(alice)
eng.add_member(backend)

company  = Department("Acme Corp")
company.add_member(ceo)
company.add_member(eng)

print(company.display())
# [Acme Corp]
#   Diana (CEO) — $200,000
#   [Engineering]
#     Alice (Engineer) — $120,000
#     [Backend]
#       Bob (Senior Engineer) — $140,000

print(company.headcount())   # 3
print(company.total_salary()) # 460000.0
```

## Constraints

- `OrgNode` **must** use `ABC` and `@abstractmethod`.
- `Employee` is a pure leaf — do **not** add `add_member` to it.
- `Department` stores members in a `list[OrgNode]`.
- `display()` must **return** a `str`, not print directly.
- Do not import anything beyond `from abc import ABC, abstractmethod`.
