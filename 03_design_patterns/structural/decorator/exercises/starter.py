"""
Decorator Pattern - Exercise Starter
======================================
Task: Implement composable text formatters using the Decorator pattern.

Instructions:
1. Read problem.md for the full requirements.
2. Implement the classes below.
3. Run tests.py to verify your solution.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component Interface — do not modify
# ---------------------------------------------------------------------------

class TextFormatter(ABC):
    """Abstract text formatting interface."""

    @abstractmethod
    def format(self, text: str) -> str:
        """Return a formatted version of the input text."""
        ...


# ---------------------------------------------------------------------------
# TODO: Implement BaseFormatter (leaf — no wrapping, returns text as-is)
# ---------------------------------------------------------------------------

class BaseFormatter(TextFormatter):
    # TODO: implement format()
    pass


# ---------------------------------------------------------------------------
# TODO: Implement base decorator class
# ---------------------------------------------------------------------------

class TextFormatterDecorator(TextFormatter):
    """
    Base decorator.
    - Stores a reference to a wrapped TextFormatter.
    - Delegates format() to the wrapped instance by default.
    - Concrete decorators override format() to add behavior.
    """

    def __init__(self, wrapped: TextFormatter) -> None:
        # TODO: store wrapped
        pass

    def format(self, text: str) -> str:
        # TODO: delegate to self._wrapped
        pass


# ---------------------------------------------------------------------------
# TODO: Implement concrete decorators
# ---------------------------------------------------------------------------

class BoldFormatter(TextFormatterDecorator):
    """Wraps formatted text in **double asterisks**."""

    def format(self, text: str) -> str:
        # TODO: get result from wrapped, then surround with **
        pass


class ItalicFormatter(TextFormatterDecorator):
    """Wraps formatted text in *single asterisks*."""

    def format(self, text: str) -> str:
        # TODO: get result from wrapped, then surround with *
        pass


class UpperCaseFormatter(TextFormatterDecorator):
    """Uppercases the result of the wrapped formatter."""

    def format(self, text: str) -> str:
        # TODO: get result from wrapped, then upper()
        pass


class TrimFormatter(TextFormatterDecorator):
    """Strips leading/trailing whitespace from the wrapped result."""

    def format(self, text: str) -> str:
        # TODO: get result from wrapped, then strip()
        pass


class PrefixFormatter(TextFormatterDecorator):
    """Prepends a fixed prefix string to the wrapped result."""

    def __init__(self, wrapped: TextFormatter, prefix: str) -> None:
        super().__init__(wrapped)
        self._prefix = prefix

    def format(self, text: str) -> str:
        # TODO: get result from wrapped, then prepend self._prefix
        pass


# ---------------------------------------------------------------------------
# Quick manual test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    base = BaseFormatter()
    print("Base:", base.format("hello"))

    bold = BoldFormatter(BaseFormatter())
    print("Bold:", bold.format("hello"))

    italic = ItalicFormatter(BaseFormatter())
    print("Italic:", italic.format("hello"))

    bold_italic = BoldFormatter(ItalicFormatter(BaseFormatter()))
    print("Bold+Italic:", bold_italic.format("hello"))

    upper_bold = UpperCaseFormatter(BoldFormatter(BaseFormatter()))
    print("Upper+Bold:", upper_bold.format("hello"))

    prefix_bold = PrefixFormatter(BoldFormatter(BaseFormatter()), prefix="NOTE: ")
    print("Prefix+Bold:", prefix_bold.format("read this"))

    trim_bold = TrimFormatter(BoldFormatter(BaseFormatter()))
    print("Trim+Bold:", trim_bold.format("  spaced  "))
