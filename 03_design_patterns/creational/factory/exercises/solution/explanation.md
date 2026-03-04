# Explanation: Factory Pattern — Log Formatter Factory

## What the Factory pattern solves

Without a factory, client code looks like:
```python
if format == "plain":
    formatter = PlainFormatter()
elif format == "json":
    formatter = JSONFormatter()
```

This is fragile: adding a new format requires editing every place that creates formatters. With a factory, client code becomes `FormatterFactory.create("json")` — no conditionals, no knowledge of concrete classes.

## Registry vs if/elif

The registry (`_registry: dict[str, type[LogFormatter]]`) extends the Open/Closed Principle to the factory itself. Adding `"xml"` requires only:
```python
FormatterFactory.register("xml", XmlFormatter)
```
No factory code changes. This is especially powerful for plugins or user-configurable formats.

## Class method vs instance method

`register()` and `create()` are class methods because the registry is shared state belonging to the class, not any particular instance. `FormatterFactory()` never needs to be instantiated.

## Case-insensitive lookup

`key = name.lower()` normalizes all keys so `"JSON"`, `"Json"`, and `"json"` all resolve to the same class. This small detail prevents frustrating bugs when format names come from config files or environment variables.

## Logger.set_formatter() at runtime

The strategy-like swap at runtime (`self._formatter = FormatterFactory.create(name)`) lets the logging destination change mid-session without restarting the application. This is a common need in production systems where log verbosity or format changes with deployment environment.

## This pattern vs Abstract Factory

- **Factory (this exercise)**: one product type (`LogFormatter`), many variants
- **Abstract Factory**: multiple related product types created together (e.g., `Button` + `Checkbox` for a UI theme)

Use Factory when you have one configurable product; use Abstract Factory when products must be consistent across a family.
