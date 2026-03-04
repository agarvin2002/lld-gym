# Explanation: Decorator Pattern — Text Formatter

## The Core Idea
Each formatter wraps another formatter. When `format(text)` is called, it calls the inner formatter first, then applies its own transformation. This chains arbitrarily without modifying any existing class.

```
text → BaseFormatter → BoldFormatter → UpperCaseFormatter → result
```

## Why Not Subclassing?
With inheritance you'd need: `BoldFormatter`, `UpperCaseFormatter`, `BoldUpperCaseFormatter`, `BoldUpperCaseTrimFormatter` — exponential explosion. With Decorator: just compose at runtime.

## Pattern Structure

```
TextFormatter (ABC)
  └── format(text) → str

BaseFormatter          ← concrete component (identity — returns text as-is)
FormatterDecorator     ← abstract decorator, wraps a TextFormatter
  ├── BoldFormatter         → **text**
  ├── UpperCaseFormatter    → TEXT
  ├── TrimFormatter         → text.strip()
  └── TruncateFormatter     → text[:n]...
```

## Key Implementation Detail

```python
class FormatterDecorator(TextFormatter):
    def __init__(self, formatter: TextFormatter) -> None:
        self._formatter = formatter   # wraps another formatter

    def format(self, text: str) -> str:
        return self._formatter.format(text)  # delegate, then augment
```

Each concrete decorator calls `super().format(text)` (or `self._formatter.format(text)`) to get the inner result, then applies its transform on top.

## Trade-offs

| | Decorator | Inheritance |
|---|---|---|
| Adding combinations | O(1) — compose at runtime | O(2^n) — new subclass per combo |
| Adding new transforms | Add one class | Add one class |
| Order matters | Yes — stack order changes result | N/A |
| Runtime flexibility | ✅ swap formatters at runtime | ❌ fixed at compile time |

## Extensibility Points
- **New transform**: one new class implementing `FormatterDecorator` — zero changes to existing code (OCP)
- **Logging decorator**: wrap any formatter in `LoggingFormatter` to print what was formatted
- **Caching decorator**: cache `format()` results for expensive transforms
