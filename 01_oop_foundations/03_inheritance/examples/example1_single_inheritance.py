"""
Example 1: Single Inheritance — Shape Hierarchy

Demonstrates:
- ABC (Abstract Base Class) as parent
- super().__init__() usage
- Method overriding (area, perimeter)
- isinstance() and issubclass()
- Polymorphism via a list of Shapes
"""
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base for all shapes. Defines the interface every shape must implement."""

    def __init__(self, color: str = "black") -> None:
        self.color = color

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""
        ...

    def describe(self) -> str:
        return (
            f"{self.__class__.__name__}(color={self.color}, "
            f"area={self.area():.2f}, perimeter={self.perimeter():.2f})"
        )


class Circle(Shape):
    def __init__(self, radius: float, color: str = "black") -> None:
        super().__init__(color)  # always call parent __init__
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float, color: str = "black") -> None:
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float, color: str = "black") -> None:
        super().__init__(color)
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides")
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        # Heron's formula
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


def print_shape_info(shape: Shape) -> None:
    """Accepts any Shape — polymorphism in action."""
    print(shape.describe())


if __name__ == "__main__":
    shapes: list[Shape] = [
        Circle(5, color="red"),
        Rectangle(4, 6, color="blue"),
        Triangle(3, 4, 5, color="green"),
    ]

    print("=== Shape Hierarchy Demo ===\n")
    for s in shapes:
        print_shape_info(s)

    print("\n=== isinstance / issubclass checks ===")
    circle = shapes[0]
    print(f"circle is Shape: {isinstance(circle, Shape)}")       # True
    print(f"circle is Circle: {isinstance(circle, Circle)}")     # True
    print(f"circle is Rectangle: {isinstance(circle, Rectangle)}")  # False
    print(f"issubclass(Circle, Shape): {issubclass(Circle, Shape)}")  # True

    print("\n=== Cannot instantiate ABC ===")
    try:
        s = Shape()
    except TypeError as e:
        print(f"TypeError: {e}")

    print("\n=== Total area of all shapes ===")
    total = sum(s.area() for s in shapes)
    print(f"Total area: {total:.2f}")
