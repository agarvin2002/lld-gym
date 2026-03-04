# Decorator Pattern

## 1. What Is It?

The Decorator pattern attaches additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

In short: **wrap an object with another object that adds behavior before or after delegating to the original.**

---

## 2. Analogy: Ice Cream Toppings

Start with a plain vanilla ice cream. Now add chocolate sauce. Now add whipped cream. Now add sprinkles.

Each topping *wraps* the previous creation — it doesn't change what's underneath. You can add, remove, or reorder toppings freely. The result is always still "ice cream" (same interface), just with extra stuff.

- **Component**: plain ice cream
- **Decorators**: chocolate sauce, whipped cream, sprinkles
- **Key insight**: each layer shares the same interface, so you can nest them infinitely

---

## 3. Python's `@decorator` vs GoF Decorator Pattern

These are **two different things that share a name**.

### Python's `@decorator` syntax

```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def greet(name: str) -> str:
    return f"Hello, {name}"
```

- Applies to **functions**
- Done at **class/module load time** (decoration happens once)
- Returns a **new function** that wraps the original
- Primarily a Python language feature

### GoF Decorator Pattern

```python
class LoggingService(Service):
    def __init__(self, wrapped: Service):
        self._wrapped = wrapped

    def process(self, data: str) -> str:
        print("Before")
        result = self._wrapped.process(data)
        print("After")
        return result
```

- Applies to **objects** (instances)
- Done at **runtime** — you choose what to wrap at any point
- Returns an **object** implementing the same interface
- A structural design pattern

**Rule of thumb**: Python `@decorator` is for aspect-like wrapping of functions. GoF Decorator is for dynamic composition of object behavior.

---

## 4. Use Cases

- **Logging**: transparently log all calls to a service
- **Authentication / Authorization**: check permissions before delegating
- **Caching**: cache results, skip computation on repeat calls
- **Rate limiting**: throttle calls without touching the service
- **Retry logic**: retry failed operations transparently
- **Compression**: transparently compress/decompress data streams
- **Validation**: validate input before passing to the real implementation

---

## 5. Quick Example: Coffee Shop

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: ...
    @abstractmethod
    def description(self) -> str: ...

class Espresso(Coffee):
    def cost(self) -> float: return 2.00
    def description(self) -> str: return "Espresso"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee) -> None:
        self._coffee = coffee
    def cost(self) -> float: return self._coffee.cost()
    def description(self) -> str: return self._coffee.description()

class Milk(CoffeeDecorator):
    def cost(self) -> float: return self._coffee.cost() + 0.30
    def description(self) -> str: return self._coffee.description() + ", Milk"

class Sugar(CoffeeDecorator):
    def cost(self) -> float: return self._coffee.cost() + 0.10
    def description(self) -> str: return self._coffee.description() + ", Sugar"

# Compose at runtime
drink = Sugar(Milk(Milk(Espresso())))
print(drink.description())  # Espresso, Milk, Milk, Sugar
print(drink.cost())          # 2.70
```

---

## 6. Structure (UML)

```
    Component (ABC)
    ┌───────────────┐
    │ + operation() │
    └───────────────┘
           ▲
           │ implements
    ┌──────┴─────────┐         ┌──────────────────┐
    │ ConcreteComponent│        │ Decorator (ABC)   │
    │ + operation()   │        │ - wrappee: Component│
    └─────────────────┘        │ + operation()     │
                               └──────────┬────────┘
                                          ▲
                               ┌──────────┴────────┐
                               │ ConcreteDecorator  │
                               │ + operation()      │
                               └────────────────────┘
```

---

## 7. Common Mistakes

1. **Confusing Python `@decorator` with GoF Decorator**: They're different. GoF Decorator is about objects, not functions.
2. **Breaking the interface contract**: Every decorator must implement the full interface — no skipping methods.
3. **Deep nesting without transparency**: If you forget to delegate to `self._wrapped`, the underlying object never gets called.
4. **Using decorators when subclassing is cleaner**: If you only have one combination, a subclass is simpler.
5. **Forgetting to forward all interface methods**: If your base class has 10 methods and you only override 3, you need a base `Decorator` class that delegates all 10.
