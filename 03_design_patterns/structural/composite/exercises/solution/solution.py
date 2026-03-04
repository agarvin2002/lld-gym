"""
Composite Pattern Exercise — Organization Chart (Solution)
==========================================================

Key design decisions:
- OrgNode is an ABC so that both Employee and Department must implement every
  method — no silent partial implementations.
- Employee is a pure leaf: no add_member, no children list.
- Department stores a list[OrgNode] — any combination of employees and
  sub-departments can be added without type checks.
- total_salary() and headcount() recurse implicitly: Department delegates to
  each child, and each child does the same until a leaf is reached.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component (abstract base)
# ---------------------------------------------------------------------------

class OrgNode(ABC):
    """Shared interface for employees (leaves) and departments (composites)."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def total_salary(self) -> float: ...

    @abstractmethod
    def headcount(self) -> int: ...

    @abstractmethod
    def display(self, indent: int = 0) -> str: ...


# ---------------------------------------------------------------------------
# Leaf
# ---------------------------------------------------------------------------

class Employee(OrgNode):
    """A single employee — leaf node with no children."""

    def __init__(self, name: str, title: str, salary: float) -> None:
        self._name   = name
        self._title  = title
        self._salary = salary

    @property
    def name(self) -> str:
        return self._name

    def total_salary(self) -> float:
        return self._salary

    def headcount(self) -> int:
        return 1

    def display(self, indent: int = 0) -> str:
        return "  " * indent + f"{self._name} ({self._title}) \u2014 ${self._salary:,.0f}"


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------

class Department(OrgNode):
    """A department that groups OrgNodes (employees or sub-departments)."""

    def __init__(self, name: str) -> None:
        self._name    = name
        self._members: list[OrgNode] = []

    @property
    def name(self) -> str:
        return self._name

    def add_member(self, node: OrgNode) -> None:
        """Append any OrgNode to this department's member list."""
        self._members.append(node)

    def total_salary(self) -> float:
        """Recursive sum across all direct and indirect members."""
        return sum(m.total_salary() for m in self._members)

    def headcount(self) -> int:
        """Recursive count of all employees at every level."""
        return sum(m.headcount() for m in self._members)

    def display(self, indent: int = 0) -> str:
        """Depth-first display: department header, then each member indented."""
        lines = ["  " * indent + f"[{self._name}]"]
        for member in self._members:
            lines.append(member.display(indent + 1))
        return "\n".join(lines)
