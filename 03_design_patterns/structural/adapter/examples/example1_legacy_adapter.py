"""
Adapter Pattern - Example 1: Legacy Printer Adapter

Scenario:
    A legacy printing system has LegacyPrinter with old_print(text, copies).
    The new system expects all printers to implement the Printer interface
    with print(document: Document). We cannot modify LegacyPrinter.

Solution:
    PrinterAdapter wraps LegacyPrinter and translates the new interface
    calls into old ones.

Real-world use: Enterprise software that wraps old ERP printer APIs behind
a clean interface so new services don't depend on legacy method signatures.
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
    def print(self, document: Document) -> None: ...

    @abstractmethod
    def get_status(self) -> str: ...


# ---------------------------------------------------------------------------
# Adaptee (legacy code we cannot modify)
# ---------------------------------------------------------------------------

class LegacyPrinter:
    """Old printer class from a legacy library. We CANNOT modify this."""

    def __init__(self, model_name: str) -> None:
        self._model = model_name
        self._is_online = True

    def old_print(self, text: str, copies: int) -> None:
        if not self._is_online:
            raise RuntimeError(f"{self._model} is offline")
        for i in range(1, copies + 1):
            preview = text[:80] + ("..." if len(text) > 80 else "")
            print(f"  [{self._model}] Copy {i}/{copies}: {preview}")

    def query_status(self) -> dict:
        return {"model": self._model, "online": self._is_online, "ink_level": 75}

    def set_offline(self) -> None:
        self._is_online = False


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

class PrinterAdapter(Printer):
    """Adapts LegacyPrinter to the new Printer interface via composition."""

    def __init__(self, legacy_printer: LegacyPrinter) -> None:
        self._legacy = legacy_printer  # hold a reference — do not inherit

    def print(self, document: Document) -> None:
        full_text = f"Title: {document.title}\n\n{document.content}"
        self._legacy.old_print(text=full_text, copies=document.copies)

    def get_status(self) -> str:
        raw = self._legacy.query_status()
        state = "ONLINE" if raw["online"] else "OFFLINE"
        return f"Printer '{raw['model']}' | {state} | Ink: {raw['ink_level']}%"


# ---------------------------------------------------------------------------
# Modern printer (native interface — no adapter needed)
# ---------------------------------------------------------------------------

class ModernLaserPrinter(Printer):
    def __init__(self, model: str) -> None:
        self._model = model

    def print(self, document: Document) -> None:
        for i in range(1, document.copies + 1):
            print(f"  [{self._model}] Copy {i}/{document.copies} of '{document.title}'")

    def get_status(self) -> str:
        return f"Printer '{self._model}' | ONLINE | Ink: 100%"


# ---------------------------------------------------------------------------
# Client code — works with any Printer, unaware of legacy vs modern
# ---------------------------------------------------------------------------

class PrintingService:
    def __init__(self, printer: Printer) -> None:
        self._printer = printer

    def print_document(self, document: Document) -> None:
        print(f"\nSending {document} to printer...")
        print(f"  Status: {self._printer.get_status()}")
        self._printer.print(document)
        print("  Done.")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    report = Document("Q4 Report", "Revenue grew 23% YoY.", copies=2)
    memo   = Document("Office Memo", "Please clean the kitchen.", copies=1)

    print("--- Modern Laser Printer (native interface) ---")
    service = PrintingService(ModernLaserPrinter("HP LaserJet Pro"))
    service.print_document(report)

    print("\n--- Legacy Dot-Matrix via Adapter ---")
    legacy  = LegacyPrinter("Epson DX-500")
    service2 = PrintingService(PrinterAdapter(legacy))
    service2.print_document(report)
    service2.print_document(memo)

    print("\n--- Offline behaviour ---")
    legacy.set_offline()
    adapted = PrinterAdapter(legacy)
    print(f"Status: {adapted.get_status()}")
    try:
        adapted.print(memo)
    except RuntimeError as e:
        print(f"Caught expected error: {e}")
