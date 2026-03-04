# Interface Segregation Principle (ISP)

## What Is It?
**Clients should not be forced to depend on interfaces they don't use.**

A "fat" interface with many methods forces every implementation to provide ALL methods, even irrelevant ones. Split big interfaces into small, focused ones.

## Real-World Analogy
A restaurant menu has hundreds of items. But you only order what you want — you're not forced to prepare all dishes just because you're a customer. If the contract said "every customer must be able to cook all menu items", that's ISP violation.

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
    def work(self): ...
    def eat(self): raise NotImplementedError  # forced!
    def sleep(self): raise NotImplementedError  # forced!
```

`Robot` is forced to "implement" methods that make no sense for it. This is ISP violation.

## The Fix: Small, Focused Interfaces

```python
class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Sleepable(ABC):
    @abstractmethod
    def sleep(self): ...

class Human(Workable, Eatable, Sleepable): ...  # implements all
class Robot(Workable): ...                       # only implements what it does
```

## Python-Specific Notes

Python's duck typing naturally reduces ISP violations — you're never technically forced to implement all methods. But ABCs and type hints make ISP important again:
- ABCs enforce method presence at instantiation time
- Type hints communicate what interface you expect
- `typing.Protocol` offers structural subtyping — an implicit interface

## Signs of Violation
- Implementing a method with `pass` or `raise NotImplementedError`
- "Does not apply" comments next to method implementations
- Client code checking `hasattr()` to see if a method exists

## Quick Example
```python
from typing import Protocol

class Printable(Protocol):
    def print_doc(self) -> str: ...

class Scannable(Protocol):
    def scan_doc(self) -> bytes: ...

class BasicPrinter:          # only needs Printable — clean!
    def print_doc(self) -> str: return "printed"

def do_print(p: Printable) -> None:  # only requires what it uses
    print(p.print_doc())
```

## Common Mistakes
- Splitting too fine-grained (one method per interface for everything)
- Applying ISP preemptively before knowing who the clients are
- Confusing ISP with SRP (ISP is for interfaces/ABCs, SRP is for classes)

## Links
- [Example 1: Fat interface violation →](examples/example1_fat_interface.py)
- [Example 2: Segregated →](examples/example2_segregated.py)
- [Exercise →](exercises/problem.md)
