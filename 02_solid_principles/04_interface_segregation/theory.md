# Interface Segregation Principle (ISP)

## What Is It?
**Clients should not be forced to depend on interfaces they don't use.**

A "fat" interface with many methods forces every implementation to provide ALL methods, even irrelevant ones. The fix: split large interfaces into small, focused, role-specific ones.

The key word is **client** — design interfaces from the perspective of what the caller needs, not what the implementer can do.

---

## Real-World Analogy

A Swiss Army knife has 15 tools. If you just need to cut bread, you're still carrying the magnifying glass, the toothpick, and the tiny scissors. You don't use them — but you're forced to drag them around.

Contrast with a chef's knife: one purpose, used exactly when needed. No unused luggage.

ISP asks: **don't give clients methods they don't need.** Give them exactly the tool they use.

---

## Why It Matters

Fat interfaces create **false dependencies**:
- A class that only reads data shouldn't depend on write methods
- A class that only prints documents shouldn't have to implement scanning
- A class that processes payments shouldn't implement refunds if it never does them

**Real cost of fat interfaces:**
1. Implementers write dummy stubs (`raise NotImplementedError`) for methods they can't support
2. Callers see a massive interface and don't know which methods are actually safe to call
3. Adding a method to a fat interface forces recompilation/changes in ALL implementations
4. Tests become heavier — mocks must implement all methods even for narrow testing

---

## The Classic Violation

```python
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...       # robots don't eat!
    @abstractmethod
    def sleep(self): ...     # robots don't sleep!

class Robot(Worker):
    def work(self): print("Working...")
    def eat(self): raise NotImplementedError  # forced! 🚩
    def sleep(self): raise NotImplementedError  # forced! 🚩
```

`Robot` is forced to "implement" methods that make no sense. This is ISP violation.
Any code that calls `worker.eat()` on a `Robot` will crash unexpectedly.

---

## The Fix: Small, Focused Role Interfaces

```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self) -> None: ...

class Eatable(ABC):
    @abstractmethod
    def eat(self) -> None: ...

class Sleepable(ABC):
    @abstractmethod
    def sleep(self) -> None: ...

class HumanWorker(Workable, Eatable, Sleepable):
    def work(self) -> None: print("Working...")
    def eat(self) -> None: print("Eating...")
    def sleep(self) -> None: print("Sleeping...")

class Robot(Workable):                   # only the interface it supports ✅
    def work(self) -> None: print("Beep boop, working...")
```

Callers that need a `Workable` accept both humans and robots. Callers that need an `Eatable` only deal with humans. No surprises.

---

## Python-Specific Notes

### Duck Typing Reduces — But Doesn't Eliminate — ISP Concerns

In Python, you're never **syntactically** forced to implement all methods of a class you inherit from (unless you use ABCs). But:

```python
def process_worker(worker):   # no type hint — duck typing
    worker.work()             # only uses work()
    worker.eat()              # if Robot is passed, crashes at runtime!
```

Type hints + ABCs make ISP important again:
```python
def schedule_work(worker: Workable) -> None:  # contract is clear
    worker.work()
```

The type hint tells both callers and implementers: "only `work()` is required."

### typing.Protocol — Structural Subtyping (Implicit Interfaces)

`Protocol` lets you define an interface without requiring explicit inheritance:

```python
from typing import Protocol

class Printable(Protocol):
    def print_doc(self) -> str: ...

class Scannable(Protocol):
    def scan_doc(self) -> bytes: ...

class BasicPrinter:          # doesn't inherit anything — just has print_doc
    def print_doc(self) -> str:
        return "printed document"

def do_print(device: Printable) -> None:  # only requires print_doc
    print(device.print_doc())

do_print(BasicPrinter())   # ✅ satisfies Printable structurally
```

This is powerful: `BasicPrinter` satisfies `Printable` without declaring it. The interface is purely defined by what the caller needs.

### Mixins as Narrow Role Implementations

Python mixins work well with ISP — each mixin provides a narrow capability:

```python
class JSONSerializableMixin:
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

class TimestampedMixin:
    def get_created_at(self) -> str:
        return self._created_at.isoformat()

class Order(JSONSerializableMixin):   # only serialization mixin needed
    def __init__(self, ...): ...
```

Each mixin is a focused interface — take only what you need.

---

## ISP in Practice: A Multi-Function Device

### Violation:

