"""Logging Framework — Reference Solution."""
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

    def __lt__(self, other): return self.value < other.value
    def __le__(self, other): return self.value <= other.value
    def __gt__(self, other): return self.value > other.value
    def __ge__(self, other): return self.value >= other.value


@dataclass(frozen=True)
class LogRecord:
    level: LogLevel
    message: str
    logger_name: str
    timestamp: float
    extra: dict = field(default_factory=dict)


class LogFilter(ABC):
    @abstractmethod
    def should_log(self, record: LogRecord) -> bool: ...


class MinLevelFilter(LogFilter):
    def __init__(self, min_level: LogLevel) -> None:
        self._min_level = min_level

    def should_log(self, record: LogRecord) -> bool:
        return record.level >= self._min_level


class LogFormatter(ABC):
    @abstractmethod
    def format(self, record: LogRecord) -> str: ...


class PlainFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        return f"[{record.level.name}] {record.logger_name}: {record.message}"


class JSONFormatter(LogFormatter):
    def format(self, record: LogRecord) -> str:
        return json.dumps({
            "level": record.level.name,
            "logger_name": record.logger_name,
            "message": record.message,
            "timestamp": record.timestamp,
        })


class LogHandler(ABC):
    def __init__(self, formatter: LogFormatter, min_level: LogLevel = LogLevel.DEBUG) -> None:
        self._formatter = formatter
        self._min_level = min_level

    def handle(self, record: LogRecord) -> None:
        if record.level >= self._min_level:
            self._write(self._formatter.format(record))

    @abstractmethod
    def _write(self, message: str) -> None: ...


class ConsoleHandler(LogHandler):
    def _write(self, message: str) -> None:
        print(message)


class MemoryHandler(LogHandler):
    def __init__(self, formatter: LogFormatter, min_level: LogLevel = LogLevel.DEBUG) -> None:
        super().__init__(formatter, min_level)
        self._records: list[str] = []

    def _write(self, message: str) -> None:
        self._records.append(message)

    @property
    def records(self) -> list[str]:
        return list(self._records)


class Logger:
    def __init__(self, name: str, min_level: LogLevel = LogLevel.DEBUG) -> None:
        self._name = name
        self._min_level = min_level
        self._handlers: list[LogHandler] = []
        self._filters: list[LogFilter] = []

    def set_level(self, level: LogLevel) -> None:
        self._min_level = level

    def add_handler(self, handler: LogHandler) -> None:
        self._handlers.append(handler)

    def remove_handler(self, handler: LogHandler) -> None:
        self._handlers.remove(handler)

    def add_filter(self, log_filter: LogFilter) -> None:
        self._filters.append(log_filter)

    def remove_filter(self, log_filter: LogFilter) -> None:
        self._filters.remove(log_filter)

    def _log(self, level: LogLevel, message: str, **extra) -> None:
        if level < self._min_level:
            return
        record = LogRecord(
            level=level,
            message=message,
            logger_name=self._name,
            timestamp=time.time(),
            extra=extra,
        )
        for f in self._filters:
            if not f.should_log(record):
                return
        for handler in self._handlers:
            handler.handle(record)

    def debug(self, message: str, **extra) -> None:
        self._log(LogLevel.DEBUG, message, **extra)

    def info(self, message: str, **extra) -> None:
        self._log(LogLevel.INFO, message, **extra)

    def warning(self, message: str, **extra) -> None:
        self._log(LogLevel.WARNING, message, **extra)

    def error(self, message: str, **extra) -> None:
        self._log(LogLevel.ERROR, message, **extra)

    def critical(self, message: str, **extra) -> None:
        self._log(LogLevel.CRITICAL, message, **extra)


class LoggerFactory:
    def __init__(self) -> None:
        self._loggers: dict[str, Logger] = {}

    def get_logger(self, name: str) -> Logger:
        if name not in self._loggers:
            self._loggers[name] = Logger(name)
        return self._loggers[name]
