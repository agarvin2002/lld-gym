"""
Tests for the Decorator exercise — Text Formatter System.

Run with:
    python tests.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    BaseFormatter,
    BoldFormatter,
    ItalicFormatter,
    UpperCaseFormatter,
    TrimFormatter,
    PrefixFormatter,
    TextFormatter,
)


class TestBaseFormatter(unittest.TestCase):
    def setUp(self):
        self.fmt = BaseFormatter()

    def test_returns_text_unchanged(self):
        self.assertEqual(self.fmt.format("hello"), "hello")

    def test_empty_string(self):
        self.assertEqual(self.fmt.format(""), "")

    def test_whitespace_preserved(self):
        self.assertEqual(self.fmt.format("  hi  "), "  hi  ")

    def test_is_text_formatter(self):
        self.assertIsInstance(self.fmt, TextFormatter)


class TestBoldFormatter(unittest.TestCase):
    def test_wraps_base_in_double_asterisks(self):
        fmt = BoldFormatter(BaseFormatter())
        self.assertEqual(fmt.format("hello"), "**hello**")

    def test_empty_string(self):
        fmt = BoldFormatter(BaseFormatter())
        self.assertEqual(fmt.format(""), "****")

    def test_is_text_formatter(self):
        self.assertIsInstance(BoldFormatter(BaseFormatter()), TextFormatter)


class TestItalicFormatter(unittest.TestCase):
    def test_wraps_base_in_single_asterisks(self):
        fmt = ItalicFormatter(BaseFormatter())
        self.assertEqual(fmt.format("hello"), "*hello*")

    def test_empty_string(self):
        fmt = ItalicFormatter(BaseFormatter())
        self.assertEqual(fmt.format(""), "**")


class TestUpperCaseFormatter(unittest.TestCase):
    def test_uppercases_result(self):
        fmt = UpperCaseFormatter(BaseFormatter())
        self.assertEqual(fmt.format("hello world"), "HELLO WORLD")

    def test_already_uppercase(self):
        fmt = UpperCaseFormatter(BaseFormatter())
        self.assertEqual(fmt.format("HELLO"), "HELLO")

    def test_mixed_case(self):
        fmt = UpperCaseFormatter(BaseFormatter())
        self.assertEqual(fmt.format("hElLo"), "HELLO")


class TestTrimFormatter(unittest.TestCase):
    def test_strips_whitespace(self):
        fmt = TrimFormatter(BaseFormatter())
        self.assertEqual(fmt.format("  hello  "), "hello")

    def test_no_whitespace_unchanged(self):
        fmt = TrimFormatter(BaseFormatter())
        self.assertEqual(fmt.format("hello"), "hello")

    def test_only_whitespace(self):
        fmt = TrimFormatter(BaseFormatter())
        self.assertEqual(fmt.format("   "), "")


class TestPrefixFormatter(unittest.TestCase):
    def test_prepends_prefix(self):
        fmt = PrefixFormatter(BaseFormatter(), prefix="NOTE: ")
        self.assertEqual(fmt.format("read this"), "NOTE: read this")

    def test_empty_prefix(self):
        fmt = PrefixFormatter(BaseFormatter(), prefix="")
        self.assertEqual(fmt.format("hello"), "hello")

    def test_prefix_applied_after_inner(self):
        # Inner bold runs first, then prefix is prepended
        fmt = PrefixFormatter(BoldFormatter(BaseFormatter()), prefix="TIP: ")
        self.assertEqual(fmt.format("important"), "TIP: **important**")


class TestComposition(unittest.TestCase):
    def test_bold_italic(self):
        # Bold wraps italic: italic runs first → *hello*, then bold wraps → ***hello***
        fmt = BoldFormatter(ItalicFormatter(BaseFormatter()))
        self.assertEqual(fmt.format("hello"), "***hello***")

    def test_italic_bold(self):
        # Italic wraps bold: bold runs first → **hello**, then italic wraps → ***hello***
        fmt = ItalicFormatter(BoldFormatter(BaseFormatter()))
        self.assertEqual(fmt.format("hello"), "***hello***")

    def test_upper_bold(self):
        # Bold first → **hello**, then upper → **HELLO**
        fmt = UpperCaseFormatter(BoldFormatter(BaseFormatter()))
        self.assertEqual(fmt.format("hello"), "**HELLO**")

    def test_bold_upper(self):
        # Upper first → HELLO, then bold → **HELLO**
        fmt = BoldFormatter(UpperCaseFormatter(BaseFormatter()))
        self.assertEqual(fmt.format("hello"), "**HELLO**")

    def test_bold_italic_upper(self):
        # Upper → HELLO, Italic → *HELLO*, Bold → ***HELLO***
        fmt = BoldFormatter(ItalicFormatter(UpperCaseFormatter(BaseFormatter())))
        self.assertEqual(fmt.format("hello"), "***HELLO***")

    def test_trim_bold(self):
        # Bold first → **  hello  **, then trim → **  hello  **
        # Wait — bold wraps the text as-is, then trim strips
        fmt = TrimFormatter(BoldFormatter(BaseFormatter()))
        self.assertEqual(fmt.format("  hello  "), "**  hello  **")

    def test_bold_trim(self):
        # Trim first → hello, then bold → **hello**
        fmt = BoldFormatter(TrimFormatter(BaseFormatter()))
        self.assertEqual(fmt.format("  hello  "), "**hello**")

    def test_prefix_italic_upper(self):
        # Upper → WORLD, Italic → *WORLD*, Prefix → "ALERT: *WORLD*"
        fmt = PrefixFormatter(
            ItalicFormatter(UpperCaseFormatter(BaseFormatter())),
            prefix="ALERT: ",
        )
        self.assertEqual(fmt.format("world"), "ALERT: *WORLD*")

    def test_deep_nesting(self):
        # 4 levels deep: trim → bold → italic → upper
        fmt = TrimFormatter(
            BoldFormatter(
                ItalicFormatter(
                    UpperCaseFormatter(BaseFormatter())
                )
            )
        )
        self.assertEqual(fmt.format("  hello  "), "***HELLO***")

    def test_each_formatter_implements_interface(self):
        formatters = [
            BaseFormatter(),
            BoldFormatter(BaseFormatter()),
            ItalicFormatter(BaseFormatter()),
            UpperCaseFormatter(BaseFormatter()),
            TrimFormatter(BaseFormatter()),
            PrefixFormatter(BaseFormatter(), prefix="X"),
        ]
        for fmt in formatters:
            self.assertIsInstance(fmt, TextFormatter)
            self.assertIsInstance(fmt.format("test"), str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
