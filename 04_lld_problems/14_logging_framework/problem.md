# Problem 14: Logging Framework

## Problem Statement

Design a production-grade logging framework (like Python's `logging` module or Log4j) that supports multiple log levels, configurable handlers, formatters, and filters.

---

## Core Concepts

### Log Levels (in order of severity)
```
DEBUG < INFO < WARNING < ERROR < CRITICAL
```

### Components

| Component | Role |
|-----------|------|
| `LogRecord` | Immutable data object: level, message, logger_name, timestamp, extra |
| `LogFilter` | Predicate: should this record be processed? |
| `LogFormatter` | Converts `LogRecord` → string |
| `LogHandler` | Writes formatted records to a destination |
| `Logger` | Entry point: accepts log calls, applies filters, dispatches to handlers |
| `LoggerFactory` | Returns named Logger instances (singleton per name) |

---

## API

```python
# Create loggers via factory
factory = LoggerFactory()
logger = factory.get_logger("app.db")

# Log at various levels
logger.debug("Query started")
logger.info("User logged in")
logger.warning("Disk at 80%")
logger.error("Connection failed")
logger.critical("System crash")

# Configure handlers
console_handler = ConsoleHandler(formatter=PlainFormatter(), min_level=LogLevel.INFO)
file_handler = FileHandler(filepath="/tmp/app.log", formatter=JSONFormatter())
logger.add_handler(console_handler)
logger.add_handler(file_handler)

# Set logger's own minimum level
logger.set_level(LogLevel.DEBUG)
```

---

## Classes

### `LogLevel(Enum)`
Values: `DEBUG=10`, `INFO=20`, `WARNING=30`, `ERROR=40`, `CRITICAL=50`

### `LogRecord`
Dataclass: `level: LogLevel`, `message: str`, `logger_name: str`, `timestamp: float`, `extra: dict`

### `LogFilter` (ABC)
`should_log(record: LogRecord) -> bool`

### `MinLevelFilter(LogFilter)`
Returns True only if `record.level >= min_level`

### `LogFormatter` (ABC)
`format(record: LogRecord) -> str`

### `PlainFormatter`
`"[LEVEL] logger_name: message"`

### `JSONFormatter`
Valid JSON string with keys: level, logger_name, message, timestamp

### `LogHandler` (ABC)
`handle(record: LogRecord) -> None`; has `formatter` and optional `min_level`; calls `formatter.format` then writes

### `ConsoleHandler(LogHandler)`
Prints to stdout. Constructor: `(formatter, min_level=LogLevel.DEBUG)`

### `MemoryHandler(LogHandler)`
Stores records in a list. `records` property returns list. Useful for testing.

### `Logger`
- `__init__(name, min_level=LogLevel.DEBUG)`
- `add_handler(handler)`, `remove_handler(handler)`
- `add_filter(filter)`, `remove_filter(filter)`
- `set_level(level)`
- `debug/info/warning/error/critical(message, **extra)`
- Internal: creates `LogRecord`, checks own level + all filters, dispatches to handlers that also pass their level check

### `LoggerFactory`
- `get_logger(name) -> Logger` — returns same instance for same name
- `configure_root(handler)` — all loggers also send to root handlers (optional stretch goal)