```python
class MultiFunctionDevice(ABC):
    @abstractmethod
    def print_doc(self, doc: str) -> None: ...
    @abstractmethod
    def scan_doc(self) -> str: ...
    @abstractmethod
    def fax_doc(self, doc: str, number: str) -> None: ...
    @abstractmethod
    def copy_doc(self, doc: str) -> str: ...

class OldPrinter(MultiFunctionDevice):
    def print_doc(self, doc: str) -> None: print(doc)
    def scan_doc(self) -> str: raise NotImplementedError("Can't scan")
    def fax_doc(self, doc: str, number: str) -> None: raise NotImplementedError
    def copy_doc(self, doc: str) -> str: raise NotImplementedError
```

### Fixed — Segregated Interfaces:

```python
class Printer(ABC):
    @abstractmethod
    def print_doc(self, doc: str) -> None: ...

class Scanner(ABC):
    @abstractmethod
    def scan_doc(self) -> str: ...

class FaxMachine(ABC):
    @abstractmethod
    def fax_doc(self, doc: str, number: str) -> None: ...

class OldPrinter(Printer):              # only what it supports ✅
    def print_doc(self, doc: str) -> None:
        print(f"Printing: {doc}")

class ModernAllInOne(Printer, Scanner, FaxMachine):  # supports all ✅
    def print_doc(self, doc: str) -> None: ...
    def scan_doc(self) -> str: ...
    def fax_doc(self, doc: str, number: str) -> None: ...

# Caller only depends on what it needs:
def print_report(printer: Printer, report: str) -> None:
    printer.print_doc(report)   # works for OldPrinter and ModernAllInOne
```

---

## Signs of ISP Violation

| Red Flag | Description |
|----------|-------------|
| `raise NotImplementedError` in an inherited method | Can't implement it — interface too fat |
| `pass` stub in an inherited method | Same — doing nothing for a required method |
| `hasattr(obj, 'method')` guards in caller code | Caller isn't sure if the method exists — interface unclear |
| "not applicable" comments in implementations | Method shouldn't be there |
| Implementing a large ABC just to use one method | One-method callers shouldn't pay for the rest |

---

## When to Split an Interface

Split when:
- Two different client types use two different subsets of methods
- Adding a method to the interface would affect implementers that don't need it
- You're writing `raise NotImplementedError` more than once in an implementation

**Don't** split when:
- Methods are genuinely cohesive and always used together
- Only one implementation exists and you're not sure of future clients
- Splitting would make the API confusing and hard to discover

---

## ISP vs. SRP — Key Distinction

| Principle | Applies To | Question |
|-----------|-----------|----------|
| SRP | Classes | Does this class have one reason to change? |
| ISP | Interfaces/ABCs | Does this interface force clients to depend on methods they don't use? |

SRP is about the class's responsibilities. ISP is about the interface's width from the caller's perspective.

---

## Quick Example — typing.Protocol for ISP

```python
from typing import Protocol

class Readable(Protocol):
    def read(self, n: int) -> bytes: ...

class Writable(Protocol):
    def write(self, data: bytes) -> int: ...

class Seekable(Protocol):
    def seek(self, pos: int) -> int: ...
    def tell(self) -> int: ...

# Callers depend only on what they use:
def read_header(stream: Readable) -> bytes:
    return stream.read(4)

def write_footer(stream: Writable, footer: bytes) -> None:
    stream.write(footer)

def reset_stream(stream: Seekable) -> None:
    stream.seek(0)
```

A `BytesIO` object satisfies all three. A network socket satisfies `Readable` and `Writable` but not `Seekable`. Each caller gets exactly the interface it needs.

---

## Common Mistakes

- **Splitting too fine-grained** — one method per interface for everything creates an explosion of tiny interfaces. Find the natural cohesion point.
- **Applying ISP preemptively** — split when you have concrete client evidence, not speculatively.
- **Confusing ISP with SRP** — ISP is about the caller's view of the interface, SRP is about the implementer's responsibilities.
- **Ignoring ISP in Python** — "duck typing handles it" only works until you add type hints, ABCs, or need to document the contract clearly.
- **Not using Protocol** — `typing.Protocol` is Python's most ISP-native tool; use it when you want structural typing without inheritance.

---

## See Also

- **Liskov Substitution** (LSP) — ISP prevents fat interfaces that force LSP violations
- **Abstraction** (Module 01, Topic 05) — ABCs are how interfaces are enforced in Python
- **Adapter Pattern** (Module 03) — adapts existing classes to satisfy narrow interfaces
