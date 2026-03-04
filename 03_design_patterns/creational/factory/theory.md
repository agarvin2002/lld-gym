# Factory Method Pattern

## 1. What Is It?

The **Factory Method pattern** defines an **interface for creating objects** but lets **subclasses decide which class to instantiate**. The Factory Method defers object creation to subclasses.

Two things to understand:
1. **The "factory" is a method** — not a separate class. It's a method on a creator class that produces products.
2. **Subclasses decide** — the creator class calls the factory method but doesn't know the concrete type; subclasses override the factory method to return specific types.

```python
# The creator has a template method that calls the factory method
class LogisticsCompany:
    def plan_delivery(self, cargo: str) -> str:
        transport = self.create_transport()   # ← factory method call
        return transport.deliver(cargo)

    def create_transport(self) -> Transport:  # ← factory method (abstract)
        raise NotImplementedError

# Subclasses override the factory method
class RoadLogistics(LogisticsCompany):
    def create_transport(self) -> Transport:
        return Truck()   # Subclass decides: Truck

class SeaLogistics(LogisticsCompany):
    def create_transport(self) -> Transport:
        return Ship()    # Subclass decides: Ship
```

---

## 2. The Analogy

Imagine a **hiring agency**. You (the client) call the agency and say: "I need a developer for a Python project."

You don't know which specific developer they'll send — that's the agency's decision. The agency has its own logic for matching candidates to roles. You just know the interface: the developer can `write_code()` and `do_code_review()`.

The agency is the **creator**. The developer it sends is the **product**. The act of selecting and sending a developer is the **factory method**. You, the client, work only with the developer interface.

---

## 3. Simple Factory vs Factory Method vs Abstract Factory

This is one of the most confusing things in design pattern literature. Here is a direct comparison:

### Simple Factory (NOT a GoF pattern)

A static or class method that takes a string/type and returns the right object. It's a utility function, not a pattern.

```python
class VehicleFactory:
    @staticmethod
    def create(vehicle_type: str) -> Vehicle:
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "truck":
            return Truck()
        raise ValueError(f"Unknown type: {vehicle_type}")
```

**Problem:** Adding a new vehicle type requires modifying `VehicleFactory`. Violates Open/Closed Principle. The factory itself knows about all concrete types.

### Factory Method (GoF Pattern)

An abstract method in a creator class. Subclasses override it to create specific products. The creator's *business logic* (the template method) is reused; only creation changes.

```python
class Creator:
    def factory_method(self) -> Product:       # abstract
        raise NotImplementedError

    def do_business(self) -> str:               # uses factory method
        product = self.factory_method()
        return product.operation()

class ConcreteCreatorA(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductA()

class ConcreteCreatorB(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductB()
```

**Key insight:** Adding a new product type means adding a new subclass of `Creator`, not modifying existing classes. Follows Open/Closed Principle.

### Abstract Factory (GoF Pattern)

Creates **families** of related objects. If Factory Method is "how do I make one type of thing," Abstract Factory is "how do I make a whole set of related things."

```python
class UIFactory(ABC):
    def create_button(self) -> Button: ...
    def create_checkbox(self) -> Checkbox: ...
    def create_textfield(self) -> TextField: ...
```

See `abstract_factory/theory.md` for details.

### When to Use Which?

| Question | Use |
|----------|-----|
| "I need to create one type of object, and the type varies by subclass" | Factory Method |
| "I need a quick function to create objects from a string/type" | Simple Factory |
| "I need to create entire families of related objects" | Abstract Factory |
| "I need to decouple creation logic from business logic" | Any factory pattern |

---

## 4. Use Cases

### When You Don't Know the Object Type Until Runtime

The type is determined by user input, config, or external data:

```python
class NotificationService:
    def create_notification(self, channel: str) -> Notification:
        raise NotImplementedError

class EmailService(NotificationService):
    def create_notification(self, channel: str) -> Notification:
        return EmailNotification()

class SMSService(NotificationService):
    def create_notification(self, channel: str) -> Notification:
        return SMSNotification()
```

### Framework Extension Points

Frameworks use Factory Method to let users plug in their own implementations. Django's `ModelAdmin.get_form()` returns the form class — you override it to return your custom form.

### Testing with Mock Objects

