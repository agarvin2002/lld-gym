# Single Responsibility Principle

## What is it?

A class should have only one reason to change. Each class should do one thing and do it well. When a class handles multiple concerns, a change in one area can accidentally break another.

## Analogy

A Swiss Army knife can cut, open bottles, and file nails — but it does none of these as well as a dedicated tool. A chef uses separate knives for bread, meat, and vegetables. Each tool has one job, so sharpening one never ruins another.

## Minimal code

```python
# Violation — one class, three responsibilities
class OrderProcessor:
    def validate(self, order): ...       # validation logic
    def charge_payment(self, order): ... # payment logic
    def send_email(self, order): ...     # notification logic

# Fix — one class per responsibility
class OrderValidator:
    def validate(self, order): ...

class PaymentProcessor:
    def charge(self, order, amount): ...

class EmailNotifier:
    def send_confirmation(self, order): ...

class OrderService:           # orchestrates the three
    def process(self, order): ...
```

## Real-world uses

- **Order management** (Zomato, Flipkart): validation, payment, and delivery updates are handled by separate services.
- **Notification systems**: `SMSSender` and `EmailSender` are separate classes so swapping SMS providers doesn't touch email code.
- **Report generation**: data collection, formatting, and file export are three separate classes — changing the output format doesn't touch the business calculations.

## One mistake

Putting validation, payment, and email all in one `OrderProcessor` class. When the email provider changes, you open a file that also contains payment logic. A bug fix in one area can accidentally break the other.

## What to do next

- See `examples/example1_violation.py` for a concrete god-class violation.
- See `examples/example2_refactored.py` for the same system split into focused classes.
- Open `exercises/starter.py` and refactor the `OrderProcessor` god class into six separate classes.
