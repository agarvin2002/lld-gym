"""
example1_single_inheritance.py
-------------------------------
Shows how inheritance works using a Shape hierarchy.

Real-world use: this parent-child pattern appears in almost every multi-class system.
  Vehicle → Car, Truck, Bike
  Room    → SingleRoom, DoubleRoom, Suite
  Spot    → CarSpot, BikeSpot, TruckSpot

Run this file directly:
    python3 example1_single_inheritance.py
"""
import math
from abc import ABC, abstractmethod


# The parent class (also called base class)
# It's abstract — you cannot create a Shape directly
class Shape(ABC):
    """Base class for all shapes. Every shape must have area() and perimeter()."""

    def __init__(self, color: str = "black") -> None:
        self.color = color

    @abstractmethod
    def area(self) -> float:
        """Every subclass must implement this."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Every subclass must implement this."""
        ...

    def describe(self) -> str:
        # This is a concrete method — all shapes can use it without rewriting
        return (
            f"{self.__class__.__name__}(color={self.color}, "
            f"area={self.area():.2f}, perimeter={self.perimeter():.2f})"
        )


# Child class 1 — inherits from Shape
class Circle(Shape):
    def __init__(self, radius: float, color: str = "black") -> None:
        super().__init__(color)   # always call parent __init__ first
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


# Child class 2
class Rectangle(Shape):
    def __init__(self, width: float, height: float, color: str = "black") -> None:
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


# Child class 3
class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float, color: str = "black") -> None:
        super().__init__(color)
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("These three sides cannot form a valid triangle")
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        # Heron's formula — works for any triangle
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# This function accepts ANY Shape — it doesn't care which one
# TIP: writing functions that accept the base class (not the specific subclass)
# is the key to flexible, extendable code.
def print_shape_info(shape: Shape) -> None:
    print(shape.describe())


# =============================================================================
# RUN THIS TO SEE IT IN ACTION
# =============================================================================

if __name__ == "__main__":
    shapes: list[Shape] = [
        Circle(5, color="red"),
        Rectangle(4, 6, color="blue"),
        Triangle(3, 4, 5, color="green"),
    ]

    print("=== Shape Hierarchy Demo ===\n")
    for s in shapes:
        print_shape_info(s)   # same function call, different output for each type

    print("\n=== isinstance checks ===")
    circle = shapes[0]
    print(f"circle is a Shape:     {isinstance(circle, Shape)}")       # True
    print(f"circle is a Circle:    {isinstance(circle, Circle)}")      # True
    print(f"circle is a Rectangle: {isinstance(circle, Rectangle)}")   # False

    print("\n=== Cannot create Shape directly ===")
    try:
        s = Shape()   # type: ignore
    except TypeError as e:
        print(f"Error: {e}")

    print("\n=== Total area of all shapes ===")
    total = sum(s.area() for s in shapes)
    print(f"Total area: {total:.2f}")