```python
class DataProcessor:
    def create_reader(self) -> DataReader:  # factory method
        return CSVReader()                   # production

class TestDataProcessor(DataProcessor):
    def create_reader(self) -> DataReader:  # override in tests
        return MockReader()                  # test version
```

### Plugin Systems

Each plugin registers a creator class. The framework calls the factory method without knowing what type of plugin it's working with.

---

## 5. Python-Specific Approaches

### `@classmethod` as Factory

Python `@classmethod` is commonly used as a named constructor — an alternative constructor that creates the object in a specific way.

```python
class Connection:
    def __init__(self, host: str, port: int, ssl: bool) -> None:
        self.host = host
        self.port = port
        self.ssl = ssl

    @classmethod
    def from_url(cls, url: str) -> "Connection":
        parsed = urlparse(url)
        return cls(parsed.hostname, parsed.port, parsed.scheme == "https")

    @classmethod
    def from_env(cls) -> "Connection":
        return cls(
            os.getenv("DB_HOST", "localhost"),
            int(os.getenv("DB_PORT", "5432")),
            os.getenv("DB_SSL", "false") == "true",
        )
```

This is technically a Simple Factory, not GoF Factory Method, but it's the most common Python pattern for "create this object in different ways."

### Registry-Based Factory

Instead of if-elif chains, use a dict as a registry. This makes adding new types trivial and doesn't require modifying the factory:

```python
class VehicleFactory:
    _registry: dict[str, type] = {}

    @classmethod
    def register(cls, name: str, vehicle_class: type) -> None:
        cls._registry[name] = vehicle_class

    @classmethod
    def create(cls, name: str) -> Vehicle:
        if name not in cls._registry:
            raise ValueError(f"Unknown vehicle: {name}")
        return cls._registry[name]()

# Register types — can happen in separate modules
VehicleFactory.register("car", Car)
VehicleFactory.register("truck", Truck)

# Adding a new type: no modification to VehicleFactory needed
VehicleFactory.register("motorcycle", Motorcycle)
```

---

## 6. Quick Example

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str: ...

class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Email: {message}"

class SMSNotification(Notification):
    def send(self, message: str) -> str:
        return f"SMS: {message}"

class PushNotification(Notification):
    def send(self, message: str) -> str:
        return f"Push: {message}"

# Simple Factory (not GoF, but practical):
class NotificationFactory:
    _creators = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        if channel not in cls._creators:
            raise ValueError(f"Unsupported channel: {channel}")
        return cls._creators[channel]()

# Client code
notif = NotificationFactory.create("email")
print(notif.send("Hello!"))  # Email: Hello!
```

---

## 7. Common Mistakes

### Mistake 1: Factory for Every Class

Not every object needs a factory. If you're creating a simple `Point(x, y)` or a `Color(r, g, b)`, just use the constructor directly. Factories are for when the *type* of object varies based on context.

### Mistake 2: Putting Business Logic in the Factory

The factory's job is *creation*. Logic like "if the user is premium, create a PremiumSubscription" belongs in the business layer, not the factory. The factory just creates; the caller decides what type to create.

### Mistake 3: Using if-elif When You Should Use a Registry

This is a code smell:
```python
def create(type_str: str):
    if type_str == "a":
        return TypeA()
    elif type_str == "b":
        return TypeB()
    elif type_str == "c":
        return TypeC()
    # You'll keep adding elifs forever
```

Use a registry dict instead. It's O(1) lookup, extensible without modification, and declarative.

### Mistake 4: Over-Engineering

The GoF Factory Method pattern (with creator classes and subclasses) is heavy. For simple cases where you just need to create different objects based on a string, a Simple Factory (registry-based dict) is perfectly fine. Don't create inheritance hierarchies to solve a problem that a dict can solve.

---

## Summary

| Aspect | Detail |
|--------|--------|
| Intent | Decouple object creation from the creator's business logic |
| Core mechanism | Abstract factory method overridden by subclasses |
| Python idiom | `@classmethod` constructors, registry dict |
| Follows | Open/Closed Principle, Dependency Inversion Principle |
| Watch out | Over-engineering, factory for every class, logic in factory |
| Simpler alternative | Simple Factory (registry-based) for most use cases |
