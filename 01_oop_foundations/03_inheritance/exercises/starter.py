"""
WHAT YOU'RE BUILDING
--------------------
You are building an Employee system for a company.

There are three types of employees:
  Manager  — gets a 20% bonus on top of their base salary
  Engineer — gets a 10% bonus on top of their base salary
  Director — gets a 40% bonus (Director also IS-A Manager, so they have a team)

Each type must know their role name and total pay including bonus.

TIP: This is exactly the same pattern used in LLD problems like
"Hotel System" (Room → SingleRoom, DoubleRoom, Suite) or
"Vehicle System" (Vehicle → Car, Truck, Bike).

HOW TO RUN TESTS
    pytest tests.py -v
"""
from abc import ABC, abstractmethod


class Employee(ABC):
    """
    Base class for all employee types.
    Cannot be created directly — you must use Manager, Engineer, or Director.
    """

    def __init__(self, name: str, employee_id: str, base_salary: float) -> None:
        # TIP: always save common attributes in the base class __init__
        self.name = name
        self.employee_id = employee_id
        self.base_salary = base_salary

    @abstractmethod
    def get_total_compensation(self) -> float:
        """Return total pay including bonus. Round to 2 decimal places."""
        ...

    @abstractmethod
    def get_role(self) -> str:
        """Return the job title (e.g. 'Manager', 'Engineer', 'Director')."""
        ...

    def __repr__(self) -> str:
        return (
            f"<{self.get_role()} {self.name} "
            f"(id={self.employee_id}) "
            f"comp=${self.get_total_compensation():.2f}>"
        )


class Manager(Employee):
    """
    A Manager gets a 20% bonus.
    Also has a team_size — how many people they manage.
    """

    def __init__(self, name: str, employee_id: str, base_salary: float, team_size: int) -> None:
        # Always call super().__init__() first — sets up name, employee_id, base_salary
        super().__init__(name, employee_id, base_salary)
        self.team_size = team_size

    def get_role(self) -> str:
        return "Manager"

    def get_total_compensation(self) -> float:
        # Manager gets base salary + 20% bonus
        return round(self.base_salary * 1.20, 2)


class Engineer(Employee):
    """
    An Engineer gets a 10% bonus.
    Also has a tech_stack — list of technologies they work with.
    """

    def __init__(self, name: str, employee_id: str, base_salary: float, tech_stack: list[str]) -> None:
        super().__init__(name, employee_id, base_salary)
        self.tech_stack = tech_stack

    def get_role(self) -> str:
        return "Engineer"

    def get_total_compensation(self) -> float:
        # Engineer gets base salary + 10% bonus
        return round(self.base_salary * 1.10, 2)


class Director(Manager):
    """
    A Director gets a 40% bonus.
    Director IS-A Manager — so they also have a team_size.
    Plus they have a department name.

    TIP: Director inherits from Manager (not Employee directly).
    This shows a real "is-a" chain: Director is a Manager, Manager is an Employee.
    """

    def __init__(
        self,
        name: str,
        employee_id: str,
        base_salary: float,
        team_size: int,
        department: str,
    ) -> None:
        # Call Manager's __init__ (which calls Employee's __init__ automatically)
        super().__init__(name, employee_id, base_salary, team_size)
        self.department = department

    def get_role(self) -> str:
        return "Director"

    def get_total_compensation(self) -> float:
        # Director gets base salary + 40% bonus
        return round(self.base_salary * 1.40, 2)
