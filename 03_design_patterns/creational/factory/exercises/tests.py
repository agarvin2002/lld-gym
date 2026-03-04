"""Tests for Factory Pattern — Log Formatter Factory."""
import sys, os, json
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    LogLevel, LogRecord, LogFormatter,
    PlainFormatter, JSONFormatter, CSVFormatter,
    FormatterFactory, Logger,
)


TS = "2024-01-01"

def make_record(level=LogLevel.INFO, msg="Hello", ts=TS):
    return LogRecord(level=level, message=msg, timestamp=ts)


# ── PlainFormatter ────────────────────────────────────────────────────────────

class TestPlainFormatter:
    def test_format_contains_level(self):
        f = PlainFormatter()
        assert "INFO" in f.format(make_record())

    def test_format_contains_message(self):
        f = PlainFormatter()
        assert "Hello" in f.format(make_record())

    def test_format_contains_timestamp(self):
        f = PlainFormatter()
        assert TS in f.format(make_record())

    def test_format_structure(self):
        f = PlainFormatter()
        result = f.format(make_record())
        assert result == f"[INFO] {TS} Hello"

    def test_warning_level(self):
        f = PlainFormatter()
        r = make_record(LogLevel.WARNING, "Watch out")
        assert f.format(r) == f"[WARNING] {TS} Watch out"


# ── JSONFormatter ─────────────────────────────────────────────────────────────

class TestJSONFormatter:
    def test_valid_json(self):
        f = JSONFormatter()
        result = f.format(make_record())
        parsed = json.loads(result)  # must not raise
        assert isinstance(parsed, dict)

    def test_json_has_level_key(self):
        f = JSONFormatter()
        parsed = json.loads(f.format(make_record()))
        assert parsed["level"] == "INFO"

    def test_json_has_message_key(self):
        f = JSONFormatter()
        parsed = json.loads(f.format(make_record()))
        assert parsed["message"] == "Hello"

    def test_json_has_timestamp_key(self):
        f = JSONFormatter()
        parsed = json.loads(f.format(make_record()))
        assert parsed["timestamp"] == TS

    def test_error_level(self):
        f = JSONFormatter()
        r = make_record(LogLevel.ERROR, "Boom")
        parsed = json.loads(f.format(r))
        assert parsed["level"] == "ERROR"
        assert parsed["message"] == "Boom"


# ── CSVFormatter ──────────────────────────────────────────────────────────────

class TestCSVFormatter:
    def test_format_structure(self):
        f = CSVFormatter()
        result = f.format(make_record())
        assert result == f"INFO,{TS},Hello"

    def test_three_parts(self):
        f = CSVFormatter()
        parts = f.format(make_record()).split(",")
        assert len(parts) == 3

    def test_debug_level(self):
        f = CSVFormatter()
        r = make_record(LogLevel.DEBUG, "Trace")
        assert f.format(r) == f"DEBUG,{TS},Trace"


# ── FormatterFactory ──────────────────────────────────────────────────────────

class TestFormatterFactory:
    def test_create_plain(self):
        f = FormatterFactory.create("plain")
        assert isinstance(f, PlainFormatter)

    def test_create_json(self):
        f = FormatterFactory.create("json")
        assert isinstance(f, JSONFormatter)

    def test_create_csv(self):
        f = FormatterFactory.create("csv")
        assert isinstance(f, CSVFormatter)

    def test_unknown_name_raises(self):
        with pytest.raises(ValueError):
            FormatterFactory.create("xml")

    def test_available_includes_defaults(self):
        available = FormatterFactory.available()
        assert "plain" in available
        assert "json" in available
        assert "csv" in available

    def test_register_custom(self):
        class XmlFormatter(LogFormatter):
            def format(self, record: LogRecord) -> str:
                return f"<log><level>{record.level.value}</level></log>"

        FormatterFactory.register("xml", XmlFormatter)
        f = FormatterFactory.create("xml")
        assert isinstance(f, XmlFormatter)

    def test_case_insensitive(self):
        f = FormatterFactory.create("JSON")
        assert isinstance(f, JSONFormatter)


# ── Logger ────────────────────────────────────────────────────────────────────

class TestLogger:
    def test_log_returns_string(self):
        logger = Logger("plain")
        result = logger.log(LogLevel.INFO, "Test")
        assert isinstance(result, str)

    def test_log_plain(self):
        logger = Logger("plain")
        result = logger.log(LogLevel.INFO, "Hello", TS)
        assert result == f"[INFO] {TS} Hello"

    def test_log_json(self):
        logger = Logger("json")
        result = logger.log(LogLevel.ERROR, "Crash", TS)
        parsed = json.loads(result)
        assert parsed["level"] == "ERROR"

    def test_set_formatter_switches(self):
        logger = Logger("plain")
        logger.set_formatter("json")
        result = logger.log(LogLevel.INFO, "Hi", TS)
        json.loads(result)  # must be valid JSON now

    def test_set_formatter_unknown_raises(self):
        logger = Logger("plain")
        with pytest.raises(ValueError):
            logger.set_formatter("unknown_format")

    def test_multiple_log_calls(self):
        logger = Logger("csv")
        r1 = logger.log(LogLevel.DEBUG, "A", TS)
        r2 = logger.log(LogLevel.ERROR, "B", TS)
        assert r1 == f"DEBUG,{TS},A"
        assert r2 == f"ERROR,{TS},B"
