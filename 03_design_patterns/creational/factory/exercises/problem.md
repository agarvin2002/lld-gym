# Exercise: Log Formatter Factory

## Problem

Implement a logging system where the output format is selected at runtime via a factory. The application code logs messages; the factory decides which formatter to instantiate.

## Classes to Implement

### `LogLevel(Enum)`
Values: `DEBUG`, `INFO`, `WARNING`, `ERROR`

### `LogRecord`
Dataclass with fields: `level: LogLevel`, `message: str`, `timestamp: str`

### `LogFormatter` (ABC)
Abstract base with one method:
```python
def format(self, record: LogRecord) -> str: ...
```

### Concrete Formatters

| Class | Output format |
|-------|---------------|
| `PlainFormatter` | `[INFO] 2024-01-01 Hello` |
| `JSONFormatter` | `{"level": "INFO", "timestamp": "2024-01-01", "message": "Hello"}` |
| `CSVFormatter` | `INFO,2024-01-01,Hello` |

### `FormatterFactory`
| Method | Description |
|--------|-------------|
| `register(name, cls)` | Class method — register a formatter class by name |
| `create(name) -> LogFormatter` | Class method — instantiate the named formatter; raise `ValueError` for unknown names |
| `available() -> list[str]` | Class method — return list of registered names |

The factory must ship with `"plain"`, `"json"`, and `"csv"` pre-registered.

### `Logger`
| Method | Description |
|--------|-------------|
| `__init__(formatter_name: str)` | Use `FormatterFactory.create(formatter_name)` |
| `log(level, message, timestamp) -> str` | Build a `LogRecord`, call `self._formatter.format(record)`, return the string |
| `set_formatter(name: str)` | Swap formatter at runtime; raise `ValueError` for unknown names |

## Constraints
- `FormatterFactory.create()` must raise `ValueError` for unknown formatter names
- After `logger.set_formatter("json")`, subsequent `log()` calls must use the new formatter
- The JSON output must be **valid JSON** (parseable by `json.loads`)

## Starter File
Edit `starter.py`. Run tests with:
```bash
pytest tests.py -v
```
