"""Factory Pattern — Example 1: Shape Factory.

The Factory pattern defines an interface for creating objects but lets
a factory function or subclass decide which class to instantiate.
This decouples object creation from the code that uses the objects.

Real-world use: shape renderers in design tools, geometry engines,
map tile generators (circle/polygon/line created from GeoJSON type strings).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import math


# ── Product Interface ─────────────────────────────────────────────────────────

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    @abstractmethod
    def describe(self) -> str: ...


# ── Concrete Products ─────────────────────────────────────────────────────────

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self._radius = radius

    def area(self) -> float:
        return math.pi * self._radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self._radius

    def describe(self) -> str:
        return f"Circle(r={self._radius})"


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    def area(self) -> float:
        return self._width * self._height

    def perimeter(self) -> float:
        return 2 * (self._width + self._height)

    def describe(self) -> str:
        return f"Rectangle({self._width}×{self._height})"


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float) -> None:
        self._a, self._b, self._c = a, b, c

    def area(self) -> float:
        s = (self._a + self._b + self._c) / 2
        return math.sqrt(s * (s - self._a) * (s - self._b) * (s - self._c))

    def perimeter(self) -> float:
        return self._a + self._b + self._c

    def describe(self) -> str:
        return f"Triangle({self._a},{self._b},{self._c})"


# ── Simple Factory Function ───────────────────────────────────────────────────
# Not a Gang-of-Four pattern — just a convenient creation function.
# Callers don't import Circle/Rectangle/Triangle directly.

def create_shape(shape_type: str, **kwargs) -> Shape:
    """Create a shape by name. kwargs are forwarded to the constructor."""
    registry: dict[str, type[Shape]] = {
        "circle":    Circle,
        "rectangle": Rectangle,
        "triangle":  Triangle,
    }
    if shape_type not in registry:
        raise ValueError(f"Unknown shape: {shape_type!r}. Choose from {list(registry)}")
    return registry[shape_type](**kwargs)


# ── Factory Method Pattern ────────────────────────────────────────────────────
# The creator defines the interface; subclasses decide which product to make.
# TIP: the creator's business logic (get_info) is reused — only creation varies.

class ShapeFactory(ABC):
    """Creator — defines the factory method."""

    @abstractmethod
    def create_shape(self) -> Shape:
        """Factory Method: subclasses override this."""

    def get_info(self) -> str:
        """Template method that uses the factory method."""
        shape = self.create_shape()
        return f"{shape.describe()} — area={shape.area():.2f}, perimeter={shape.perimeter():.2f}"


class CircleFactory(ShapeFactory):
    def __init__(self, radius: float) -> None:
        self._radius = radius

    def create_shape(self) -> Shape:
        return Circle(self._radius)


class RectangleFactory(ShapeFactory):
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    def create_shape(self) -> Shape:
        return Rectangle(self._width, self._height)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Simple Factory Function ===")
    for spec in [
        ("circle", {"radius": 5}),
        ("rectangle", {"width": 4, "height": 6}),
        ("triangle", {"a": 3, "b": 4, "c": 5}),
    ]:
        shape = create_shape(spec[0], **spec[1])
        print(f"{shape.describe()}: area={shape.area():.2f}")

    print("\n=== Factory Method Pattern ===")
    factories: list[ShapeFactory] = [CircleFactory(3), RectangleFactory(5, 8)]
    for factory in factories:
        print(factory.get_info())
