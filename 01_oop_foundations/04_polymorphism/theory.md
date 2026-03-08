# Polymorphism

## What is it?

**Polymorphism** means: many different things, one common action.

Think of a notification app:
- You call `send()` to send a notification.
- But the app can send via WhatsApp, email, or SMS.
- Each one does `send()` differently. But you just call `send()` — one action.

That is polymorphism. **Same method name, different behaviour for each class.**

---

## See it in code

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass   # each subclass must implement this

class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending EMAIL: {message}")

class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")

# one function works for ALL notification types
def notify_user(notification: Notification, msg: str) -> None:
    notification.send(msg)   # no if/elif needed

notify_user(EmailNotification(), "Your order is placed!")
notify_user(SMSNotification(), "Your order is placed!")
```

**You never use `if type == "email"` or `elif type == "sms"`.**
You just call `.send()` — Python figures out which one to run.

---

## The anti-pattern: don't do this

```python
# BAD — breaks every time you add a new notification type
def notify_user(notification, msg):
    if isinstance(notification, EmailNotification):
        print(f"EMAIL: {msg}")
    elif isinstance(notification, SMSNotification):
        print(f"SMS: {msg}")
    # forgot WhatsApp? Now it silently does nothing.
```

This code breaks every time you add a new type. The polymorphic version above never breaks.

---

## Real-world applications

- This is **the most used pattern in system design.**
- Parking lot: `Vehicle.get_fee()` — Car, Bike, Truck each return different fees.
- Hotel booking: `Room.calculate_price()` — Single, Double, Suite each return different prices.
- Good design means: use method overriding, not `if/elif` chains that break when you add a new type.

---

## The one mistake beginners make

**Using `isinstance()` checks instead of method overriding.**

If you find yourself writing `if isinstance(x, Car)` or `if type(x) == "car"`,
stop and think: can I add a method to the class and call that instead?
Almost always, the answer is yes.

---

## What to do next

1. Open `examples/example1_method_overriding.py` — see the good vs bad approach side by side
2. (Optional, advanced) `examples/example2_duck_typing.py` — polymorphism without inheritance
3. Do `exercises/starter.py` — build a discount system using polymorphism
