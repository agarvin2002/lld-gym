# Topic 05: Abstraction

## 1. What Is Abstraction?

Abstraction means: **hide implementation details, expose only the essential interface**.

You define *what* an object can do (the interface), not *how* it does it (the implementation). The caller knows what to call — it does not need to know what happens inside.

```python
# The caller sees this:
result = database.save(user)

# The caller does NOT see:
# - The SQL query being constructed
# - The connection pool being accessed
# - The retry logic on failure
# - The serialization format
```

This separation is the foundation of software design. Without it, every change
to how something is implemented requires changing every caller.

---

## 2. Analogy: The ATM Machine

An ATM is a perfect abstraction:

**Interface (what you see):**
- Insert card
- Enter PIN
- Press "Withdraw $200"
- Take your cash

**Implementation (what you don't see):**
- Authentication service calls
- Ledger database queries
- Bank network protocols
- Fraud detection algorithms
- Physical cash dispensing mechanism

You can use an ATM from any bank in any country without understanding any of
those details. If the bank replaces their entire backend, the ATM interface
stays the same — and you never notice.

That is exactly what abstraction does in software.

---

## 3. Why It Matters

### Loose Coupling
Code that depends on an abstraction (interface) is not tied to a specific
implementation. You can swap implementations without changing the caller.

```python
# Coupled to implementation:
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()  # hardcoded — changing DB requires editing this

# Depends on abstraction:
class OrderService:
    def __init__(self, storage: DataStore):  # any DataStore works
        self.storage = storage
```

### Testability
Abstractions make code testable by allowing fake/mock implementations:

```python
class InMemoryDataStore(DataStore):
    """Fast, no disk I/O — perfect for tests."""
    ...

service = OrderService(storage=InMemoryDataStore())  # fast test
service = OrderService(storage=PostgresDataStore())  # real production
```

### Replaceability
When requirements change (new database, new payment provider, new message bus),
you write a new implementation of the existing interface — you do not rewrite
all the business logic.

---

## 4. Python-Specific Mechanics

### 4.1 `abc.ABC` and `@abstractmethod`

Python's `abc` (Abstract Base Classes) module provides the tools to define
enforced interfaces:

```python
from abc import ABC, abstractmethod

class DataStore(ABC):
    @abstractmethod
    def save(self, key: str, data: dict) -> None: ...

    @abstractmethod
    def load(self, key: str) -> dict: ...
```

Rules enforced by `abc.ABC`:
- You **cannot** instantiate `DataStore` directly — `TypeError` is raised.
- Any subclass that does not implement **all** abstract methods also cannot
  be instantiated — another `TypeError`.
- This is Python's way of saying: "this is a contract, not an implementation."

```python
class InMemoryStore(DataStore):
    def save(self, key: str, data: dict) -> None:
        self._store[key] = data

    def load(self, key: str) -> dict:
        return self._store[key]

# Works:
store = InMemoryStore()

# Fails with TypeError:
store = DataStore()
```

### 4.2 Abstract Properties

Use `@property` combined with `@abstractmethod` to require subclasses to
define properties:

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @property
    @abstractmethod
    def currency_code(self) -> str:
        """Subclasses must provide their supported currency code."""
        ...

class StripeGateway(PaymentGateway):
    @property
    def currency_code(self) -> str:
        return "USD"
```

Note: `abc.abstractproperty` is **deprecated** since Python 3.3. Always use
`@property` + `@abstractmethod` together instead.

### 4.3 `typing.Protocol` for Structural Abstraction

`typing.Protocol` (Python 3.8+) provides **structural subtyping**: a class
satisfies a Protocol if it has the right methods — without inheriting from it.

```python
from typing import Protocol

class DataStore(Protocol):
    def save(self, key: str, data: dict) -> None: ...
    def load(self, key: str) -> dict: ...
```

Any class with `save()` and `load()` satisfies `DataStore` — regardless of
its class hierarchy. This is useful for third-party classes and for keeping
code loosely coupled.

### 4.4 Abstract vs Interface: Python Has No `interface` Keyword

In Java and C#, `interface` is a language keyword. In Python:

| Java/C# concept | Python equivalent |
|---|---|
| `interface` | `abc.ABC` with all `@abstractmethod` methods |
| `abstract class` | `abc.ABC` with some concrete + some abstract methods |
| Structural interface | `typing.Protocol` |

Python ABCs can have:
- Abstract methods (must be overridden)
- Concrete methods (inherited as-is, can be overridden)
- Abstract properties
- Class methods and static methods marked `@abstractmethod`

This makes Python ABCs more flexible than Java interfaces — they are closer
to Java abstract classes.

---

## 5. When to Use Abstraction

**Use abstraction when:**
- You have (or anticipate) multiple implementations of the same concept
- You want to test components in isolation
- You want to defer the implementation decision (program to interfaces first)
- The implementation is likely to change over time

**Do NOT abstract when:**
- There is only one implementation and no plans for more
- The abstraction adds complexity without benefit
- You are in early exploration — premature abstraction is as bad as no abstraction

> "Make it work, make it right, make it fast." — Kent Beck
>
> Abstract when "make it right" tells you there are multiple valid implementations.

---

## 6. Quick Example: DataStore

```python
from abc import ABC, abstractmethod

class DataStore(ABC):
    @abstractmethod
    def save(self, key: str, value: str) -> None: ...

    @abstractmethod
    def load(self, key: str) -> str: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

class InMemoryStore(DataStore):
    def __init__(self):
        self._data: dict[str, str] = {}

    def save(self, key: str, value: str) -> None:
        self._data[key] = value

    def load(self, key: str) -> str:
        return self._data[key]

    def delete(self, key: str) -> None:
        del self._data[key]

class SQLiteStore(DataStore):
    def save(self, key: str, value: str) -> None:
        # ... sqlite3 INSERT OR REPLACE ...

    def load(self, key: str) -> str:
        # ... sqlite3 SELECT ...

    def delete(self, key: str) -> None:
        # ... sqlite3 DELETE ...

class RedisStore(DataStore):
    def save(self, key: str, value: str) -> None:
        # ... redis client SET ...

    # etc.


# Business logic depends only on DataStore, never on a specific backend:
class UserRepository:
    def __init__(self, store: DataStore):
        self.store = store

    def create_user(self, user_id: str, name: str) -> None:
        self.store.save(f"user:{user_id}", name)

# Swappable at construction time:
repo = UserRepository(InMemoryStore())     # tests
repo = UserRepository(SQLiteStore())       # local dev
repo = UserRepository(RedisStore())        # production
```

---

## 7. Common Mistakes

### Mistake 1: Abstracting Too Early

```python
# PREMATURE: only one implementation exists, probably ever will
class UserNameFormatterABC(ABC):
    @abstractmethod
    def format(self, first: str, last: str) -> str: ...

class StandardUserNameFormatter(UserNameFormatterABC):
    def format(self, first: str, last: str) -> str:
        return f"{first} {last}"

# Just write a function:
def format_name(first: str, last: str) -> str:
    return f"{first} {last}"
```

### Mistake 2: ABC With Only One Implementation

An ABC with one concrete subclass (in the entire codebase) is usually a sign
that the abstraction was premature. Wait until the second implementation exists
before introducing the abstraction.

### Mistake 3: Leaking Implementation Details Through the Interface

```python
# BAD: interface exposes SQL concepts — tightly couples callers to SQL
class DataStore(ABC):
    @abstractmethod
    def execute_sql(self, query: str) -> list: ...  # SQL leaks out

# GOOD: interface is storage-agnostic
class DataStore(ABC):
    @abstractmethod
    def save(self, key: str, data: dict) -> None: ...
    @abstractmethod
    def load(self, key: str) -> dict: ...
```

### Mistake 4: Concrete Classes Depending on Concrete Classes

```python
# BAD: OrderService is tied to PostgresDB
class OrderService:
    def __init__(self):
        self.db = PostgresDB()  # hardcoded concrete class

# GOOD: inject the abstraction
class OrderService:
    def __init__(self, storage: DataStore):
        self.storage = storage
```

This is called **Dependency Injection** — passing the dependency in rather
than creating it internally.

---

## Summary

| Concept | Key Idea |
|---|---|
| Abstraction | Hide implementation, expose interface |
| `abc.ABC` | Enforced abstract class — subclasses must implement marked methods |
| `@abstractmethod` | Method must be overridden in concrete subclasses |
| `@property` + `@abstractmethod` | Abstract property — subclass must define a property |
| `typing.Protocol` | Structural interface — no inheritance required |
| Dependency injection | Pass the abstraction in; don't create it internally |
| Null Object | Use a no-op implementation instead of `None` checks |
| When to abstract | When multiple implementations exist or are clearly needed |

The core insight: **depend on abstractions, not on concretions**. This is
the Dependency Inversion Principle (the D in SOLID), and abstraction is the
mechanism that makes it possible.
