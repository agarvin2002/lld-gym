# Open/Closed Principle (OCP)

## 1. Definition

> **"Software entities (classes, modules, functions) should be open for extension, but closed for modification."**
> — Bertrand Meyer, popularized by Robert C. Martin

"Open for extension" means you can add new behavior.
"Closed for modification" means adding new behavior does not require changing existing, tested code.

The underlying insight: existing code that works should not be touched when you add features. Every time you change working code, you risk introducing bugs. Every regression is a bug introduced in existing code. OCP minimizes that risk.

---

## 2. Analogy: The Power Strip

A power strip has a fixed design. It does not need to be modified every time you want to plug in a new device. You simply plug in a new lamp, monitor, or phone charger — the strip itself never changes.

The socket interface is the abstraction. Every device conforms to it. The strip is "closed" to modification and "open" for any new device that follows the standard.

In software, the power strip is your class. The socket is an abstract interface. New features are new "devices" that plug in.

---

## 3. Why OCP Matters

### Safety in Production
In production systems, regression risk is the primary concern. Every modification to working code is a potential source of new bugs. OCP drives you to add new behavior through extension (new classes, new modules) rather than modification. A class that is never changed after release is a class that never introduces regressions.

### Maintainability at Scale
In a codebase with many feature variants, if-else chains that grow with each new feature become impossible to maintain. A team adding a new discount type should not need to understand the internals of every existing discount type. With OCP, they write a new class in isolation.

### Testability
New behavior in a new class is independently testable. You do not need to re-test all existing discount logic when you add a new discount type. The new type is tested independently, and the orchestrator's tests remain stable.

---

## 4. Python-Specific Approaches

### Inheritance (Polymorphism)
The classic OCP mechanism. Define an abstract base class with a method signature. Subclasses provide implementations. The caller only knows the abstract type.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def area(self) -> float: return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def area(self) -> float: return self.width * self.height
```

Adding a `Triangle` requires no modification to `Shape` or any existing code.

### Strategy Pattern
The Strategy pattern is the most explicit OCP mechanism. Extract the varying behavior (the "algorithm") into its own class hierarchy. The context class accepts a strategy object and delegates to it.

```python
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, subtotal: float) -> float: ...

class PercentageDiscount(DiscountStrategy):
    def calculate(self, subtotal: float) -> float:
        return subtotal * 0.10

class FixedDiscount(DiscountStrategy):
    def calculate(self, subtotal: float) -> float:
        return 10.0

# New discount type: just add a new class, modify nothing
class BuyOneGetOneFree(DiscountStrategy):
    def calculate(self, subtotal: float) -> float:
        return subtotal * 0.50
```

### Python Protocols (Structural Subtyping)
Python's `typing.Protocol` allows OCP without explicit inheritance. Any class that implements the right methods satisfies the protocol — the strategy pattern with duck typing:

```python
from typing import Protocol

class DiscountStrategy(Protocol):
    def calculate(self, subtotal: float) -> float: ...
```

### Decorators
Python decorators are another OCP tool. They extend behavior without modifying the decorated function:

```python
def with_logging(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

---

## 5. How to Spot OCP Violations

### The Growing if/elif Chain
The most common OCP violation is an if/elif chain that must be extended every time a new type is added:

```python
def calculate_discount(order_type: str, amount: float) -> float:
    if order_type == "percentage":
        return amount * 0.10
    elif order_type == "fixed":
        return 10.0
    elif order_type == "bogo":          # Added when BOGO was requested
        return amount * 0.50
    elif order_type == "seasonal":       # Added during Q4
        return amount * 0.20
    # Every new discount type requires modifying this function!
```

Each new discount type requires:
1. Opening this file
2. Adding an elif branch
3. Re-testing all existing branches (because you modified them)
4. Risk of accidentally breaking an existing branch

### The switch on type()
```python
for shape in shapes:
    if isinstance(shape, Circle):
        area = 3.14 * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        area = shape.width * shape.height
    # Adding Triangle requires modifying this loop
```

### The Modification Smell
If every new feature request requires you to open and modify an existing, working class, that class is not closed for modification.

---

## 6. Quick Example: ShapeAreaCalculator

### Violation: if/elif on shape type

```python
class AreaCalculator:
    def calculate(self, shape: dict) -> float:
        if shape["type"] == "circle":
            return 3.14 * shape["radius"] ** 2
        elif shape["type"] == "rectangle":
            return shape["width"] * shape["height"]
        # Adding Triangle: must MODIFY this class
```

### OCP-Compliant: Polymorphic Approach

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius
    def area(self) -> float:
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    def area(self) -> float:
        return self.width * self.height

class AreaCalculator:
    def calculate(self, shape: Shape) -> float:
        return shape.area()  # Never changes, regardless of how many Shape types exist
```

Adding `Triangle` is a new file, zero modifications to existing code.

---

## 7. Common Mistakes

### Over-Engineering from Day One (YAGNI)
OCP should not be applied speculatively. If you have two discount types and no indication there will be more, an if/elif is fine. The abstraction cost (more files, more indirection) is not worth it for a system unlikely to grow.

Apply OCP *when you feel the pain* — when you're about to add the third or fourth type and you recognize the pattern. This is the Boy Scout Rule applied to architecture: refactor when you need to.

### Treating OCP as "Never Modify"
OCP is not a command to never modify existing code. Bug fixes, performance improvements, and refactoring all require modification. OCP specifically applies to *adding new behavior*: new feature variants should not require modifying stable code.

### Choosing the Wrong Abstraction
OCP only works when you identify the right axis of variation. If you abstract on the wrong thing, you get the wrong extension points. Spend time identifying what is most likely to change.

For example, in a notification system, the right axis of variation is probably the *delivery channel* (email, SMS, push). Don't abstract on *message type* unless message types are more likely to change than delivery channels.

### Making Everything Extensible
Every abstraction has a cost. If a class has a single implementation and no realistic second implementation on the horizon, do not create an abstract base class for it. Wait until you have a second implementor before introducing the abstraction.

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Definition | New behavior via extension, not modification |
| Mechanism | Strategy pattern, polymorphism, Protocols |
| Violation signal | Growing if/elif chain, isinstance switches |
| Benefit | Safer extension, reduced regression risk, independent testability |
| Python tip | Protocols allow structural subtyping — no explicit inheritance required |
| Warning | Don't abstract speculatively — wait until you have two implementations |
