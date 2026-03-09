# Open/Closed Principle

## What is it?

A class should be open for extension but closed for modification. You should be able to add new behavior without changing existing, working code. The primary tool for this in Python is the **Strategy pattern**: swap behavior at runtime by injecting different objects that share the same interface.

## Analogy

A power strip has fixed slots. You add new devices by plugging them in — you never rewire the strip itself. The strip is closed for modification (you don't change it), but open for extension (you add new devices at any time).

## Minimal code

```python
# Violation — every new discount type requires editing this class
class DiscountCalculator:
    def calculate(self, total, discount_type):
        if discount_type == "PERCENTAGE": return total * 0.10
        elif discount_type == "FIXED":      return 20.0
        elif discount_type == "SEASONAL":   return total * 0.25
        # Adding LOYALTY requires opening and editing this file

# Fix — add new types as new classes, never edit the calculator
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float: ...

class PercentageDiscount(DiscountStrategy):
    def apply(self, price: float) -> float: return price * 0.90

class SeasonalDiscount(DiscountStrategy):     # new type — no edits above
    def apply(self, price: float) -> float: return price * 0.75

class PriceCalculator:                        # never changes
    def __init__(self, strategy: DiscountStrategy) -> None:
        self.strategy = strategy
    def calculate(self, price: float) -> float:
        return self.strategy.apply(price)
```

## Real-world uses

- **Checkout systems** (Razorpay, Paytm, UPI): new payment gateways are added as new classes without touching the existing payment flow.
- **Report exporters**: CSV, JSON, and XML are three separate strategy classes; adding PDF doesn't change the exporter.
- **Notification channels**: SMS, email, and Slack are separate sender classes; adding WhatsApp is a new class.

## One mistake

Adding a new `elif` branch to an existing method every time a new type is needed. Each addition risks breaking all the existing branches and requires re-testing the whole method.

## What to do next

- See `examples/example1_violation.py` for an `if/elif` discount chain that grows with every new type.
- See `examples/example2_with_strategy.py` for the Strategy pattern fix.
- Open `exercises/starter.py` and implement the `ExportStrategy` subclasses without modifying `ReportExporter`.
