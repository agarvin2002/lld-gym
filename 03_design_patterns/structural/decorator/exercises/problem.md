# Exercise: Decorator Pattern — Text Formatter System

## Background

You are building a text formatting library. The formatters must be composable: you should be able
to wrap any formatter inside another and get combined behavior.

---

## The Interface

```python
class TextFormatter(ABC):
    @abstractmethod
    def format(self, text: str) -> str:
        """Return the formatted version of text."""
        ...
```

---

## Required Formatters

| Class | What it does | Example |
|---|---|---|
| `BaseFormatter` | Returns text unchanged | `"hello"` → `"hello"` |
| `BoldFormatter` | Wraps text in `**` | `"hello"` → `"**hello**"` |
| `ItalicFormatter` | Wraps text in `*` | `"hello"` → `"*hello*"` |
| `UpperCaseFormatter` | Uppercases text | `"hello"` → `"HELLO"` |
| `TrimFormatter` | Strips leading/trailing whitespace | `"  hi  "` → `"hi"` |
| `PrefixFormatter` | Prepends a fixed prefix | `prefix="NOTE: "` → `"NOTE: hello"` |

---

## Composition Requirements

All formatters must be composable:

```python
# Bold + Italic
formatter = BoldFormatter(ItalicFormatter(BaseFormatter()))
formatter.format("hello")  # "***hello***"  (bold wraps italic)

# Uppercase + Bold
formatter = UpperCaseFormatter(BoldFormatter(BaseFormatter()))
formatter.format("hello")  # "**HELLO**"

# All three
formatter = BoldFormatter(ItalicFormatter(UpperCaseFormatter(BaseFormatter())))
formatter.format("hello")  # "***HELLO***"

# Prefix + Bold
formatter = PrefixFormatter(BoldFormatter(BaseFormatter()), prefix="TIP: ")
formatter.format("read this")  # "TIP: **read this**"
```

---

## Notes

- Decorators apply from inside out: the innermost formatter runs first.
- `BoldFormatter(ItalicFormatter(BaseFormatter()))`:
  - BaseFormatter returns `"hello"`
  - ItalicFormatter wraps it → `"*hello*"`
  - BoldFormatter wraps that → `"**\*hello\***"`
- `BaseFormatter` is the leaf — it does nothing but satisfy the interface.
- Your `TextFormatterDecorator` base class should store `self._wrapped` and delegate.

---

## Files

- `starter.py` — skeleton to fill in
- `tests.py` — run with `python tests.py`
- `solution/solution.py` — reference solution
- `solution/explanation.md` — design notes
