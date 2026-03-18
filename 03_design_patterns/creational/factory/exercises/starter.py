"""
WHAT YOU'RE BUILDING
====================
A log formatter factory.

A Logger produces formatted log lines. The format can be plain text, JSON,
or CSV — chosen at construction time and swappable later. You will build:

  - Three formatters: PlainFormatter, JSONFormatter, CSVFormatter
  - A FormatterFactory that creates formatters by name ("plain", "json", "csv")
  - A Logger that uses the factory to get the right formatter

Usage:
    logger = Logger("json")
    logger.log(LogLevel.ERROR, "Crash", "2024-01-01")
    # → '{"level": "ERROR", "timestamp": "2024-01-01", "message": "Crash"}'

    logger.set_formatter("plain")
    logger.log(LogLevel.INFO, "Started", "2024-01-01")
    # → '[INFO] 2024-01-01 Started'

Read exercises/problem.md for full requirements.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import json


class LogLevel(Enum):
    DEBUG   = "DEBUG"
    INFO    = "INFO"
    WARNING = "WARNING"
    ERROR   = "ERROR"


@dataclass
class LogRecord:
    level: LogLevel
    message: str
    timestamp: str


class LogFormatter(ABC):
    @abstractmethod
    def format(self, record: LogRecord) -> str: ...


class PlainFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        # TODO: Return a string in the form: "[LEVEL] timestamp message"
        # Example: "[INFO] 2024-01-01 Server started"
        pass


class JSONFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        # TODO: Return a JSON string with keys "level", "timestamp", "message"
        # HINT: use json.dumps({"level": record.level.value, ...})
        pass


class CSVFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        # TODO: Return a comma-separated string: "LEVEL,timestamp,message"
        # Example: "ERROR,2024-01-01,Crash"
        pass


class FormatterFactory:
    _registry: dict[str, type[LogFormatter]] = {}

    @classmethod
    def register(cls, name: str, formatter_class: type[LogFormatter]) -> None:
        # TODO: Store formatter_class in _registry under name.lower()
        pass

    @classmethod
    def create(cls, name: str) -> LogFormatter:
        # TODO: Look up name.lower() in _registry
        # TODO: Raise ValueError if not found — include the available names
        # HINT: raise ValueError(f"Unknown formatter {name!r}. Available: {sorted(cls._registry)}")
        # TODO: Return an instance of the matching formatter class (no constructor args needed)
        pass

    @classmethod
    def available(cls) -> list[str]:
        # TODO: Return a sorted list of registered formatter names
        pass


# Register the three built-in formatters here (after the class definition)
# TODO: FormatterFactory.register("plain", PlainFormatter)
# TODO: FormatterFactory.register("json",  JSONFormatter)
# TODO: FormatterFactory.register("csv",   CSVFormatter)


class Logger:
    def __init__(self, formatter_name: str) -> None:
        # TODO: Set self._formatter by calling FormatterFactory.create(formatter_name)
        pass

    def log(self, level: LogLevel, message: str, timestamp: str = "2024-01-01") -> str:
        # TODO: Build a LogRecord and call self._formatter.format(record)
        # HINT: record = LogRecord(level=level, message=message, timestamp=timestamp)
        pass

    def set_formatter(self, name: str) -> None:
        # TODO: Replace self._formatter with a new one from FormatterFactory.create(name)
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/creational/factory/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
