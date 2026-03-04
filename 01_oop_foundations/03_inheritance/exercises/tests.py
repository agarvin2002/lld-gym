"""
Tests for the Employee Hierarchy exercise.
Run: pytest tests.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import Employee, Manager, Engineer, Director


class TestEmployee:
    def test_employee_is_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            Employee("Alice", "E001", 80000)


class TestManager:
    def setup_method(self):
        self.manager = Manager("Bob", "M001", 100_000, team_size=5)

    def test_manager_name(self):
        assert self.manager.name == "Bob"

    def test_manager_employee_id(self):
        assert self.manager.employee_id == "M001"

    def test_manager_base_salary(self):
        assert self.manager.base_salary == 100_000

    def test_manager_team_size(self):
        assert self.manager.team_size == 5

    def test_manager_get_role(self):
        assert self.manager.get_role() == "Manager"

    def test_manager_total_compensation_includes_20_percent_bonus(self):
        assert self.manager.get_total_compensation() == pytest.approx(120_000.00)

    def test_manager_is_instance_of_employee(self):
        assert isinstance(self.manager, Employee)


class TestEngineer:
    def setup_method(self):
        self.engineer = Engineer("Carol", "E001", 90_000, tech_stack=["Python", "Go"])

    def test_engineer_name(self):
        assert self.engineer.name == "Carol"

    def test_engineer_tech_stack(self):
        assert self.engineer.tech_stack == ["Python", "Go"]

    def test_engineer_get_role(self):
        assert self.engineer.get_role() == "Engineer"

    def test_engineer_total_compensation_includes_10_percent_bonus(self):
        assert self.engineer.get_total_compensation() == pytest.approx(99_000.00)

    def test_engineer_is_instance_of_employee(self):
        assert isinstance(self.engineer, Employee)


class TestDirector:
    def setup_method(self):
        self.director = Director("Dave", "D001", 150_000, team_size=20, department="Engineering")

    def test_director_name(self):
        assert self.director.name == "Dave"

    def test_director_department(self):
        assert self.director.department == "Engineering"

    def test_director_team_size_inherited_from_manager(self):
        assert self.director.team_size == 20

    def test_director_get_role(self):
        assert self.director.get_role() == "Director"

    def test_director_total_compensation_includes_40_percent_bonus(self):
        assert self.director.get_total_compensation() == pytest.approx(210_000.00)

    def test_director_is_instance_of_manager(self):
        assert isinstance(self.director, Manager)

    def test_director_is_instance_of_employee(self):
        assert isinstance(self.director, Employee)

    def test_issubclass_director_of_manager(self):
        assert issubclass(Director, Manager)

    def test_issubclass_director_of_employee(self):
        assert issubclass(Director, Employee)
