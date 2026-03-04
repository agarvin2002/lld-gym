# Inheritance

## What Is It?
Inheritance lets a class **acquire attributes and methods** from another class. The child class (subclass) is a specialization of the parent (superclass) — an "is-a" relationship.

## Real-World Analogy
Animal → Mammal → Dog → Labrador

Every Labrador is a Dog. Every Dog is a Mammal. Every Mammal is an Animal.
A Labrador inherits traits (warm-blooded, has fur) from all ancestors, but also adds specifics (friendly, retrieves things).

## Why It Matters in LLD
- **Code reuse**: common logic lives once in the base class
- **Polymorphism foundation**: you can treat all `Shape` objects uniformly
- **Model real hierarchies**: Vehicle → Car + Truck reflects the domain naturally

## Python Syntax

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def breathe(self) -> str:
        return f"{self.name} breathes"

class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)  # call parent __init__ first!
        self.breed = breed

    def bark(self) -> str:
        return "Woof!"
```

### `super()` — Always Call It
`super().__init__()` ensures the parent class is properly initialized. Forgetting it is a common bug — parent attributes won't exist.

### MRO (Method Resolution Order)
Python uses **C3 linearization** to determine which method to call in multiple inheritance:

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass  # MRO: D → B → C → A

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

### Checking Types
```python
isinstance(my_dog, Dog)     # True
isinstance(my_dog, Animal)  # True (Dog is-a Animal)
issubclass(Dog, Animal)     # True
```

## When to Use Inheritance vs Composition

| Use Inheritance | Use Composition |
|-----------------|-----------------|
| True "is-a" relationship | "has-a" relationship |
| Share interface + behavior | Share behavior only |
| Hierarchy ≤ 3 levels deep | Complex/flexible behavior |
| Example: Car is-a Vehicle | Example: Car has-a Engine |

**Rule of thumb**: Prefer composition. Only use inheritance when the "is-a" relationship is stable and genuine.

## Quick Example

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand: str, year: int) -> None:
        self.brand = brand
        self.year = year

    @abstractmethod
    def fuel_type(self) -> str: ...

    def describe(self) -> str:
        return f"{self.year} {self.brand} ({self.fuel_type()})"

class Car(Vehicle):
    def fuel_type(self) -> str:
        return "Gasoline"

class ElectricCar(Vehicle):
    def fuel_type(self) -> str:
        return "Electric"

tesla = ElectricCar("Tesla", 2024)
print(tesla.describe())  # 2024 Tesla (Electric)
print(isinstance(tesla, Vehicle))  # True
```

## Common Mistakes

1. **Forgetting `super().__init__()`** — parent attributes won't be set
2. **Deep hierarchies** — max 3 levels; deeper = hard to understand
3. **Inheriting just for code reuse** — use composition or mixins instead
4. **Overriding with incompatible behavior** — violates Liskov Substitution Principle

## Links
- [Exercise →](exercises/problem.md)
- [Example 1: Shape hierarchy →](examples/example1_single_inheritance.py)
- [Example 2: MRO and mixins →](examples/example2_mro_and_super.py)
