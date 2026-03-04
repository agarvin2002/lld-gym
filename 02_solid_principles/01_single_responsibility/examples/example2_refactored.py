"""
SRP Refactored Example: Report System with Separated Concerns
=============================================================
This file shows the same Report system from example1_violation.py,
now correctly decomposed into classes each with a single responsibility.

The four classes:
  - ReportDataCollector  → collects and processes raw data (Reason: data logic changes)
  - ReportFormatter      → converts data to text/HTML output (Reason: format requirements change)
  - ReportExporter       → persists formatted output to storage (Reason: storage mechanism changes)
  - ReportService        → orchestrates the above three (Reason: workflow changes)

Now when the email team asks for HTML reports, only ReportFormatter changes.
When DevOps moves storage to S3, only ReportExporter changes.
When finance changes the calculation rules, only ReportDataCollector changes.
"""

from __future__ import annotations

import json
import os
from datetime import date
from dataclasses import dataclass, field
from typing import Any


# =============================================================================
# DATA MODEL — A simple dataclass whose only job is holding report row data
# =============================================================================

@dataclass
class ReportRow:
    """
    Represents a single row in the report.
    Responsibility: data holder. No computation, no formatting, no I/O.
    """
    product: str
    quantity: int
    unit_price: float
    line_total: float
    date: str
    is_summary: bool = False


@dataclass
class ReportData:
    """
    Represents the complete collected data for a report.
    Responsibility: data holder. Contains rows and aggregate metadata.
    """
    title: str
    generated_on: str
    rows: list[ReportRow] = field(default_factory=list)
    total_units: int = 0
    total_revenue: float = 0.0


# =============================================================================
# RESPONSIBILITY #1: Data Collection / Business Logic
# Reason to change: ONLY when data collection or business rules change
# =============================================================================

class ReportDataCollector:
    """
    Collects and processes raw transaction data into a ReportData object.

    This class knows about business rules:
    - Only completed transactions count
    - How to compute line totals
    - How to aggregate totals

    It knows NOTHING about formatting or file I/O.
    """

    def collect(
        self,
        title: str,
        transactions: list[dict[str, Any]],
    ) -> ReportData:
        """
        Process raw transactions and return structured ReportData.

        Args:
            title: Report title
            transactions: List of raw transaction dicts

        Returns:
            ReportData with processed rows and aggregates
        """
        report = ReportData(title=title, generated_on=str(date.today()))

        for tx in transactions:
            # Business rule: only count completed transactions
            if tx.get("status") != "completed":
                continue

            revenue = tx["quantity"] * tx["unit_price"]
            report.total_revenue += revenue
            report.total_units += tx["quantity"]

            report.rows.append(
                ReportRow(
                    product=tx["product_name"],
                    quantity=tx["quantity"],
                    unit_price=tx["unit_price"],
                    line_total=revenue,
                    date=tx["date"],
                )
            )

        return report


# =============================================================================
# RESPONSIBILITY #2: Formatting / Presentation
# Reason to change: ONLY when output format requirements change
# =============================================================================

class ReportFormatter:
    """
    Converts a ReportData object into a human-readable string format.

    This class knows about presentation:
    - Column widths and alignment
    - Header/footer decorators
    - HTML tags

    It knows NOTHING about where the data came from or where output goes.
    """

    def to_text(self, report: ReportData) -> str:
        """
        Format ReportData as a plain-text table.

        Args:
            report: Processed report data

        Returns:
            Plain text representation of the report
        """
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append(f"REPORT: {report.title}")
        lines.append(f"Generated: {report.generated_on}")
        lines.append("=" * 60)
        lines.append(f"{'Product':<20} {'Qty':>6} {'Unit Price':>12} {'Total':>12}")
        lines.append("-" * 60)

        for row in report.rows:
            lines.append(
                f"{row.product:<20} {row.quantity:>6} "
                f"${row.unit_price:>11.2f} ${row.line_total:>11.2f}"
            )

        lines.append("-" * 60)
        lines.append(
            f"{'TOTAL':<20} {report.total_units:>6} {'':>12} ${report.total_revenue:>11.2f}"
        )
        lines.append("=" * 60)
        return "\n".join(lines)

    def to_html(self, report: ReportData) -> str:
        """
        Format ReportData as an HTML table.

        Args:
            report: Processed report data

        Returns:
            HTML string representation of the report
        """
        rows_html = ""
        for row in report.rows:
            rows_html += (
                f"<tr>"
                f"<td>{row.product}</td>"
                f"<td>{row.quantity}</td>"
                f"<td>${row.unit_price:.2f}</td>"
                f"<td>${row.line_total:.2f}</td>"
                f"</tr>\n        "
            )

        return f"""<!DOCTYPE html>
<html>
<head><title>{report.title}</title></head>
<body>
  <h1>{report.title}</h1>
  <p>Generated: {report.generated_on}</p>
  <table border="1">
    <tr><th>Product</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr>
        {rows_html}
    <tr><td><strong>TOTAL</strong></td><td>{report.total_units}</td>
        <td></td><td><strong>${report.total_revenue:.2f}</strong></td></tr>
  </table>
</body>
</html>"""

    def to_json(self, report: ReportData) -> str:
        """
        Format ReportData as a JSON string.

        Args:
            report: Processed report data

        Returns:
            JSON string representation of the report
        """
        payload = {
            "title": report.title,
            "generated": report.generated_on,
            "summary": {
                "total_units": report.total_units,
                "total_revenue": report.total_revenue,
            },
            "rows": [
                {
                    "product": row.product,
                    "quantity": row.quantity,
                    "unit_price": row.unit_price,
                    "line_total": row.line_total,
                    "date": row.date,
                }
                for row in report.rows
            ],
        }
        return json.dumps(payload, indent=2)


