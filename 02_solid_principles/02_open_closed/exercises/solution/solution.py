"""Solution: Extensible Report Exporter (OCP)"""
import json
from abc import ABC, abstractmethod


class ExportStrategy(ABC):
    @abstractmethod
    def export(self, data: list[dict]) -> str: ...


class CSVExporter(ExportStrategy):
    def export(self, data: list[dict]) -> str:
        if not data:
            return ""
        header = ",".join(data[0].keys())
        rows = [",".join(str(v) for v in row.values()) for row in data]
        return "\n".join([header] + rows) + "\n"


class JSONExporter(ExportStrategy):
    def export(self, data: list[dict]) -> str:
        return json.dumps(data, indent=2)


class XMLExporter(ExportStrategy):
    def export(self, data: list[dict]) -> str:
        lines = ["<records>"]
        for row in data:
            lines.append("  <record>")
            for key, val in row.items():
                lines.append(f"    <{key}>{val}</{key}>")
            lines.append("  </record>")
        lines.append("</records>")
        return "\n".join(lines)


class ReportExporter:
    def __init__(self, strategy: ExportStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: ExportStrategy) -> None:
        self._strategy = strategy

    def export(self, data: list[dict]) -> str:
        return self._strategy.export(data)
