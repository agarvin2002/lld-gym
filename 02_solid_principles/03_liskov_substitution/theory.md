# Liskov Substitution Principle (LSP)

## What Is It?
If `S` is a subtype of `T`, objects of type `T` may be replaced with objects of type `S` **without altering the correctness of the program**.

In plain English: **A subclass should be fully usable wherever the base class is used.** No surprises, no broken behavior, no "this method doesn't apply to me."

---

## Real-World Analogy

If a recipe says "add 200ml of liquid", you substitute water and it works. You substitute juice and it probably works. You substitute concrete and the recipe breaks — even though concrete is technically a "material" like water.

The key isn't the label ("it's a liquid subtype!"), it's whether the **behavioral contract** is preserved. Concrete doesn't pour, doesn't mix — it violates what the recipe *assumed* about liquids.

LSP is about honoring the behavioral contract, not just the syntactic signature.

---

## Why It Matters

Without LSP, polymorphism breaks. Callers that use a base type reference start needing `isinstance()` checks to handle different subtypes differently. That defeats the entire point of inheritance.

**Signs you've lost LSP:**
```python
def process(shape: Shape) -> float:
    if isinstance(shape, Square):    # 🚩 red flag — why special-case?
        return shape.side ** 2
    return shape.area()              # works for Rectangle
```

This code is now brittle and grows with each new subtype.

---

## Classic Violation: Rectangle → Square

```python
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = self.height = w   # "clever" — both sides equal
    def set_height(self, h):
        self.width = self.height = h   # same
```

Now this function breaks:
```python
def test_area(r: Rectangle):
    r.set_width(5)
    r.set_height(4)
    assert r.area() == 20   # passes for Rectangle
                             # FAILS for Square: area = 4*4 = 16!
```

`Square` violates LSP: it **can't be substituted** for `Rectangle` without breaking correct code. The postcondition "width and height are independent after setting" is violated.

---

## Formal Rules (Barbara Liskov's Contract)

1. **Preconditions cannot be strengthened** — subclass can't demand more from the caller than the base class did.
   ```python
   # Base: accepts any int
   def deposit(self, amount: int) -> None: ...
   # Violation: subclass demands positive amounts only
   def deposit(self, amount: int) -> None:
       if amount <= 0: raise ValueError  # stronger precondition 🚩
   ```

2. **Postconditions cannot be weakened** — subclass can't return less/different than the base promised.
   ```python
   # Base: always returns a non-empty list
   def get_items(self) -> list: ...
   # Violation: subclass may return None
   def get_items(self): return None  # weaker postcondition 🚩
   ```

3. **Invariants must be preserved** — what holds for the base class instance must hold for the subclass.
   ```python
   # Base invariant: balance is always >= 0
   class BankAccount:
       def withdraw(self, amount): ...  # enforces balance >= 0
   # Violation: subclass allows negative balance
   class OverdraftAccount(BankAccount):
       def withdraw(self, amount): self.balance -= amount  # can go negative 🚩
   ```

4. **No new exceptions** — subclass can't raise exceptions the caller doesn't expect from the base.
   ```python
   # Base: never raises
   def process(self) -> None: ...
   # Violation: subclass raises unexpectedly
   def process(self) -> None: raise NotImplementedError  # 🚩
   ```

---

## Python-Specific Notes

### ABCs Enforce Signatures, Not Contracts
`@abstractmethod` ensures a method *exists* in subclasses, but it does NOT verify:
- That the return type is correct
- That invariants are preserved
- That exceptions are not strengthened

Contract adherence is a design responsibility, not enforced by the language.

### collections.abc — Python's Built-In Behavioral Contracts
Python's `collections.abc` module defines interfaces with well-specified behavioral contracts:

```python
from collections.abc import Sequence, MutableMapping

class MyList(Sequence):
    # Must implement: __getitem__, __len__
    # Contract: indexable, iterable, len() works, in-operator works
    # LSP: any code expecting a Sequence works with MyList
```

When you extend these, you inherit behavioral expectations. Users of `Sequence` expect indexing, slicing, iteration — your subclass must honor all of these.

### Type Hints Don't Enforce LSP Either
```python
def compute(r: Rectangle) -> float:
    return r.area()  # caller assumes r behaves like Rectangle

compute(Square(5))   # Python won't stop this — runtime only
```

