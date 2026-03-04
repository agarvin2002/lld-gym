# Topic 01: Classes and Objects

## 1. What is a Class? What is an Object?

A **class** is a blueprint that defines the structure and behavior of a category of things — it specifies what data those things hold and what operations they can perform.

An **object** (also called an *instance*) is a concrete realization of that blueprint — it is an actual thing in memory with its own specific data.

---

## 2. Real-World Analogy: Blueprint vs. House

Think of an architectural blueprint for a house. The blueprint defines:
- How many rooms there are
- Where the doors and windows go
- What the load-bearing walls are

But the blueprint is **not** a house you can live in. You use it to *build* houses — and each house built from the same blueprint is its own physical thing with its own address, its own paint color, and its own residents.

```
Blueprint  →  Class
House      →  Object (instance)
```

You can build many houses from one blueprint. Similarly, you can create many objects from one class. Each object has its own copy of the data (attributes), but all share the same behavior (methods) defined in the class.

---

## 3. Why Classes Matter in LLD

In Low-Level Design, you are asked to model real systems. Classes are the primary tool for this for three reasons:

**Modeling**: A class maps directly to a real-world entity or concept. A `PaymentGateway` class is recognizable to every engineer on the team. A dict `{"gateway": "stripe", "key": "sk_..."}` is not.

**Reuse**: Once you define a `User` class, you can create thousands of user objects. You write the logic once (validation, formatting, serialization) and every object gets it for free.

**Encapsulation**: A class bundles data and the methods that operate on it. This means the class itself enforces its own rules. You cannot set a negative price on a `Product` if the class prevents it — you don't need to remember to check everywhere else.

---

## 4. Python-Specific: The Core Mechanics

### `__init__` — The Constructor

`__init__` is called automatically when you create an object. It initializes the object's attributes.

```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0):
        self.owner = owner
        self._balance = initial_balance  # underscore = "internal, handle with care"
```

### `self` — The Instance Reference

`self` is a reference to the object being operated on. Python passes it automatically as the first argument to every instance method. When you call `account.deposit(100)`, Python translates this to `BankAccount.deposit(account, 100)`.

Without `self`, a method cannot access or modify the object's attributes.

### `__repr__` vs `__str__`

Both control how objects are displayed as strings, but they serve different audiences:

| Method | Audience | Purpose | Example output |
|--------|----------|---------|----------------|
| `__repr__` | Developers | Unambiguous, ideally reconstructable | `BankAccount(owner='Alice', balance=500.0)` |
| `__str__` | End users | Human-readable | `Alice's account: $500.00` |

If only one is defined, Python falls back to `__repr__` for both. **Always define `__repr__`**. It makes debugging dramatically easier — you can see the state of an object at a glance in the REPL or in error messages.

```python
def __repr__(self) -> str:
    return f"BankAccount(owner={self.owner!r}, balance={self._balance:.2f})"

def __str__(self) -> str:
    return f"{self.owner}'s account: ${self._balance:.2f}"
```

### `__eq__` and `__hash__`

By default, Python compares objects by identity (same memory address). Two distinct `BankAccount` objects are never `==` even if they have the same data.

If you want value-based equality (two accounts are equal if they have the same owner and balance), define `__eq__`:

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, BankAccount):
        return NotImplemented
    return self.owner == other.owner and self._balance == other._balance
```

**Critical rule**: If you define `__eq__`, you must also define `__hash__` — or Python will make your objects unhashable (cannot be used in sets or as dict keys). If equality is based on mutable state, set `__hash__ = None` explicitly. If equality is based on immutable identity fields, implement `__hash__` consistently:

```python
def __hash__(self) -> int:
    return hash(self.owner)  # only hash immutable fields
```

### `dataclasses`

Python's `dataclasses` module auto-generates `__init__`, `__repr__`, and optionally `__eq__` and `__hash__` for you based on field annotations. Use it when your class is primarily a data container:

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = "unnamed"

p = Point(1.0, 2.0)
print(p)  # Point(x=1.0, y=2.0, label='unnamed')
```

