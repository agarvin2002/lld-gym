"""
Tests for the Composite exercise — Organization Chart.

Run with:
    /tmp/lld_venv/bin/pytest 03_design_patterns/structural/composite/exercises/tests.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import Employee, Department


# ---------------------------------------------------------------------------
# TestEmployee
# ---------------------------------------------------------------------------

class TestEmployee:
    def test_name_is_correct(self):
        e = Employee("Alice", "Engineer", 120_000)
        assert e.name == "Alice"

    def test_total_salary_returns_own_salary(self):
        e = Employee("Bob", "Manager", 95_000)
        assert e.total_salary() == 95_000

    def test_headcount_is_one(self):
        e = Employee("Carol", "Designer", 80_000)
        assert e.headcount() == 1

    def test_display_contains_name(self):
        e = Employee("Dave", "Analyst", 70_000)
        result = e.display()
        assert "Dave" in result

    def test_display_contains_title(self):
        e = Employee("Eve", "Director", 150_000)
        result = e.display()
        assert "Director" in result

    def test_display_contains_salary(self):
        e = Employee("Frank", "VP", 200_000)
        result = e.display()
        # Salary should appear formatted (e.g. 200,000 or 200000)
        assert "200" in result

    def test_display_at_zero_indent(self):
        e = Employee("Grace", "Engineer", 120_000)
        result = e.display(0)
        # Should not start with leading spaces at indent=0
        assert result.startswith("Grace")

    def test_display_at_nonzero_indent(self):
        e = Employee("Hank", "Engineer", 120_000)
        result = e.display(2)
        # Should start with 4 spaces (2 * "  ")
        assert result.startswith("    ")
        assert "Hank" in result

    def test_employee_is_orgnode(self):
        from starter import OrgNode
        e = Employee("Iris", "Intern", 40_000)
        assert isinstance(e, OrgNode)

    def test_salary_as_float(self):
        e = Employee("Jack", "Engineer", 115_000.5)
        assert e.total_salary() == 115_000.5


# ---------------------------------------------------------------------------
# TestDepartment
# ---------------------------------------------------------------------------

class TestDepartment:
    def test_empty_department_headcount_is_zero(self):
        d = Department("Engineering")
        assert d.headcount() == 0

    def test_empty_department_total_salary_is_zero(self):
        d = Department("Engineering")
        assert d.total_salary() == 0.0

    def test_name_is_correct(self):
        d = Department("Marketing")
        assert d.name == "Marketing"

    def test_add_one_employee_headcount_is_one(self):
        d = Department("Design")
        d.add_member(Employee("Alice", "Designer", 80_000))
        assert d.headcount() == 1

    def test_add_two_employees_headcount_is_two(self):
        d = Department("Design")
        d.add_member(Employee("Alice", "Designer", 80_000))
        d.add_member(Employee("Bob", "Designer", 82_000))
        assert d.headcount() == 2

    def test_total_salary_sums_employees(self):
        d = Department("Sales")
        d.add_member(Employee("Alice", "Rep", 60_000))
        d.add_member(Employee("Bob", "Rep", 65_000))
        assert d.total_salary() == 125_000

    def test_department_is_orgnode(self):
        from starter import OrgNode
        d = Department("HR")
        assert isinstance(d, OrgNode)

    def test_add_member_accepts_department(self):
        parent = Department("Company")
        child  = Department("Engineering")
        parent.add_member(child)   # should not raise
        assert parent.headcount() == 0  # no employees yet

    def test_total_salary_single_employee(self):
        d = Department("Finance")
        d.add_member(Employee("Zara", "Accountant", 90_000))
        assert d.total_salary() == 90_000.0


# ---------------------------------------------------------------------------
# TestNestedDepartment
# ---------------------------------------------------------------------------

class TestNestedDepartment:
    def setup_method(self):
        """
        Company
        ├── CEO (Diana)          $200,000
        └── Engineering
            ├── Alice            $120,000
            └── Backend
                └── Bob          $140,000
        """
        self.diana   = Employee("Diana", "CEO",             200_000)
        self.alice   = Employee("Alice", "Engineer",        120_000)
        self.bob     = Employee("Bob",   "Senior Engineer", 140_000)

        self.backend = Department("Backend")
        self.backend.add_member(self.bob)

        self.eng = Department("Engineering")
        self.eng.add_member(self.alice)
        self.eng.add_member(self.backend)

        self.company = Department("Acme Corp")
        self.company.add_member(self.diana)
        self.company.add_member(self.eng)

    def test_total_headcount(self):
        assert self.company.headcount() == 3

    def test_total_salary(self):
        assert self.company.total_salary() == 460_000.0

    def test_nested_department_headcount(self):
        assert self.eng.headcount() == 2

    def test_nested_department_salary(self):
        assert self.eng.total_salary() == 260_000.0

    def test_leaf_department_headcount(self):
        assert self.backend.headcount() == 1

    def test_leaf_department_salary(self):
        assert self.backend.total_salary() == 140_000.0

    def test_multiple_nesting_levels(self):
        """Four levels deep should still aggregate correctly."""
        l3 = Department("Level3")
        l3.add_member(Employee("E1", "Dev", 50_000))

        l2 = Department("Level2")
        l2.add_member(Employee("E2", "Dev", 60_000))
        l2.add_member(l3)

        l1 = Department("Level1")
        l1.add_member(l2)

        assert l1.headcount() == 2
        assert l1.total_salary() == 110_000.0


# ---------------------------------------------------------------------------
# TestDisplay
# ---------------------------------------------------------------------------

class TestDisplay:
    def test_employee_display_contains_name(self):
        e = Employee("Alice", "Engineer", 120_000)
        assert "Alice" in e.display()

    def test_department_display_contains_department_name(self):
        d = Department("Engineering")
        d.add_member(Employee("Alice", "Engineer", 120_000))
        result = d.display()
        assert "Engineering" in result

    def test_department_display_contains_employee_name(self):
        d = Department("Engineering")
        d.add_member(Employee("Alice", "Engineer", 120_000))
        result = d.display()
        assert "Alice" in result

    def test_department_display_contains_all_employee_names(self):
        d = Department("Team")
        d.add_member(Employee("Alice", "Dev", 100_000))
        d.add_member(Employee("Bob",   "Dev", 100_000))
        result = d.display()
        assert "Alice" in result
        assert "Bob" in result

    def test_nested_display_contains_all_names(self):
        backend = Department("Backend")
        backend.add_member(Employee("Bob", "Senior Engineer", 140_000))

        eng = Department("Engineering")
        eng.add_member(Employee("Alice", "Engineer", 120_000))
        eng.add_member(backend)

        company = Department("Acme Corp")
        company.add_member(Employee("Diana", "CEO", 200_000))
        company.add_member(eng)

        result = company.display()
        assert "Acme Corp"   in result
        assert "Diana"       in result
        assert "Engineering" in result
        assert "Alice"       in result
        assert "Backend"     in result
        assert "Bob"         in result

    def test_display_returns_string(self):
        e = Employee("Alice", "Engineer", 120_000)
        assert isinstance(e.display(), str)

    def test_department_display_returns_string(self):
        d = Department("HR")
        assert isinstance(d.display(), str)

    def test_employee_indent_increases_leading_spaces(self):
        e = Employee("Alice", "Engineer", 120_000)
        r0 = e.display(0)
        r1 = e.display(1)
        r2 = e.display(2)
        # Each indent level adds 2 spaces
        assert r1.startswith("  ")
        assert r2.startswith("    ")
        # The name appears in all
        assert "Alice" in r0
        assert "Alice" in r1
        assert "Alice" in r2
