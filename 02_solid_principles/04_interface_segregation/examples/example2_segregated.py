"""
ISP Example 2: Segregated Printer Interfaces

Each capability is its own small interface.
Classes only implement what they actually support.
"""
from abc import ABC, abstractmethod


# ─── Small, Focused Interfaces ────────────────────────────────────

class Printable(ABC):
    @abstractmethod
    def print_doc(self, document: str) -> None: ...


class Scannable(ABC):
    @abstractmethod
    def scan_doc(self) -> str: ...


class Faxable(ABC):
    @abstractmethod
    def fax_doc(self, document: str, fax_number: str) -> bool: ...


class Copyable(ABC):
    @abstractmethod
    def copy_doc(self, copies: int) -> None: ...


# ─── Concrete Implementations ─────────────────────────────────────

class BasicPrinter(Printable):
    """Only prints. No surprise NotImplementedError. ✅"""

    def print_doc(self, document: str) -> None:
        print(f"[BasicPrinter] Printing: {document}")


class ScannerPrinter(Printable, Scannable):
    """Prints and scans. Doesn't pretend to fax. ✅"""

    def print_doc(self, document: str) -> None:
        print(f"[ScannerPrinter] Printing: {document}")

    def scan_doc(self) -> str:
        return "[ScannerPrinter] Scanned document content"


class MultiFunctionPrinter(Printable, Scannable, Faxable, Copyable):
    """Office-grade MFP. Implements everything. ✅"""

    def print_doc(self, document: str) -> None:
        print(f"[MFP] Printing: {document}")

    def scan_doc(self) -> str:
        return "[MFP] Scanned document content"

    def fax_doc(self, document: str, fax_number: str) -> bool:
        print(f"[MFP] Faxing to {fax_number}")
        return True

    def copy_doc(self, copies: int) -> None:
        print(f"[MFP] Copying {copies} times")


# ─── Client Functions — Only Ask For What They Need ───────────────

def do_print(printer: Printable, doc: str) -> None:
    """Only requires Printable — works with ANY printer type."""
    printer.print_doc(doc)


def do_scan(scanner: Scannable) -> str:
    """Only requires Scannable — not all printers."""
    return scanner.scan_doc()


def do_fax(faxer: Faxable, doc: str, number: str) -> bool:
    """Only requires Faxable."""
    return faxer.fax_doc(doc, number)


if __name__ == "__main__":
    basic = BasicPrinter()
    scanner_printer = ScannerPrinter()
    mfp = MultiFunctionPrinter()

    print("=== All can print ===")
    for printer in [basic, scanner_printer, mfp]:
        do_print(printer, "Report.pdf")

    print("\n=== Only scanners can scan ===")
    for scanner in [scanner_printer, mfp]:
        print(do_scan(scanner))

    print("\n=== Only MFP can fax ===")
    do_fax(mfp, "Contract.pdf", "555-9999")

    print("\n=== Segregation in action ===")
    print("BasicPrinter has no scan/fax methods at all — not just NotImplementedError.")
    print("isinstance(basic, Scannable):", isinstance(basic, Scannable))   # False
    print("isinstance(mfp, Scannable):", isinstance(mfp, Scannable))       # True
