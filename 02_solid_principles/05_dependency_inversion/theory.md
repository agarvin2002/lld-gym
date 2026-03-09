# Dependency Inversion Principle

## What is it?

High-level classes should not depend on low-level classes. Both should depend on abstractions (interfaces). High-level means: business logic, orchestration. Low-level means: databases, email senders, loggers. The abstraction sits between them so either side can change without affecting the other.

## Analogy

A laptop charger uses a universal adapter. The laptop doesn't care whether power comes from a UK socket, a US socket, or a power bank. It depends on the standard connector (abstraction), not on the specific socket (concrete implementation). Swapping sockets requires no change to the laptop.

## Minimal code

```python
# Violation — UserService creates its own dependencies
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()   # hardcoded — can't test, can't swap
        self.email = GmailSender()  # hardcoded

# Fix — inject dependencies through the constructor
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def query(self, sql: str) -> list: ...

class EmailSenderInterface(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None: ...

class UserService:
    def __init__(self, db: DatabaseInterface, email: EmailSenderInterface):
        self.db = db        # injected — can swap MySQL for Postgres or Mock
        self.email = email  # injected — can swap Gmail for SendGrid or Mock
```

## Real-world uses

- **Notification services**: `NotificationService` accepts a `NotificationSenderInterface`. Swap `SMSSender` for `EmailSender` or `SlackSender` without changing the service.
- **Payment gateways** (Razorpay, Paytm, UPI): a `PaymentGatewayInterface` is injected into the checkout service. Switching providers requires no change to checkout logic.
- **Database layers**: tests inject a `MockDatabase` instead of a real PostgreSQL connection — no infrastructure needed.

## One mistake

Writing `self.db = MySQLDatabase()` inside `__init__`. Now UserService is impossible to unit test without a real database. To test it, you must run infrastructure. To swap the database, you must edit UserService source code. Both are avoidable by accepting the dependency as a constructor parameter.

## When not to apply

DIP is valuable when a dependency has multiple implementations (production + test, or multiple providers). If a class has only one concrete dependency that will never change — like a `UUIDGenerator` or a value object — adding an interface layer creates complexity without benefit. Apply DIP where swappability or testability is a real need.

## What to do next

- See `examples/example1_tight_coupling.py` for `UserService` that hardcodes its dependencies.
- See `examples/example2_with_di.py` for the same service using constructor injection.
- Open `exercises/starter.py` and implement a notification service that accepts any `NotificationSenderInterface`.
