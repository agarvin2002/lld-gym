# Inheritance

## What is it?

Inheritance means: **one class can get everything from another class.**

The class that shares its things is called the **parent** (or base class).
The class that takes those things is called the **child** (or subclass).

Think of it like this:
- A Vehicle has wheels and can move.
- A Car is a Vehicle. So a Car also has wheels and can move.
- A Car also has its own things (like a music system).

You do not rewrite the wheel code. The Car just **inherits** it from Vehicle.

---

## See it in code

```python
class Vehicle:
    def __init__(self, brand: str, speed: int):
        self.brand = brand
        self.speed = speed

    def move(self) -> str:
        return f"{self.brand} is moving at {self.speed} km/h"

class Car(Vehicle):             # Car inherits from Vehicle
    def __init__(self, brand: str, speed: int, num_doors: int):
        super().__init__(brand, speed)  # call Vehicle's __init__ first
        self.num_doors = num_doors      # Car's own new attribute

    def honk(self) -> str:
        return f"{self.brand}: Beep beep!"

car = Car("Maruti", 80, 4)
print(car.move())   # Maruti is moving at 80 km/h  ← from Vehicle
print(car.honk())   # Maruti: Beep beep!           ← Car's own method
```

**`super().__init__(...)`** — this calls the parent's `__init__`. Always call this first in the child's `__init__`. If you forget, the parent's attributes won't be set up.

---

## Overriding a method

The child can change how a parent method works:

```python
class ElectricCar(Car):
    def move(self) -> str:
        return f"{self.brand} is moving silently at {self.speed} km/h"

e = ElectricCar("Tata Nexon EV", 120, 4)
print(e.move())  # Tata Nexon EV is moving silently at 120 km/h
```

Same method name (`move`), different behaviour. This is called **overriding**.

---

## Real-world applications

- Almost every multi-class system has a base class. Example: `Vehicle → Car, Truck, Bike`.
- Always call `super().__init__()` in the child's `__init__` — this is a common source of bugs when forgotten.
- Use inheritance when classes share real common behaviour, not just to avoid repeating code.

---

## The one mistake beginners make

**Forgetting `super().__init__()`.**

```python
class Car(Vehicle):
    def __init__(self, brand, speed, num_doors):
        # forgot super().__init__() !
        self.num_doors = num_doors

car = Car("Maruti", 80, 4)
print(car.speed)  # AttributeError! speed was never set
```

Always call `super().__init__(...)` as the first line in the child's `__init__`.

---

## When to use inheritance vs. composition

Use inheritance when the relationship is a genuine **"is-a"**: a `Car` is a `Vehicle`. If you find yourself inheriting just to reuse a method, that's a sign the relationship is really **"has-a"** — and composition is the better fit.

```python
# Composition — Engine is not a Car, it's part of a Car
class Engine:
    def start(self) -> str:
        return "Engine started"

class Car:
    def __init__(self):
        self._engine = Engine()   # Car "has an" Engine

    def start(self) -> str:
        return self._engine.start()
```

A deeper discussion of when inheritance breaks down appears in `02_solid_principles/03_liskov_substitution/`.

---

## What to do next

1. Open `examples/example1_single_inheritance.py` — see shapes using inheritance
2. (Optional, advanced) `examples/example2_mro_and_super.py` — how Python handles multiple parents
3. Do `exercises/starter.py` — build an Employee hierarchy
