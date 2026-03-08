"""
example1_basic_class.py
-----------------------
A complete BankAccount class showing the core ideas of classes and objects.

Real-world use: you will define classes like this for every entity in a system.
  Parking lot → ParkingSpot class
  ATM system  → Account class
  Hotel       → Room class

Run this file directly:
    python3 example1_basic_class.py
"""

from datetime import datetime


class BankAccount:
    """
    One bank account belonging to one person.

    It stores: owner name, account number, balance, and a transaction history.
    You can deposit, withdraw, and check the balance.
    """

    def __init__(self, owner: str, account_number: str, initial_balance: float = 0.0) -> None:
        # Always check inputs at the start — never let an object start in a bad state
        if not owner.strip():
            raise ValueError("Owner name cannot be empty")
        if not account_number.strip():
            raise ValueError("Account number cannot be empty")
        if initial_balance < 0:
            raise ValueError(f"Initial balance cannot be negative, got {initial_balance}")

        self.owner: str = owner
        self.account_number: str = account_number
        self._balance: float = initial_balance          # the _ means: "internal, don't touch directly"
        self._opened_at: datetime = datetime.now()
        self._transaction_history: list[str] = []       # a fresh list for EACH account

        if initial_balance > 0:
            self._transaction_history.append(f"Initial deposit: +₹{initial_balance:.2f}")

    def deposit(self, amount: float) -> None:
        """Add money to the account. Amount must be positive."""
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}")
        self._balance += amount
        self._transaction_history.append(f"Deposit: +₹{amount:.2f} | Balance: ₹{self._balance:.2f}")

    def withdraw(self, amount: float) -> None:
        """Take money out. Amount must be positive and not more than the balance."""
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive, got {amount}")
        if amount > self._balance:
            raise ValueError(
                f"Not enough money: balance is ₹{self._balance:.2f}, "
                f"you want to withdraw ₹{amount:.2f}"
            )
        self._balance -= amount
        self._transaction_history.append(f"Withdrawal: -₹{amount:.2f} | Balance: ₹{self._balance:.2f}")

    def get_balance(self) -> float:
        """Return the current balance."""
        return self._balance

    def get_transaction_history(self) -> list[str]:
        """Return a copy of the transaction history list."""
        return list(self._transaction_history)  # return a copy so nobody can change the original

    def __repr__(self) -> str:
        # TIP: always define __repr__ — it shows you what is inside the object when debugging
        return (
            f"BankAccount("
            f"owner={self.owner!r}, "
            f"account_number={self.account_number!r}, "
            f"balance={self._balance:.2f})"
        )

    def __str__(self) -> str:
        # __str__ is what shows up when you do print(account)
        return f"Account [{self.account_number}] | Owner: {self.owner} | Balance: ₹{self._balance:.2f}"


# =============================================================================
# RUN THIS TO SEE IT IN ACTION
# =============================================================================

if __name__ == "__main__":
    print("=== BankAccount Demo ===\n")

    # --- Creating objects ---
    # Each call to BankAccount() creates one NEW object in memory
    rahul_account = BankAccount("Rahul", "ACC001", 1000.0)
    priya_account = BankAccount("Priya", "ACC002", 500.0)

    print(repr(rahul_account))   # developer view — uses __repr__
    print(rahul_account)         # user view — uses __str__

    # --- Deposits and withdrawals ---
    print("\n--- Rahul's transactions ---")
    rahul_account.deposit(250.0)
    print(rahul_account)

    rahul_account.withdraw(100.0)
    print(rahul_account)

    # --- Transaction history ---
    print("\n--- Rahul's history ---")
    for entry in rahul_account.get_transaction_history():
        print(f"  {entry}")

    # --- Catching errors ---
    print("\n--- Errors are caught early ---")
    try:
        rahul_account.deposit(-50)
    except ValueError as e:
        print(f"Error caught: {e}")

    try:
        priya_account.withdraw(10000)  # more than balance
    except ValueError as e:
        print(f"Error caught: {e}")

    print("\nDone!")
