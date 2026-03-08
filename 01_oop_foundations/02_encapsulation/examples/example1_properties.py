"""
example1_properties.py
----------------------
Shows WHY @property is useful — with a before/after example.

Real-world use: @property is useful when you need to:
  - Make a field read-only (e.g., ticket_id should not change after booking)
  - Validate before saving (e.g., seat count must be > 0)

Run this file directly:
    python3 example1_properties.py
"""


# =============================================================================
# PART 1a: THE PROBLEM — public attribute with no protection
# =============================================================================

class BankAccountNaive:
    """
    Bad version: balance is a plain public attribute.
    Anyone can set it to any value — even negative.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = initial_balance   # no protection — anyone can overwrite this


# =============================================================================
# PART 1b: THE FIX — @property with validation
# =============================================================================

class BankAccountBetter:
    """
    Good version: balance is protected by @property.

    You can READ balance easily: account.balance
    But you cannot set it to an invalid value.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = initial_balance   # this calls the setter below (validation runs in __init__ too)

    # The getter — called when you do: account.balance
    @property
    def balance(self) -> float:
        """Read the balance."""
        return self._balance

    # The setter — called when you do: account.balance = 500
    @balance.setter
    def balance(self, value: float) -> None:
        """Set the balance. Rejects negative values."""
        if value < 0:
            raise ValueError(f"Balance cannot be negative, got {value}")
        self._balance = float(value)

    def deposit(self, amount: float) -> None:
        """Add money. Only this method changes the balance."""
        if amount <= 0:
            raise ValueError(f"Deposit must be positive, got {amount}")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Remove money. Cannot go below zero."""
        if amount <= 0:
            raise ValueError(f"Withdrawal must be positive, got {amount}")
        if amount > self._balance:
            raise ValueError(f"Not enough balance: have ₹{self._balance:.2f}, want ₹{amount:.2f}")
        self._balance -= amount

    def __repr__(self) -> str:
        return f"BankAccountBetter(owner={self.owner!r}, balance={self._balance:.2f})"

    def __str__(self) -> str:
        return f"{self.owner}'s account — Balance: ₹{self._balance:.2f}"


# =============================================================================
# PART 2: Read-only property (no setter)
# =============================================================================

class BookingTicket:
    """
    Once a ticket is created, the ticket_id must never change.
    We use @property with NO setter to make it read-only.

    In real systems like hotel booking or movie ticketing,
    the booking ID should always be read-only.
    """

    def __init__(self, ticket_id: str, movie: str, seat: str) -> None:
        self._ticket_id = ticket_id   # stored internally
        self.movie = movie
        self.seat = seat

    @property
    def ticket_id(self) -> str:
        """Ticket ID — read-only, never changes."""
        return self._ticket_id   # no setter = read-only

    def __repr__(self) -> str:
        return f"Ticket({self._ticket_id} | {self.movie} | seat {self.seat})"


# =============================================================================
# RUN THIS TO SEE IT IN ACTION
# =============================================================================

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    print("=== Part 1a: The problem with no protection ===\n")
    naive = BankAccountNaive("Alice", 1000.0)
    print(f"Balance: {naive.balance}")

    naive.balance = -99999          # Python allows this! Object is now broken.
    print(f"After naive.balance = -99999: {naive.balance}")
    print("  ↑ This is a bug! No error was raised.\n")

    # -------------------------------------------------------------------------
    print("=== Part 1b: @property stops the bad value ===\n")
    account = BankAccountBetter("Rahul", 500.0)
    print(account)

    account.deposit(200.0)
    print(f"After deposit: {account}")

    account.withdraw(100.0)
    print(f"After withdrawal: {account}")

    print("\nTrying to set balance to -500 directly:")
    try:
        account.balance = -500          # calls the setter, which raises ValueError
    except ValueError as e:
        print(f"  Error caught: {e}")

    # -------------------------------------------------------------------------
    print("\n=== Part 2: Read-only property ===\n")
    ticket = BookingTicket("TKT-001", "Pushpa 2", "A7")
    print(ticket)
    print(f"Ticket ID: {ticket.ticket_id}")

    print("\nTrying to change the ticket ID:")
    try:
        ticket.ticket_id = "TKT-HACKED"    # no setter, raises AttributeError
    except AttributeError as e:
        print(f"  Error caught: {e}")

    print("\nDone!")
