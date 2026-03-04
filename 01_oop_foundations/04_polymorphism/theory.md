# Topic 04: Polymorphism

## 1. What Is Polymorphism?

Polymorphism comes from Greek: *poly* (many) + *morphe* (form). In programming it means:

> **The same interface can produce different behaviors depending on the object behind it.**

You call the same method name on different objects, and each object does the right thing for its own type — without the caller needing to know which type it is.

```python
for animal in [Dog(), Cat(), Duck()]:
    animal.speak()   # each type decides what "speak" means
```

---

## 2. Analogy: The `+` Operator

Python's `+` operator is the simplest everyday example of polymorphism:

```python
3 + 4          # → 7        (integer addition)
"hello" + "!"  # → "hello!" (string concatenation)
[1, 2] + [3]   # → [1, 2, 3] (list merge)
```

The *interface* is identical (`a + b`). The *behavior* is completely different depending on the type. You never write:

```python
if isinstance(a, int):
    ...
elif isinstance(a, str):
    ...
```

The object itself knows what to do. That is polymorphism.

---

## 3. Why It Matters

### Extensibility
Add a new type without changing existing code. A new `CryptoPayment` class just needs a `charge()` method — the rest of the system works automatically.

### Open/Closed Principle (Preview)
Classes should be **open for extension, closed for modification**. Polymorphism is the mechanism that makes this possible. You extend by adding new classes, not by editing old ones.

### Clean Conditionals
Compare these two approaches:

**Without polymorphism (bad):**
```python
def process_payment(payment, amount):
    if isinstance(payment, CreditCard):
        payment.charge_card(amount)
    elif isinstance(payment, PayPal):
        payment.send_paypal_request(amount)
    elif isinstance(payment, Crypto):
        payment.broadcast_transaction(amount)
    # Every new type requires editing this function
```

**With polymorphism (good):**
```python
def process_payment(payment, amount):
    payment.charge(amount)   # works for any payment type
```

The second version never needs to change when you add a new payment method.

---

## 4. Python-Specific Mechanics

### 4.1 Method Overriding

A subclass provides its own implementation of a method defined in the parent class:

```python
class Notification:
    def send(self, message: str) -> bool:
        raise NotImplementedError

class EmailNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"Sending email: {message}")
        return True

class SMSNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"Sending SMS: {message}")
        return True
```

Python uses **late binding** — the method looked up is always from the actual runtime type, not the declared type. This is dynamic dispatch.

### 4.2 Duck Typing

> *"If it walks like a duck and quacks like a duck, it's a duck."*

Python does not require explicit inheritance to achieve polymorphism. If an object has the right method, it works:

```python
class Dog:
    def speak(self):
        return "Woof"

class Robot:
    def speak(self):
        return "Beep boop"

def make_noise(thing):   # no type constraint at all
    print(thing.speak())

make_noise(Dog())    # Woof
make_noise(Robot())  # Beep boop — Robot is not a Dog, but it works
```

