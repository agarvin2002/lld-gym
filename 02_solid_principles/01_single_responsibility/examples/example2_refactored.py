# Advanced topic — how to split a god class into single-responsibility components
"""
SRP Refactored: Report system with separated concerns.

The four classes each have exactly one reason to change:
  - ReportDataCollector  → changes when data/business rules change
  - ReportFormatter      → changes when output format changes
  - ReportExporter       → changes when storage mechanism changes
  - ReportService        → changes when the workflow steps change
"""

from __future__ import annotations

import os
from datetime import date
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReportRow:
    product: str
    quantity: int
    unit_price: float
    line_total: float
    date: str


@dataclass
class ReportData:
    title: str
    generated_on: str
    rows: list[ReportRow] = field(default_factory=list)
    total_units: int = 0
    total_revenue: float = 0.0


class ReportDataCollector:
    """Collects raw transactions into ReportData. Knows nothing about formatting or I/O."""

    def collect(self, title: str, transactions: list[dict[str, Any]]) -> ReportData:
        report = ReportData(title=title, generated_on=str(date.today()))
        for tx in transactions:
            if tx.get("status") != "completed":
                continue
            revenue = tx["quantity"] * tx["unit_price"]
            report.total_revenue += revenue
            report.total_units += tx["quantity"]
            report.rows.append(ReportRow(
                product=tx["product_name"], quantity=tx["quantity"],
                unit_price=tx["unit_price"], line_total=revenue, date=tx["date"],
            ))
        return report


class ReportFormatter:
    """Converts ReportData into a string. Knows nothing about where data came from or where it goes."""

    def to_text(self, report: ReportData) -> str:
        lines = [f"REPORT: {report.title}", f"Generated: {report.generated_on}", "-" * 40]
        for row in report.rows:
            lines.append(f"{row.product:<20} qty={row.quantity}  total=${row.line_total:.2f}")
        lines.append(f"{'TOTAL':<20} qty={report.total_units}  total=${report.total_revenue:.2f}")
        return "\n".join(lines)


class ReportExporter:
    """Writes content to disk. Knows nothing about report data or formatting."""

    def __init__(self, output_dir: str = "./reports") -> None:
        self.output_dir = output_dir

    def export(self, content: str, filename: str) -> str:
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath


class ReportService:
    """Orchestrates collect → format → export. Changes only when the workflow steps change."""

    def __init__(self, collector: ReportDataCollector, formatter: ReportFormatter, exporter: ReportExporter) -> None:
        self.collector = collector
        self.formatter = formatter
        self.exporter = exporter

    def generate_text_report(self, title: str, transactions: list[dict[str, Any]], filename: str) -> str:
        data = self.collector.collect(title, transactions)
        text = self.formatter.to_text(data)
        self.exporter.export(text, filename)
        return text


if __name__ == "__main__":
    transactions = [
        {"product_name": "Widget A", "quantity": 10, "unit_price": 25.0, "status": "completed", "date": "2024-01-15"},
        {"product_name": "Widget B", "quantity": 5,  "unit_price": 50.0, "status": "completed", "date": "2024-01-16"},
    ]
    service = ReportService(ReportDataCollector(), ReportFormatter(), ReportExporter("./demo_reports"))
    print(service.generate_text_report("Q1 Sales", transactions, "q1.txt"))

    import shutil
    if os.path.exists("./demo_reports"):
        shutil.rmtree("./demo_reports")
