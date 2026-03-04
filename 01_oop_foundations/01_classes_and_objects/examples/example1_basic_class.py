"""
example1_basic_class.py
-----------------------
Demonstrates the fundamentals of Python classes using a BankAccount example.

Concepts covered:
  - Defining a class with __init__
  - Instance variables vs class variables
  - Instance methods
  - __repr__ and __str__
  - Input validation in the constructor
  - Creating and using objects

Run this file directly:
    python3 example1_basic_class.py
"""

from datetime import datetime


# =============================================================================
# THE CLASS DEFINITION
# =============================================================================

class BankAccount:
    """
    A simple bank account that demonstrates core class concepts.

    A class is a blueprint. This blueprint defines:
      - What data a bank account holds (owner, account_number, balance)
      - What operations you can perform (deposit, withdraw, get_balance)
    """

    # -------------------------------------------------------------------------
    # CLASS VARIABLE (shared by ALL instances)
    # -------------------------------------------------------------------------
    # This is defined on the class itself, not on any specific instance.
    # Every BankAccount object shares this one value.
    # Useful for things like: default interest rate, bank name, counters.
    interest_rate: float = 0.03  # 3% annual interest rate for all accounts

    # -------------------------------------------------------------------------
    # __init__: The Constructor
    # -------------------------------------------------------------------------
    # Python calls __init__ automatically when you do: BankAccount("Alice", "ACC001")
    # The job of __init__ is to set up the object's INSTANCE VARIABLES —
    # the data that belongs to THIS specific object, not all objects.
    #
    # 'self' is a reference to the object being created. When you write
    # self.owner = owner, you're saying: "store the value of the 'owner'
    # parameter on THIS specific account object."
    def __init__(self, owner: str, account_number: str, initial_balance: float = 0.0) -> None:
        """
        Initialize a new BankAccount.

        Args:
            owner:           The name of the account holder.
            account_number:  A unique identifier for this account.
            initial_balance: Starting balance. Must be >= 0. Defaults to 0.0.

        Raises:
            ValueError: If initial_balance is negative.
            TypeError:  If owner or account_number are not strings.
        """
        # --- Validation ---
        # Always validate inputs in __init__. This ensures the object is
        # ALWAYS in a valid state from the moment it is created.
        # An object in an invalid state causes bugs that are hard to track down.
        if not isinstance(owner, str) or not owner.strip():
            raise TypeError("owner must be a non-empty string.")
        if not isinstance(account_number, str) or not account_number.strip():
            raise TypeError("account_number must be a non-empty string.")
        if initial_balance < 0:
            raise ValueError(f"Initial balance cannot be negative, got {initial_balance}.")

        # --- Instance Variables ---
        # These are stored on 'self', meaning each object has its own copy.
        self.owner: str = owner                  # Public: fine to read directly
        self.account_number: str = account_number  # Public: stable identifier

        # The leading underscore on _balance signals to other developers:
        # "this is an internal detail — don't modify it directly from outside."
        # This is a CONVENTION in Python (not enforced by the language).
        self._balance: float = initial_balance

        # A private record of when this account was opened.
        self._opened_at: datetime = datetime.now()

        # A list to record transactions. Note: we create a NEW list for each
        # object — we do NOT use a mutable default argument (a common bug).
        self._transaction_history: list[str] = []

        # Record the initial deposit if there was one
        if initial_balance > 0:
            self._transaction_history.append(f"Initial deposit: +${initial_balance:.2f}")

    # -------------------------------------------------------------------------
    # INSTANCE METHODS
    # -------------------------------------------------------------------------
    # Methods are functions defined inside a class. They always receive 'self'
    # as their first argument — Python passes it automatically when you call
    # account.deposit(100). You never pass self explicitly.

    def deposit(self, amount: float) -> None:
        """
        Add funds to the account.

        Args:
            amount: The amount to deposit. Must be a positive number.

        Raises:
            ValueError: If amount is not positive.
        """
        # Validate every public method's inputs — don't assume callers are careful
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}.")

        self._balance += amount
        self._transaction_history.append(f"Deposit: +${amount:.2f} | New balance: ${self._balance:.2f}")

    def withdraw(self, amount: float) -> None:
        """
        Remove funds from the account.

        Args:
            amount: The amount to withdraw. Must be positive and <= current balance.

        Raises:
            ValueError: If amount is not positive, or exceeds available balance.
        """
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive, got {amount}.")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds: balance is ${self._balance:.2f}, "
                f"requested ${amount:.2f}."
            )

        self._balance -= amount
        self._transaction_history.append(f"Withdrawal: -${amount:.2f} | New balance: ${self._balance:.2f}")

    def get_balance(self) -> float:
        """Return the current account balance."""
        return self._balance

    def get_transaction_history(self) -> list[str]:
        """Return a copy of the transaction history."""
        # Return a copy so callers cannot mutate the internal list
        return list(self._transaction_history)

    def apply_interest(self) -> None:
        """Apply the annual interest rate to the current balance."""
        # We access the class variable via self — Python looks it up on the class
        # if it's not found on the instance.
        interest_earned = self._balance * BankAccount.interest_rate
        self.deposit(interest_earned)
        self._transaction_history[-1] = (
            self._transaction_history[-1].replace("Deposit:", "Interest:")
        )

    # -------------------------------------------------------------------------
    # __repr__: Developer-Facing String Representation
    # -------------------------------------------------------------------------
    # This is the MOST IMPORTANT dunder to define. It appears in:
    #   - The Python REPL when you evaluate an expression
    #   - Logs and error messages
    #   - Inside collections: print([account1, account2])
    #
    # The goal: provide enough information to understand the object's state.
    # Ideal: the string could be used to reconstruct the object.
    def __repr__(self) -> str:
        return (
            f"BankAccount("
            f"owner={self.owner!r}, "         # !r adds quotes around strings
            f"account_number={self.account_number!r}, "
            f"balance={self._balance:.2f}"
            f")"
        )

    # -------------------------------------------------------------------------
    # __str__: User-Facing String Representation
    # -------------------------------------------------------------------------
    # This appears when you call str(account) or print(account).
    # It should be human-readable, not necessarily reconstructable.
    # If __str__ is not defined, Python falls back to __repr__.
    def __str__(self) -> str:
        return (
            f"Account [{self.account_number}] | "
            f"Owner: {self.owner} | "
            f"Balance: ${self._balance:.2f}"
        )

    # -------------------------------------------------------------------------
    # __eq__: Equality Comparison
    # -------------------------------------------------------------------------
    # By default, two objects are equal only if they are the SAME object (same
    # memory address). account1 == account2 would be False even if both have the
    # same owner and balance, unless we override __eq__.
    #
    # For bank accounts, two accounts are "the same" if they have the same
    # account_number — that is the stable, unique identity.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented  # Let Python handle comparison with other types
        return self.account_number == other.account_number

    # -------------------------------------------------------------------------
    # __hash__: Hash Value for Use in Sets and Dicts
    # -------------------------------------------------------------------------
    # RULE: If you define __eq__, you must define __hash__ (or set it to None
    # if objects should be unhashable).
    # __hash__ must be consistent with __eq__: objects that are equal must have
    # the same hash.
    def __hash__(self) -> int:
        return hash(self.account_number)


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("BankAccount Class Demonstration")
    print("=" * 60)

    # --- Creating objects ---
    # Each call to BankAccount(...) creates a brand new object in memory.
    # Each object has its own _balance, _transaction_history, etc.
    print("\n--- Creating Accounts ---")
    alice_account = BankAccount("Alice", "ACC001", 1000.0)
    bob_account = BankAccount("Bob", "ACC002", 500.0)

    # __repr__ is what you see in the REPL or when printing with repr()
    print(repr(alice_account))   # BankAccount(owner='Alice', ...)
    print(repr(bob_account))

    # __str__ is what you see with print() or str()
    print(str(alice_account))    # Account [ACC001] | Owner: Alice | Balance: $1000.00

    # --- Calling methods ---
    print("\n--- Performing Transactions ---")
    alice_account.deposit(250.0)
    print(f"After deposit:     {alice_account}")

    alice_account.withdraw(100.0)
    print(f"After withdrawal:  {alice_account}")

    alice_account.apply_interest()
    print(f"After interest:    {alice_account}")

    # --- Transaction history ---
    print("\n--- Alice's Transaction History ---")
    for entry in alice_account.get_transaction_history():
        print(f"  {entry}")

    # --- Class variables are shared ---
    print("\n--- Class Variables ---")
    print(f"Interest rate (via class):    {BankAccount.interest_rate}")
    print(f"Interest rate (via instance): {alice_account.interest_rate}")
    # Modifying via the class affects all instances
    BankAccount.interest_rate = 0.05
    print(f"After updating class rate:    {bob_account.interest_rate}")

    # --- Equality and hashing ---
    print("\n--- Equality and Hashing ---")
    alice_copy = BankAccount("Alice Duplicate", "ACC001", 9999.0)
    # Same account_number → equal, even though other data differs
    print(f"alice_account == alice_copy: {alice_account == alice_copy}")   # True
    print(f"alice_account == bob_account: {alice_account == bob_account}") # False

    # Because we defined __hash__, we can use accounts in sets and as dict keys
    account_set = {alice_account, bob_account, alice_copy}
    print(f"Accounts in set (deduped by account_number): {len(account_set)}")  # 2

    # --- Error handling ---
    print("\n--- Validation Errors ---")
    try:
        alice_account.deposit(-50)
    except ValueError as e:
        print(f"Caught error: {e}")

    try:
        bob_account.withdraw(1000)  # more than balance
    except ValueError as e:
        print(f"Caught error: {e}")

    try:
        bad_account = BankAccount("", "ACC003")
    except TypeError as e:
        print(f"Caught error: {e}")

    print("\nDone.")
