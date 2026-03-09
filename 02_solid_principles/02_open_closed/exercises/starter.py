"""
WHAT YOU'RE BUILDING
====================
A report exporter that supports multiple output formats (CSV, JSON, XML).
The key rule: adding a new format must NOT require editing ReportExporter.

Each format is a separate strategy class. ReportExporter is wired to
whichever strategy it receives — it never needs to know about format details.

The tests also check that you can add a brand-new MarkdownExporter without
touching any existing code. That's OCP in action.
"""
import json
from abc import ABC, abstractmethod


class ExportStrategy(ABC):
    """
    Abstract base for all export formats.
    Add new formats by subclassing — never modify ReportExporter.
    """

    @abstractmethod
    def export(self, data: list[dict]) -> str:
        """Convert list of dicts to a format-specific string."""
        ...


class CSVExporter(ExportStrategy):
    """Exports data as CSV. First row is the header (dict keys)."""

    def export(self, data: list[dict]) -> str:
        # TODO: Return a CSV string
        # Row 1: comma-joined keys from the first dict  → "name,price,qty\n"
        # Rows 2+: comma-joined string values for each dict → "Widget A,25.0,2\n"
        # HINT: "\n".join([header] + [",".join(str(v) for v in row.values()) for row in data])
        pass


class JSONExporter(ExportStrategy):
    """Exports data as an indented JSON string."""

    def export(self, data: list[dict]) -> str:
        # TODO: Return json.dumps(data, indent=2)
        pass


class XMLExporter(ExportStrategy):
    """Exports data as simple XML."""

    def export(self, data: list[dict]) -> str:
        # TODO: Wrap each dict as <record>...</record> with each key as a child tag
        # Wrap everything in <records>...</records>
        # HINT: build a list of strings and join them.
        #   Each dict becomes: "<record><name>Widget A</name><price>25.0</price></record>"
        pass


class ReportExporter:
    """
    Exports reports using an injected ExportStrategy.
    Never modified when new formats are added.
    """

    def __init__(self, strategy: ExportStrategy) -> None:
        # TODO: Store strategy as self._strategy
        pass

    def set_strategy(self, strategy: ExportStrategy) -> None:
        # TODO: Replace self._strategy with the new strategy
        pass

    def export(self, data: list[dict]) -> str:
        # TODO: Delegate to self._strategy.export(data) and return the result
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/02_open_closed/exercises/tests.py -v
#
# Run all SOLID exercises at once:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/ -v
# =============================================================================
