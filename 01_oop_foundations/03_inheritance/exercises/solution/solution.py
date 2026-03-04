"""
Solution: Employee Compensation Hierarchy
"""
from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, name: str, employee_id: str, base_salary: float) -> None:
        self.name = name
        self.employee_id = employee_id
        self.base_salary = base_salary

    @abstractmethod
    def get_total_compensation(self) -> float: ...

    @abstractmethod
    def get_role(self) -> str: ...

    def __repr__(self) -> str:
        return (
            f"<{self.get_role()} {self.name} "
            f"(id={self.employee_id}) "
            f"comp=${self.get_total_compensation():.2f}>"
        )


class Manager(Employee):
    def __init__(self, name: str, employee_id: str, base_salary: float, team_size: int) -> None:
        super().__init__(name, employee_id, base_salary)
        self.team_size = team_size

    def get_role(self) -> str:
        return "Manager"

    def get_total_compensation(self) -> float:
        return round(self.base_salary * 1.20, 2)


class Engineer(Employee):
    def __init__(self, name: str, employee_id: str, base_salary: float, tech_stack: list[str]) -> None:
        super().__init__(name, employee_id, base_salary)
        self.tech_stack = tech_stack

    def get_role(self) -> str:
        return "Engineer"

    def get_total_compensation(self) -> float:
        return round(self.base_salary * 1.10, 2)


class Director(Manager):
    def __init__(
        self,
        name: str,
        employee_id: str,
        base_salary: float,
        team_size: int,
        department: str,
    ) -> None:
        super().__init__(name, employee_id, base_salary, team_size)
        self.department = department

    def get_role(self) -> str:
        return "Director"

    def get_total_compensation(self) -> float:
        return round(self.base_salary * 1.40, 2)
