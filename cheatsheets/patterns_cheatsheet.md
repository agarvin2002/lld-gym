# Design Patterns Cheatsheet

## All 13 Patterns at a Glance

| Pattern | Category | Problem It Solves | Key Classes | Appears In |
|---------|----------|-------------------|-------------|-----------|
| **Singleton** | Creational | One instance globally | `__new__`, `Lock` | Config, DB pool, Logger |
| **Factory Method** | Creational | Decouple object creation | Creator, ConcreteCreator | Payment, Transport |
| **Abstract Factory** | Creational | Create families of objects | AbstractFactory, Families | UI themes, DB drivers |
| **Builder** | Creational | Complex multi-step construction | Builder, Director, Product | QueryBuilder, Pizza |
| **Adapter** | Structural | Incompatible interfaces | Adapter, Adaptee, Target | Legacy integration |
| **Decorator** | Structural | Add behavior dynamically | Component, Decorator | Logging, Caching, Auth |
| **Composite** | Structural | Tree structures, uniform treatment | Component, Leaf, Composite | File system, Org chart |
| **Facade** | Structural | Simplify complex subsystem | Facade, Subsystems | Hotel booking, Home theater |
| **Observer** | Behavioral | One-to-many notification | Subject, Observer | Events, Pub/sub, MVC |
| **Strategy** | Behavioral | Interchangeable algorithms | Context, Strategy | Payment, Sorting, Export |
| **Command** | Behavioral | Encapsulate requests, support undo | Command, Invoker, Receiver | Editor undo, Task queue |
| **State** | Behavioral | Behavior changes with state | Context, State | ATM, Vending machine |
| **Iterator** | Behavioral | Sequential access, hide structure | Iterator, Iterable | Collections, Streams |

---

## Quick Python Snippets

### Singleton
```python
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Factory Method
```python
class Creator(ABC):
    @abstractmethod
    def create_product(self) -> Product: ...
    def operate(self): return self.create_product().use()
```

### Builder
```python
class QueryBuilder:
    def select(self, cols): self._cols = cols; return self
    def where(self, cond): self._where = cond; return self
    def build(self): return f"SELECT {self._cols} WHERE {self._where}"
```

### Adapter
```python
class LegacyPrinterAdapter(NewPrinter):
    def __init__(self, legacy): self._legacy = legacy
    def print(self, doc): self._legacy.old_print(doc, copies=1)
```

### Decorator
```python
class LoggingService(Service):
    def __init__(self, wrapped: Service): self._wrapped = wrapped
    def process(self, req):
        print(f"Processing {req}")
        return self._wrapped.process(req)
```

### Observer
```python
class EventBus:
    def __init__(self): self._handlers = defaultdict(list)
    def subscribe(self, event, fn): self._handlers[event].append(fn)
    def emit(self, event, data): [fn(data) for fn in self._handlers[event]]
```

### Strategy
```python
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy): self._s = strategy
    def pay(self, amount): return self._s.charge(amount)
```

### State
```python
class ATM:
    def withdraw(self, amt):
        if self.state != ATMState.PIN_VERIFIED:
            raise InvalidStateError(...)
        # ... process
```

### Command
```python
class InsertCommand:
    def __init__(self, editor, pos, text): ...
    def execute(self): self.editor.insert(self.pos, self.text)
    def undo(self): self.editor.delete(self.pos, len(self.text))
```

---

## Pattern Selection Guide

**Need to create objects?**
- One object, controlled creation → Singleton
- Object type decided at runtime → Factory Method
- Family of related objects → Abstract Factory
- Complex multi-step object → Builder

**Need to compose objects?**
- Incompatible interfaces → Adapter
- Add behavior without subclassing → Decorator
- Tree structure, uniform treatment → Composite
- Simplify complex subsystem → Facade

**Need to define behavior?**
- One-to-many notifications → Observer
- Swap algorithms at runtime → Strategy
- Encapsulate request, support undo → Command
- Behavior depends on state → State
- Sequential access to collection → Iterator

---

## Patterns You'll Use Most in FAANG LLD Interviews

1. **Strategy** — payment methods, discount rules, sorting
2. **Observer** — event systems, notifications
3. **State** — ATM, vending machine, order lifecycle
4. **Factory** — object creation based on type/config
5. **Singleton** — config, connection pool
6. **Decorator** — adding behaviors (logging, auth, caching)
