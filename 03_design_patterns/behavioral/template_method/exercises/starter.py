"""
Exercise: Report Generator (Template Method Pattern)
Fill in the TODOs. Run: /tmp/lld_venv/bin/pytest exercises/tests.py -v
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


# ---------------------------------------------------------------------------
# Concrete generator 1: CSV
# ---------------------------------------------------------------------------

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
        pass

    def format_row(self, row: dict) -> str:
        # TODO: return f"| {row['name']} | {row['category']} | {row['price']} |\n"
        pass

    def format_footer(self, total: int) -> str:
        # TODO: return f"\n*Total: {total} items*"
        pass
