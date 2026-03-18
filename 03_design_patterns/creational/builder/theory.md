# Builder

## What is it?
Builder separates object construction from the finished object. You set fields one step at a time on a builder object, then call `build()` to get the final product. This avoids long constructor argument lists and lets you validate all fields together before creating the object.

## Analogy
Ordering at a Subway counter: you pick bread, then protein, then toppings, then extras. The sandwich is only handed to you at the end. You never have to say everything in one breath, and the staff can catch missing required choices before wrapping it up.

## Minimal code
```python
class QueryBuilder:
    def __init__(self):
        self._table = ""
        self._conditions = []

    def table(self, name: str) -> "QueryBuilder":
        self._table = name
        return self  # return self enables chaining

    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self

    def build(self) -> str:
        if not self._table:
            raise ValueError("Table name is required")
        sql = f"SELECT * FROM {self._table}"
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        return sql

# Method chaining reads like a sentence
query = QueryBuilder().table("orders").where("status = 'paid'").build()
```

## Real-world uses
- Flipkart/Amazon search: building a product query with optional filters (price range, rating, category) step by step
- Hotel booking form: pick city, then dates, then room type, then add-ons — assembled into a `BookingRequest`
- Aadhaar e-KYC API request: mandatory fields (UID, OTP) plus optional extras, validated before sending

## One mistake
Forgetting to call `build()` — you end up holding the builder, not the product.
```python
resume = ResumeBuilder().contact("Alice", "alice@example.com")
# resume is a ResumeBuilder, NOT a Resume
# Fix: add .build() at the end
```

## What to do next
- Read `examples/example1_pizza.py` — fluent pizza builder with a Director for named presets.
- Read `examples/example2_http_request.py` — builder with validation inside `build()`.
- Open `exercises/starter.py` and implement the Resume builder step by step.
