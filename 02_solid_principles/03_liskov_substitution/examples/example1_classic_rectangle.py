"""
LSP Example 1: The Classic Rectangle → Square Violation

Demonstrates why mathematically correct "is-a" ≠ OOP correct "is-a".
"""


# ─── VIOLATION ────────────────────────────────────────────────────

class RectangleViolation:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def set_width(self, w: float) -> None:
        self.width = w

    def set_height(self, h: float) -> None:
        self.height = h

    def area(self) -> float:
        return self.width * self.height


class SquareViolation(RectangleViolation):
    """Square tries to enforce equal sides — but breaks Rectangle's contract."""

    def set_width(self, w: float) -> None:
        self.width = w
        self.height = w  # "clever" — but violates LSP!

    def set_height(self, h: float) -> None:
        self.width = h
        self.height = h


def test_rectangle_area(r: RectangleViolation) -> None:
    """This function should work correctly with ANY Rectangle subtype."""
    r.set_width(5)
    r.set_height(4)
    expected = 20
    actual = r.area()
    if actual == expected:
        print(f"✅ {r.__class__.__name__}: area = {actual} (correct)")
    else:
        print(f"❌ {r.__class__.__name__}: area = {actual}, expected {expected} (LSP VIOLATED!)")


# ─── FIX: Separate classes, common interface ──────────────────────

from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def set_width(self, w: float) -> None:
        self.width = w

    def set_height(self, h: float) -> None:
        self.height = h

    def area(self) -> float:
        return self.width * self.height


class Square(Shape):
    """Square IS-A Shape (not a Rectangle). No LSP violation."""

    def __init__(self, side: float) -> None:
        self.side = side

    def set_side(self, s: float) -> None:
        self.side = s

    def area(self) -> float:
        return self.side ** 2


def print_area(s: Shape) -> None:
    """Works correctly with ANY Shape subtype — no surprises."""
    print(f"{s.__class__.__name__}: area = {s.area():.2f}")


if __name__ == "__main__":
    print("=== LSP VIOLATION ===")
    test_rectangle_area(RectangleViolation(1, 1))  # passes
    test_rectangle_area(SquareViolation(1, 1))      # fails!

    print("\n=== LSP COMPLIANT FIX ===")
    shapes: list[Shape] = [Rectangle(5, 4), Square(5)]
    for s in shapes:
        print_area(s)
    print("\nBoth work correctly via Shape interface. ✅")
