"""
example2_dunder_methods.py
--------------------------
Demonstrates Python's "dunder" (double-underscore) methods — the special
methods that plug your objects into the Python language's built-in operations.

Concepts covered:
  - __eq__ and __hash__ for equality and use in sets/dicts
  - __lt__, __le__, __gt__, __ge__ for comparison and sorting
  - __add__, __sub__ for operator overloading
  - __len__, __contains__, __iter__ for container-like behavior
  - The dataclasses equivalent (much less code, same result)
  - Using objects in sets, dicts, and with sorted()

The class used: Point (a 2D coordinate)

Run this file directly:
    python3 example2_dunder_methods.py
"""

from __future__ import annotations  # Allows 'Point' type hint inside the class itself
import math
from dataclasses import dataclass, field
from functools import total_ordering


# =============================================================================
# PART 1: Manual Dunder Methods on a Point Class
# =============================================================================

@total_ordering  # Auto-generates __le__, __gt__, __ge__ from __eq__ and __lt__
class Point:
    """
    A 2D point with full dunder method support.

    This class shows how to make Python's built-in operators (+, ==, <, etc.)
    work with your own objects.
    """

    def __init__(self, x: float, y: float, label: str = "") -> None:
        self.x = x
        self.y = y
        self.label = label

    # -------------------------------------------------------------------------
    # __repr__: What developers see
    # -------------------------------------------------------------------------
    # This should be precise enough to reconstruct the object.
    # Tip: use !r for strings so quotes are included automatically.
    def __repr__(self) -> str:
        if self.label:
            return f"Point(x={self.x}, y={self.y}, label={self.label!r})"
        return f"Point(x={self.x}, y={self.y})"

    # -------------------------------------------------------------------------
    # __str__: What end-users see
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        name = f" ({self.label})" if self.label else ""
        return f"({self.x}, {self.y}){name}"

    # -------------------------------------------------------------------------
    # __eq__: Value-based equality
    # -------------------------------------------------------------------------
    # Without this, `Point(1, 2) == Point(1, 2)` is False because Python
    # compares object identity (memory address) by default.
    #
    # After this, equality is based on x and y coordinates.
    # Note: we intentionally exclude 'label' from equality — two points at
    # the same coordinates are the same point, regardless of their label.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented  # Signal that we don't know how to compare
        return self.x == other.x and self.y == other.y

    # -------------------------------------------------------------------------
    # __hash__: Consistent with __eq__
    # -------------------------------------------------------------------------
    # RULE: If a == b, then hash(a) must == hash(b).
    # RULE: Only include the same fields you use in __eq__.
    # RULE: Use immutable fields only (x and y are floats — immutable).
    #
    # hash() of a tuple is a well-distributed hash combining all elements.
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # -------------------------------------------------------------------------
    # __lt__: Less-than comparison (enables sorting)
    # -------------------------------------------------------------------------
    # We define ordering by distance from the origin (0, 0).
    # @total_ordering will derive __le__, __gt__, __ge__ from __eq__ and __lt__.
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.distance_from_origin() < other.distance_from_origin()

    # -------------------------------------------------------------------------
    # __add__: + operator overloading
    # -------------------------------------------------------------------------
    # Point(1, 2) + Point(3, 4) → Point(4, 6)
    # This is called "operator overloading" — we're defining what + means for Points.
    def __add__(self, other: Point) -> Point:
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    # -------------------------------------------------------------------------
    # __sub__: - operator overloading
    # -------------------------------------------------------------------------
    def __sub__(self, other: Point) -> Point:
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    # -------------------------------------------------------------------------
    # __mul__: * operator (scalar multiplication)
    # -------------------------------------------------------------------------
    # Point(2, 3) * 4 → Point(8, 12)
    def __mul__(self, scalar: float) -> Point:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Point(self.x * scalar, self.y * scalar)

    # -------------------------------------------------------------------------
    # __rmul__: Right-side * (so 4 * Point(2, 3) also works)
    # -------------------------------------------------------------------------
    # Python tries a.__mul__(b) first. If that returns NotImplemented, it tries
    # b.__rmul__(a). This lets you write: 4 * point (scalar on the left).
    def __rmul__(self, scalar: float) -> Point:
        return self.__mul__(scalar)

    # -------------------------------------------------------------------------
    # __abs__: abs() built-in
    # -------------------------------------------------------------------------
    # abs(point) → distance from origin (magnitude of the vector)
    def __abs__(self) -> float:
        return self.distance_from_origin()

    # -------------------------------------------------------------------------
    # __bool__: Truth value (used in if statements)
    # -------------------------------------------------------------------------
    # A point is falsy only if it's the origin (0, 0).
    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0

    # --- Helper method ---
    def distance_from_origin(self) -> float:
        """Return the Euclidean distance from (0, 0)."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, other: Point) -> float:
        """Return the Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


# =============================================================================
# PART 2: The Same Thing with @dataclass
# =============================================================================
# Python's dataclasses module auto-generates many dunder methods for you.
# This is the preferred approach for classes that are primarily data containers.

@dataclass
class PointDC:
    """
    A Point implemented with dataclass.

    @dataclass auto-generates:
      - __init__  (from the field annotations)
      - __repr__  (shows all fields)
      - __eq__    (compares all fields)

    It does NOT auto-generate __hash__ by default if __eq__ is generated
    (because mutable objects should not be hashable).

    Use @dataclass(frozen=True) to make it immutable AND hashable.
    Use @dataclass(order=True) to get __lt__, __le__, etc. based on field order.
    """
    x: float
    y: float
    label: str = ""  # default value for optional field


