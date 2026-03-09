"""
SRP Violation: The Report God Class
====================================
The `Report` class below has THREE distinct reasons to change:
  1. DATA LOGIC changes   — how sales data is collected or computed
  2. FORMAT changes       — plain text vs. HTML vs. JSON output
  3. STORAGE changes      — local file vs. S3 vs. database

When any of these three things change, a developer must open this file
and modify it. A bug fix in file storage can accidentally break data logic.

Real-world use: This pattern appears in order management systems (Flipkart,
Amazon) where a single class handles product data, invoice formatting, and
email delivery. Separating these concerns is one of the most common early
refactors in production codebases.
"""

from __future__ import annotations

import json
import os
from datetime import date
from typing import Any


class Report:
    """
    GOD CLASS — three responsibilities in one class.

    Reason to change #1: business logic for data collection changes.
    Reason to change #2: output format requirements change.
    Reason to change #3: storage mechanism changes.
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.report_data: list[dict[str, Any]] = []
        self.output_dir: str = "./reports"  # storage concern embedded in data class

    # --- RESPONSIBILITY 1: Data Collection ---

    def collect_sales_data(self, transactions: list[dict[str, Any]]) -> None:
        """Process raw transaction data into report rows."""
        total_revenue = 0.0
        total_units = 0

        for tx in transactions:
            if tx.get("status") != "completed":  # business rule: skip non-completed
                continue

            revenue = tx["quantity"] * tx["unit_price"]
            total_revenue += revenue
            total_units += tx["quantity"]

            self.report_data.append({
                "product": tx["product_name"],
                "quantity": tx["quantity"],
                "unit_price": tx["unit_price"],
                "line_total": revenue,
                "date": tx["date"],
            })

        self.report_data.append({  # summary row — also a data concern
            "product": "TOTAL",
            "quantity": total_units,
            "unit_price": 0.0,
            "line_total": total_revenue,
            "date": str(date.today()),
        })

    # --- RESPONSIBILITY 2: Formatting ---

    def format_as_text(self) -> str:
        """Format collected data as plain text."""
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
                lines.append(f"{'TOTAL':<20} {row['quantity']:>6} {'':>12} ${row['line_total']:>11.2f}")
            else:
                lines.append(
                    f"{row['product']:<20} {row['quantity']:>6} "
                    f"${row['unit_price']:>11.2f} ${row['line_total']:>11.2f}"
                )

        lines.append("=" * 60)
        return "\n".join(lines)

    # --- RESPONSIBILITY 3: File Storage ---

    def save_to_file(self, filename: str) -> str:
        """Save the text-formatted report to a local file."""
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)

        content = self.format_as_text()  # TIP: calling another responsibility from here
        with open(filepath, "w") as f:
            f.write(content)

        return filepath

    def save_as_json(self, filename: str) -> str:
        """Save raw report data as JSON."""
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
    transactions = [
        {"product_name": "Widget A", "quantity": 10, "unit_price": 25.00, "status": "completed", "date": "2024-01-15"},
        {"product_name": "Widget B", "quantity": 5,  "unit_price": 50.00, "status": "completed", "date": "2024-01-16"},
        {"product_name": "Widget C", "quantity": 100, "unit_price": 5.00, "status": "pending",   "date": "2024-01-17"},
    ]

    report = Report(title="Q1 Sales Report")
    report.collect_sales_data(transactions)
    print(report.format_as_text())

    print("\nVIOLATION: This class has 3 reasons to change.")
    print("  1. Sales logic  → collect_sales_data()")
    print("  2. Format       → format_as_text()")
    print("  3. Storage      → save_to_file(), save_as_json()")
    print("\nSee example2_refactored.py for the solution.")
