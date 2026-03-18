"""
WHAT YOU'RE BUILDING
====================
You are building an Organisation Chart using the Composite pattern.

The org chart has two kinds of nodes:
- Employee  — a single person with a name, title, and salary (leaf)
- Department — a group that contains employees and/or sub-departments (composite)

Both share the OrgNode interface. That means you can call total_salary(),
headcount(), or display() on either an individual or an entire department
and the maths will just work — no isinstance() checks needed.

Your job: implement Employee and Department below.
OrgNode is already provided — do not modify it.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Component (abstract base) — do not modify
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
# TODO: Implement Employee (leaf)
# ---------------------------------------------------------------------------

class Employee(OrgNode):
    """A single employee. No children. Just returns its own values."""

    def __init__(self, name: str, title: str, salary: float) -> None:
        # TODO: Store name, title, and salary as private attributes
        pass

    @property
    def name(self) -> str:
        # TODO: Return the employee's name
        pass

    def total_salary(self) -> float:
        # TODO: Return this employee's own salary (not a sum — just one value)
        pass

    def headcount(self) -> int:
        # TODO: Return 1 — a single employee counts as one person
        pass

    def display(self, indent: int = 0) -> str:
        # TODO: Return "  " * indent + "{name} ({title}) — ${salary:,.0f}"
        # HINT: Use an em dash (—) or a plain hyphen. Keep it on one line.
        pass


# ---------------------------------------------------------------------------
# TODO: Implement Department (composite)
# ---------------------------------------------------------------------------

class Department(OrgNode):
    """A department that groups OrgNodes (employees or sub-departments)."""

    def __init__(self, name: str) -> None:
        # TODO: Store the name and create an empty list self._members: list[OrgNode]
        pass

    @property
    def name(self) -> str:
        # TODO: Return the department name
        pass

    def add_member(self, node: OrgNode) -> None:
        # TODO: Append the node to self._members
        pass

    def total_salary(self) -> float:
        # TODO: Return the sum of total_salary() across all members
        # HINT: Use sum(m.total_salary() for m in self._members)
        pass

    def headcount(self) -> int:
        # TODO: Return the sum of headcount() across all members
        # HINT: Works the same way as total_salary() — delegate to each child
        pass

    def display(self, indent: int = 0) -> str:
        # TODO: Return a multi-line string:
        #   Line 1: "  " * indent + "[{department name}]"
        #   Then each member's display(indent + 1) on its own line
        # HINT: Build a list of strings and join with "\n"
        pass


# ---------------------------------------------------------------------------
# Quick manual test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    eng = Department("Engineering")
    eng.add_member(Employee("Alice", "Staff Engineer", 180_000))
    eng.add_member(Employee("Bob",   "SDE II",         120_000))

    design = Department("Design")
    design.add_member(Employee("Carol", "Lead Designer", 140_000))

    company = Department("Acme Corp")
    company.add_member(eng)
    company.add_member(design)

    print(company.display())
    print(f"\nTotal salary : ${company.total_salary():,.0f}")
    print(f"Headcount    : {company.headcount()}")


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/structural/composite/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
