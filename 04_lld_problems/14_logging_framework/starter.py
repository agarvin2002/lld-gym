"""
Logging Framework — Starter File
===================================
Your task: Build a structured logging framework (similar to Python's logging module).

Read problem.md and design.md before starting.

Design decisions:
  - LogLevel Enum with numeric values; must support comparison operators (< <= > >=)
  - LogRecord: immutable frozen dataclass holding all log metadata
  - LogFilter ABC: pluggable filtering (MinLevelFilter is the concrete implementation)
  - LogFormatter ABC: two formatters — PlainFormatter and JSONFormatter
  - LogHandler ABC: ConsoleHandler (prints) and MemoryHandler (stores for tests)
    - Handler has its own min_level; only handles records at or above that level
  - Logger: holds handlers and filters; _log() creates records and dispatches
  - LoggerFactory: registry of named loggers (Singleton-style per factory instance)
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import json
import time


class LogLevel(Enum):
    DEBUG    = 10
    INFO     = 20
    WARNING  = 30
    ERROR    = 40
    CRITICAL = 50

    # TODO: Implement comparison operators so LogLevel values can be compared:
    # __lt__, __le__, __gt__, __ge__ — compare using self.value vs other.value
    pass


@dataclass(frozen=True)
class LogRecord:
    level: LogLevel
    message: str
    logger_name: str
    timestamp: float
    extra: dict = field(default_factory=dict)


class LogFilter(ABC):
    @abstractmethod
    def should_log(self, record: LogRecord) -> bool:
        """Return True if this record should be logged."""
        ...


class MinLevelFilter(LogFilter):
    def __init__(self, min_level: LogLevel) -> None:
        # TODO: Store _min_level
        pass

    def should_log(self, record: LogRecord) -> bool:
        # TODO: Return True if record.level >= self._min_level
        pass


class LogFormatter(ABC):
    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """Convert a LogRecord to a formatted string."""
        ...


class PlainFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        # TODO: Return "[LEVEL] logger_name: message"
        # Example: "[INFO] app: Server started"
        pass


class JSONFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        # TODO: Return JSON string with keys: level, logger_name, message, timestamp
        pass


class LogHandler(ABC):
    def __init__(self, formatter: LogFormatter, min_level: LogLevel = LogLevel.DEBUG) -> None:
        # TODO: Store _formatter and _min_level
        pass

    def handle(self, record: LogRecord) -> None:
        """Format and write the record if it meets the handler's minimum level.

        TODO:
            - If record.level >= _min_level: call _write(self._formatter.format(record))
        """
        pass

    @abstractmethod
    def _write(self, message: str) -> None:
        """Write the formatted message to the output destination."""
        ...


class ConsoleHandler(LogHandler):
    def _write(self, message: str) -> None:
        # TODO: print(message)
        pass


class MemoryHandler(LogHandler):
    """Stores formatted records in memory (useful for testing)."""

    def __init__(self, formatter: LogFormatter, min_level: LogLevel = LogLevel.DEBUG) -> None:
        # TODO: Call super().__init__(formatter, min_level)
        # TODO: Create _records: list[str] = []
        pass

    def _write(self, message: str) -> None:
        # TODO: Append message to _records
        pass

    @property
    def records(self) -> list[str]:
        # TODO: Return a copy of _records
        pass


class Logger:
    def __init__(self, name: str, min_level: LogLevel = LogLevel.DEBUG) -> None:
        # TODO: Store _name and _min_level
        # TODO: Create _handlers: list[LogHandler] = []
        # TODO: Create _filters: list[LogFilter] = []
        pass

    def set_level(self, level: LogLevel) -> None:
        # TODO: Update _min_level
        pass

    def add_handler(self, handler: LogHandler) -> None:
        # TODO: Append to _handlers
        pass

    def remove_handler(self, handler: LogHandler) -> None:
        # TODO: Remove from _handlers
        pass

    def add_filter(self, log_filter: LogFilter) -> None:
        # TODO: Append to _filters
        pass

    def remove_filter(self, log_filter: LogFilter) -> None:
        # TODO: Remove from _filters
        pass

    def _log(self, level: LogLevel, message: str, **extra) -> None:
        """Create a LogRecord and dispatch to all handlers.

        TODO:
            - Return immediately if level < _min_level
            - Create LogRecord(level, message, _name, time.time(), extra)
            - Run all filters; if any returns False, return without logging
            - Call handler.handle(record) for each handler
        """
        pass

    def debug(self, message: str, **extra) -> None:
        # TODO: Call _log(LogLevel.DEBUG, message, **extra)
        pass

    def info(self, message: str, **extra) -> None:
        # TODO: Call _log(LogLevel.INFO, message, **extra)
        pass

    def warning(self, message: str, **extra) -> None:
        # TODO: Call _log(LogLevel.WARNING, message, **extra)
        pass

    def error(self, message: str, **extra) -> None:
        # TODO: Call _log(LogLevel.ERROR, message, **extra)
        pass

    def critical(self, message: str, **extra) -> None:
        # TODO: Call _log(LogLevel.CRITICAL, message, **extra)
        pass


class LoggerFactory:
    """Registry of named Logger instances."""

    def __init__(self) -> None:
        # TODO: Create _loggers: dict[str, Logger] = {}
        pass

    def get_logger(self, name: str) -> Logger:
        """Return existing logger or create a new one.

        TODO:
            - If name not in _loggers: create Logger(name), store it
            - Return _loggers[name]
        """
        pass
