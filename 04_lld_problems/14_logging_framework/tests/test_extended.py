"""Logging Framework — Extended Tests."""
import sys, os, json
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import (
    LogLevel, Logger, MemoryHandler, PlainFormatter, JSONFormatter,
    MinLevelFilter, LoggerFactory,
)


class TestFilters:
    def test_min_level_filter_blocks_lower(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.add_filter(MinLevelFilter(LogLevel.ERROR))
        logger.info("blocked")
        logger.warning("blocked")
        logger.error("passes")
        assert len(h.records) == 1

    def test_remove_filter_restores_logging(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        f = MinLevelFilter(LogLevel.ERROR)
        logger.add_filter(f)
        logger.info("blocked")
        logger.remove_filter(f)
        logger.info("now passes")
        assert len(h.records) == 1

    def test_multiple_filters_all_must_pass(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.add_filter(MinLevelFilter(LogLevel.INFO))
        logger.add_filter(MinLevelFilter(LogLevel.ERROR))
        logger.info("blocked by second filter")
        logger.error("passes both")
        assert len(h.records) == 1


class TestHandlerMinLevel:
    def test_handler_level_independent_of_logger(self):
        logger = Logger("app", min_level=LogLevel.DEBUG)
        h_warn = MemoryHandler(PlainFormatter(), min_level=LogLevel.WARNING)
        h_debug = MemoryHandler(PlainFormatter(), min_level=LogLevel.DEBUG)
        logger.add_handler(h_warn)
        logger.add_handler(h_debug)
        logger.debug("debug msg")
        assert len(h_warn.records) == 0
        assert len(h_debug.records) == 1

    def test_remove_handler(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.info("recorded")
        logger.remove_handler(h)
        logger.info("not recorded")
        assert len(h.records) == 1


class TestAllLevels:
    def test_all_methods_log(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.debug("d")
        logger.info("i")
        logger.warning("w")
        logger.error("e")
        logger.critical("c")
        assert len(h.records) == 5

    def test_level_names_in_output(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.warning("watch out")
        assert "WARNING" in h.records[0]

    def test_critical_in_json(self):
        logger = Logger("app")
        h = MemoryHandler(JSONFormatter())
        logger.add_handler(h)
        logger.critical("crash")
        parsed = json.loads(h.records[0])
        assert parsed["level"] == "CRITICAL"
        assert parsed["message"] == "crash"


class TestLoggerFactory:
    def test_factory_loggers_are_independent(self):
        factory = LoggerFactory()
        l1 = factory.get_logger("svc1")
        l2 = factory.get_logger("svc2")
        h1 = MemoryHandler(PlainFormatter())
        h2 = MemoryHandler(PlainFormatter())
        l1.add_handler(h1)
        l2.add_handler(h2)
        l1.info("for svc1")
        assert len(h1.records) == 1
        assert len(h2.records) == 0

    def test_shared_logger_instance_via_factory(self):
        factory = LoggerFactory()
        l = factory.get_logger("shared")
        h = MemoryHandler(PlainFormatter())
        l.add_handler(h)
        factory.get_logger("shared").info("via second ref")
        assert len(h.records) == 1
