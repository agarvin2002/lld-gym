"""
Exercise: Employee Compensation Hierarchy

Fill in the TODOs. Run tests with: pytest tests.py -v
"""
from abc import ABC, abstractmethod


class Employee(ABC):
    """
    Abstract base class for all employee types.

    Subclasses must implement get_total_compensation() and get_role().
    """

    def __init__(self, name: str, employee_id: str, base_salary: float) -> None:
        # TODO: store name, employee_id, base_salary as instance attributes
        pass

    @abstractmethod
    def get_total_compensation(self) -> float:
        """Return total compensation including bonuses. Round to 2 decimal places."""
        ...

    @abstractmethod
    def get_role(self) -> str:
        """Return the role title as a string (e.g., 'Manager')."""
        ...

    def __repr__(self) -> str:
        # TODO: return f"<{role} {name} (id={employee_id}) comp=${total_comp:.2f}>"
        pass


class Manager(Employee):
    """
    A manager receives a 20% bonus on top of base salary.

    Additional attribute: team_size (number of direct reports)
    """

    def __init__(self, name: str, employee_id: str, base_salary: float, team_size: int) -> None:
        # TODO: call super().__init__() with name, employee_id, base_salary
        # TODO: store team_size
        pass

    def get_role(self) -> str:
        # TODO: return "Manager"
        pass

    def get_total_compensation(self) -> float:
        # TODO: return base_salary * 1.20, rounded to 2 decimal places
        pass


class Engineer(Employee):
    """
    An engineer receives a 10% bonus on top of base salary.

    Additional attribute: tech_stack (list of technologies)
    """

    def __init__(self, name: str, employee_id: str, base_salary: float, tech_stack: list[str]) -> None:
        # TODO: call super().__init__()
        # TODO: store tech_stack
        pass

    def get_role(self) -> str:
        # TODO: return "Engineer"
        pass

    def get_total_compensation(self) -> float:
        # TODO: return base_salary * 1.10, rounded to 2 decimal places
        pass


class Director(Manager):
    """
    A director receives a 40% bonus on top of base salary.
    Director IS-A Manager (inherits team_size).

    Additional attribute: department name
    """

    def __init__(
        self,
        name: str,
        employee_id: str,
        base_salary: float,
        team_size: int,
        department: str,
    ) -> None:
        # TODO: call super().__init__() with name, employee_id, base_salary, team_size
        # TODO: store department
        pass

    def get_role(self) -> str:
        # TODO: return "Director"
        pass

    def get_total_compensation(self) -> float:
        # TODO: return base_salary * 1.40, rounded to 2 decimal places
        pass