@dataclass(frozen=True, order=True)
class ImmutablePoint:
    """
    An immutable, orderable, hashable Point.

    frozen=True:
      - Makes the object immutable (raises FrozenInstanceError on assignment)
      - Generates a correct __hash__ automatically

    order=True:
      - Generates __lt__, __le__, __gt__, __ge__
      - Comparison is done field-by-field in definition order (x, then y)
      - Note: the 'label' field is excluded from ordering via field(compare=False)
    """
    x: float
    y: float
    label: str = field(default="", compare=False)  # don't include label in ordering or equality


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Dunder Methods Demonstration")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # PART 1: Manual Point class
    # -------------------------------------------------------------------------
    print("\n--- Basic Creation and Representation ---")
    p1 = Point(3.0, 4.0, label="A")
    p2 = Point(1.0, 2.0, label="B")
    p3 = Point(3.0, 4.0, label="Different label, same coords")

    print(f"repr(p1):  {repr(p1)}")   # Point(x=3.0, y=4.0, label='A')
    print(f"str(p1):   {str(p1)}")    # (3.0, 4.0) (A)
    print(f"print(p1): ", end=""); print(p1)  # uses __str__

    # --- __eq__ and __hash__ ---
    print("\n--- Equality (__eq__) ---")
    print(f"p1 == p3: {p1 == p3}")   # True — same x, y (label is ignored)
    print(f"p1 == p2: {p1 == p2}")   # False

    print(f"p1 is p3: {p1 is p3}")   # False — different objects in memory

    print("\n--- Hashing — use in sets and dicts (__hash__) ---")
    # Because we defined __hash__, Points can be used in sets and as dict keys
    point_set = {p1, p2, p3}
    # p1 and p3 have the same coordinates → same hash → deduplicated in set
    print(f"set size (p1, p2, p3): {len(point_set)}")  # 2

    point_dict = {p1: "origin area", p2: "close to origin"}
    print(f"Dict lookup p3 (== p1): {point_dict[p3]}")  # "origin area" — p3 == p1

    # --- __lt__ and sorting ---
    print("\n--- Comparison and Sorting (__lt__ via @total_ordering) ---")
    points = [Point(5, 0), Point(1, 0), Point(3, 4), Point(0, 2)]
    print("Before sort:")
    for p in points:
        print(f"  {p} | distance from origin: {p.distance_from_origin():.2f}")

    sorted_points = sorted(points)  # uses __lt__ under the hood
    print("After sort (by distance from origin):")
    for p in sorted_points:
        print(f"  {p} | distance from origin: {p.distance_from_origin():.2f}")

    # --- __add__, __sub__, __mul__ ---
    print("\n--- Operator Overloading (__add__, __sub__, __mul__) ---")
    a = Point(1.0, 2.0)
    b = Point(3.0, 4.0)

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")   # Point(4.0, 6.0)
    print(f"b - a = {b - a}")   # Point(2.0, 2.0)
    print(f"a * 3 = {a * 3}")   # Point(3.0, 6.0)
    print(f"3 * a = {3 * a}")   # Point(3.0, 6.0) — uses __rmul__

    # --- __abs__ ---
    print("\n--- __abs__ ---")
    p = Point(3.0, 4.0)
    print(f"abs(Point(3, 4)) = {abs(p)}")  # 5.0 — the classic 3-4-5 right triangle

    # --- __bool__ ---
    print("\n--- __bool__ (truth value) ---")
    origin = Point(0.0, 0.0)
    nonzero = Point(1.0, 0.0)
    print(f"bool(Point(0, 0)): {bool(origin)}")   # False — at origin
    print(f"bool(Point(1, 0)): {bool(nonzero)}")  # True

    if nonzero:
        print("nonzero point is truthy — if block executes")
    if not origin:
        print("origin point is falsy — if not block executes")

    # -------------------------------------------------------------------------
    # PART 2: @dataclass comparison
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("dataclass Comparison")
    print("=" * 60)

    print("\n--- Basic @dataclass ---")
    dp1 = PointDC(3.0, 4.0, label="A")
    dp2 = PointDC(3.0, 4.0, label="B")  # same coords, different label
    dp3 = PointDC(1.0, 2.0)

    print(f"repr: {repr(dp1)}")            # PointDC(x=3.0, y=4.0, label='A')
    print(f"dp1 == dp2: {dp1 == dp2}")     # False — label IS included in equality for @dataclass

    # Note the difference: in our manual Point, label was excluded from __eq__.
    # In @dataclass, ALL fields are included by default.

    # PointDC objects are NOT hashable because @dataclass with eq=True sets __hash__ = None
    try:
        s = {dp1}
    except TypeError as e:
        print(f"PointDC not hashable: {e}")

    print("\n--- @dataclass(frozen=True, order=True) ---")
    ip1 = ImmutablePoint(3.0, 4.0, label="A")
    ip2 = ImmutablePoint(1.0, 2.0, label="B")
    ip3 = ImmutablePoint(3.0, 4.0, label="different")  # same coords

    print(f"repr: {repr(ip1)}")

    # frozen=True makes it hashable
    ip_set = {ip1, ip2, ip3}
    # ip1 and ip3 have same x, y — label has compare=False so they ARE equal
    print(f"ImmutablePoint set size (ip1, ip2, ip3): {len(ip_set)}")  # 2

    # order=True gives us sorting
    ip_list = [ImmutablePoint(5, 0), ImmutablePoint(1, 0), ImmutablePoint(3, 4)]
    # Note: ImmutablePoint sorts by (x, y) field order, NOT by distance!
    sorted_ip = sorted(ip_list)
    print("Sorted ImmutablePoints (by x, then y):")
    for ip in sorted_ip:
        print(f"  {ip}")

    # frozen=True prevents modification
    try:
        ip1.x = 99  # type: ignore
    except Exception as e:
        print(f"Cannot modify frozen dataclass: {type(e).__name__}: {e}")

    print("\nDone.")
