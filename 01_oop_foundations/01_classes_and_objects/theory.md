# Classes and Objects

## What is it?

A **class** is a template. It describes what a thing looks like and what it can do.
An **object** is one real thing made from that template.

Think of it like this:
- Class = the design of an Aadhaar card (what fields it has, what it does)
- Object = your actual Aadhaar card (filled with your name, your number)

---

## See it in 10 lines

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner      # who owns this account
        self.balance = balance  # how much money is in it

    def deposit(self, amount: float) -> None:
        self.balance += amount  # add money

    def __repr__(self) -> str:
        return f"BankAccount({self.owner}, ₹{self.balance})"

acc = BankAccount("Rahul", 1000)
acc.deposit(500)
print(acc)   # BankAccount(Rahul, ₹1500)
```

**`__init__`** — runs when you create the object. Use it to set starting values.

**`self`** — means "this object". Always the first argument in every method.

**`__repr__`** — decides what prints when you do `print(obj)`. Always add this — it helps you while debugging.

---

## Real-world applications

- Every system design problem is built from classes. Parking lot → `ParkingSpot`. ATM → `Account`.
- Good design means: put the right data in `__init__`, add the right methods to the class.
- A good `__repr__` makes debugging fast — you always know what is inside your object.

---

## The one mistake beginners make

**Forgetting to check inputs in `__init__`.**

```python
# BAD — what if someone passes balance = -500?
def __init__(self, balance):
    self.balance = balance

# GOOD — catch the problem early
def __init__(self, balance):
    if balance < 0:
        raise ValueError("Balance cannot be negative")
    self.balance = balance
```

Check your inputs at the start. This stops bugs before they happen.

---

## What to do next

1. Open `examples/example1_basic_class.py` — see a full working BankAccount
2. (Optional, advanced) `examples/example2_dunder_methods.py` — Python magic methods
3. Do `exercises/starter.py` — build a Product and ShoppingCart yourself
