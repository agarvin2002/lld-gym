"""
example1_properties.py
----------------------
Demonstrates Python's @property decorator for controlled attribute access.

Concepts covered:
  - @property getter (read-only attribute)
  - @property.setter with validation
  - @property.deleter
  - Why properties are better than public attributes with raw access
  - BankAccount as a complete, realistic example

Run this file directly:
    python3 example1_properties.py
"""


# =============================================================================
# PART 1: Why Properties Exist — The Problem with Direct Attributes
# =============================================================================

class BankAccountNaive:
    """
    A naive BankAccount with a public balance attribute.

    PROBLEM: There is nothing stopping callers from doing:
        account.balance = -99999
    This puts the object in an invalid state silently.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = initial_balance  # Public — anyone can write to this


class BankAccountBetter:
    """
    An improved BankAccount using @property for controlled access.

    The balance is stored internally as _balance (protected convention).
    External code can READ balance via the property, but can only CHANGE it
    via deposit() and withdraw() — both of which validate inputs.

    This ensures the object is always in a valid state.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        """
        Initialize the account. Note: we assign via self.balance = initial_balance,
        which goes THROUGH the setter — so validation runs even in __init__.
        """
        self.owner = owner
        # Assign via property setter, not _balance directly.
        # This means the __init__ benefits from the same validation as any setter.
        self.balance = initial_balance  # This calls the @balance.setter below

    # -------------------------------------------------------------------------
    # @property: Define a getter
    # -------------------------------------------------------------------------
    # This makes `account.balance` work as a read access, calling this function.
    # From the caller's perspective: account.balance looks like a simple attribute.
    # From the class's perspective: it's a function call we control.
    @property
    def balance(self) -> float:
        """
        Current account balance (read-only from outside).

        Note the docstring goes on the getter — this becomes the property's
        docstring, accessible via help(account.balance) or IDE tooltips.
        """
        return self._balance

    # -------------------------------------------------------------------------
    # @balance.setter: Define a setter
    # -------------------------------------------------------------------------
    # Called when someone does: account.balance = 500
    # We can validate here and reject invalid values.
    #
    # Note: the setter name MUST match the property name exactly.
    @balance.setter
    def balance(self, value: float) -> None:
        """Setter with validation — balance cannot be negative."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"Balance must be a number, got {type(value).__name__}.")
        if value < 0:
            raise ValueError(f"Balance cannot be negative, got {value}.")
        self._balance = float(value)

    # -------------------------------------------------------------------------
    # @balance.deleter: Define a deleter
    # -------------------------------------------------------------------------
    # Called when someone does: del account.balance
    # In practice, deleting a balance is unusual — this just demonstrates syntax.
    @balance.deleter
    def balance(self) -> None:
        """Deleter — removes the internal _balance attribute."""
        print(f"[Warning] Deleting balance for {self.owner}'s account.")
        del self._balance

    # -------------------------------------------------------------------------
    # Public methods for mutating state
    # -------------------------------------------------------------------------
    # These are the ONLY ways to change the balance.
    # Both validate their inputs.

    def deposit(self, amount: float) -> None:
        """Add funds. Amount must be positive."""
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}.")
        # We could write self._balance += amount, but going through the setter
        # is safer in case the setter has additional side effects (like logging).
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Remove funds. Amount must be positive and not exceed balance."""
        if amount <= 0:
            raise ValueError(f"Withdrawal must be positive, got {amount}.")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds: balance is ${self._balance:.2f}, "
                f"requested ${amount:.2f}."
            )
        self._balance -= amount

    def __repr__(self) -> str:
        return f"BankAccountBetter(owner={self.owner!r}, balance={self._balance:.2f})"

    def __str__(self) -> str:
        return f"{self.owner}'s account — Balance: ${self._balance:.2f}"


# =============================================================================
# PART 2: Computed / Derived Properties
# =============================================================================
# A property doesn't have to just return a stored value.
# It can compute a value on the fly from other attributes.

