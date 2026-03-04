# SOLID Principles Cheatsheet

## Quick Reference

| Principle | One-Liner | Violation Sign | Fix |
|-----------|-----------|----------------|-----|
| **SRP** | One class, one reason to change | Class name has "And"; God class | Extract into focused classes |
| **OCP** | Open for extension, closed for modification | if/elif chains that grow with features | Strategy/Template Method pattern |
| **LSP** | Subtypes must be substitutable | `isinstance()` guards in base-class functions | Redesign hierarchy; use composition |
| **ISP** | Don't force unused interface methods | `raise NotImplementedError` in subclass | Split into smaller interfaces |
| **DIP** | Depend on abstractions, not concretions | `self.db = MySQLDatabase()` in `__init__` | Inject via constructor |

---

## SRP — Ask Yourself
> "How many reasons does this class have to change?"

If the answer is more than one → extract.

```python
# ❌ Three reasons to change: data logic, formatting, storage
class Report:
    def get_data(self): ...
    def format_as_html(self): ...
    def save_to_db(self): ...

# ✅ One reason each
class ReportData:    def collect(self): ...
class ReportFormatter: def to_html(self, data): ...
class ReportRepository: def save(self, report): ...
```

---

## OCP — Ask Yourself
> "To add a new feature, do I need to modify existing tested code?"

If yes → OCP violation.

```python
# ❌ Adding new shape requires editing calculate_area
def calculate_area(shape):
    if shape.type == "circle": ...
    elif shape.type == "rect": ...  # modify here for every new shape!

# ✅ Add new shape = add new class only
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
```

---

## LSP — Ask Yourself
> "Can I pass a subclass wherever the base class is expected, with no surprises?"

If no → LSP violation.

```python
# ❌ Square breaks rectangle's invariant
def test(r: Rectangle):
    r.set_width(5); r.set_height(4)
    assert r.area() == 20  # fails for Square!

# ✅ Separate independent hierarchies
class Shape(ABC): ...
class Rectangle(Shape): ...  # independent
class Square(Shape): ...     # independent
```

---

## ISP — Ask Yourself
> "Does any implementing class have a method it doesn't use?"

If yes → interface is too fat.

```python
# ❌ Robot forced to implement eat() and sleep()
class Worker(ABC):
    def work(self): ...
    def eat(self): ...   # robot doesn't eat!
    def sleep(self): ...  # robot doesn't sleep!

# ✅ Segregated
class Workable(ABC): def work(self): ...
class Eatable(ABC): def eat(self): ...
class Human(Workable, Eatable): ...   # only what it needs
class Robot(Workable): ...            # only what it needs
```

---

## DIP — Ask Yourself
> "Does my high-level class create its own dependencies?"

If yes → DIP violation.

```python
# ❌ Hardcoded — can't test, can't swap
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()   # hardcoded!

# ✅ Injected — testable, swappable
class OrderService:
    def __init__(self, db: DatabaseInterface):
        self.db = db
```

---

## Pre-Submission Checklist

Before finishing your LLD design, check:
- [ ] Each class has a single clear responsibility (SRP)
- [ ] Adding features doesn't require modifying working code (OCP)
- [ ] Subclasses can replace base classes without surprises (LSP)
- [ ] No class implements methods it doesn't use (ISP)
- [ ] High-level classes accept interfaces, not concrete implementations (DIP)
