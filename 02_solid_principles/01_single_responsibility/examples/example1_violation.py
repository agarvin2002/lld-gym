"""
SRP Violation Example: The Report God Class
============================================
This file demonstrates a clear Single Responsibility Principle violation.

The `Report` class below has THREE distinct reasons to change:
  1. The DATA LOGIC changes  → how sales data is collected or computed
  2. The FORMAT changes      → HTML vs plain text vs JSON output
  3. The STORAGE changes     → local file vs S3 vs database

When any of these three things change, a developer must open THIS file
and modify it. That means a bug fix for file storage can accidentally
break data logic. A formatting change requires touching persistence code.
This is the core problem SRP solves.
"""

from __future__ import annotations

import json
import os
from datetime import date
from typing import Any


class Report:
    """
    GOD CLASS — violates SRP by having three distinct responsibilities.

    Reason to change #1: Business logic for data collection changes.
    Reason to change #2: Output format requirements change.
    Reason to change #3: Storage mechanism changes (file location, format, provider).

    A developer changing the file storage backend has no business
    reading or modifying the data collection logic. Yet they must,
    because it all lives here.
    """

    def __init__(self, title: str) -> None:
        self.title = title
        # Mix of data-related state and storage-related state in one class
        self.report_data: list[dict[str, Any]] = []
        self.output_dir: str = "./reports"  # storage concern embedded in data class

    # ------------------------------------------------------------------
    # RESPONSIBILITY #1: Data Collection / Business Logic
    # This section changes when: sales calculations change, new data
    # sources are added, the data model changes.
    # ------------------------------------------------------------------

    def collect_sales_data(self, transactions: list[dict[str, Any]]) -> None:
        """
        Processes raw transaction data into report-ready format.

        Why this is a data concern: it computes totals, filters records,
        and builds the internal data representation. This logic should
        live close to the domain, not next to file I/O code.
        """
        total_revenue = 0.0
        total_units = 0

        for tx in transactions:
            # Business rule: only count completed transactions
            if tx.get("status") != "completed":
                continue

            revenue = tx["quantity"] * tx["unit_price"]
            total_revenue += revenue
            total_units += tx["quantity"]

            self.report_data.append(
                {
                    "product": tx["product_name"],
                    "quantity": tx["quantity"],
                    "unit_price": tx["unit_price"],
                    "line_total": revenue,
                    "date": tx["date"],
                }
            )

        # Aggregate row — also a data/business concern
        self.report_data.append(
            {
                "product": "TOTAL",
                "quantity": total_units,
                "unit_price": 0.0,
                "line_total": total_revenue,
                "date": str(date.today()),
            }
        )

    # ------------------------------------------------------------------
    # RESPONSIBILITY #2: Formatting / Presentation
    # This section changes when: stakeholders want a different look,
    # output format changes (plain text → HTML → CSV), branding changes.
    # ------------------------------------------------------------------

    def format_as_text(self) -> str:
        """
        Formats collected data as plain text.

        Why this is a presentation concern: it deals only with how the
        data is displayed, not what the data means. If the stakeholder
        asks for HTML output tomorrow, this method gets replaced — but
        why should data collection code sit next to that change?
        """
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append(f"REPORT: {self.title}")
        lines.append(f"Generated: {date.today()}")
        lines.append("=" * 60)
        lines.append(f"{'Product':<20} {'Qty':>6} {'Unit Price':>12} {'Total':>12}")
        lines.append("-" * 60)

        for row in self.report_data:
            if row["product"] == "TOTAL":
                lines.append("-" * 60)
                lines.append(
                    f"{'TOTAL':<20} {row['quantity']:>6} {'':>12} ${row['line_total']:>11.2f}"
                )
            else:
                lines.append(
                    f"{row['product']:<20} {row['quantity']:>6} "
                    f"${row['unit_price']:>11.2f} ${row['line_total']:>11.2f}"
                )

        lines.append("=" * 60)
        return "\n".join(lines)

    def format_as_html(self) -> str:
        """
        Formats collected data as an HTML table.

        Another formatting method. Now we have two formatting concerns
        in the same class that also handles data and file I/O.
        """
        rows_html = ""
        for row in self.report_data:
            rows_html += (
                f"<tr>"
                f"<td>{row['product']}</td>"
                f"<td>{row['quantity']}</td>"
                f"<td>${row['unit_price']:.2f}</td>"
                f"<td>${row['line_total']:.2f}</td>"
                f"</tr>\n"
            )

        return f"""<!DOCTYPE html>
<html>
<head><title>{self.title}</title></head>
<body>
  <h1>{self.title}</h1>
  <table border="1">
    <tr><th>Product</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr>
    {rows_html}
  </table>
</body>
</html>"""

    # ------------------------------------------------------------------
    # RESPONSIBILITY #3: File Storage / Persistence
    # This section changes when: storage location changes, file format
    # changes, we move from local disk to S3, permissions change.
    # ------------------------------------------------------------------

    def save_to_file(self, filename: str) -> str:
        """
        Saves the text-formatted report to a local file.

        Why this is a storage concern: it handles file paths, directory
        creation, and I/O operations. This has nothing to do with
        computing revenue totals or rendering HTML.

        If we switch from local file storage to S3, we modify this class —
        which also contains our sales calculation logic. That is the SRP
        violation in action.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)

        content = self.format_as_text()  # Calling another responsibility from this one!
        with open(filepath, "w") as f:
            f.write(content)

        return filepath

    def save_as_json(self, filename: str) -> str:
        """
        Saves raw report data as JSON.

        Notice how save_as_json mixes storage (file I/O) with
        a formatting decision (JSON serialization). It's not even
        clear which responsibility this belongs to.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)

        payload = {
            "title": self.title,
            "generated": str(date.today()),
            "data": self.report_data,
        }

        with open(filepath, "w") as f:
            json.dump(payload, f, indent=2)

        return filepath


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
            "product_name": "Widget C",  # This one is pending — should be excluded
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

    # Using the god class — it "works" but is a design disaster
    report = Report(title="Q1 Sales Report")
    report.collect_sales_data(transactions)

    # Show formatted output
    print(report.format_as_text())
    print()

    # Show the HTML output (second formatter in same class)
    html_output = report.format_as_html()
    print("HTML output generated (first 200 chars):")
    print(html_output[:200])
    print("...")

    print()
    print("=== VIOLATION SUMMARY ===")
    print("This Report class has 3 reasons to change:")
    print("  1. Sales data logic changes    → collect_sales_data() changes")
    print("  2. Output format changes       → format_as_text(), format_as_html() change")
    print("  3. Storage mechanism changes   → save_to_file(), save_as_json() change")
    print()
    print("A bug fix in file I/O requires opening a file with sales calculation logic.")
    print("That is the SRP violation. See example2_refactored.py for the solution.")
