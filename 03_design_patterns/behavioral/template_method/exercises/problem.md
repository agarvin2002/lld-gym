# Exercise: Report Generator (Template Method Pattern)

## Problem

Build a report generation system that can output the same product data in three different formats (CSV, HTML, Markdown). The iteration logic (looping over rows, counting total) must live only in the base class — subclasses supply only the formatting steps.

## What to build

### `ReportGenerator` (ABC)

Template method:
```
generate(data: list[dict]) -> str
```
Internal sequence:
1. Call `format_header(title: str) -> str` with `title="Products"`
2. For each row in `data`, call `format_row(row: dict) -> str`
3. Call `format_footer(total: int) -> str` with `total = len(data)`
4. Join all parts and return the complete string

Abstract hooks (`@abstractmethod`):
- `format_header(self, title: str) -> str`
- `format_row(self, row: dict) -> str`
- `format_footer(self, total: int) -> str`

### `CSVReportGenerator(ReportGenerator)`
| Hook | Return value |
|------|-------------|
| `format_header(title)` | `"Name,Category,Price\n"` |
| `format_row(row)` | `f"{row['name']},{row['category']},{row['price']}\n"` |
| `format_footer(total)` | `f"Total rows: {total}\n"` |

### `HTMLReportGenerator(ReportGenerator)`
| Hook | Return value |
|------|-------------|
| `format_header(title)` | `"<table><tr><th>Name</th><th>Category</th><th>Price</th></tr>\n"` |
| `format_row(row)` | `f"<tr><td>{row['name']}</td><td>{row['category']}</td><td>{row['price']}</td></tr>\n"` |
| `format_footer(total)` | `f"</table><p>Total: {total} items</p>"` |

### `MarkdownReportGenerator(ReportGenerator)`
| Hook | Return value |
|------|-------------|
| `format_header(title)` | `"| Name | Category | Price |\n|------|----------|-------|\n"` |
| `format_row(row)` | `f"| {row['name']} | {row['category']} | {row['price']} |\n"` |
| `format_footer(total)` | `f"\n*Total: {total} items*"` |

## Constraints
- The `generate()` method lives only in `ReportGenerator` — do not duplicate it in subclasses
- Row dicts always have keys: `name`, `category`, `price`
- `generate([])` (empty list) is valid and returns `format_header("Products") + format_footer(0)`

## Run tests
```bash
/tmp/lld_venv/bin/pytest exercises/tests.py -v
```
