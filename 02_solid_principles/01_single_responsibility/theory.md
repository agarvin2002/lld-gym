# Single Responsibility Principle (SRP)

## 1. Definition

> **"A class should have only one reason to change."**
> — Robert C. Martin

This is the most foundational of the SOLID principles. At first glance it sounds like "do one thing" — but the precise formulation is about **reasons to change**, not number of methods.

A class has multiple reasons to change when different stakeholders — different axes of business logic — can independently demand modifications to it. When that happens, a change for one stakeholder risks breaking the code for another.

---

## 2. Analogy: Swiss Army Knife vs. Specialized Tools

A Swiss Army knife is impressive for travel but terrible in a professional kitchen. A chef uses:
- A chef's knife (cutting)
- A boning knife (precision work)
- A peeler (peeling)

Each tool is optimized for its job. If the peeler breaks, the chef replaces only the peeler — not the entire knife set.

**In software:** a class that handles validation, persistence, and email sending is a Swiss Army knife. When the email provider changes, you open the same class that handles database writes. That is dangerous. Specialized classes let you change one thing without touching another.

---

## 3. Why SRP Matters

### Isolation of Change
When a class has one responsibility, a change in requirements for that responsibility affects only that class. A class with three responsibilities means three different change vectors all converge on one file.

### Testability
A class that only validates data can be tested without a database or email server. When responsibilities are mixed, your unit tests become integration tests — they require real infrastructure to run.

### Readability
A class with one clear job is self-documenting. A developer reading `UserValidator` immediately knows what it does. A developer reading `UserService` must read every method to understand the scope.

### Team Collaboration
When two developers need to modify different responsibilities in the same class simultaneously, they create merge conflicts. SRP naturally separates concerns into different files, reducing collaboration friction.

---

## 4. Python-Specific Guidance

### Identifying SRP Violations

Ask these questions about any class you write:

1. **What is the single noun that describes what this class IS?** If you need two nouns, it's a violation.
2. **List all the methods. Do they all operate on the same core data?** If half the methods use `self.user_data` and half use `self.smtp_config`, the class is doing two things.
3. **How many different people (roles) would ask you to change this class?** A business analyst changes validation rules. A DevOps engineer changes logging strategy. An email team changes notification templates. Three people = three responsibilities.

### When Functions Are Enough

Not every piece of logic needs a class. In Python, module-level functions are first-class citizens. If a responsibility is purely procedural and has no state, a module with functions is cleaner than a class:

```python
# This doesn't need to be a class
class EmailFormatter:
    def format(self, subject: str, body: str) -> str:
        return f"Subject: {subject}\n\n{body}"

# A function is cleaner
def format_email(subject: str, body: str) -> str:
    return f"Subject: {subject}\n\n{body}"
```

Use a class when you need to maintain state, inject dependencies, or participate in a polymorphic hierarchy.

### Dataclasses for Data Holding

Python's `@dataclass` decorator is excellent for classes whose only responsibility is holding data:

```python
from dataclasses import dataclass

@dataclass
class Order:
    order_id: str
    customer_email: str
    items: list[str]
    total_amount: float
```

This is perfectly SRP-compliant — the class's single responsibility is representing order data.

---

## 5. Signs of SRP Violation

### The "And" Name Test
If the best name for your class contains "And", it's doing too much:
- `UserValidatorAndSaver` → two classes needed
- `ReportGeneratorAndEmailer` → two classes needed
- `PaymentProcessorAndNotifier` → two classes needed

### Methods That Don't Use `self`'s Core Data
If a class has methods that don't touch the instance's main data fields, those methods probably belong elsewhere:

```python
class UserService:
    def __init__(self, user_data: dict):
        self.user_data = user_data

    def validate_email(self) -> bool:  # Uses self.user_data — belongs here
        return "@" in self.user_data["email"]

    def send_smtp_email(self, smtp_host: str) -> None:  # Uses smtp_host, not user_data — WRONG PLACE
        ...
```

### God Classes
A class with 20+ methods and 300+ lines is almost certainly a god class — it knows too much and does too much. Common examples in real codebases:
- `UserService` that handles authentication, profile editing, password reset, notifications, and billing
- `OrderController` that validates, processes, persists, and notifies all in one place
- Any class called `Manager`, `Handler`, or `Processor` that has grown organically over years

### Divergent Change
If you find yourself saying "I need to change this class every time the database schema changes AND every time the email template changes AND every time the validation rules change" — that class has too many reasons to change.

---

## 6. Quick Example: The Refactoring Pattern

### Violation: UserService Doing Everything

```python
class UserService:
    def validate_user(self, email: str, password: str) -> bool:
        # Reason to change #1: validation rules change
        return "@" in email and len(password) >= 8

    def save_user(self, email: str, password: str) -> None:
        # Reason to change #2: database changes (MySQL → PostgreSQL)
        print(f"INSERT INTO users (email, password) VALUES ({email}, {password})")

    def send_welcome_email(self, email: str) -> None:
        # Reason to change #3: email provider changes (SMTP → SendGrid)
        print(f"Sending welcome email to {email}")
```

**Three reasons to change. Three responsibilities. One class. Violation.**

### Refactored: Separated Concerns

```python
class UserValidator:
    # Reason to change: ONLY when validation rules change
    def validate(self, email: str, password: str) -> bool:
        return "@" in email and len(password) >= 8

class UserRepository:
    # Reason to change: ONLY when persistence layer changes
    def save(self, email: str, password: str) -> None:
        print(f"INSERT INTO users VALUES ({email}, {password})")

class UserEmailer:
    # Reason to change: ONLY when email communication changes
    def send_welcome(self, email: str) -> None:
        print(f"Sending welcome email to {email}")

class UserRegistrationService:
    # Reason to change: ONLY when the registration workflow changes
    def __init__(self, validator: UserValidator, repo: UserRepository, emailer: UserEmailer):
        self.validator = validator
        self.repo = repo
        self.emailer = emailer

    def register(self, email: str, password: str) -> bool:
        if not self.validator.validate(email, password):
            return False
        self.repo.save(email, password)
        self.emailer.send_welcome(email)
        return True
```

Now each class has exactly one reason to change.

---

## 7. Common Mistakes

### Going Too Far: One Method Per Class
SRP does NOT mean one method per class. A `UserValidator` that validates email format, password strength, AND username uniqueness is perfectly fine — all three are about validation. The class still has one responsibility: ensuring user data is valid.

```python
class UserValidator:
    def validate_email(self, email: str) -> bool: ...    # Fine
    def validate_password(self, password: str) -> bool: ...  # Fine
    def validate_username(self, username: str) -> bool: ...  # Fine
    # All three are "validation" — one responsibility
```

### Not Going Far Enough
The opposite mistake is applying SRP only to the most obvious violations. A class with 8 methods might still violate SRP if 4 methods are about data transformation and 4 are about persistence — even if each group of 4 feels "small."

### Applying SRP to the Wrong Level
SRP applies to classes, modules, and services — not just methods. A module that contains both `authentication.py` logic and `billing.py` logic violates SRP at the module level.

### Premature Decomposition
Don't decompose before you understand the responsibilities. Start with a simpler structure and refactor when a second "reason to change" emerges. Over-decomposed systems are as hard to work with as god classes — they just fail differently (too many files, too much indirection).

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Definition | One class, one reason to change |
| Measure | How many different stakeholders would ask you to change this? |
| Benefit | Isolates change, improves testability, reduces merge conflicts |
| Python tip | Use dataclasses for data, ABCs for interfaces, functions for stateless logic |
| Warning | Don't go too far — one responsibility can involve multiple methods |
