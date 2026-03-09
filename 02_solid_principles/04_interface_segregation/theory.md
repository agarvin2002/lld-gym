# Interface Segregation Principle

## What is it?

Clients should not be forced to depend on methods they don't use. Instead of one large interface, define several small, focused ones. Each class implements only the interfaces it actually supports.

## Analogy

A chef uses a dedicated knife for bread, not a Swiss Army knife. The Swiss Army knife has a saw, scissors, and a corkscrew — but the chef only needs one blade. Using the wrong tool forces you to carry features you'll never use.

## Minimal code

```python
# Violation — BasicPrinter forced to implement scan, fax, staple
class FatPrinter(ABC):
    @abstractmethod
    def print_doc(self, doc): ...
    @abstractmethod
    def scan_doc(self): ...    # BasicPrinter can't scan
    @abstractmethod
    def fax_doc(self, doc): ... # BasicPrinter can't fax

class BasicPrinter(FatPrinter):
    def print_doc(self, doc): print(doc)
    def scan_doc(self):       raise NotImplementedError  # surprise!
    def fax_doc(self, doc):   raise NotImplementedError  # surprise!

# Fix — split into small interfaces
class Printable(ABC):
    @abstractmethod
    def print_doc(self, doc): ...

class Scannable(ABC):
    @abstractmethod
    def scan_doc(self): ...

class BasicPrinter(Printable):        # only implements what it supports
    def print_doc(self, doc): print(doc)

class MultiFunctionPrinter(Printable, Scannable):  # implements both
    def print_doc(self, doc): print(doc)
    def scan_doc(self): return "scanned content"
```

## Real-world uses

- **Media players**: a `VideoPlayable` and an `AudioPlayable` are separate interfaces. A podcast player implements `AudioPlayable` and `SpeedControllable` but not `VideoPlayable`.
- **Notification senders** (Zomato, Swiggy): `SMSSender` and `EmailSender` implement a narrow `NotificationSender` interface with only `send()`. Neither is forced to implement methods of the other.
- **Cloud storage**: `Readable`, `Writable`, and `Deletable` are separate. A read-only storage class implements only `Readable`.

## One mistake

Defining one large ABC with all operations, then having classes raise `NotImplementedError` for the methods they don't support. This defeats the purpose of an interface — callers cannot trust it.

## What to do next

- See `examples/example1_fat_interface.py` for a `FatPrinter` that forces `BasicPrinter` to stub scan and fax.
- See `examples/example2_segregated.py` for the split interface design.
- Open `exercises/starter.py` and implement four media player classes, each implementing only the interfaces it needs.
