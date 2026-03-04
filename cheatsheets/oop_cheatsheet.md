# OOP Cheatsheet

## 4 Pillars

| Pillar | One-Liner | Python Syntax |
|--------|-----------|---------------|
| **Encapsulation** | Bundle data + methods, hide internals | `@property`, `_private`, `__mangled` |
| **Inheritance** | "is-a" — acquire parent's interface + behavior | `class Dog(Animal):`, `super().__init__()` |
| **Polymorphism** | Same interface, different behavior | Method overriding, duck typing |
| **Abstraction** | Hide implementation, expose interface | `abc.ABC`, `@abstractmethod`, `Protocol` |

---

## Python Syntax Quick Reference

### Properties
```python
class BankAccount:
    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0: raise ValueError("Negative balance")
        self._balance = value
```

### ABC
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...   # must implement in subclass
```

### Protocol (structural typing)
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...    # no inheritance needed
```

### Dunder Methods Reference
| Method | When Called | Use |
|--------|------------|-----|
| `__init__` | `MyClass()` | Constructor |
| `__repr__` | `repr(obj)` | Debugging string |
| `__str__` | `str(obj)`, `print(obj)` | User-friendly string |
| `__eq__` | `a == b` | Equality comparison |
| `__hash__` | `hash(obj)`, in sets/dicts | Hashability |
| `__len__` | `len(obj)` | Length |
| `__iter__` | `for x in obj` | Iteration |
| `__next__` | `next(obj)` | Next item in iterator |
| `__lt__` | `a < b` | Less-than (enables sorting) |
| `__add__` | `a + b` | Addition operator |
| `__enter__`/`__exit__` | `with obj:` | Context manager |

---

## Inheritance vs Composition

| Use Inheritance | Use Composition |
|-----------------|-----------------|
| True "is-a" relationship | "has-a" relationship |
| ≤ 3 levels deep | Complex, flexible behavior |
| Share interface AND behavior | Share behavior only |
| `Car is-a Vehicle` ✅ | `Car has-a Engine` ✅ |
| `Square is-a Rectangle` ❌ (LSP!) | `Square has-a Side` ✅ |

**Rule**: When in doubt, prefer composition.

---

## When to Use `@property`

✅ When you need **validation** on set
✅ When value is **computed** from other attrs
✅ When you want **read-only** access
❌ Not needed for simple storage (just use a public attr)

---

## MRO Quick Reference

```python
class D(B, C):  # MRO: D → B → C → A → object
    pass

print(D.__mro__)  # shows full resolution order
super()           # calls next in MRO (not just direct parent!)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `super().__init__()` | Always call it in subclasses |
| Mutable default arg: `def __init__(self, items=[])` | Use `items=None`, then `items or []` |
| Deep inheritance (5+ levels) | Flatten with composition |
| `__eq__` without `__hash__` | If you define `__eq__`, define `__hash__` too |
| `class Dog(Animal): pass` (empty, no `super()`) | Always call super() |
