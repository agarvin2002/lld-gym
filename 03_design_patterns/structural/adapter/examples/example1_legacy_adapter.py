"""
Adapter Pattern - Example 1: Legacy Printer Adapter

Scenario:
    A legacy printing system has LegacyPrinter with old_print(text, copies).
    The new system expects all printers to implement the Printer interface
    with print(document: Document). We cannot modify LegacyPrinter.

Solution:
    PrinterAdapter wraps LegacyPrinter and translates the new interface
    calls into old ones.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Domain model
# ---------------------------------------------------------------------------

@dataclass
class Document:
    title: str
    content: str
    copies: int = 1

    def __str__(self) -> str:
        return f"Document(title='{self.title}', copies={self.copies})"


# ---------------------------------------------------------------------------
# Target Interface (what the new system expects)
# ---------------------------------------------------------------------------

class Printer(ABC):
    """Target interface used by the new printing system."""

    @abstractmethod
    def print(self, document: Document) -> None:
        """Print the given document."""
        ...

    @abstractmethod
    def get_status(self) -> str:
        """Return a human-readable status string."""
        ...


# ---------------------------------------------------------------------------
# Adaptee (legacy code we cannot modify)
# ---------------------------------------------------------------------------

class LegacyPrinter:
    """
    Old printer class from a legacy library.
    Has a different interface from what the new system expects.
    We CANNOT modify this class.
    """

    def __init__(self, model_name: str) -> None:
        self._model = model_name
        self._is_online = True

    def old_print(self, text: str, copies: int) -> None:
        """Legacy print method — takes raw text and number of copies."""
        if not self._is_online:
            raise RuntimeError(f"{self._model} is offline")
        for i in range(1, copies + 1):
            print(f"  [{self._model}] Printing copy {i}/{copies}:")
            # Simulate printing first 80 chars of content
            preview = text[:80] + ("..." if len(text) > 80 else "")
            print(f"    {preview}")

    def query_status(self) -> dict:
        """Legacy status method — returns a raw dict."""
        return {
            "model": self._model,
            "online": self._is_online,
            "ink_level": 75,
        }

    def set_offline(self) -> None:
        self._is_online = False


# ---------------------------------------------------------------------------
# Adapter (bridges LegacyPrinter to Printer interface)
# ---------------------------------------------------------------------------

class PrinterAdapter(Printer):
    """
    Adapts LegacyPrinter to the new Printer interface.

    The adapter:
    1. Takes a Document and extracts what LegacyPrinter needs (text + copies).
    2. Translates the status dict into a human-readable string.
    """

    def __init__(self, legacy_printer: LegacyPrinter) -> None:
        self._legacy = legacy_printer

    def print(self, document: Document) -> None:
        """Convert Document to args legacy printer understands."""
        full_text = f"Title: {document.title}\n\n{document.content}"
        self._legacy.old_print(text=full_text, copies=document.copies)

    def get_status(self) -> str:
        """Convert legacy dict status to a clean string."""
        raw = self._legacy.query_status()
        state = "ONLINE" if raw["online"] else "OFFLINE"
        return (
            f"Printer '{raw['model']}' | Status: {state} | "
            f"Ink: {raw['ink_level']}%"
        )


# ---------------------------------------------------------------------------
# New Printer implementation (no adapter needed — native implementation)
# ---------------------------------------------------------------------------

class ModernLaserPrinter(Printer):
    """A new-style printer that natively implements the Printer interface."""

    def __init__(self, model: str) -> None:
        self._model = model

    def print(self, document: Document) -> None:
        for i in range(1, document.copies + 1):
            print(f"  [{self._model}] Copy {i}/{document.copies} of '{document.title}'")

    def get_status(self) -> str:
        return f"Printer '{self._model}' | Status: ONLINE | Ink: 100%"


# ---------------------------------------------------------------------------
# Client code — works with any Printer, unaware of legacy vs modern
# ---------------------------------------------------------------------------

class PrintingService:
    """High-level service that prints documents through any Printer."""

    def __init__(self, printer: Printer) -> None:
        self._printer = printer

    def print_document(self, document: Document) -> None:
        print(f"\nPrintingService: Sending {document} to printer...")
        print(f"  Status: {self._printer.get_status()}")
        self._printer.print(document)
        print("  Done.")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("ADAPTER PATTERN - Legacy Printer Demo")
    print("=" * 60)

    # Create documents
    report = Document(
        title="Q4 Financial Report",
        content="Revenue grew 23% YoY. EBITDA margin improved to 18%.",
        copies=2,
    )
    memo = Document(
        title="Office Memo",
        content="Please remember to clean the kitchen after use. Thank you.",
        copies=1,
    )

    # --- Modern printer (native interface, no adapter needed) ---
    print("\n--- Modern Laser Printer (native interface) ---")
    modern = ModernLaserPrinter("HP LaserJet Pro")
    service = PrintingService(modern)
    service.print_document(report)

    # --- Legacy printer via adapter ---
    print("\n--- Legacy Dot-Matrix via Adapter ---")
    legacy = LegacyPrinter("Epson DX-500")
    adapted = PrinterAdapter(legacy)

    # Client code is identical — it doesn't know it's talking to a legacy printer
    service2 = PrintingService(adapted)
    service2.print_document(report)
    service2.print_document(memo)

    # --- Show that status translation also works ---
    print("\n--- Status Comparison ---")
    print(f"Modern:  {modern.get_status()}")
    print(f"Adapted: {adapted.get_status()}")

    # --- Show offline behaviour passes through ---
    print("\n--- Testing offline legacy printer ---")
    legacy.set_offline()
    print(f"After set_offline(): {adapted.get_status()}")
    try:
        adapted.print(memo)
    except RuntimeError as e:
        print(f"  Caught expected error: {e}")

    print("\nDone.")
