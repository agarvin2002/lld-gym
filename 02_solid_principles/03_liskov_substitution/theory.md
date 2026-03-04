# Liskov Substitution Principle (LSP)

## What Is It?
If `S` is a subtype of `T`, objects of type `T` may be replaced with objects of type `S` **without altering the correctness of the program**.

In plain English: **A subclass should be fully usable wherever the base class is used.** No surprises.

## Real-World Analogy
If a recipe says "add 200ml of liquid", you substitute water and it works. You substitute oil and it might work. You substitute concrete and the recipe breaks — even though concrete is technically a "material" like liquid. The substitution violates the recipe's expectations.

## Classic Violation: Rectangle → Square

```python
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height

class Square(Rectangle):
    def set_width(self, w):
        self.width = self.height = w   # "clever" — both sides equal
    def set_height(self, h):
        self.width = self.height = h   # same
```

Now this function breaks:
```python
def test_area(r: Rectangle):
    r.set_width(5)
    r.set_height(4)
    assert r.area() == 20   # passes for Rectangle
                             # FAILS for Square: area = 4*4 = 16!
```

`Square` violates LSP: it can't be substituted for `Rectangle` without breaking correct code.

## Formal Rules
1. **Preconditions cannot be strengthened** — subclass can't demand more from caller
2. **Postconditions cannot be weakened** — subclass can't return less/different than promised
3. **Invariants must be preserved** — what holds for base must hold for subclass
4. **No new exceptions** — subclass can't raise exceptions the base doesn't raise

## How to Spot Violations
- `isinstance()` checks in code that should work with any subtype
- Overriding methods with `raise NotImplementedError`
- Subclass method ignoring parameters the base uses
- Tests written for base class that fail when given a subclass

## Fix Strategies
1. **Redesign hierarchy** — separate independent concepts
2. **Composition over inheritance** — use "has-a" instead of "is-a"
3. **Interface segregation** — don't force subclasses to implement unused methods

## Quick Example (Correct)
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Rectangle(Shape):    # Rectangle IS-A Shape ✅
    def __init__(self, w, h): self.width, self.height = w, h
    def area(self): return self.width * self.height

class Square(Shape):       # Square IS-A Shape ✅ (not Rectangle)
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2
```

Both substitute for `Shape`. Neither substitutes for the other — and that's correct.

## Common Mistakes
- Thinking "Square is mathematically a rectangle" means `Square(Rectangle)` is correct OOP
- Using `NotImplementedError` in subclass methods (violates postcondition)
- Deep hierarchies where each level narrows what the interface promises

## Links
- [Example 1: Rectangle violation →](examples/example1_classic_rectangle.py)
- [Example 2: Correct hierarchy →](examples/example2_correct_hierarchy.py)
- [Exercise →](exercises/problem.md)
