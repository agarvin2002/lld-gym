"""Factory Pattern Exercise — Log Formatter Factory Reference Solution."""
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
        return f"[{record.level.value}] {record.timestamp} {record.message}"


class JSONFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        return json.dumps({
            "level": record.level.value,
            "timestamp": record.timestamp,
            "message": record.message,
        })


class CSVFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        return f"{record.level.value},{record.timestamp},{record.message}"


class FormatterFactory:
    _registry: dict[str, type[LogFormatter]] = {}

    @classmethod
    def register(cls, name: str, formatter_class: type[LogFormatter]) -> None:
        cls._registry[name.lower()] = formatter_class

    @classmethod
    def create(cls, name: str) -> LogFormatter:
        key = name.lower()
        if key not in cls._registry:
            raise ValueError(
                f"Unknown formatter {name!r}. Available: {sorted(cls._registry)}"
            )
        return cls._registry[key]()

    @classmethod
    def available(cls) -> list[str]:
        return sorted(cls._registry)


FormatterFactory.register("plain", PlainFormatter)
FormatterFactory.register("json",  JSONFormatter)
FormatterFactory.register("csv",   CSVFormatter)


class Logger:
    def __init__(self, formatter_name: str) -> None:
        self._formatter: LogFormatter = FormatterFactory.create(formatter_name)

    def log(self, level: LogLevel, message: str, timestamp: str = "2024-01-01") -> str:
        record = LogRecord(level=level, message=message, timestamp=timestamp)
        return self._formatter.format(record)

    def set_formatter(self, name: str) -> None:
        self._formatter = FormatterFactory.create(name)
