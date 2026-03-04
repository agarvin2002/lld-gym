"""Tests for OCP Report Exporter exercise."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import CSVExporter, JSONExporter, XMLExporter, ReportExporter

SAMPLE = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]


class TestCSVExporter:
    def test_csv_has_header_row(self):
        result = CSVExporter().export(SAMPLE)
        assert result.startswith("name,age")

    def test_csv_has_data_rows(self):
        result = CSVExporter().export(SAMPLE)
        assert "Alice,30" in result
        assert "Bob,25" in result

    def test_csv_empty_data(self):
        result = CSVExporter().export([])
        assert result == "" or result is not None  # at minimum doesn't crash


class TestJSONExporter:
    def test_json_is_valid(self):
        result = JSONExporter().export(SAMPLE)
        parsed = json.loads(result)
        assert len(parsed) == 2

    def test_json_contains_data(self):
        result = JSONExporter().export(SAMPLE)
        assert "Alice" in result


class TestXMLExporter:
    def test_xml_has_root_element(self):
        result = XMLExporter().export(SAMPLE)
        assert "<records>" in result
        assert "</records>" in result

    def test_xml_has_record_elements(self):
        result = XMLExporter().export(SAMPLE)
        assert "<record>" in result

    def test_xml_contains_data(self):
        result = XMLExporter().export(SAMPLE)
        assert "Alice" in result


class TestReportExporter:
    def test_exporter_delegates_to_strategy(self):
        exporter = ReportExporter(CSVExporter())
        result = exporter.export(SAMPLE)
        assert "name" in result

    def test_exporter_can_switch_strategy(self):
        exporter = ReportExporter(CSVExporter())
        exporter.set_strategy(JSONExporter())
        result = exporter.export(SAMPLE)
        parsed = json.loads(result)
        assert isinstance(parsed, list)

    def test_ocp_new_exporter_does_not_change_report_exporter(self):
        """Verify ReportExporter works with any new strategy without modification."""
        from abc import ABC, abstractmethod

        class MarkdownExporter(CSVExporter):  # new format
            def export(self, data: list[dict]) -> str:
                if not data:
                    return ""
                headers = " | ".join(data[0].keys())
                separator = " | ".join(["---"] * len(data[0]))
                rows = [" | ".join(str(v) for v in row.values()) for row in data]
                return "\n".join([headers, separator] + rows)

        exporter = ReportExporter(MarkdownExporter())  # ReportExporter unchanged
        result = exporter.export(SAMPLE)
        assert "Alice" in result
