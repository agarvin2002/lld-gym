# Abstract Factory Pattern

## 1. What Is It?

The **Abstract Factory pattern** provides an interface for creating **families of related objects** without specifying their concrete classes. It is often called a "factory of factories."

Where **Factory Method** creates *one* product, Abstract Factory creates a *suite* of products that belong together — ensuring consistency across the family.

```python
# Factory Method — one product
button = button_factory.create_button()

# Abstract Factory — a coordinated family of products
button   = ui_factory.create_button()
input    = ui_factory.create_text_input()
checkbox = ui_factory.create_checkbox()
# All three belong to the same theme — guaranteed
```

The client never names a concrete class. It asks the factory, and the factory returns objects that are all consistent with each other.

---

## 2. The Analogy

Think of **IKEA furniture families**. IKEA sells several furniture lines — for example, KALLAX (modular shelving) and HEMNES (traditional wood). Each line includes a table, a chair, and a lamp designed to look good together.

If you're decorating in the **HEMNES** style, you pick:
- HEMNES table
- HEMNES chair
- HEMNES lamp

You wouldn't mix a HEMNES table with a KALLAX chair — they'd look mismatched. The Abstract Factory is the catalog page for a single family: it guarantees everything you get belongs together.

Other real-world analogies:
- **Operating system themes**: Light mode vs Dark mode each produce matching title bars, buttons, and scroll bars
- **Vehicle manufacturing**: A car factory for sedans vs SUVs — each produces matching doors, seats, and dashboards for that vehicle type
- **Restaurant kitchen**: A sushi kitchen vs a pizzeria — each produces matching appetizers, mains, and desserts from a consistent cuisine

---

## 3. How It Differs from Factory Method

| Aspect | Factory Method | Abstract Factory |
|--------|----------------|------------------|
| Scope | Creates **one** product | Creates a **family** of products |
| Structure | One abstract method to override | Multiple abstract methods — one per product |
| Variation point | Subclass overrides one creator | Swap entire factory to switch families |
| Use case | "I need a button" | "I need a button, input, and checkbox — all matching" |

**Factory Method** is for one product with varying implementations.
**Abstract Factory** is for a consistent suite of products, where the entire suite varies together.

---

## 4. Python-Specific Implementation

Python uses `ABC` and `@abstractmethod` for both the abstract factory and the abstract products. Type hints make it clear what each factory method returns.

### Minimal UIFactory Example (15 lines)

```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...

class LightButton(Button):
    def render(self) -> str: return "<button style='light'>Click</button>"

class LightThemeFactory(UIFactory):
    def create_button(self) -> Button: return LightButton()

# Usage — client only sees UIFactory, never LightThemeFactory directly
def build_ui(factory: UIFactory) -> str:
    return factory.create_button().render()
```

The client function `build_ui` accepts any `UIFactory`. Swap the factory, get a different family — no changes to the client.

### ABC Enforcement

If a concrete factory forgets to implement a method, Python raises `TypeError` at instantiation:

```python
class IncompleteFactory(UIFactory):
    pass  # forgot create_button

factory = IncompleteFactory()  # TypeError: Can't instantiate abstract class
```

This is a significant advantage over duck typing — mistakes are caught early.

---

## 5. When to Use

**Abstract Factory is the right tool when:**

1. **Your system must work with multiple families of related products** — UI themes, database drivers, cross-platform widget toolkits
2. **You want to enforce family consistency** — prevent mixing a Light button with a Dark checkbox
3. **You want to switch entire product suites at runtime** — change theme, change database, change locale — by swapping one factory object
4. **You're building a library** — consumers can provide their own factory to customize product creation

**Common real-world contexts:**
- UI frameworks: Light/Dark/High-Contrast themes, each producing matching widgets
- Database abstraction layers: PostgreSQL vs SQLite vs MySQL — each producing matching Connection, QueryBuilder, Migrator
- Cross-platform UI: Windows vs macOS vs Linux widgets
- Game engines: UI skins, character asset sets, environment themes

---

## 6. When to Avoid

**Abstract Factory is overkill when:**

1. **You only have one product** — use Factory Method instead; Abstract Factory adds unnecessary complexity
2. **The products don't need to be consistent** — if mixing families is fine, you don't need the "family guarantee"
3. **You only have one family** — if you'll never have a second implementation, the abstraction adds no value
4. **The team is unfamiliar with the pattern** — for simple cases, dependency injection or straightforward constructors are clearer

A useful heuristic: if you find yourself writing only one concrete factory, you don't need Abstract Factory yet. Add it when the second family arrives.

---

## 7. Structure

```
AbstractFactory
├── create_product_a() -> AbstractProductA
├── create_product_b() -> AbstractProductB
└── create_product_c() -> AbstractProductC

ConcreteFactory1(AbstractFactory)
├── create_product_a() -> ConcreteProductA1
├── create_product_b() -> ConcreteProductB1
└── create_product_c() -> ConcreteProductC1

ConcreteFactory2(AbstractFactory)
├── create_product_a() -> ConcreteProductA2
├── create_product_b() -> ConcreteProductB2
└── create_product_c() -> ConcreteProductC2
```

The client depends only on `AbstractFactory` and the abstract product interfaces. It never imports any concrete class.

---

## 8. Common Mistakes

### Mixing Products from Different Factories

```python
# BAD — products from different families, inconsistent result
light_factory = LightThemeFactory()
dark_factory  = DarkThemeFactory()

button   = light_factory.create_button()    # Light button
checkbox = dark_factory.create_checkbox()   # Dark checkbox — MISMATCH
```

The point of Abstract Factory is to prevent exactly this. The fix is to use one factory throughout.

### Making Factories Stateful

Factories should be **stateless creation helpers**. If your factory stores product instances or counts, you've tangled factory logic with other concerns.

### Too Many Products per Family

If your factory has 15 abstract methods, it's probably doing too much. Consider whether some products should be split into a separate factory.

### Hardcoding Concrete Factories in Client Code

```python
# BAD — defeats the purpose
class Dialog:
    def __init__(self):
        self.factory = LightThemeFactory()  # hardcoded!
```

The client should receive the factory via constructor injection:

```python
# GOOD — factory injected, client is flexible
class Dialog:
    def __init__(self, factory: UIFactory) -> None:
        self.factory = factory
```

---

## Summary

| Aspect | Detail |
|--------|--------|
| Intent | Create families of related objects without specifying concrete classes |
| Also known as | Kit |
| Applicability | UI themes, DB drivers, cross-platform widgets, game asset sets |
| Key participants | AbstractFactory, ConcreteFactory, AbstractProduct, ConcreteProduct, Client |
| Python idiom | ABC + @abstractmethod for factory and products; constructor injection for factory |
| Versus Factory Method | Multiple products (suite) vs single product |
| Key benefit | Family consistency guarantee — no accidental cross-family mixing |
| Watch out | Overkill for one product; adding new products requires changing all factories |
