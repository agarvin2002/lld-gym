# Explanation: Temperature Class

## Key Design Decisions

### 1. Call the setter from `__init__`
```python
def __init__(self, celsius: float) -> None:
    self.celsius = celsius  # NOT self._celsius = celsius
```
By assigning through the property setter, validation runs automatically during construction. If we wrote `self._celsius = celsius` directly, we'd bypass validation and someone could create `Temperature(-500)` without error.

### 2. Single source of truth
`fahrenheit` and `kelvin` are **computed** from `_celsius`, not stored separately. This means:
- You can't get out of sync (no stale fahrenheit value)
- Changing `celsius` immediately reflects in all units
- Less memory used

### 3. `@property` separates interface from implementation
Callers use `t.celsius` like a regular attribute, but we control:
- What happens on read (return `_celsius`)
- What happens on write (validate, then store)

Later you could change internal storage from Celsius to Kelvin, and no calling code would break.

### 4. `__repr__` for debugging
Always implement `__repr__` — it makes debugging in a REPL or pytest output much more informative than `<Temperature object at 0x...>`.

### 5. `__eq__` returns `NotImplemented` for unknown types
Returning `NotImplemented` (not `False`) tells Python to try the other operand's `__eq__`. This is more correct than returning `False` because `other == self` might still work.

## Real-World Application
This pattern — private storage, computed properties, validation on set — appears in:
- Currency classes (store as smallest unit, display as float)
- Age validators (validate non-negative)
- Coordinates (validate lat/lng ranges)
- File size classes (store bytes, display as KB/MB/GB)
