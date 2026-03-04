"""
Example 2: MRO (Method Resolution Order) and Mixins

Demonstrates:
- Multiple inheritance with mixins
- super() following MRO (not just direct parent)
- __mro__ inspection
- Diamond inheritance resolution
- Practical mixin pattern for LLD
"""
from datetime import datetime


# ─── Mixin Classes ────────────────────────────────────────────────

class LoggingMixin:
    """Adds logging capability to any class."""

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.__class__.__name__}: {message}")


class TimestampMixin:
    """Adds created_at / updated_at tracking."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)  # pass remaining kwargs up the chain
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

    def touch(self) -> None:
        self.updated_at = datetime.now()


# ─── Real Class Using Mixins ──────────────────────────────────────

class Employee(LoggingMixin, TimestampMixin):
    """Employee that gains logging and timestamps via mixins."""

    def __init__(self, name: str, role: str) -> None:
        super().__init__()  # calls TimestampMixin.__init__ via MRO
        self.name = name
        self.role = role

    def promote(self, new_role: str) -> None:
        self.log(f"Promoted from {self.role} to {new_role}")
        self.role = new_role
        self.touch()  # update timestamp


# ─── MRO Inspection ──────────────────────────────────────────────

def show_mro(cls) -> None:
    print(f"\nMRO for {cls.__name__}:")
    for i, c in enumerate(cls.__mro__):
        print(f"  {i}: {c.__name__}")


# ─── Diamond Inheritance ──────────────────────────────────────────
#
#       A
#      / \
#     B   C
#      \ /
#       D
#
# Without MRO, D.method() would call A.method() twice — the "diamond problem".
# Python's C3 linearization ensures each class is only visited once.

class A:
    def greet(self) -> str:
        return "Hello from A"

class B(A):
    def greet(self) -> str:
        return f"B → {super().greet()}"  # super() follows MRO, not just A

class C(A):
    def greet(self) -> str:
        return f"C → {super().greet()}"  # super() follows MRO

class D(B, C):
    def greet(self) -> str:
        return f"D → {super().greet()}"  # MRO: D → B → C → A


if __name__ == "__main__":
    print("=== Mixin Demo ===")
    emp = Employee("Alice", "Engineer")
    emp.log("Starting work")
    emp.promote("Senior Engineer")
    print(f"Created at: {emp.created_at}")
    print(f"Updated at: {emp.updated_at}")

    show_mro(Employee)

    print("\n=== Diamond Inheritance ===")
    show_mro(D)
    d = D()
    print(f"\nd.greet() = '{d.greet()}'")
    # Output shows each class called once: D → B → C → A

    print("\n=== Key takeaway ===")
    print("super() does NOT mean 'call the direct parent'.")
    print("It means 'call the next class in the MRO'.")
    print("This ensures correct cooperative multiple inheritance.")
