# Exercise: Temperature Converter

## What You'll Build

A `Temperature` class that stores temperature internally in Celsius and exposes it in all three units (Celsius, Fahrenheit, Kelvin) via properties.

## Requirements

- `Temperature(celsius: float)` — constructor takes Celsius value
- `celsius` — readable **and writable** property; setter validates value
- `fahrenheit` — read-only property, computed from Celsius
- `kelvin` — read-only property, computed from Celsius
- Setting `celsius` below **-273.15** (absolute zero) raises `ValueError`
- `__repr__` shows all three values
- `__eq__` compares by Celsius value

## Conversion Formulas

```
Fahrenheit = Celsius × 9/5 + 32
Kelvin     = Celsius + 273.15
```

## Constraints

- Internal storage must use a private attribute (`_celsius`)
- `fahrenheit` and `kelvin` must be **computed**, not stored
- Validation must happen in the setter, not `__init__` separately

## Hints

1. Call `self.celsius = celsius` from `__init__` — this triggers the setter and validation automatically
2. `@property` for getters, `@celsius.setter` for the setter
3. `__eq__` should handle the case where `other` is not a `Temperature` instance

## What You'll Practice

- `@property` and `@setter` syntax
- Private attribute convention (`_celsius`)
- Preventing invalid state via validation
- Computing derived values instead of storing them
- `__repr__` and `__eq__` dunder methods
