# Exercise: Extensible Report Exporter

## What You'll Build

A report export system where new export formats can be added **without modifying** the core `ReportExporter` class.

## Requirements

### `ExportStrategy` (ABC)
- `export(data: list[dict]) -> str` — converts data to the format's string representation

### `CSVExporter(ExportStrategy)`
- Returns CSV string (first dict's keys = header row, then values)
- Example: `[{"name": "Alice", "age": 30}]` → `"name,age\nAlice,30\n"`

### `JSONExporter(ExportStrategy)`
- Returns valid JSON string using `json.dumps(data, indent=2)`

### `XMLExporter(ExportStrategy)`
- Returns basic XML string:
```xml
<records>
  <record><name>Alice</name><age>30</age></record>
</records>
```

### `ReportExporter`
- `__init__(strategy: ExportStrategy)`
- `export(data: list[dict]) -> str` — delegates to strategy
- `set_strategy(strategy: ExportStrategy) -> None` — swap strategy at runtime

## The OCP Requirement
Adding `MarkdownExporter` should require:
- Writing a new `MarkdownExporter` class ✅
- **NOT** modifying `ReportExporter` ✅

## Constraints
- `ExportStrategy` must be an ABC
- `ReportExporter` must not contain any format-specific logic (no `if format == "csv"`)

## Hints
1. `",".join(str(v) for v in row.values())` for CSV rows
2. `json.dumps(data, indent=2)` for JSON
3. f-strings work fine for simple XML

## What You'll Practice
- OCP via Strategy pattern
- ABC as interface
- Runtime strategy swapping
