# Explanation: Template Method Pattern — Report Generator

## The Core Insight

Without Template Method, the iteration logic is duplicated in every report class:

```python
class CSVReport:
    def generate(self, data):
        out = "Name,Category,Price\n"    # format varies
        for row in data:                 # THIS LOOP is always identical
            out += f"{row['name']},..."
        out += f"Total rows: {len(data)}\n"
        return out

class HTMLReport:
    def generate(self, data):
        out = "<table>..."
        for row in data:                 # SAME LOOP copied here
            out += f"<tr><td>..."
        out += "</table>..."
        return out
```

If you later need to filter empty rows before generating, you must update every class.

With Template Method, the loop lives in exactly one place:

```python
class ReportGenerator(ABC):
    def generate(self, data: list[dict]) -> str:
        parts = [self.format_header("Products")]
        for row in data:                          # ONE loop, one place
            parts.append(self.format_row(row))
        parts.append(self.format_footer(len(data)))
        return "".join(parts)
```

Change the loop once — all three generators benefit.

## Why `generate()` Is Not Abstract

`generate()` is the **template method** — it defines the algorithm skeleton. Making it abstract would allow subclasses to override the order of steps, defeating the pattern's purpose. It is deliberately concrete and documented as "do not override."

## The Hollywood Principle

> "Don't call us, we'll call you."

`ReportGenerator.generate()` calls `format_header()`, `format_row()`, and `format_footer()` — the base class calls into the subclass, not the other way around. The subclass never invokes `generate()` or any other base method explicitly.

## Why `"".join(parts)` Instead of `+= string`?

String concatenation inside a loop (`output += piece`) creates a new string object on every iteration — O(n²) in the worst case. Collecting into a list and joining at the end is O(n). For small reports the difference is negligible, but the list-join idiom is the idiomatic Python approach.

## Testing the Template Method Contract

The most important test in this exercise:

```python
def test_generate_is_defined_only_in_base_class(self):
    for cls in (CSVReportGenerator, HTMLReportGenerator, MarkdownReportGenerator):
        assert "generate" not in cls.__dict__
```

If a subclass defines `generate()` in its own `__dict__`, it has overridden the template — which breaks the entire pattern.

## Design Decisions

### `format_header` receives `title`

Even though all three generators ignore the `title` parameter in this exercise, including it in the signature is intentional. A real-world generator might use `title` to produce `<h1>Products</h1>` or `# Products`. Following the interface as defined in the ABC keeps subclasses honest and avoids a future signature change.

### Return strings, not print

Each hook returns a string. The template method assembles them. This separation means:
- Hooks are pure functions — easy to unit test in isolation.
- The template method owns I/O decisions (return string vs. write to file).

### Abstract vs Optional Hooks

All three hooks are `@abstractmethod` here because there is no sensible default for any of them — a report without a header, row format, or footer would be meaningless. If a hook had a reasonable default (e.g., "no footer"), it would be a concrete method returning `""`.

## Extending the System

Adding a new format (e.g., `JSONReportGenerator`) requires only a new class:

```python
import json

class JSONReportGenerator(ReportGenerator):
    def __init__(self):
        self._rows = []

    def format_header(self, title: str) -> str:
        self._rows = []
        return ""   # JSON doesn't have a textual header

    def format_row(self, row: dict) -> str:
        self._rows.append(row)
        return ""

    def format_footer(self, total: int) -> str:
        return json.dumps({"total": total, "rows": self._rows})
```

Zero changes to `ReportGenerator` or the existing three subclasses — Open/Closed Principle satisfied.
