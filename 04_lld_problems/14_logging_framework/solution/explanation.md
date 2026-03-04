# Logging Framework — Solution Explanation

## Architecture: Chain of Responsibility + Strategy

```
Logger._log()
  ├── Level check (Logger's own min_level)
  ├── Filter chain (all must pass)
  └── For each handler:
        └── Handler.handle()
              ├── Handler's own min_level check
              └── Formatter.format() → _write()
```

Each layer independently gates records, following the **Chain of Responsibility** pattern. The formatter is a **Strategy** — swappable without changing the handler.

## Why two level checks?

The **Logger level** is a coarse gate (e.g., production loggers set to `INFO`, dev to `DEBUG`). The **Handler level** is a fine gate for specific destinations (e.g., console at `WARNING`, file at `DEBUG`). This matches real logging frameworks like Python's `logging` and Log4j.

## `LogRecord` is frozen (immutable)

```python
@dataclass(frozen=True)
class LogRecord:
```

Once created, a record cannot be modified. This prevents handlers from accidentally mutating records that are shared across multiple handlers.

## `LogFilter` chain semantics

All filters must return `True` for the record to proceed. This is AND logic — useful for combining: "level >= INFO AND logger_name starts with 'db'".

## `LoggerFactory` as Registry

```python
def get_logger(self, name: str) -> Logger:
    if name not in self._loggers:
        self._loggers[name] = Logger(name)
    return self._loggers[name]
```

Same name → same instance. This is the **Registry** pattern. It ensures that configuring `factory.get_logger("db")` in one place affects all code that uses `factory.get_logger("db")`.

## `MemoryHandler` for testing

`MemoryHandler` stores formatted strings in a list. It's the testing double for `ConsoleHandler` — no stdout required, easy to assert against. This is the same pattern Python's `logging.handlers.MemoryHandler` uses.

## `LogLevel` comparison via `__lt__`/`__ge__`

Python Enum doesn't support `<` by default. Adding `__lt__` etc. on the class allows natural comparisons: `record.level >= LogLevel.WARNING`. Using `.value` comparisons internally keeps it simple.