Static type checkers (mypy, pyright) can help catch some violations.

### Covariance and Contravariance
Advanced LSP topic: return types may be more specific (covariant), parameter types may be more general (contravariant):

```python
class Animal:
    def make_sound(self) -> str: ...

class Dog(Animal):
    def make_sound(self) -> str:   # same return type — fine
        return "Woof"

# Contravariance: subclass can accept MORE general params (rare in Python)
```

---

## How to Spot LSP Violations

| Red Flag | What It Means |
|----------|--------------|
| `isinstance()` checks in shared code | Caller treats subtypes differently — polymorphism failed |
| `raise NotImplementedError` in subclass | Subclass can't fulfil the contract |
| Method ignores parameters the base uses | Subclass changes observable behavior |
| Test written for base fails on subclass | Direct violation by definition |
| Comment "not applicable in this subtype" | Wrong hierarchy |

---

## Fix Strategies

### 1. Redesign the Hierarchy
Keep independent concepts separate:
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Rectangle(Shape):
    def __init__(self, w: float, h: float) -> None:
        self.width, self.height = w, h
    def area(self) -> float:
        return self.width * self.height

class Square(Shape):           # Square IS-A Shape ✅ (not Rectangle)
    def __init__(self, side: float) -> None:
        self.side = side
    def area(self) -> float:
        return self.side ** 2
```

Both substitute cleanly for `Shape`. Neither substitutes for the other — correct!

### 2. Composition Over Inheritance
Instead of `Square(Rectangle)`, use a helper:
```python
class Square:
    def __init__(self, side: float) -> None:
        self._rect = Rectangle(side, side)  # composition

    def area(self) -> float:
        return self._rect.area()
```

### 3. Interface Segregation (ISP)
If a subclass keeps raising `NotImplementedError`, the interface is too broad. Split it into smaller, more focused interfaces — only subclasses that fully implement each part.

---

## Quick Example — Correct

```python
from abc import ABC, abstractmethod
from typing import List

class Notification(ABC):
    """Base contract: send a message string to a recipient."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Return True if sent successfully, False otherwise. Never raise."""
        ...

class EmailNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Email → {recipient}: {message}")
        return True   # postcondition: returns bool ✅

class SMSNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        print(f"SMS → {recipient}: {message[:160]}")   # SMS limit
        return True   # postcondition: returns bool ✅

class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        if not recipient.startswith("device_"):
            return False   # valid: returns bool (False, not raise) ✅
        print(f"Push → {recipient}: {message}")
        return True

# ✅ LSP satisfied: every subclass can replace Notification without breaking caller
def notify_all(users: List[str], notifier: Notification) -> None:
    for user in users:
        notifier.send(user, "Welcome!")   # same call, any subtype
```

---

## When to Use Inheritance (LSP-Safe) vs. Composition

| Use inheritance when | Use composition when |
|---------------------|---------------------|
| Subtype truly IS the base type (behaviorally) | Subtype only USES the base type |
| All base methods make sense in subtype | Some methods don't apply |
| Caller should freely substitute | Caller explicitly chooses the implementation |

**Rule of thumb:** If you ever write `raise NotImplementedError` in an inherited method, consider composition instead.

---

## Common Mistakes

- **"Square is mathematically a rectangle"** — mathematical relationships don't always translate to OOP substitutability. The behavior must be compatible, not just the label.
- **Using `NotImplementedError` in subclass methods** — violates postcondition; use ISP or composition instead.
- **Deep inheritance hierarchies** — each level adds risk of narrowing the contract. Prefer shallow hierarchies (max 2-3 levels).
- **Forgetting invariants** — a subclass that preserves method signatures but breaks class-level invariants (e.g., "balance always >= 0") still violates LSP.
- **Overriding methods to do nothing (`pass`)** — technically doesn't raise, but weakens postcondition (caller expected some side effect).

---

## See Also

- **Polymorphism** (Module 01, Topic 04) — LSP is what makes polymorphism safe
- **Interface Segregation** (LSP and ISP are complementary — ISP prevents fat interfaces that force LSP violations)
- **Strategy Pattern** (Module 03) — concrete example of LSP-correct substitution