class Rectangle:
    """
    A rectangle where area and perimeter are computed properties.

    Instead of storing area and perimeter as attributes (which would get out of
    sync if width or height changes), we compute them fresh each time they're
    accessed. This ensures consistency.
    """

    def __init__(self, width: float, height: float) -> None:
        # These go through setters, so validation runs in __init__ too
        self.width = width
        self.height = height

    @property
    def width(self) -> float:
        """Width of the rectangle. Must be positive."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"Width must be positive, got {value}.")
        self._width = value

    @property
    def height(self) -> float:
        """Height of the rectangle. Must be positive."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"Height must be positive, got {value}.")
        self._height = value

    # -------------------------------------------------------------------------
    # COMPUTED PROPERTIES — no setter, no stored _area, _perimeter attributes
    # -------------------------------------------------------------------------
    # These are read-only (no setter defined). They're always in sync with
    # width and height because they're computed fresh on every access.

    @property
    def area(self) -> float:
        """Area of the rectangle (width * height). Computed on access."""
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        """Perimeter of the rectangle. Computed on access."""
        return 2 * (self._width + self._height)

    @property
    def is_square(self) -> bool:
        """Return True if width == height."""
        return self._width == self._height

    def __repr__(self) -> str:
        return f"Rectangle(width={self._width}, height={self._height})"

    def __str__(self) -> str:
        return (
            f"Rectangle {self._width}x{self._height} | "
            f"area={self.area}, perimeter={self.perimeter}"
        )


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    # Show the problem with naive direct attribute access
    # -------------------------------------------------------------------------
    print("=" * 60)
    print("PART 1a: The Problem with Public Attributes")
    print("=" * 60)

    naive = BankAccountNaive("Alice", 1000.0)
    print(f"Initial balance: {naive.balance}")

    # This should be illegal — but Python allows it with no validation:
    naive.balance = -99999  # Silent corruption!
    print(f"After naive.balance = -99999: {naive.balance}")  # -99999
    print("  ^^^ This is a bug! The object is now in an invalid state.\n")

    # -------------------------------------------------------------------------
    # Show how @property prevents this
    # -------------------------------------------------------------------------
    print("=" * 60)
    print("PART 1b: @property with Validation")
    print("=" * 60)

    account = BankAccountBetter("Bob", 500.0)
    print(f"Created: {account}")

    # Reading balance via the property (calls the getter)
    print(f"account.balance: {account.balance}")

    # Depositing updates _balance via the method (which directly updates _balance)
    account.deposit(200.0)
    print(f"After deposit($200): {account}")

    # Withdrawing
    account.withdraw(100.0)
    print(f"After withdraw($100): {account}")

    # Trying to set balance directly to a negative value — the setter rejects it
    print("\nTrying to set balance directly to a negative value:")
    try:
        account.balance = -500  # Calls the setter, which raises ValueError
    except ValueError as e:
        print(f"  Caught ValueError: {e}")

    # Trying to set balance to a valid positive value directly
    # (Property allows this — the setter validates and accepts it)
    account.balance = 1000.0
    print(f"After account.balance = 1000.0: {account}")

    # Demonstrating the deleter
    print("\nDemonstrating @balance.deleter:")
    del account.balance  # Calls the deleter

    # -------------------------------------------------------------------------
    # Computed properties
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PART 2: Computed / Derived Properties")
    print("=" * 60)

    rect = Rectangle(6.0, 4.0)
    print(f"Rectangle: {rect}")
    print(f"  area:       {rect.area}")        # 24.0 — computed on access
    print(f"  perimeter:  {rect.perimeter}")   # 20.0 — computed on access
    print(f"  is_square:  {rect.is_square}")   # False

    # Modify width — area and perimeter update automatically
    rect.width = 4.0
    print(f"\nAfter width = 4.0:")
    print(f"  area:       {rect.area}")        # 16.0 — still correct
    print(f"  perimeter:  {rect.perimeter}")   # 16.0
    print(f"  is_square:  {rect.is_square}")   # True

    # Validation on setter
    print("\nTrying to set width to -5:")
    try:
        rect.width = -5
    except ValueError as e:
        print(f"  Caught ValueError: {e}")

    # Trying to set area directly (no setter defined — raises AttributeError)
    print("\nTrying to set area directly (no setter):")
    try:
        rect.area = 100  # type: ignore
    except AttributeError as e:
        print(f"  Caught AttributeError: {e}")

    print("\nDone.")
