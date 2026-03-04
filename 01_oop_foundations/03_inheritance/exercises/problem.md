# Exercise: Employee Compensation Hierarchy

## What You'll Build

An employee class hierarchy where each role has a different compensation structure.

## Class Hierarchy

```
Employee (ABC)
├── Manager
│   └── Director
└── Engineer
```

## Requirements

### `Employee` (Abstract Base Class)
- Attributes: `name: str`, `employee_id: str`, `base_salary: float`
- Abstract method: `get_total_compensation() -> float`
- Abstract method: `get_role() -> str`
- Concrete method: `__repr__` showing name, id, role, total comp

### `Manager(Employee)`
- Additional attribute: `team_size: int`
- `get_role()` → `"Manager"`
- `get_total_compensation()` → `base_salary * 1.20` (20% bonus)

### `Engineer(Employee)`
- Additional attribute: `tech_stack: list[str]`
- `get_role()` → `"Engineer"`
- `get_total_compensation()` → `base_salary * 1.10` (10% bonus)

### `Director(Manager)`
- Additional attribute: `department: str`
- `get_role()` → `"Director"`
- `get_total_compensation()` → `base_salary * 1.40` (40% bonus)

## Constraints
- All subclasses must call `super().__init__()` properly
- `Employee` must not be instantiatable directly (use ABC)
- `get_total_compensation()` should return rounded to 2 decimal places

## Hints
1. `from abc import ABC, abstractmethod`
2. `Director` inherits from `Manager` — remember to call `super().__init__(name, employee_id, base_salary, team_size)` from Director
3. `isinstance(director, Manager)` should be `True` because Director IS-A Manager

## What You'll Practice
- Abstract base classes
- `super().__init__()` chaining through multiple levels
- Method overriding
- `isinstance()` / `issubclass()` behavior
