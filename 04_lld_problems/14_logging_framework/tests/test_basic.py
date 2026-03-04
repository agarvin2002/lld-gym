"""Logging Framework — Basic Tests."""
import sys, os, json
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import (
    LogLevel, LogRecord, PlainFormatter, JSONFormatter,
    MemoryHandler, ConsoleHandler, Logger, LoggerFactory, MinLevelFilter,
)


def make_record(level=LogLevel.INFO, msg="hello", name="test"):
    import time
    return LogRecord(level=level, message=msg, logger_name=name, timestamp=time.time())


class TestLogLevel:
    def test_ordering(self):
        assert LogLevel.DEBUG < LogLevel.INFO < LogLevel.WARNING < LogLevel.ERROR < LogLevel.CRITICAL

    def test_equality(self):
        assert LogLevel.INFO == LogLevel.INFO

    def test_gte(self):
        assert LogLevel.ERROR >= LogLevel.WARNING


class TestPlainFormatter:
    def test_contains_level(self):
        f = PlainFormatter()
        assert "INFO" in f.format(make_record())

    def test_contains_message(self):
        f = PlainFormatter()
        assert "hello" in f.format(make_record())

    def test_contains_logger_name(self):
        f = PlainFormatter()
        assert "test" in f.format(make_record())


class TestJSONFormatter:
    def test_valid_json(self):
        f = JSONFormatter()
        parsed = json.loads(f.format(make_record()))
        assert isinstance(parsed, dict)

    def test_json_level_field(self):
        f = JSONFormatter()
        parsed = json.loads(f.format(make_record()))
        assert parsed["level"] == "INFO"

    def test_json_message_field(self):
        f = JSONFormatter()
        parsed = json.loads(f.format(make_record()))
        assert parsed["message"] == "hello"

    def test_json_timestamp_field(self):
        f = JSONFormatter()
        parsed = json.loads(f.format(make_record()))
        assert "timestamp" in parsed


class TestMemoryHandler:
    def test_record_stored(self):
        h = MemoryHandler(PlainFormatter())
        h.handle(make_record())
        assert len(h.records) == 1

    def test_records_returns_copy(self):
        h = MemoryHandler(PlainFormatter())
        h.handle(make_record())
        snap = h.records
        h.handle(make_record())
        assert len(snap) == 1   # snapshot unchanged

    def test_min_level_filtering(self):
        h = MemoryHandler(PlainFormatter(), min_level=LogLevel.WARNING)
        h.handle(make_record(LogLevel.DEBUG))
        h.handle(make_record(LogLevel.INFO))
        h.handle(make_record(LogLevel.WARNING))
        assert len(h.records) == 1

    def test_content_is_formatted_string(self):
        h = MemoryHandler(PlainFormatter())
        h.handle(make_record(msg="test msg"))
        assert "test msg" in h.records[0]


class TestLogger:
    def test_debug_reaches_handler(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.debug("msg")
        assert len(h.records) == 1

    def test_info_reaches_handler(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.info("hi")
        assert len(h.records) == 1

    def test_set_level_blocks_lower(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.set_level(LogLevel.WARNING)
        logger.debug("ignored")
        logger.info("ignored")
        logger.warning("passes")
        assert len(h.records) == 1

    def test_multiple_handlers(self):
        logger = Logger("app")
        h1 = MemoryHandler(PlainFormatter())
        h2 = MemoryHandler(JSONFormatter())
        logger.add_handler(h1)
        logger.add_handler(h2)
        logger.info("hello")
        assert len(h1.records) == 1
        assert len(h2.records) == 1


class TestLoggerFactory:
    def test_same_name_same_instance(self):
        factory = LoggerFactory()
        l1 = factory.get_logger("db")
        l2 = factory.get_logger("db")
        assert l1 is l2

    def test_different_names_different_instances(self):
        factory = LoggerFactory()
        l1 = factory.get_logger("db")
        l2 = factory.get_logger("cache")
        assert l1 is not l2
