"""
WHAT YOU'RE BUILDING
====================
You are building a set of composable text formatters using the Decorator pattern.

Start with a BaseFormatter that returns text unchanged.
Then build decorator classes that each add one transformation:
- BoldFormatter      → wraps text in **double asterisks**
- ItalicFormatter    → wraps text in *single asterisks*
- UpperCaseFormatter → converts text to UPPER CASE
- TrimFormatter      → strips leading/trailing whitespace
- PrefixFormatter    → prepends a fixed string

Because every class shares the TextFormatter interface, you can stack them
in any order: BoldFormatter(ItalicFormatter(UpperCaseFormatter(BaseFormatter())))

Your job: implement all six classes below.
TextFormatter (the interface) is already provided — do not modify it.
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
# TODO: Implement BaseFormatter (leaf — no wrapping)
# ---------------------------------------------------------------------------

class BaseFormatter(TextFormatter):
    # TODO: Return text exactly as received — no changes
    pass


# ---------------------------------------------------------------------------
# TODO: Implement the base decorator class
# ---------------------------------------------------------------------------

class TextFormatterDecorator(TextFormatter):
    """
    Base decorator.
    Stores a reference to a wrapped TextFormatter.
    Delegates format() to the wrapped instance.
    Concrete decorators override format() to add their transformation.
    """

    def __init__(self, wrapped: TextFormatter) -> None:
        # TODO: Store the wrapped formatter as self._wrapped
        pass

    def format(self, text: str) -> str:
        # TODO: Call and return self._wrapped.format(text)
        # HINT: This is the default — subclasses call this first, then transform
        pass


# ---------------------------------------------------------------------------
# TODO: Implement concrete decorators
# ---------------------------------------------------------------------------

class BoldFormatter(TextFormatterDecorator):
    """Wraps the result of the inner formatter in **double asterisks**."""

    def format(self, text: str) -> str:
        # TODO: Get the result from the wrapped formatter, then return f"**{result}**"
        pass


class ItalicFormatter(TextFormatterDecorator):
    """Wraps the result of the inner formatter in *single asterisks*."""

    def format(self, text: str) -> str:
        # TODO: Get the result from the wrapped formatter, then return f"*{result}*"
        pass


class UpperCaseFormatter(TextFormatterDecorator):
    """Uppercases the result of the wrapped formatter."""

    def format(self, text: str) -> str:
        # TODO: Get the result from the wrapped formatter, then call .upper() on it
        pass


class TrimFormatter(TextFormatterDecorator):
    """Strips leading/trailing whitespace from the wrapped result."""

    def format(self, text: str) -> str:
        # TODO: Get the result from the wrapped formatter, then call .strip() on it
        pass


class PrefixFormatter(TextFormatterDecorator):
    """Prepends a fixed prefix string to the wrapped result."""

    def __init__(self, wrapped: TextFormatter, prefix: str) -> None:
        super().__init__(wrapped)
        self._prefix = prefix

    def format(self, text: str) -> str:
        # TODO: Get the result from the wrapped formatter, then return self._prefix + result
        # HINT: The prefix was set in __init__ — just prepend it to whatever the inner formatter returns
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


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/structural/decorator/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
