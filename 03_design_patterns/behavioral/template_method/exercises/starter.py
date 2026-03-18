"""
WHAT YOU'RE BUILDING
====================
A report generator that produces the same product data in three formats:
CSV, HTML, and Markdown.

The base class ReportGenerator owns the algorithm skeleton in generate():
  1. Call format_header("Products")
  2. Call format_row(row) for each row
  3. Call format_footer(len(data))
  4. Join all parts and return the complete string

You implement three concrete subclasses that fill in the three formatting steps.
The generate() method is already written — do not override it in subclasses.

Classes to implement:
  - ReportGenerator (ABC) — template method already stubbed below
  - CSVReportGenerator    — comma-separated output
  - HTMLReportGenerator   — HTML table output
  - MarkdownReportGenerator — Markdown table output
"""
from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    """
    Template Method: generate() defines the report-building sequence.
    Subclasses implement format_header, format_row, and format_footer.
    """

    def generate(self, data: list[dict]) -> str:
        """
        Build and return a complete report string.

        Sequence:
          1. format_header("Products")
          2. format_row(row) for each row in data
          3. format_footer(len(data))
          4. join all parts and return
        """
        # TODO: build a list called 'parts'
        # TODO: append self.format_header("Products")
        # TODO: for each row in data, append self.format_row(row)
        # TODO: append self.format_footer(len(data))
        # TODO: return "".join(parts)
        # HINT: parts is just a list of strings — build it step by step then join
        pass

    @abstractmethod
    def format_header(self, title: str) -> str:
        """Return the report header string."""
        ...

    @abstractmethod
    def format_row(self, row: dict) -> str:
        """Return a formatted string for a single data row."""
        ...

    @abstractmethod
    def format_footer(self, total: int) -> str:
        """Return the report footer string."""
        ...


class CSVReportGenerator(ReportGenerator):
    """Generates a comma-separated values report."""

    def format_header(self, title: str) -> str:
        # TODO: return "Name,Category,Price\n"
        pass

    def format_row(self, row: dict) -> str:
        # TODO: return f"{row['name']},{row['category']},{row['price']}\n"
        pass

    def format_footer(self, total: int) -> str:
        # TODO: return f"Total rows: {total}\n"
        pass


class HTMLReportGenerator(ReportGenerator):
    """Generates an HTML table report."""

    def format_header(self, title: str) -> str:
        # TODO: return "<table><tr><th>Name</th><th>Category</th><th>Price</th></tr>\n"
        pass

    def format_row(self, row: dict) -> str:
        # TODO: return f"<tr><td>{row['name']}</td><td>{row['category']}</td><td>{row['price']}</td></tr>\n"
        pass

    def format_footer(self, total: int) -> str:
        # TODO: return f"</table><p>Total: {total} items</p>"
        pass


class MarkdownReportGenerator(ReportGenerator):
    """Generates a Markdown table report."""

    def format_header(self, title: str) -> str:
        # TODO: return "| Name | Category | Price |\n|------|----------|-------|\n"
        # HINT: Two lines — the column headers and the separator row of dashes
        pass

    def format_row(self, row: dict) -> str:
        # TODO: return f"| {row['name']} | {row['category']} | {row['price']} |\n"
        pass

    def format_footer(self, total: int) -> str:
        # TODO: return f"\n*Total: {total} items*"
        # HINT: The leading \n separates the last row from the footer
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/behavioral/template_method/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
