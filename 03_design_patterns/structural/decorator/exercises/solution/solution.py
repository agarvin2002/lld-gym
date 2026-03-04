"""
Decorator Pattern - Exercise Solution: Text Formatter System
"""

from __future__ import annotations
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component Interface
# ---------------------------------------------------------------------------

class TextFormatter(ABC):
    @abstractmethod
    def format(self, text: str) -> str:
        ...


# ---------------------------------------------------------------------------
# Leaf: BaseFormatter
# ---------------------------------------------------------------------------

class BaseFormatter(TextFormatter):
    """Leaf node — returns text unchanged."""

    def format(self, text: str) -> str:
        return text


# ---------------------------------------------------------------------------
# Base Decorator
# ---------------------------------------------------------------------------

class TextFormatterDecorator(TextFormatter):
    """Holds a reference to a wrapped formatter and delegates by default."""

    def __init__(self, wrapped: TextFormatter) -> None:
        self._wrapped = wrapped

    def format(self, text: str) -> str:
        return self._wrapped.format(text)


# ---------------------------------------------------------------------------
# Concrete Decorators
# ---------------------------------------------------------------------------

class BoldFormatter(TextFormatterDecorator):
    """Wraps the inner result in **double asterisks**."""

    def format(self, text: str) -> str:
        inner = self._wrapped.format(text)
        return f"**{inner}**"


class ItalicFormatter(TextFormatterDecorator):
    """Wraps the inner result in *single asterisks*."""

    def format(self, text: str) -> str:
        inner = self._wrapped.format(text)
        return f"*{inner}*"


class UpperCaseFormatter(TextFormatterDecorator):
    """Uppercases the inner result."""

    def format(self, text: str) -> str:
        return self._wrapped.format(text).upper()


class TrimFormatter(TextFormatterDecorator):
    """Strips leading/trailing whitespace from the inner result."""

    def format(self, text: str) -> str:
        return self._wrapped.format(text).strip()


class PrefixFormatter(TextFormatterDecorator):
    """Prepends a fixed prefix to the inner result."""

    def __init__(self, wrapped: TextFormatter, prefix: str) -> None:
        super().__init__(wrapped)
        self._prefix = prefix

    def format(self, text: str) -> str:
        return self._prefix + self._wrapped.format(text)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Text Formatter Decorator Demo ===\n")

    cases = [
        ("Base only",             BaseFormatter()),
        ("Bold",                   BoldFormatter(BaseFormatter())),
        ("Italic",                 ItalicFormatter(BaseFormatter())),
        ("UpperCase",              UpperCaseFormatter(BaseFormatter())),
        ("Bold + Italic",          BoldFormatter(ItalicFormatter(BaseFormatter()))),
        ("Upper + Bold",           UpperCaseFormatter(BoldFormatter(BaseFormatter()))),
        ("Bold + Italic + Upper",  BoldFormatter(ItalicFormatter(UpperCaseFormatter(BaseFormatter())))),
        ("Prefix + Bold",          PrefixFormatter(BoldFormatter(BaseFormatter()), prefix="TIP: ")),
        ("Trim + Bold",            TrimFormatter(BoldFormatter(BaseFormatter()))),
    ]

    for label, fmt in cases:
        text = "  hello world  "
        result = fmt.format(text)
        print(f"  {label:30s}: '{result}'")
