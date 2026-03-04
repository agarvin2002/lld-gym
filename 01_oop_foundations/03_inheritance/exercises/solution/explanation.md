# Explanation: Employee Hierarchy

## Key Design Decisions

### 1. ABC prevents accidental instantiation
```python
class Employee(ABC):
    @abstractmethod
    def get_total_compensation(self) -> float: ...
```
Without ABC, someone could instantiate `Employee("Alice", "E001", 80000)` and call `.get_total_compensation()` — which would fail at runtime. ABC catches this at instantiation time, which is earlier and clearer.

### 2. `super().__init__()` chain
```
Director.__init__()
  → Manager.__init__()  (via super())
    → Employee.__init__()  (via super())
```
Each class passes its relevant args up. Director doesn't re-set `name`, `employee_id`, `base_salary` — it trusts the chain. This is **cooperative multiple inheritance** working correctly.

### 3. Director overrides `get_total_compensation()` completely
Director doesn't call `super().get_total_compensation()`. It defines its own logic (40% bonus). The Manager's 20% logic is irrelevant to Director — they just share the `team_size` attribute.

### 4. `isinstance()` behavior
```python
director = Director("Dave", "D001", 150_000, 20, "Engineering")
isinstance(director, Director)  # True
isinstance(director, Manager)   # True  ← Director IS-A Manager
isinstance(director, Employee)  # True  ← transitively
isinstance(director, Engineer)  # False ← not in that branch
```
This is the MRO at work. Python checks the full ancestor chain.

## The "is-a" Relationship
Director IS-A Manager IS-A Employee — this means:
- Anywhere code accepts an `Employee`, a `Director` works
- Anywhere code accepts a `Manager`, a `Director` works
- This enables **polymorphism**: a list of `Employee` objects can contain any mix

## What About Deep Hierarchies?
This example has 3 levels (Employee → Manager → Director). That's the practical maximum. Deeper hierarchies become hard to trace. If you find yourself going 4+ levels, consider:
- Are some classes just configuration? Use composition instead.
- Is the hierarchy modeling something real, or is it code reuse abuse?
