# Topic 02: Encapsulation

## 1. What is Encapsulation?

Encapsulation is the practice of **bundling data and the methods that operate on that data together** within a class, and **restricting direct access to some of that data** so the object can control how it is modified.

In other words: an object owns its data and controls the rules under which that data can change. The outside world interacts with the object through a defined interface, not by reaching in and flipping values directly.

---

## 2. Real-World Analogies

### The Pill Capsule

A medication capsule bundles the active ingredients inside a controlled shell. You don't interact with the raw chemicals — you interact with the capsule. The capsule controls when the ingredients are released (often in a delayed or targeted way). You cannot inject things into the capsule after it's manufactured.

This is encapsulation: the internals are hidden and controlled.

### The Car

You drive a car using the **steering wheel, accelerator, and brake** — the *interface*. You don't need to understand how the fuel injector, crankshaft, or ABS system work internally. In fact, if you tried to directly manipulate the engine while driving, you'd probably crash.

The car's internals are **hidden from the driver**. The car's designers chose which controls to expose (steering, gas, brakes) and kept everything else internal. This lets them redesign the engine entirely without changing how drivers use the car.

---

## 3. Why Encapsulation Matters

### Prevent Invalid State

Without encapsulation, any code anywhere in the system can set a `BankAccount`'s balance to a negative number or a string. With encapsulation, the `BankAccount` class controls all mutations and can reject invalid inputs.

```python
# Without encapsulation — anyone can do this:
account.balance = -9999  # silent corruption, causes bugs later

# With encapsulation — the object rejects this:
account.deposit(-9999)   # raises ValueError immediately at the point of error
```

### Hide Complexity

The internal implementation of a class can be arbitrarily complex — caching, lazy computation, format conversion, validation chains — without the caller needing to know about any of it. This reduces the cognitive load for everyone using the class.

### Enable Refactoring

If all access to internal data goes through methods and properties, you can change the internal representation without breaking external code. For example, if a `Temperature` class initially stores temperature in Celsius, you can later switch to Kelvin internally without changing any code that uses the class — because all access goes through `@property` getters.

---

## 4. Python-Specific: Access Control Conventions and Mechanisms

Python does not have strict private/public/protected access modifiers like Java or C++. Instead, it uses conventions that every Python developer understands:

### Public (no prefix): `self.name`
Anyone can read and write this. Use it for attributes that are genuinely part of the public interface.

```python
self.name = "Alice"    # Public — safe to read from outside
```

### Protected (single underscore): `self._balance`
The single underscore is a *convention* saying: "This is an internal implementation detail. Don't access it from outside the class unless you know what you're doing." It is not enforced by Python — it's a social contract between developers.

Use this for attributes you want to protect but might need to access from subclasses.

```python
self._balance = 0.0    # Protected — internal detail, handle with care
```

### Private (double underscore): `self.__password`
The double underscore triggers **name mangling**: Python renames the attribute from `__password` to `_ClassName__password`. This is a technical mechanism (not just convention) designed to prevent *accidental* name collisions in subclasses.

```python
class MyClass:
    def __init__(self):
        self.__secret = 42

obj = MyClass()
# obj.__secret       # AttributeError — name doesn't exist at this name
# obj._MyClass__secret  # This works — the mangled name is accessible
```

Use `__private` sparingly — only when you genuinely need to prevent subclasses from accidentally overriding an attribute name. Overuse creates friction and is considered Pythonic bad practice.

### `@property`: Controlled Attribute Access

A `@property` lets you define getter/setter/deleter behavior for what looks like an attribute from the outside. This is the primary encapsulation tool in Python.

**Getter only (read-only attribute):**
```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        """Read-only access to the radius."""
        return self._radius
```

**Getter + Setter (with validation):**
```python
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius  # Goes through the setter — validation runs here too

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"Radius must be positive, got {value}.")
        self._radius = value
```

**Getter + Deleter:**
```python
@radius.deleter
def radius(self) -> None:
    del self._radius
```

### When to Use `@property` vs Direct Attribute

| Use `@property` | Use Direct Attribute |
|-----------------|----------------------|
| You need validation on set | Value is always valid (set once in `__init__`) |
| Value is computed from other attributes | Simple public data, no invariants to enforce |
| You want read-only access | Class is a simple data container (`@dataclass`) |
| You need to change internal representation later | Attribute is intentionally public API |

---

## 5. Quick Example: BankAccount with Encapsulation

```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.owner = owner        # Public — the owner's name is fine to read
        self._balance = initial_balance  # Protected — don't set this directly

    @property
    def balance(self) -> float:
        """Read-only access to balance. Balance can only change via deposit/withdraw."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Add funds. Validates that amount is positive."""
        if amount <= 0:
            raise ValueError(f"Deposit must be positive, got {amount}.")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Remove funds. Validates amount and checks sufficient funds."""
        if amount <= 0:
            raise ValueError(f"Withdrawal must be positive, got {amount}.")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds.")
        self._balance -= amount
```

Notice:
- `balance` is a read-only property — callers can see the balance but cannot directly set it
- Mutations only happen through `deposit()` and `withdraw()`, both of which validate input
- The `_balance` attribute is protected by convention — but the property provides safe access

---

## 6. When Properties Are Better Than Direct Attributes

Consider a `Rectangle` where width and height are set directly:

```python
# Without property — anyone can set invalid values
rect = Rectangle(10, 5)
rect.width = -3    # Oops — negative width, but no error raised
rect.area()        # returns -15 — silent corruption
```

With properties:

```python
# With property — setter validates immediately
rect = Rectangle(10, 5)
rect.width = -3    # Raises ValueError — caught immediately at the point of error
```

The property approach **fails fast and loudly** instead of silently corrupting state.

---

## 7. Common Mistakes

### Over-Privatizing

```python
# Overkill — using __ when _ would do
class Person:
    def __init__(self, name: str) -> None:
        self.__name = name  # Why? There's no subclass collision risk here.
        # Use self._name or even self.name instead.
```

Use `__private` only when you have a specific reason to prevent subclasses from accessing or accidentally overriding the attribute. For typical "internal implementation detail" use cases, `_protected` is the right choice.

### Forgetting That `__private` Is Not Actually Private

```python
class Safe:
    def __init__(self):
        self.__secret = "the password"

s = Safe()
print(s._Safe__secret)  # Prints "the password" — still accessible!
```

Name mangling prevents *accidental* access, not *intentional* access. Do not rely on `__private` for security.

### Mutable Property Returns

```python
class Config:
    def __init__(self):
        self._settings = {"debug": False}

    @property
    def settings(self) -> dict:
        return self._settings  # WRONG — caller can mutate the internal dict!
        # CORRECT: return dict(self._settings)  # return a copy
```

If a property returns a mutable object (list, dict, set), return a copy unless you intentionally want callers to be able to modify the internal state.

### Using `@property` for Expensive Computations Without Caching

A property that does heavy computation will re-run that computation every time the attribute is accessed. If the result doesn't change often, consider caching or using a regular method to signal that calling it has a cost.

---

## 8. Exercises

Head to [exercises/problem.md](exercises/problem.md) to build a `Temperature` class that uses properties for unit conversion.

The exercise reinforces:
- Using `@property` for read-only computed attributes
- Using `@property` + `@setter` with validation
- Internal storage in one representation, public API in multiple representations
- Proper encapsulation: only one setter, all other conversions are derived

After attempting the exercise, compare your solution to [exercises/solution/solution.py](exercises/solution/solution.py) and read [exercises/solution/explanation.md](exercises/solution/explanation.md).
