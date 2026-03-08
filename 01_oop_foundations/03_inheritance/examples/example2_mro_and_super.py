"""
example2_mro_and_super.py
--------------------------
Advanced topic — covers Mixins and how super() behaves with multiple parents.

What's in here:
  - Mixin — a small class that adds one feature to any class that includes it
  - super() works cooperatively whether you have one parent or multiple

Run this file directly:
    python3 example2_mro_and_super.py
"""

from datetime import datetime


# =============================================================================
# Mixin — a class that adds one extra feature without being a full parent class
# =============================================================================
#
# A mixin is a small class that does ONE thing.
# You mix it into other classes to give them that feature.
# It is like a plugin.

class LoggingMixin:
    """
    Adds a log() method to any class.
    You mix this in if you want logging.
    """

    def log(self, message: str) -> None:
        time = datetime.now().strftime("%H:%M:%S")
        print(f"[{time}] {self.__class__.__name__}: {message}")


# =============================================================================
# Using the mixin
# =============================================================================

class Employee(LoggingMixin):
    """
    Employee gains log() from LoggingMixin.
    super() in __init__ calls LoggingMixin (then object) automatically.
    """

    def __init__(self, name: str, role: str) -> None:
        super().__init__()    # good practice — always call super().__init__()
        self.name = name
        self.role = role

    def promote(self, new_role: str) -> None:
        self.log(f"{self.name} promoted from {self.role} to {new_role}")
        self.role = new_role


class OrderService(LoggingMixin):
    """
    A completely different class that also uses LoggingMixin.
    Same mixin, different class — no code duplication.
    """

    def __init__(self) -> None:
        super().__init__()
        self._orders: list[str] = []

    def place_order(self, order_id: str) -> None:
        self._orders.append(order_id)
        self.log(f"Order placed: {order_id}")


# =============================================================================
# RUN THIS TO SEE IT IN ACTION
# =============================================================================

if __name__ == "__main__":
    print("=== Mixin Demo ===\n")

    emp = Employee("Priya", "Engineer")
    emp.log("Starting work today")
    emp.promote("Senior Engineer")

    print()

    service = OrderService()
    service.place_order("ORD-001")
    service.place_order("ORD-002")

    print("\nKey takeaway:")
    print("A mixin is a small class that adds one feature.")
    print("Different unrelated classes can use the same mixin.")
    print("This is an advanced pattern — useful once you are comfortable with basic inheritance.")
