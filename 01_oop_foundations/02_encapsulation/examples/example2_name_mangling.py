"""
example2_name_mangling.py
-------------------------
Advanced topic — explains Python's attribute naming conventions.

What's in here:
  - The _ (single underscore) convention — signals an internal attribute
  - A brief note on __ (double underscore / name mangling) for completeness

Run this file directly:
    python3 example2_name_mangling.py
"""


# =============================================================================
# Python's attribute naming conventions
# =============================================================================
#
# In Python, there is no truly "private" variable. But there is a convention:
#
#   self.name       → public   — anyone can read and write this
#   self._name      → internal — "I wrote this for internal use, be careful"
#   self.__name     → advanced — name mangling (rarely needed)
#
# The single underscore _ is the most common choice for internal attributes.
# It signals: "this is an internal detail, access it through the public methods."

class BankAccount:
    """
    Simple example showing the _ convention.

    _balance has a single underscore.
    It signals: use deposit() and withdraw() to change the balance.
    Don't set self._balance directly from outside the class.
    """

    def __init__(self, owner: str, balance: float) -> None:
        self.owner = owner           # public — fine to access directly
        self._balance = balance      # internal — access through methods

    def deposit(self, amount: float) -> None:
        """The correct way to add money."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount

    def get_balance(self) -> float:
        """The correct way to read the balance."""
        return self._balance

    def __repr__(self) -> str:
        return f"BankAccount({self.owner}, ₹{self._balance})"


# =============================================================================
# RUN THIS TO SEE IT IN ACTION
# =============================================================================

if __name__ == "__main__":
    print("=== Single Underscore Convention ===\n")

    acc = BankAccount("Rahul", 1000)

    # Correct way — use the public method
    acc.deposit(500)
    print(f"Balance via get_balance(): {acc.get_balance()}")

    # You CAN access _balance directly — Python does not stop you
    # But you SHOULD NOT in real code. The underscore is a warning sign.
    print(f"Balance via _balance directly: {acc._balance}")

    print("\nKey takeaway:")
    print("Use a single underscore _ to mark internal attributes.")
    print("It is a convention — a signal to other developers, not a lock.")
    print("In practice, you will see self._balance, self._bookings, self._items, etc.")
