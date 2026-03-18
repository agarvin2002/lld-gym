# Factory Method Pattern

## What is it?

The Factory pattern centralises object creation behind a single interface.
Callers ask for an object by name or type — they never import or instantiate
concrete classes directly. When you need a new type, you add it to the factory
without touching any caller code.

## Analogy

Swiggy's notification system needs to send order updates via Email, SMS, or
push notification. The dispatch code does not import `SMSNotification` — it
calls `NotificationFactory.create("sms")` and gets back an object it can
call `.send()` on. Adding WhatsApp later means registering one new class,
nothing else changes.

## Minimal code

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, msg: str) -> str: ...

class EmailNotification(Notification):
    def send(self, msg: str) -> str:
        return f"Email: {msg}"

class SMSNotification(Notification):
    def send(self, msg: str) -> str:
        return f"SMS: {msg}"

class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms":   SMSNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        if channel not in cls._registry:
            raise ValueError(f"Unknown channel: {channel}")
        return cls._registry[channel]()

# Caller knows nothing about EmailNotification or SMSNotification
n = NotificationFactory.create("email")
print(n.send("Your order is out for delivery"))
```

## Real-world uses

- Payment gateway selection: Razorpay, Paytm, or UPI — one factory, caller picks by string
- Log formatter selection: plain text, JSON, or CSV — swap at runtime without code changes
- Ride type creation in a booking app: Bike, Auto, Cab — factory returns the right pricer

## One mistake

Putting business logic inside the factory. The factory's only job is to
instantiate the right class. Decisions like "premium users get a different
formatter" belong in the caller, not the factory.

## What to do next

- `examples/example1_shapes.py` — Simple Factory function and Factory Method pattern side by side
- `examples/example2_notifications.py` — Registry-based factory with runtime registration
- `exercises/starter.py` — build a log formatter factory yourself
