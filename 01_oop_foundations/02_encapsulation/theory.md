# Encapsulation

## What is it?

Encapsulation means: **keep the inside safe, show only what others need.**

Think of an ATM machine:
- You can check your balance and withdraw money (you see the outside)
- You cannot touch the cash box or change the database directly (the inside is protected)

That is encapsulation. The ATM controls how you interact with it.

---

## The problem without encapsulation

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance  # anyone can change this directly

acc = BankAccount(1000)
acc.balance = -99999  # oops! this should not be allowed
```

There is no protection. Anyone can break the object by setting bad values.

---

## The fix: use `@property`

`@property` lets you control how a value is read and changed.

```python
class BankAccount:
    def __init__(self, balance: float):
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = balance  # the _ means "don't touch this directly"

    @property
    def balance(self) -> float:
        return self._balance     # safe way to read the balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount  # only this method can change the balance

acc = BankAccount(1000)
print(acc.balance)   # 1000  ← uses @property
acc.deposit(500)     # safe
# acc.balance = -99999  ← this would raise an error now
```

**What is `_balance`?**
The single underscore `_` is a signal: "this is internal, don't touch it from outside."
Python does not block you, but it is a strong convention that everyone follows.

**`@property`** makes `acc.balance` work like a variable, but secretly runs your getter method.

---

## Real-world applications

- Many systems need read-only fields. Example: a ticket ID should never change after booking.
- Use `@property` without a setter to make a field read-only.
- Validation in setters prevents objects from ever being in an invalid state.

```python
@property
def ticket_id(self) -> str:
    return self._ticket_id  # read-only, no setter
```

---

## The one mistake beginners make

**Adding `@property` for everything.** Not every field needs it.

Use `@property` when:
- You need validation (e.g., age must be > 0)
- The field should be read-only
- You need to compute a value (e.g., `area = width * height`)

For simple fields that don't need protection, just use a plain attribute.

---

## What to do next

1. Open `examples/example1_properties.py` — see the before/after with a real example
2. (Optional, advanced) `examples/example2_name_mangling.py` — deeper Python conventions
3. Do `exercises/starter.py` — build a Temperature class with properties