# =============================================================================
# RESPONSIBILITY #3: File Storage / Persistence
# Reason to change: ONLY when the storage mechanism changes
# =============================================================================

class ReportExporter:
    """
    Saves formatted report content to a file on disk.

    This class knows about I/O concerns:
    - File path construction
    - Directory creation
    - Writing bytes/strings to disk

    It knows NOTHING about report data structure or formatting rules.
    In a real system, you might have S3Exporter, DatabaseExporter, etc.
    all with the same interface but different implementations.
    """

    def __init__(self, output_dir: str = "./reports") -> None:
        self.output_dir = output_dir

    def export(self, content: str, filename: str) -> str:
        """
        Write content to a file in the output directory.

        Args:
            content: The formatted string to write (text, HTML, or JSON)
            filename: The filename to use (e.g., "report.txt")

        Returns:
            Absolute path to the saved file
        """
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath


# =============================================================================
# RESPONSIBILITY #4: Orchestration
# Reason to change: ONLY when the high-level workflow changes
# =============================================================================

class ReportService:
    """
    Orchestrates the report generation workflow.

    This is the only class that knows about all three other classes.
    Its responsibility is: coordinate data collection → formatting → export.

    This class changes ONLY when the workflow steps change (e.g., adding
    a step to archive old reports, or email the report after export).

    It does NOT change when storage moves to S3 (that's ReportExporter's job).
    It does NOT change when formatting style changes (that's ReportFormatter's job).
    """

    def __init__(
        self,
        collector: ReportDataCollector,
        formatter: ReportFormatter,
        exporter: ReportExporter,
    ) -> None:
        self.collector = collector
        self.formatter = formatter
        self.exporter = exporter

    def generate_text_report(
        self,
        title: str,
        transactions: list[dict[str, Any]],
        filename: str,
    ) -> tuple[str, str]:
        """
        End-to-end: collect → format as text → export.

        Returns:
            Tuple of (formatted_text, file_path)
        """
        data = self.collector.collect(title, transactions)
        text = self.formatter.to_text(data)
        filepath = self.exporter.export(text, filename)
        return text, filepath

    def generate_html_report(
        self,
        title: str,
        transactions: list[dict[str, Any]],
        filename: str,
    ) -> tuple[str, str]:
        """
        End-to-end: collect → format as HTML → export.

        Returns:
            Tuple of (formatted_html, file_path)
        """
        data = self.collector.collect(title, transactions)
        html = self.formatter.to_html(data)
        filepath = self.exporter.export(html, filename)
        return html, filepath

    def generate_json_report(
        self,
        title: str,
        transactions: list[dict[str, Any]],
        filename: str,
    ) -> tuple[str, str]:
        """
        End-to-end: collect → format as JSON → export.

        Returns:
            Tuple of (json_string, file_path)
        """
        data = self.collector.collect(title, transactions)
        json_str = self.formatter.to_json(data)
        filepath = self.exporter.export(json_str, filename)
        return json_str, filepath


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    # Sample transaction data
    transactions = [
        {
            "product_name": "Widget A",
            "quantity": 10,
            "unit_price": 25.00,
            "status": "completed",
            "date": "2024-01-15",
        },
        {
            "product_name": "Widget B",
            "quantity": 5,
            "unit_price": 50.00,
            "status": "completed",
            "date": "2024-01-16",
        },
        {
            "product_name": "Widget C",  # pending — excluded by business rule
            "quantity": 100,
            "unit_price": 5.00,
            "status": "pending",
            "date": "2024-01-17",
        },
        {
            "product_name": "Widget D",
            "quantity": 3,
            "unit_price": 100.00,
            "status": "completed",
            "date": "2024-01-18",
        },
    ]

    # Wire up the components (this could also be done by a DI framework)
    collector = ReportDataCollector()
    formatter = ReportFormatter()
    exporter = ReportExporter(output_dir="./demo_reports")
    service = ReportService(collector, formatter, exporter)

    print("=== REFACTORED REPORT SYSTEM (SRP Compliant) ===\n")

    # Generate plain text report
    text_output, text_path = service.generate_text_report(
        title="Q1 Sales Report",
        transactions=transactions,
        filename="q1_report.txt",
    )
    print(text_output)
    print(f"\nSaved to: {text_path}\n")

    # We can also use components individually — great for testing!
    print("=== USING COMPONENTS INDIVIDUALLY (testability benefit) ===\n")

    # Only test the data collection logic — no file I/O needed
    data = collector.collect("Test Report", transactions)
    print(f"Total revenue from completed transactions: ${data.total_revenue:.2f}")
    print(f"Total units from completed transactions: {data.total_units}")
    print(f"Number of product rows: {len(data.rows)}")

    print("\n=== SRP BENEFIT SUMMARY ===")
    print("ReportDataCollector → changes when: sales rules change")
    print("ReportFormatter     → changes when: output format changes")
    print("ReportExporter      → changes when: storage mechanism changes")
    print("ReportService       → changes when: workflow steps change")
    print("\nEach class has EXACTLY ONE reason to change.")

    # Clean up demo files
    import shutil
    if os.path.exists("./demo_reports"):
        shutil.rmtree("./demo_reports")
        print("\n(Demo report files cleaned up)")
