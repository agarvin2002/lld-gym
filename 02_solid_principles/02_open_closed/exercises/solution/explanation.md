# Explanation: OCP Report Exporter

## The Violation (before)
Without OCP:
```python
class ReportExporter:
    def export(self, data, format):
        if format == "csv":   ...  # change here for csv bugs
        elif format == "json": ...  # change here for json bugs
        elif format == "xml":  ...  # change here for xml bugs
        # Adding markdown requires modifying this class!
```
Every new format is a modification. Every bug fix to CSV risks breaking JSON.

## The Fix (OCP)
```python
class ReportExporter:
    def export(self, data):
        return self._strategy.export(data)  # never changes
```
`ReportExporter` is **closed for modification** — it never changes.
New formats are **open for extension** — just add a new class.

## Why Strategy Pattern Achieves OCP
The Strategy pattern encapsulates each algorithm (format) in its own class. `ReportExporter` depends only on the `ExportStrategy` abstraction, not any concrete format. This is the essence of OCP.

## Real-World Uses
- Django REST Framework: serializers (JSON, XML, YAML) are strategy-like
- Python's `logging.Handler` subclasses (FileHandler, SMTPHandler, etc.)
- `pathlib.Path` can be extended with custom path types

## When OCP Is Overkill
Don't apply OCP from the start. When you have **one** format, a simple function is fine. OCP pays off when you have **two or more** similar but different behaviors, and you expect more in the future.
