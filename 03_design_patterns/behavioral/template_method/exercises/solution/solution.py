"""Template Method Pattern Exercise — Reference Solution.

ReportGenerator defines the skeleton; CSV, HTML, and Markdown subclasses
implement the three formatting hooks.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Abstract base — template method lives here
# ---------------------------------------------------------------------------

class ReportGenerator(ABC):
    """
    Abstract base class for report generators.

    ``generate()`` is the Template Method: it defines the fixed sequence
    (header → rows → footer) and delegates formatting details to subclasses
    via three abstract hook methods.
    """

    def generate(self, data: list[dict]) -> str:
        """
        Build and return a complete report string.

        Sequence:
          1. format_header("Products")
          2. format_row(row) for each row in data
          3. format_footer(len(data))
          4. return "".join(all parts)
        """
        parts: list[str] = []
        parts.append(self.format_header("Products"))
        for row in data:
            parts.append(self.format_row(row))
        parts.append(self.format_footer(len(data)))
        return "".join(parts)

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


# ---------------------------------------------------------------------------
# Concrete generator 1: CSV
# ---------------------------------------------------------------------------

class CSVReportGenerator(ReportGenerator):
    """Generates a comma-separated values (CSV) report."""

    def format_header(self, title: str) -> str:
        """Return the CSV column header row."""
        return "Name,Category,Price\n"

    def format_row(self, row: dict) -> str:
        """Return one CSV data row."""
        return f"{row['name']},{row['category']},{row['price']}\n"

    def format_footer(self, total: int) -> str:
        """Return a row count summary."""
        return f"Total rows: {total}\n"


# ---------------------------------------------------------------------------
# Concrete generator 2: HTML
# ---------------------------------------------------------------------------

class HTMLReportGenerator(ReportGenerator):
    """Generates an HTML ``<table>`` report."""

    def format_header(self, title: str) -> str:
        """Return the opening ``<table>`` tag with column headings."""
        return (
            "<table>"
            "<tr><th>Name</th><th>Category</th><th>Price</th></tr>\n"
        )

    def format_row(self, row: dict) -> str:
        """Return one HTML table row."""
        return (
            f"<tr>"
            f"<td>{row['name']}</td>"
            f"<td>{row['category']}</td>"
            f"<td>{row['price']}</td>"
            f"</tr>\n"
        )

    def format_footer(self, total: int) -> str:
        """Return the closing table tag with a row count paragraph."""
        return f"</table><p>Total: {total} items</p>"


# ---------------------------------------------------------------------------
# Concrete generator 3: Markdown
# ---------------------------------------------------------------------------

class MarkdownReportGenerator(ReportGenerator):
    """Generates a Markdown pipe-table report."""

    def format_header(self, title: str) -> str:
        """Return the Markdown table header with a separator row."""
        return "| Name | Category | Price |\n|------|----------|-------|\n"

    def format_row(self, row: dict) -> str:
        """Return one Markdown table row."""
        return f"| {row['name']} | {row['category']} | {row['price']} |\n"

    def format_footer(self, total: int) -> str:
        """Return the total count as a Markdown italic paragraph."""
        return f"\n*Total: {total} items*"
