"""
ISP Example 1: Fat Interface Violation

A Printer ABC forces ALL printer types to implement ALL functions —
even ones they don't support.

Real-world use: This pattern appears in media player frameworks where a
single Player interface forces simple audio players to stub out video,
download, and subtitle methods they'll never use.
"""
from abc import ABC, abstractmethod


class FatPrinter(ABC):
    """
    One big interface for all printer capabilities.
    PROBLEM: BasicPrinter is forced to implement fax/scan/staple.
    """

    @abstractmethod
    def print_doc(self, document: str) -> None: ...

    @abstractmethod
    def scan_doc(self) -> str: ...

    @abstractmethod
    def fax_doc(self, document: str, fax_number: str) -> bool: ...

    @abstractmethod
    def copy_doc(self, copies: int) -> None: ...

    @abstractmethod
    def staple_doc(self) -> None: ...


class BasicPrinterViolation(FatPrinter):
    """
    A basic printer that only prints.
    But it's FORCED to implement scan, fax, copy, staple — ISP violation!
    """

    def print_doc(self, document: str) -> None:
        print(f"Printing: {document}")

    def scan_doc(self) -> str:
        raise NotImplementedError("BasicPrinter cannot scan")  # ❌ surprise!

    def fax_doc(self, document: str, fax_number: str) -> bool:
        raise NotImplementedError("BasicPrinter cannot fax")  # ❌ surprise!

    def copy_doc(self, copies: int) -> None:
        raise NotImplementedError("BasicPrinter cannot copy")  # ❌ surprise!

    def staple_doc(self) -> None:
        raise NotImplementedError("BasicPrinter cannot staple")  # ❌ surprise!


if __name__ == "__main__":
    printer = BasicPrinterViolation()
    printer.print_doc("Hello World")   # works

    print("\nProblems with fat interface:")
    try:
        printer.scan_doc()
    except NotImplementedError as e:
        print(f"  ❌ scan_doc: {e}")

    try:
        printer.fax_doc("doc", "555-1234")
    except NotImplementedError as e:
        print(f"  ❌ fax_doc: {e}")

    print("\nClients using FatPrinter can't trust the interface.")
    print("They need to check if methods actually work — defeats the purpose.")
