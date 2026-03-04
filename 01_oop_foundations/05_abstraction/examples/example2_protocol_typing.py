"""
Example 2: typing.Protocol — Structural Abstraction
=====================================================

Python 3.8 introduced typing.Protocol, which provides structural subtyping:
a class satisfies a Protocol if it has the right methods — without inheriting
from it. This is "duck typing with type hints".

This example demonstrates:
- Defining a Protocol (Drawable)
- Multiple classes satisfying the Protocol without inheritance
- @runtime_checkable and isinstance() with Protocols
- Contrast: Protocol (structural) vs ABC (nominal)
- When to choose each
- How Protocol enables working with third-party code

Key terms:
- Nominal typing: compatibility based on declared class hierarchy (ABC, Java)
- Structural typing: compatibility based on method/attribute shape (Protocol, Go)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Protocol definition: what a Drawable object must look like
# ---------------------------------------------------------------------------

@runtime_checkable
class Drawable(Protocol):
    """
    Structural type: any object with draw() and bounding_box() is Drawable.

    Classes do NOT inherit from Drawable. The Protocol describes the
    expected shape, not the hierarchy.

    @runtime_checkable allows isinstance(obj, Drawable) at runtime.
    Note: runtime isinstance only checks method presence, not signatures.
    Static type checkers (mypy, pyright) check the full signatures.
    """

    def draw(self) -> str:
        """Render this object and return a string representation."""
        ...

    def bounding_box(self) -> tuple[float, float, float, float]:
        """
        Return (x_min, y_min, x_max, y_max) bounding box.
        Used for layout, collision detection, etc.
        """
        ...


@runtime_checkable
class Resizable(Protocol):
    """
    Structural type: any object with resize() is Resizable.
    Protocols can be combined (structural intersection via multiple protocols).
    """

    def resize(self, factor: float) -> None:
        """Scale this object by factor."""
        ...


# ---------------------------------------------------------------------------
# Classes satisfying Drawable — NO inheritance from Drawable
# ---------------------------------------------------------------------------

@dataclass
class Circle:
    """
    A circle. Does NOT inherit from Drawable.
    Satisfies the Drawable protocol purely by having draw() and bounding_box().
    """
    x: float
    y: float
    radius: float

    def draw(self) -> str:
        return f"Circle at ({self.x}, {self.y}) r={self.radius}"

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def resize(self, factor: float) -> None:
        self.radius *= factor


@dataclass
class Rectangle:
    """
    A rectangle. Also does NOT inherit from Drawable.
    Compatible with Drawable AND Resizable protocols.
    """
    x: float
    y: float
    width: float
    height: float

    def draw(self) -> str:
        return f"Rectangle at ({self.x}, {self.y}) {self.width}x{self.height}"

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def resize(self, factor: float) -> None:
        self.width *= factor
        self.height *= factor


@dataclass
class TextLabel:
    """
    A text label. Has draw() and bounding_box() but NOT resize().
    Satisfies Drawable but NOT Resizable.
    """
    x: float
    y: float
    text: str
    font_size: float = 12.0

    def draw(self) -> str:
        return f"Text '{self.text}' at ({self.x}, {self.y}) size={self.font_size}"

    def bounding_box(self) -> tuple[float, float, float, float]:
        # Approximation: each character is ~0.6 * font_size wide
        approx_width = len(self.text) * self.font_size * 0.6
        return (self.x, self.y, self.x + approx_width, self.y + self.font_size)


# ---------------------------------------------------------------------------
# Third-party simulation: a class we cannot modify
# ---------------------------------------------------------------------------

class ExternalChartWidget:
    """
    Imagine this comes from a third-party charting library.
    We cannot make it inherit from Drawable.
    But it has draw() and bounding_box() — so it structurally satisfies Drawable.
    """

    def __init__(self, title: str) -> None:
        self.title = title

    def draw(self) -> str:
        return f"[ChartWidget] Bar chart: {self.title}"

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (0.0, 0.0, 400.0, 300.0)

    # Extra methods the library has — irrelevant to Drawable
    def export_png(self, filepath: str) -> None:
        print(f"Exporting chart to {filepath}")

    def set_data(self, data: list[float]) -> None:
        self._data = data


# ---------------------------------------------------------------------------
# Functions that accept Drawable — structural typing in action
# ---------------------------------------------------------------------------

def render_all(shapes: list[Drawable]) -> None:
    """
    Render all drawable objects.

    The parameter type is list[Drawable]. Any object that structurally
    satisfies Drawable works here — no inheritance required.
    """
    print("Rendering scene:")
    for shape in shapes:
        print(f"  {shape.draw()}")


def compute_scene_bounds(shapes: list[Drawable]) -> tuple[float, float, float, float]:
    """
    Compute the bounding box that encloses all shapes in the scene.

    Works with any collection of Drawables — all via structural typing.
    """
    if not shapes:
        return (0.0, 0.0, 0.0, 0.0)

    boxes = [shape.bounding_box() for shape in shapes]
    x_min = min(b[0] for b in boxes)
    y_min = min(b[1] for b in boxes)
    x_max = max(b[2] for b in boxes)
    y_max = max(b[3] for b in boxes)
    return (x_min, y_min, x_max, y_max)


def resize_all(shapes: list[Resizable], factor: float) -> None:
    """
    Resize all resizable objects by a factor.

    TextLabel is NOT Resizable — so it cannot be passed here.
    Circle and Rectangle can be passed here.
    """
    for shape in shapes:
        shape.resize(factor)
    print(f"All shapes resized by factor {factor}")


# ---------------------------------------------------------------------------
# ABC vs Protocol comparison
# ---------------------------------------------------------------------------

def compare_abc_vs_protocol() -> None:
    """
    Illustrates the key difference between ABC and Protocol.

    ABC (Nominal Typing):
    - Requires explicit inheritance: class Circle(Drawable)
    - isinstance() works natively
    - Python enforces the contract at class definition time
    - Best for: internal APIs where you own all implementations

    Protocol (Structural Typing):
    - No inheritance required: class Circle (just has draw())
    - isinstance() works only with @runtime_checkable
    - mypy/pyright enforce at analysis time (not runtime)
    - Best for: working with external code, loose coupling, flexible APIs

    Quick decision guide:
    ┌─────────────────────────────────────┬────────┬──────────┐
    │ Situation                           │ ABC    │ Protocol │
    ├─────────────────────────────────────┼────────┼──────────┤
    │ You own all implementations         │  ✓     │  ✓       │
    │ Third-party classes must conform    │        │  ✓       │
    │ Runtime isinstance() needed         │  ✓     │  ✓ *     │
    │ Want Python to enforce at runtime   │  ✓     │          │
    │ Retroactive compatibility           │        │  ✓       │
    │ Shared base class behavior needed   │  ✓     │          │
    └─────────────────────────────────────┴────────┴──────────┘
    * @runtime_checkable only checks method presence, not signatures
    """
    print("[compare_abc_vs_protocol] — see docstring for full comparison table")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: typing.Protocol — Structural Abstraction")
    print("=" * 60)

    # --- Part 1: Create objects — no Drawable inheritance ---
    circle = Circle(x=10, y=10, radius=5)
    rect = Rectangle(x=0, y=0, width=20, height=10)
    label = TextLabel(x=5, y=5, text="Hello, World!")
    chart = ExternalChartWidget(title="Q1 Sales")

    shapes: list[Drawable] = [circle, rect, label, chart]

    # --- Part 2: isinstance() with @runtime_checkable ---
    print("\n[Part 1] isinstance() with @runtime_checkable Protocol")
    print("-" * 50)
    for obj in shapes:
        is_drawable = isinstance(obj, Drawable)
        is_resizable = isinstance(obj, Resizable)
        print(
            f"  {type(obj).__name__:25}"
            f"Drawable={is_drawable}  Resizable={is_resizable}"
        )

    # TextLabel has no resize() — not Resizable
    # ExternalChartWidget has no resize() — not Resizable

    # --- Part 3: render_all — works with all Drawables ---
    print("\n[Part 2] render_all() — accepts any Drawable")
    print("-" * 50)
    render_all(shapes)

    # --- Part 4: compute scene bounds ---
    print("\n[Part 3] compute_scene_bounds() — structural typing")
    print("-" * 50)
    bounds = compute_scene_bounds([circle, rect, label])
    print(f"Scene bounding box: {bounds}")

    # --- Part 5: resize only the Resizable ones ---
    print("\n[Part 4] resize_all() — only Resizable objects")
    print("-" * 50)
    resizables: list[Resizable] = [circle, rect]   # TextLabel excluded
    resize_all(resizables, factor=2.0)
    print(f"After resize: {circle.draw()}")
    print(f"After resize: {rect.draw()}")

    # --- Part 6: Third-party class as Drawable ---
    print("\n[Part 5] Third-party ExternalChartWidget — fits Drawable protocol")
    print("-" * 50)
    print(f"isinstance(chart, Drawable): {isinstance(chart, Drawable)}")
    # ExternalChartWidget never inherited from Drawable —
    # yet it fits because it has draw() and bounding_box()
    render_all([chart])

    # --- Part 7: Object that does NOT satisfy Drawable ---
    print("\n[Part 6] Object that does NOT satisfy Drawable")
    print("-" * 50)

    class NotDrawable:
        """Has draw() but no bounding_box() — does not fully satisfy Drawable."""
        def draw(self) -> str:
            return "I only have draw()"

    nd = NotDrawable()
    print(f"isinstance(NotDrawable(), Drawable): {isinstance(nd, Drawable)}")
    # False — missing bounding_box()

    # --- Part 8: ABC vs Protocol summary ---
    print("\n[Part 7] ABC vs Protocol — when to use each")
    print("-" * 50)
    print("ABC  (Nominal):    requires 'class Circle(Drawable)' — explicit hierarchy")
    print("Protocol (Struct): any class with draw() + bounding_box() qualifies")
    print("ExternalChartWidget works as Drawable because of Protocol — impossible with ABC")
    print("Use ABC when you own all implementations and want Python enforcement.")
    print("Use Protocol when you need structural flexibility or third-party compatibility.")

    print("\n--- End of demo ---")
