# Dependency Inversion Principle (DIP)

## What Is It?
1. **High-level modules should not depend on low-level modules.** Both should depend on abstractions.
2. **Abstractions should not depend on details.** Details should depend on abstractions.

In practice: **inject dependencies — don't create them inside classes.**

High-level = business logic (what you do). Low-level = implementation details (how you do it, e.g., which database, which email provider).

---

## Real-World Analogy

Your laptop plugs into **any** power socket via a standard plug (abstraction). It's not hardwired to a specific power plant. You can plug it into a UK, US, or EU socket (different implementations) without changing the laptop.

The laptop is the high-level module. The power socket standard is the abstraction. The specific socket (UK/US/EU) is the low-level module. All depend on the standard — neither the laptop nor the socket depends on each other directly.

---

## Why It Matters

**Without DIP:**
```
OrderService  ──depends on──>  MySQLDatabase
OrderService  ──depends on──>  GmailSender
OrderService  ──depends on──>  FileLogger
```

Problems:
- **Untestable**: `OrderService` requires real MySQL, real Gmail, real filesystem
- **Brittle**: changing MySQL to PostgreSQL means editing `OrderService`
- **Inflexible**: each new environment (prod/staging/test) needs different wiring

**With DIP:**
```
OrderService  ──depends on──>  DatabaseInterface  <──implements──  MySQLDatabase
OrderService  ──depends on──>  EmailSenderInterface  <──implements──  GmailSender
```

`OrderService` only knows abstractions. Concrete implementations are injected externally.

---

## The Violation

```python
class UserService:
    def __init__(self):
        self.db = PostgreSQLDatabase()  # 🚩 hardcoded concrete class
        self.email = GmailSender()      # 🚩 hardcoded
        self.logger = FileLogger()      # 🚩 hardcoded

    def create_user(self, name: str, email: str) -> None:
        self.logger.log(f"Creating user {name}")
        self.db.insert("users", {"name": name, "email": email})
        self.email.send(email, "Welcome!", "Your account is ready.")
```

You **cannot** test `create_user` without:
- A running PostgreSQL server
- Valid Gmail credentials
- A writable filesystem

This violates DIP: `UserService` (high-level) depends on `PostgreSQLDatabase` (low-level).

---

## The Fix: Inject Abstractions

```python
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def insert(self, table: str, record: dict) -> None: ...

class EmailSenderInterface(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None: ...

class LoggerInterface(ABC):
    @abstractmethod
    def log(self, message: str) -> None: ...


class UserService:
    def __init__(
        self,
        db: DatabaseInterface,
        email: EmailSenderInterface,
        logger: LoggerInterface,
    ) -> None:
        self._db = db
        self._email = email
        self._logger = logger

    def create_user(self, name: str, email: str) -> None:
        self._logger.log(f"Creating user {name}")
        self._db.insert("users", {"name": name, "email": email})
        self._email.send(email, "Welcome!", "Your account is ready.")
```

Now:
- **Testable**: inject `MockDatabase()`, `MockEmailSender()`, `NullLogger()`
- **Swappable**: change from Gmail to SendGrid by injecting a different implementation
- **Decoupled**: `UserService` has zero knowledge of PostgreSQL, Gmail, or files

---

## Python-Specific Notes

### No DI Container Needed

Unlike Java Spring or C# .NET, Python almost never needs a DI container framework. Constructor injection (passing dependencies in `__init__`) is usually sufficient:

```python
# Production wiring
service = UserService(
    db=PostgreSQLDatabase(url=DB_URL),
    email=GmailSender(api_key=GMAIL_KEY),
    logger=ConsoleLogger(),
)

# Test wiring — no real services needed
service = UserService(
    db=MockDatabase(),
    email=MockEmailSender(),
    logger=NullLogger(),
)
```

### Three Forms of Dependency Injection

**1. Constructor injection** (most common, best for required dependencies):
```python
class OrderProcessor:
    def __init__(self, payment: PaymentGateway) -> None:
        self._payment = payment  # required — can't work without it
```

**2. Method injection** (for optional, one-time dependencies):
```python
class ReportGenerator:
    def generate(self, data: list, formatter: Formatter) -> str:
        return formatter.format(data)  # injected per-call
```

**3. Property injection** (for optional, reconfigurable dependencies):
```python
class DataPipeline:
    def __init__(self) -> None:
        self.logger: Logger = NullLogger()  # default; can be replaced

pipeline = DataPipeline()
pipeline.logger = VerboseLogger()  # replace when needed
```

### Factory Functions as Lightweight DI

```python
def create_order_service(env: str = "prod") -> OrderService:
    if env == "test":
        return OrderService(
            db=InMemoryDatabase(),
            notifier=MockNotifier(),
        )
    return OrderService(
        db=PostgreSQLDatabase(url=os.getenv("DATABASE_URL")),
        notifier=EmailNotifier(api_key=os.getenv("EMAIL_KEY")),
    )
```

