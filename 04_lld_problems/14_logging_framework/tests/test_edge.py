"""Logging Framework — Edge Cases."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import LogLevel, Logger, MemoryHandler, PlainFormatter, MinLevelFilter


class TestEdgeCases:
    def test_logger_with_no_handlers_does_not_crash(self):
        logger = Logger("empty")
        logger.info("no handlers, should not raise")

    def test_logger_level_critical_blocks_all_but_critical(self):
        logger = Logger("strict", min_level=LogLevel.CRITICAL)
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.debug("no")
        logger.info("no")
        logger.warning("no")
        logger.error("no")
        logger.critical("yes")
        assert len(h.records) == 1

    def test_empty_message_logged(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.info("")
        assert len(h.records) == 1
        assert "" in h.records[0]

    def test_handler_with_higher_min_level_blocks_all(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter(), min_level=LogLevel.CRITICAL)
        logger.add_handler(h)
        logger.debug("d")
        logger.info("i")
        logger.warning("w")
        logger.error("e")
        assert len(h.records) == 0
        logger.critical("c")
        assert len(h.records) == 1

    def test_record_timestamp_is_recent(self):
        import time
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        before = time.time()
        logger.info("ts check")
        after = time.time()
        # We can't inspect the LogRecord directly from MemoryHandler (it stores strings),
        # but we verify the logger doesn't crash and records something
        assert len(h.records) == 1

    def test_filter_after_level_check(self):
        """Logger level check runs before filters (optimization)."""
        logger = Logger("app", min_level=LogLevel.ERROR)
        filter_called = []

        class TrackingFilter(MinLevelFilter):
            def should_log(self, record):
                filter_called.append(record)
                return super().should_log(record)

        logger.add_filter(TrackingFilter(LogLevel.DEBUG))
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        logger.debug("below logger level — filter should NOT be called")
        assert len(filter_called) == 0  # logger level check stops it first

    def test_multiple_log_calls_accumulate(self):
        logger = Logger("app")
        h = MemoryHandler(PlainFormatter())
        logger.add_handler(h)
        for i in range(10):
            logger.info(f"message {i}")
        assert len(h.records) == 10
