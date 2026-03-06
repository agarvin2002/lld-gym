# Design — Logging Framework

## Clarifying Questions (Interview Simulation)

Before drawing any class diagram, ask these in an interview:

1. What log levels do we need? → DEBUG, INFO, WARNING, ERROR, CRITICAL (numeric values like Python's logging).
2. Where should logs be written? → Console and in-memory (for testing); design for extensibility.
3. Do we need structured logging (JSON)? → Yes, support both plain text and JSON formatters.
4. Should loggers be filtered? → Yes, by minimum level and by pluggable filters.
5. Can multiple handlers be attached to one logger? → Yes.
6. Do we need named loggers with a factory/registry? → Yes, LoggerFactory for reuse.
7. Thread safety? → Basic implementation; handler writes are single-threaded.
8. Parent/child logger hierarchy (like Python's logging)? → Not required for this exercise.

---

## Core Entities

### 1. LogLevel (Enum)
Numeric values (10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL).
Must support comparison operators (`<`, `<=`, `>`, `>=`) for level filtering.

### 2. LogRecord (Frozen Dataclass)
Immutable snapshot of a log event: level, message, logger_name, timestamp, extra kwargs.
Created by `Logger._log()` and passed to handlers.

### 3. LogFilter (ABC)
Pluggable filter. `should_log(record) -> bool`.
`MinLevelFilter` is the concrete implementation — checks `record.level >= min_level`.

### 4. LogFormatter (ABC)
Converts a `LogRecord` to a string.
`PlainFormatter`: `[LEVEL] name: message`.
`JSONFormatter`: JSON with level, logger_name, message, timestamp keys.

### 5. LogHandler (ABC)
Combines a formatter and a min_level. `handle(record)` checks level and calls `_write(formatted)`.
`ConsoleHandler`: writes to stdout.
`MemoryHandler`: accumulates formatted strings in a list (great for testing).

### 6. Logger
Holds a list of handlers and filters. `_log()` creates a `LogRecord`, applies filters, dispatches.
Convenience methods: `debug()`, `info()`, `warning()`, `error()`, `critical()`.

### 7. LoggerFactory
Registry pattern: `get_logger(name)` returns the existing logger or creates a new one.
Prevents creating duplicate loggers for the same name.

---

## Class Diagram (ASCII)

```
+------------------+
|  LoggerFactory   |
+------------------+
| - _loggers: dict |------>  Logger (1..*)
+------------------+
| + get_logger(name)|
+------------------+

+------------------------------+
|           Logger             |
+------------------------------+
| - _name: str                 |
| - _min_level: LogLevel       |
| - _handlers: list[LogHandler]|------>  LogHandler (0..*)
| - _filters: list[LogFilter]  |------>  LogFilter (0..*)
+------------------------------+
| + set_level(level)           |
| + add_handler(h)             |
| + add_filter(f)              |
| + debug/info/warning/error/  |
|   critical(message)          |
| - _log(level, message)       |------>  LogRecord
+------------------------------+

      LogRecord (frozen dataclass)
      ┌────────────────────┐
      │ level: LogLevel    │
      │ message: str       │
      │ logger_name: str   │
      │ timestamp: float   │
      │ extra: dict        │
      └────────────────────┘

  LogFilter (ABC)             LogFormatter (ABC)
  ┌────────────────┐          ┌───────────────────┐
  │ + should_log() │          │ + format(record)  │
  └────────────────┘          └───────────────────┘
          │                           │
  MinLevelFilter          PlainFormatter | JSONFormatter

  LogHandler (ABC)
  ┌──────────────────────┐
  │ - _formatter         │------>  LogFormatter
  │ - _min_level         │
  │ + handle(record)     │
  │ - _write(message)    │
  └──────────────────────┘
          │
  ConsoleHandler | MemoryHandler
```

---

## Log Processing Pipeline

```
logger.info("Server started")
         │
         ▼
   Logger._log(INFO, "Server started")
         │
   [1] Check: INFO >= logger._min_level?  ──No──> drop
         │ Yes
   [2] Create LogRecord(INFO, "Server started", name, time.time())
         │
   [3] Run each LogFilter.should_log(record) ──Any False──> drop
         │ All True
   [4] For each LogHandler:
         │   handler.handle(record)
         │      → check record.level >= handler._min_level
         │      → formatter.format(record) → formatted string
         │      → _write(formatted string)
         ▼
   Output (console, memory, file, ...)
```

---

## LogLevel Comparison Implementation

```python
class LogLevel(Enum):
    DEBUG = 10
    INFO  = 20
    ...
    def __lt__(self, other): return self.value < other.value
    def __le__(self, other): return self.value <= other.value
    def __gt__(self, other): return self.value > other.value
    def __ge__(self, other): return self.value >= other.value
```

This allows natural comparisons: `LogLevel.INFO >= LogLevel.DEBUG` → True.

---

## Design Decisions & Trade-offs

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| Frozen LogRecord | Immutable — safe to pass across handlers | Cannot add fields after creation |
| Handler has own min_level | Fine-grained: e.g., console=INFO, file=DEBUG | Extra level check per handler |
| Filter as ABC | Pluggable: keyword filter, rate-limit filter, etc. | More classes to write |
| MemoryHandler for tests | Tests can inspect formatted output | Not production-appropriate |
| LoggerFactory registry | Single instance per name, no duplicates | Not thread-safe (add lock if needed) |

---

## Extensibility

**Add file logging:**
- Create `FileHandler(LogHandler)` — open a file in `__init__`, write in `_write()`.

**Add keyword filter:**
```python
class KeywordFilter(LogFilter):
    def __init__(self, keyword: str):
        self._keyword = keyword
    def should_log(self, record: LogRecord) -> bool:
        return self._keyword in record.message
```

**Add log rotation:**
- Subclass FileHandler with a max-size check before each write.