Python resolves method calls at runtime. If the attribute exists, the call succeeds. This is structurally more flexible than nominal typing (Java/C# style).

### 4.3 `isinstance()` vs Duck Typing — Tradeoffs

| Approach | Pros | Cons |
|---|---|---|
| `isinstance()` | Explicit, IDE-friendly, documents intent | Couples code to class hierarchy, hard to extend |
| Duck typing | Flexible, no inheritance needed, easy to mock | Less obvious what interface is expected |
| `typing.Protocol` | Best of both: structural + static type checking | Requires Python 3.8+, slight learning curve |

**Rule of thumb:** Prefer duck typing in internal code. Use `isinstance()` at system boundaries (user input, deserialization). Use `Protocol` when you want static analysis without forcing inheritance.

### 4.4 `@functools.singledispatch` (Brief Mention)

For function-level (rather than method-level) polymorphism, Python provides `singledispatch`:

```python
from functools import singledispatch

@singledispatch
def process(value):
    raise NotImplementedError(f"No handler for {type(value)}")

@process.register(int)
def _(value: int):
    print(f"Integer: {value * 2}")

@process.register(str)
def _(value: str):
    print(f"String: {value.upper()}")

process(42)      # Integer: 84
process("hello") # String: HELLO
```

This is useful when you cannot add methods to the types involved (e.g., built-in types or third-party classes).

---

## 5. Two Types of Polymorphism in Python

### Subtype Polymorphism (Nominal)
The classical OOP form. A subclass inherits from a base class and overrides methods. The relationship is explicit in the code.

```python
class Shape:
    def area(self) -> float: ...

class Circle(Shape):
    def area(self) -> float: return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def area(self) -> float: return self.width * self.height
```

Any code expecting a `Shape` can receive a `Circle` or `Rectangle`.

### Duck Typing Polymorphism (Structural)
No inheritance required. Objects are compatible if they have the right attributes/methods.

```python
# These classes share NO common ancestor
class Circle:
    def area(self) -> float: ...

class Triangle:
    def area(self) -> float: ...

def total_area(shapes: list) -> float:
    return sum(s.area() for s in shapes)  # works for both
```

`typing.Protocol` makes structural typing explicit and statically checkable.

---

## 6. Quick Example: Payment Processor

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool: ...

class CreditCard(PaymentProcessor):
    def charge(self, amount: float) -> bool:
        print(f"Charging ${amount} to credit card")
        return True

class PayPal(PaymentProcessor):
    def charge(self, amount: float) -> bool:
        print(f"Sending ${amount} via PayPal")
        return True

class Crypto(PaymentProcessor):
    def charge(self, amount: float) -> bool:
        print(f"Broadcasting ${amount} crypto transaction")
        return True

def checkout(processor: PaymentProcessor, amount: float) -> None:
    success = processor.charge(amount)
    print("Payment successful" if success else "Payment failed")

# All three work identically from the caller's perspective
checkout(CreditCard(), 99.99)
checkout(PayPal(), 49.50)
checkout(Crypto(), 0.005)
```

Adding a new payment method like `ApplePay` requires zero changes to `checkout()`.

---

## 7. Common Mistakes

### Mistake 1: `isinstance` Chains Instead of Polymorphism

```python
# BAD — violates open/closed principle
def calculate_discount(item):
    if isinstance(item, PremiumItem):
        return item.price * 0.8
    elif isinstance(item, SaleItem):
        return item.price * 0.5
    elif isinstance(item, RegularItem):
        return item.price
    # Adding a new item type requires editing this function

# GOOD — each class knows its own discount
class PremiumItem:
    def discounted_price(self) -> float:
        return self.price * 0.8

def calculate_discount(item):
    return item.discounted_price()   # never changes
```

### Mistake 2: Overriding Without Calling `super()`

When a parent class has important logic in a method, forgetting `super()` silently breaks it:

```python
class Base:
    def setup(self):
        self.initialized = True   # important!

class Child(Base):
    def setup(self):
        self.name = "child"       # forgot super().setup()
        # self.initialized never set — silent bug
```

### Mistake 3: Changing the Method Signature in Subclasses

Polymorphism only works if the interface is consistent. Changing parameter names or types in a subclass violates the Liskov Substitution Principle (covered in SOLID topics).

```python
# BAD — breaks the contract
class EmailNotification(Notification):
    def send(self, message: str, recipient: str) -> bool:  # extra param!
        ...
```

---

## Summary

| Concept | Key Idea |
|---|---|
| Polymorphism | Same interface, different behavior per type |
| Method overriding | Subclass redefines parent method |
| Duck typing | "Has the method" is enough — no inheritance needed |
| `isinstance` chains | Red flag — usually means polymorphism is missing |
| `singledispatch` | Function-level dispatch by argument type |
| `typing.Protocol` | Structural typing with static analysis support |

The core insight: **write code that talks to interfaces, not implementations**. When you call `payment.charge()`, you don't care whether it's a credit card or crypto — and that's the point.
