"""
Exercise: Extensible Report Exporter (OCP)

Fill in the TODOs. Run: pytest tests.py -v
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
        """Convert list of dicts to format-specific string."""
        ...


class CSVExporter(ExportStrategy):
    """Exports data as CSV. First row is header (keys), remaining rows are values."""

    def export(self, data: list[dict]) -> str:
        # TODO: build CSV string
        # First row: comma-joined keys of first dict
        # Remaining rows: comma-joined string values for each dict
        # End with newline
        pass


class JSONExporter(ExportStrategy):
    """Exports data as indented JSON string."""

    def export(self, data: list[dict]) -> str:
        # TODO: return json.dumps(data, indent=2)
        pass


class XMLExporter(ExportStrategy):
    """Exports data as simple XML."""

    def export(self, data: list[dict]) -> str:
        # TODO: wrap each dict as <record>...</record> with each key as a tag
        # Wrap all in <records>...</records>
        pass


class ReportExporter:
    """
    Exports reports using an injected ExportStrategy.
    NEVER modified when new formats are added.
    """

    def __init__(self, strategy: ExportStrategy) -> None:
        # TODO: store strategy
        pass

    def set_strategy(self, strategy: ExportStrategy) -> None:
        # TODO: update strategy
        pass

    def export(self, data: list[dict]) -> str:
        # TODO: delegate to strategy.export(data)
        pass
