"""
example2_dunder_methods.py
--------------------------
Advanced topic — shows how @dataclass reduces boilerplate in data classes.

What's in here:
  - @dataclass — auto-generates __init__, __repr__, and __eq__ for you

Run this file directly:
    python3 example2_dunder_methods.py
"""

from __future__ import annotations
from dataclasses import dataclass


# =============================================================================
# @dataclass saves you from writing __init__, __repr__, and __eq__ manually
# =============================================================================
#
# Without @dataclass, you write this (boring and repetitive):
#
#     class Point:
#         def __init__(self, x, y):
#             self.x = x
#             self.y = y
#         def __repr__(self):
#             return f"Point(x={self.x}, y={self.y})"
#         def __eq__(self, other):
#             return self.x == other.x and self.y == other.y
#
# With @dataclass, Python generates all of the above automatically:

@dataclass
class Point:
    """A 2D point. @dataclass gives us __init__, __repr__, and __eq__ for free."""
    x: float
    y: float


# Use @dataclass for simple data containers — classes that are mostly data, not behaviour.
# Example:
#   @dataclass
#   class ParkingTicket:
#       ticket_id: str
#       spot_number: int
#       vehicle_type: str


# =============================================================================
# RUN THIS TO SEE IT IN ACTION
# =============================================================================

if __name__ == "__main__":
    print("=== @dataclass Demo ===\n")

    p1 = Point(3.0, 4.0)
    p2 = Point(3.0, 4.0)
    p3 = Point(1.0, 2.0)

    # __repr__ is auto-generated — shows all fields
    print(repr(p1))             # Point(x=3.0, y=4.0)
    print(repr(p3))             # Point(x=1.0, y=2.0)

    # __eq__ is auto-generated — compares all fields
    print(f"p1 == p2: {p1 == p2}")   # True — same values
    print(f"p1 == p3: {p1 == p3}")   # False — different values

    print("\nKey takeaway:")
    print("Use @dataclass for simple data containers to avoid boilerplate.")
    print("You only need to write the field names and their types.")