Use `@dataclass(frozen=True)` for immutable objects (gets you a correct `__hash__` automatically). Use `@dataclass(order=True)` to get `__lt__`, `__le__`, etc. for sorting.

---

## 5. When to Use a Class vs a Function vs a Dict

This is a judgment call that comes up constantly in LLD:

| Use this | When |
|----------|------|
| **Class** | The thing has both data AND behavior. Multiple instances will exist. You need to enforce invariants (rules about valid state). |
| **Function** | It's a pure computation — input goes in, output comes out, no state persists. |
| **Dict** | Temporary data grouping, no behavior, no validation, not a first-class citizen of your design. Probably thrown away soon. |
| **dataclass** | Mostly data, minimal behavior, you want auto-generated dunder methods. |
| **namedtuple** | Immutable record, no behavior, needs to be hashable and lightweight. |

**Red flags for "this should be a class"**:
- You keep passing the same group of variables into multiple functions together
- You need to validate that data is in a valid state
- The "thing" has a lifecycle (created, modified, destroyed)
- Other parts of the system need to interact with this thing in structured ways

---

## 6. Quick Example: BankAccount Class

```python
from datetime import datetime

class BankAccount:
    """A simple bank account demonstrating core class concepts."""

    def __init__(self, owner: str, account_number: str, initial_balance: float = 0.0) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.owner = owner
        self.account_number = account_number
        self._balance = initial_balance
        self._created_at = datetime.now()

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}.")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive, got {amount}.")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds: balance is {self._balance}, requested {amount}.")
        self._balance -= amount

    def get_balance(self) -> float:
        return self._balance

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, account_number={self.account_number!r}, balance={self._balance:.2f})"

    def __str__(self) -> str:
        return f"Account [{self.account_number}] owned by {self.owner} — Balance: ${self._balance:.2f}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.account_number == other.account_number

    def __hash__(self) -> int:
        return hash(self.account_number)
```

Notice:
- `__init__` validates input immediately — the object is always born in a valid state
- `_balance` uses a leading underscore to signal "don't touch this directly"
- `__repr__` shows all the information needed to understand the object's state
- `__eq__` uses `account_number` (the stable identity), not `balance` (which changes)
- `__hash__` is consistent with `__eq__`

---

## 7. Common Mistakes

### Mutable Default Arguments

```python
# WRONG — all instances share the same list!
class ShoppingCart:
    def __init__(self, items=[]):
        self.items = items

# CORRECT — create a new list for each instance
class ShoppingCart:
    def __init__(self):
        self.items = []
```

This is one of Python's most infamous gotchas. Default argument values are evaluated once at function definition time, not each time the function is called. Using a mutable default (list, dict, set) means all instances that don't pass an argument will share the same object.

### Forgetting `self`

```python
# WRONG — balance is a local variable, not an instance attribute
class BankAccount:
    def __init__(self, balance):
        balance = balance  # this does nothing useful

# CORRECT
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
```

### Not Defining `__hash__` When Defining `__eq__`

If you define `__eq__` without `__hash__`, Python sets `__hash__` to `None`, making your objects unhashable. This will crash if you try to put them in a set or use them as dict keys.

### Using `__private` When You Mean `_protected`

Double-underscore name mangling (`__attr`) is for avoiding name collisions in subclasses, not for security. Use single underscore (`_attr`) for "this is an implementation detail, be careful". Reserve `__attr` for cases where you genuinely need to prevent subclasses from accidentally overriding a name.

### `__str__` Without `__repr__`

Always define `__repr__`. If you only define `__str__`, the REPL and logging will still show the useless default `<ClassName object at 0x...>` in many contexts.

---

## 8. Exercises

Head to [exercises/problem.md](exercises/problem.md) to build a `Product` and `ShoppingCart` class from scratch.

The exercise reinforces:
- Defining classes with validation in `__init__`
- Instance methods that modify state
- `__repr__` for debugging
- `__eq__` for comparisons

After attempting the exercise, compare your solution to [exercises/solution/solution.py](exercises/solution/solution.py) and read [exercises/solution/explanation.md](exercises/solution/explanation.md) for the reasoning behind the design decisions.
