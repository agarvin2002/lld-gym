"""Tests for Template Method Pattern — Report Generator."""
import sys, os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    ReportGenerator,
    CSVReportGenerator,
    HTMLReportGenerator,
    MarkdownReportGenerator,
)


# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

SAMPLE_DATA = [
    {"name": "Widget",    "category": "Hardware",     "price": 9.99},
    {"name": "Gadget",    "category": "Electronics",  "price": 49.99},
    {"name": "Doodad",    "category": "Accessories",  "price": 4.50},
]

SINGLE_ROW = [{"name": "Widget", "category": "Hardware", "price": 9.99}]


# ---------------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------------

class TestReportGeneratorInterface:
    def test_csv_is_report_generator_subclass(self):
        assert issubclass(CSVReportGenerator, ReportGenerator)

    def test_html_is_report_generator_subclass(self):
        assert issubclass(HTMLReportGenerator, ReportGenerator)

    def test_markdown_is_report_generator_subclass(self):
        assert issubclass(MarkdownReportGenerator, ReportGenerator)

    def test_report_generator_is_abstract(self):
        """Cannot instantiate ReportGenerator directly."""
        with pytest.raises(TypeError):
            ReportGenerator()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# CSVReportGenerator
# ---------------------------------------------------------------------------

class TestCSVReportGenerator:
    def setup_method(self):
        self.gen = CSVReportGenerator()

    def test_output_contains_csv_header(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "Name,Category,Price" in result

    def test_header_on_first_line(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert result.startswith("Name,Category,Price")

    def test_row_has_comma_separated_values(self):
        result = self.gen.generate(SINGLE_ROW)
        assert "Widget,Hardware,9.99" in result

    def test_all_rows_present(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "Widget,Hardware,9.99" in result
        assert "Gadget,Electronics,49.99" in result
        assert "Doodad,Accessories,4.5" in result

    def test_footer_contains_total_count(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "Total rows: 3" in result

    def test_footer_count_correct_for_single_row(self):
        result = self.gen.generate(SINGLE_ROW)
        assert "Total rows: 1" in result

    def test_empty_data_returns_header_and_footer(self):
        result = self.gen.generate([])
        assert "Name,Category,Price" in result
        assert "Total rows: 0" in result

    def test_empty_data_has_no_row_content(self):
        result = self.gen.generate([])
        assert "Widget" not in result

    def test_generate_returns_string(self):
        assert isinstance(self.gen.generate(SAMPLE_DATA), str)

    def test_row_count_in_output(self):
        result = self.gen.generate(SAMPLE_DATA)
        # 3 data rows + header line + footer line = 5 lines minimum
        lines = [l for l in result.splitlines() if l.strip()]
        assert len(lines) >= 4  # header + 3 rows (footer may be on same line)


# ---------------------------------------------------------------------------
# HTMLReportGenerator
# ---------------------------------------------------------------------------

class TestHTMLReportGenerator:
    def setup_method(self):
        self.gen = HTMLReportGenerator()

    def test_output_contains_table_tag(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "<table>" in result

    def test_output_contains_header_th_tags(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "<th>Name</th>" in result
        assert "<th>Category</th>" in result
        assert "<th>Price</th>" in result

    def test_row_wrapped_in_tr_td_tags(self):
        result = self.gen.generate(SINGLE_ROW)
        assert "<tr><td>Widget</td>" in result

    def test_all_rows_present_in_table(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "Widget" in result
        assert "Gadget" in result
        assert "Doodad" in result

    def test_row_contains_category_in_td(self):
        result = self.gen.generate(SINGLE_ROW)
        assert "<td>Hardware</td>" in result

    def test_row_contains_price_in_td(self):
        result = self.gen.generate(SINGLE_ROW)
        assert "<td>9.99</td>" in result

    def test_footer_contains_closing_table_tag(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "</table>" in result

    def test_footer_contains_total_count(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "3" in result
        assert "items" in result

    def test_empty_data_returns_table_tags(self):
        result = self.gen.generate([])
        assert "<table>" in result
        assert "</table>" in result
        assert "0" in result

    def test_table_tag_before_closing_tag(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert result.index("<table>") < result.index("</table>")

    def test_generate_returns_string(self):
        assert isinstance(self.gen.generate(SAMPLE_DATA), str)


# ---------------------------------------------------------------------------
# MarkdownReportGenerator
# ---------------------------------------------------------------------------

class TestMarkdownReportGenerator:
    def setup_method(self):
        self.gen = MarkdownReportGenerator()

    def test_output_contains_pipe_characters(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "|" in result

    def test_header_contains_column_names(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "Name" in result
        assert "Category" in result
        assert "Price" in result

    def test_header_separator_row_present(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "---" in result or "----" in result

    def test_separator_is_second_line(self):
        result = self.gen.generate(SAMPLE_DATA)
        lines = result.splitlines()
        assert "|" in lines[0]   # header row
        assert "---" in lines[1] or "----" in lines[1]  # separator row

    def test_data_row_pipe_format(self):
        result = self.gen.generate(SINGLE_ROW)
        assert "| Widget |" in result

    def test_all_rows_present(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "Widget" in result
        assert "Gadget" in result
        assert "Doodad" in result

    def test_footer_contains_total_with_asterisks(self):
        result = self.gen.generate(SAMPLE_DATA)
        assert "*" in result
        assert "3" in result

    def test_footer_uses_markdown_italic(self):
        result = self.gen.generate(SAMPLE_DATA)
        # Markdown italic: *Total: N items*
        assert "*Total:" in result

    def test_empty_data_returns_header_and_footer(self):
        result = self.gen.generate([])
        assert "|" in result
        assert "0" in result

    def test_generate_returns_string(self):
        assert isinstance(self.gen.generate(SAMPLE_DATA), str)


# ---------------------------------------------------------------------------
# Cross-generator: same data, different formats
# ---------------------------------------------------------------------------

class TestAllGenerators:
    """Verify each generator produces correct output for the same data."""

    def test_all_generators_include_all_product_names(self):
        generators = [
            CSVReportGenerator(),
            HTMLReportGenerator(),
            MarkdownReportGenerator(),
        ]
        for gen in generators:
            result = gen.generate(SAMPLE_DATA)
            for row in SAMPLE_DATA:
                assert str(row["name"]) in result, (
                    f"{gen.__class__.__name__} missing '{row['name']}'"
                )

    def test_all_generators_handle_empty_data(self):
        generators = [
            CSVReportGenerator(),
            HTMLReportGenerator(),
            MarkdownReportGenerator(),
        ]
        for gen in generators:
            result = gen.generate([])
            assert isinstance(result, str)
            assert len(result) > 0, (
                f"{gen.__class__.__name__}.generate([]) returned empty string"
            )

    def test_generate_is_defined_only_in_base_class(self):
        """Verify subclasses do not override generate()."""
        for cls in (CSVReportGenerator, HTMLReportGenerator, MarkdownReportGenerator):
            assert "generate" not in cls.__dict__, (
                f"{cls.__name__} must not override generate() — "
                "only ReportGenerator should define it."
            )

    def test_all_generators_footer_reflects_actual_row_count(self):
        data_5 = [{"name": f"Item{i}", "category": "Cat", "price": i} for i in range(5)]
        generators = [
            (CSVReportGenerator(), "5"),
            (HTMLReportGenerator(), "5"),
            (MarkdownReportGenerator(), "5"),
        ]
        for gen, expected_count in generators:
            result = gen.generate(data_5)
            assert expected_count in result, (
                f"{gen.__class__.__name__} footer should contain '5'"
            )
