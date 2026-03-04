# Dependency Inversion Principle (DIP)

## What Is It?
1. **High-level modules should not depend on low-level modules.** Both should depend on abstractions.
2. **Abstractions should not depend on details.** Details should depend on abstractions.

In practice: inject dependencies — don't create them inside classes.

## Real-World Analogy
Your laptop plugs into **any** power socket via a standard plug (abstraction). It's not hardwired to the power plant. You can plug it into UK, US, or EU sockets (different implementations). The laptop doesn't change — only the adapter.

## The Violation

```python
class UserService:
    def __init__(self):
        self.db = PostgreSQLDatabase()  # hardcoded low-level module!
        self.email = GmailSender()      # hardcoded!
        self.logger = FileLogger()      # hardcoded!
```

Problems:
- **Can't test**: `PostgreSQLDatabase()` requires a real database
- **Can't swap**: changing to MySQL means editing `UserService`
- **Tight coupling**: `UserService` knows about PostgreSQL internals

## The Fix: Inject Abstractions

```python
class UserService:
    def __init__(
        self,
        db: DatabaseInterface,
        email: EmailSenderInterface,
        logger: LoggerInterface,
    ) -> None:
        self.db = db
        self.email = email
        self.logger = logger
```

Now:
- **Testable**: inject `MockDatabase()` — no real database needed
- **Swappable**: change from Gmail to SendGrid by injecting a different implementation
- **Decoupled**: `UserService` knows only the abstraction, not the implementation

## Python-Specific Notes

Python has no DI containers needed (unlike Java Spring). Constructor injection is usually enough:

```python
# Production
service = UserService(
    db=PostgreSQLDatabase(url=DB_URL),
    email=GmailSender(api_key=KEY),
    logger=ConsoleLogger(),
)

# Testing
service = UserService(
    db=MockDatabase(),
    email=MockEmailSender(),
    logger=NullLogger(),
)
```

## DIP vs IoC vs DI
- **DIP**: the design principle (don't depend on concretions)
- **IoC**: the technique (inversion of control — let caller control dependencies)
- **DI**: the implementation (dependency injection — passing dependencies in)

DIP → IoC → DI. DIP is the "why", DI is the "how".

## Signs of Violation
- `self.x = SomeConcreteClass()` inside `__init__`
- `import` of low-level modules at top of high-level module
- Can't test a class without its real dependencies running

## Common Mistakes
- DI containers (overkill in most Python projects)
- Abstracting things that only ever have one implementation
- Injecting too many dependencies (SRP might be violated)

## Links
- [Example 1: Tight coupling →](examples/example1_tight_coupling.py)
- [Example 2: With DI →](examples/example2_with_di.py)
- [Exercise →](exercises/problem.md)