This is essentially a manual DI container — simple and explicit.

### ABCs vs. typing.Protocol for Abstractions

**ABC** (explicit inheritance required):
```python
class DatabaseInterface(ABC):
    @abstractmethod
    def query(self, sql: str) -> list[dict]: ...

class PostgreSQLDatabase(DatabaseInterface):  # must declare it
    def query(self, sql: str) -> list[dict]: ...
```

**Protocol** (structural — no inheritance needed):
```python
from typing import Protocol

class DatabaseInterface(Protocol):
    def query(self, sql: str) -> list[dict]: ...

class PostgreSQLDatabase:   # no inheritance — just has query()
    def query(self, sql: str) -> list[dict]: ...
```

`Protocol` is more flexible (existing third-party classes can satisfy it), but ABC makes the relationship explicit and enforces method presence at class-definition time.

---

## DIP vs. IoC vs. DI — Demystified

| Term | Type | Meaning |
|------|------|---------|
| **DIP** | Design principle | Don't depend on concrete implementations |
| **IoC** (Inversion of Control) | Design pattern | Caller controls which implementation is used |
| **DI** (Dependency Injection) | Implementation technique | Pass dependencies from outside |

DIP is the **why** (principle). IoC is the **what** (pattern). DI is the **how** (technique).

You apply DIP by using IoC, typically implemented via DI.

---

## Signs of DIP Violation

| Red Flag | Reason |
|----------|--------|
| `self.x = SomeConcreteClass()` inside `__init__` | High-level creates low-level directly |
| `from concrete_module import ConcreteClass` at top of high-level module | Import coupling |
| Can't run tests without real database/email/file system | Dependencies are hardcoded |
| Changing a low-level module breaks high-level tests | High-level knows too much about low-level |
| Mocking requires monkey-patching | Dependencies not injected — they're internal |

---

## Testing Benefits

DIP's most immediate practical benefit is testability:

```python
class MockDatabase(DatabaseInterface):
    def __init__(self):
        self.inserted_records: list[dict] = []

    def insert(self, table: str, record: dict) -> None:
        self.inserted_records.append({"table": table, **record})

def test_create_user_inserts_record():
    mock_db = MockDatabase()
    mock_email = MockEmailSender()
    mock_logger = NullLogger()

    service = UserService(mock_db, mock_email, mock_logger)
    service.create_user("Alice", "alice@example.com")

    assert len(mock_db.inserted_records) == 1
    assert mock_db.inserted_records[0]["name"] == "Alice"
```

No database. No network. Instant test execution.

---

## Quick Example — Complete DIP-Compliant System

```python
from abc import ABC, abstractmethod
from typing import List

class NotificationSender(ABC):
    """Abstraction — what high-level code depends on."""
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool: ...

# Low-level implementations
class EmailSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Email → {recipient}: {message}")
        return True

class SMSSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        print(f"SMS → {recipient}: {message}")
        return True

# High-level business logic
class AlertSystem:
    """High-level module — depends only on NotificationSender (abstraction)."""

    def __init__(self, sender: NotificationSender) -> None:
        self._sender = sender

    def send_alert(self, recipients: List[str], message: str) -> None:
        for r in recipients:
            success = self._sender.send(r, message)
            if not success:
                print(f"Failed to notify {r}")

# Wiring (done at the top level, not inside business logic)
alert_system = AlertSystem(sender=EmailSender())   # swap to SMSSender with no code change
alert_system.send_alert(["alice@co.com"], "Server down!")
```

---

## When Not to Apply DIP

DIP adds a layer of abstraction. Not all code needs it:

- **Single, stable implementation**: if a dependency never changes and never needs mocking, the abstraction is overhead
- **Framework glue code**: Django views, Flask routes — these are already managed by the framework
- **Simple scripts**: a one-off script doesn't need DI
- **Value objects and pure functions**: no side effects, nothing to inject

Apply DIP where you need: testability, replaceability, or multiple environments.

---

## Common Mistakes

- **DI containers (overkill in Python)**: most Python projects don't need frameworks like `injector` or `dependency-injector`. Plain constructor injection is enough.
- **Abstracting things that only ever have one implementation**: don't create `DatabaseInterface` if you'll never have more than one database. YAGNI.
- **Injecting too many dependencies**: if your `__init__` takes 8 dependencies, it's a sign that the class violates SRP.
- **Forgetting to inject in tests**: using the real implementation in unit tests defeats the point — always inject test doubles.
- **Property injection for required dependencies**: if the object can't function without a dependency, inject it via the constructor, not a settable property.

---

## See Also

- **Abstraction** (Module 01, Topic 05) — ABCs are how you create the abstractions DIP depends on
- **Single Responsibility** (Module 02, SRP) — each dependency should have a focused purpose
- **Strategy Pattern** (Module 03) — concrete example of DIP in action (injectable algorithm)
- **Observer Pattern** (Module 03) — loose coupling via abstracted notification
