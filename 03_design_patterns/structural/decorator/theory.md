# Decorator Pattern

## What is it?
The Decorator pattern adds behaviour to an object by wrapping it in another object that shares the same interface.
The wrapper calls through to the original and adds something before or after — logging, caching, auth, retries.
You can stack multiple wrappers. Each layer is unaware of the others.

## Analogy
Think of a plain filter coffee. Add a shot of vanilla syrup — still a coffee. Add whipped cream on top — still a coffee.
Each addition wraps the previous cup. You can add or remove toppings freely.
The barista (your client code) always handles a "coffee" — they never need to know how many layers are inside.

## Minimal code
```python
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailService(NotificationService):
    def send(self, message: str) -> None:
        print(f"Email: {message}")

class LoggingDecorator(NotificationService):
    def __init__(self, wrapped: NotificationService) -> None:
        self._wrapped = wrapped

    def send(self, message: str) -> None:
        print(f"[LOG] Sending: {message}")
        self._wrapped.send(message)   # delegate — never skip this

class RetryDecorator(NotificationService):
    def __init__(self, wrapped: NotificationService, retries: int = 3) -> None:
        self._wrapped = wrapped
        self._retries = retries

    def send(self, message: str) -> None:
        for _ in range(self._retries):
            try:
                self._wrapped.send(message)
                return
            except Exception:
                pass

# Compose at runtime — client only sees NotificationService
service = RetryDecorator(LoggingDecorator(EmailService()))
service.send("Your Paytm payment of ₹500 is confirmed.")
```

## Real-world uses
- Logging every call to a Razorpay payment service without touching its code
- Adding auth token injection to an HTTP client used by a Swiggy-style delivery service
- Caching repeated database reads in a product catalogue

## One mistake
Forgetting to call `self._wrapped.send(...)` inside the decorator.
If you add behaviour but never delegate to the wrapped object, the original service never runs.
Always delegate — that is the whole point of the pattern.

## What to do next
- Read `examples/example1_logging_decorator.py` to see logging and caching decorators on a data service.
- Read `examples/example2_auth_decorator.py` to see auth and retry decorators on an API client.
- Then open `exercises/starter.py` and build your own text formatter decorators.
