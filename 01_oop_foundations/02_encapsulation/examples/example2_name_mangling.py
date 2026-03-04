"""
example2_name_mangling.py
-------------------------
Demonstrates Python's name mangling for double-underscore attributes,
and explains when to use _ vs __ in practice.

Concepts covered:
  - What name mangling actually does (technical mechanism)
  - Why __ exists (preventing subclass name collisions, not security)
  - When to use _protected vs __private
  - A practical example: PasswordManager
  - Best practices and common misconceptions

Run this file directly:
    python3 example2_name_mangling.py
"""


# =============================================================================
# PART 1: What Name Mangling Actually Does
# =============================================================================

class ExplainMangling:
    """
    Minimal class to show name mangling in isolation.
    """

    def __init__(self) -> None:
        self.public = "anyone can read/write this"
        self._protected = "convention: internal detail, handle with care"
        self.__private = "name-mangled: stored as _ExplainMangling__private"

    def get_private(self) -> str:
        """Access __private from inside the class — works fine."""
        return self.__private  # Python translates this to self._ExplainMangling__private

    def show_all(self) -> None:
        print(f"  public:            {self.public}")
        print(f"  _protected:        {self._protected}")
        print(f"  __private (via method): {self.__private}")


# =============================================================================
# PART 2: Why __ Exists — Subclass Name Collision Prevention
# =============================================================================
# The purpose of __ is NOT security.
# The purpose is to avoid ACCIDENTAL attribute collisions in subclasses.
# Without mangling, a subclass that defines a method with the same name as
# a parent's "private" attribute would silently overwrite it.

class Base:
    def __init__(self) -> None:
        # With mangling, this becomes _Base__value
        # Subclasses defining their own __value won't collide with this.
        self.__value = "Base's value"

    def get_base_value(self) -> str:
        return self.__value  # Accesses _Base__value


class Child(Base):
    def __init__(self) -> None:
        super().__init__()
        # This becomes _Child__value — does NOT collide with _Base__value
        self.__value = "Child's value"

    def get_child_value(self) -> str:
        return self.__value  # Accesses _Child__value


# =============================================================================
# PART 3: Practical Example — PasswordManager
# =============================================================================

import hashlib
import secrets


class PasswordManager:
    """
    Manages a hashed password for a user account.

    Uses __password (name mangling) to demonstrate the pattern,
    while acknowledging that _ would work just as well for this case.

    Key behaviors:
      - The raw password is NEVER stored — only the hash
      - The hash is stored as a name-mangled attribute
      - Setting a new password goes through a validation method
      - Verification is done by hashing the input and comparing
    """

    # Minimum password requirements
    MIN_LENGTH = 8

    def __init__(self, username: str, initial_password: str) -> None:
        """
        Initialize with a username and initial password.

        The password is immediately hashed — the plaintext is discarded.

        Raises:
            ValueError: If the password does not meet minimum requirements.
        """
        self.username = username
        # _validate_password raises if invalid, so set happens only if valid
        self._validate_password(initial_password)
        # Store the hash, not the plaintext
        # __password_hash becomes _PasswordManager__password_hash
        self.__password_hash: str = self._hash_password(initial_password)

    # -----------------------------------------------------------------------
    # Private helpers (using _ convention — no need for __ here)
    # -----------------------------------------------------------------------

    def _validate_password(self, password: str) -> None:
        """
        Check that the password meets minimum requirements.

        Using _ (not __) because subclasses might want to override validation
        with stricter or more lenient rules. Name mangling would prevent that.
        """
        if len(password) < self.MIN_LENGTH:
            raise ValueError(
                f"Password must be at least {self.MIN_LENGTH} characters, "
                f"got {len(password)}."
            )

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash a password using SHA-256. Returns the hex digest."""
        # In production, use bcrypt or argon2 — SHA-256 is too fast for passwords.
        # This is for demonstration only.
        return hashlib.sha256(password.encode()).hexdigest()

    # -----------------------------------------------------------------------
    # Public interface
    # -----------------------------------------------------------------------

    def verify_password(self, password: str) -> bool:
        """
        Return True if the given password matches the stored hash.

        We compare hashes, never raw passwords. This means even if someone
        reads __password_hash, they don't get the original password.
        """
        return self.__password_hash == self._hash_password(password)

    def change_password(self, old_password: str, new_password: str) -> None:
        """
        Change the password after verifying the old one.

        Raises:
            ValueError: If old_password is incorrect or new_password fails validation.
        """
        if not self.verify_password(old_password):
            raise ValueError("Current password is incorrect.")
        self._validate_password(new_password)
        self.__password_hash = self._hash_password(new_password)
        print(f"Password for {self.username!r} changed successfully.")

    def __repr__(self) -> str:
        """Do NOT include the hash in __repr__ — that's a security leak."""
        return f"PasswordManager(username={self.username!r})"


# =============================================================================
# PART 4: Single Underscore Best Practices
# =============================================================================

class DataProcessor:
    """
    Shows the _ convention for internal methods and attributes.

    Everything prefixed with _ is an "internal implementation detail":
      - Callers should use the public interface, not _ attributes/methods
      - Subclasses CAN access _ attributes (they're not mangled)
      - Tests can access _ attributes if needed (e.g., to verify internal state)
    """

    def __init__(self, data: list[int]) -> None:
        self._raw_data = list(data)      # Internal — callers use get_data()
        self._processed = False          # Tracks processing state

    def process(self) -> None:
        """Public method — the intended way to trigger processing."""
        if self._processed:
            print("Data already processed. Skipping.")
            return
        self._raw_data = self._normalize(self._raw_data)
        self._processed = True

    def get_data(self) -> list[int]:
        """Return a copy of the current data."""
        return list(self._raw_data)

    def _normalize(self, data: list[int]) -> list[int]:
        """
        Internal normalization. Prefixed with _ because callers should use
        process(), not this directly. But subclasses could override this to
        apply different normalization logic.
        """
        if not data:
            return data
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            return [0 for _ in data]
        return [int((x - min_val) / (max_val - min_val) * 100) for x in data]


# =============================================================================
# DEMONSTRATION
# =============================================================================

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    # PART 1: What name mangling does
    # -------------------------------------------------------------------------
    print("=" * 60)
    print("PART 1: Name Mangling Mechanics")
    print("=" * 60)

    obj = ExplainMangling()
    obj.show_all()

    print("\nAccessing attributes from outside the class:")
    print(f"  obj.public:        {obj.public}")       # Works
    print(f"  obj._protected:    {obj._protected}")   # Works (but discouraged)

    # obj.__private would raise AttributeError
    try:
        _ = obj.__private  # type: ignore
    except AttributeError as e:
        print(f"  obj.__private: AttributeError — {e}")

    # But the mangled name IS accessible if you know it:
    print(f"  obj._ExplainMangling__private: {obj._ExplainMangling__private}")

    # You can see ALL attributes (including mangled ones) with vars()
    print("\nvars(obj) — all instance attributes:")
    for attr, val in vars(obj).items():
        print(f"  {attr!r}: {val!r}")

    # -------------------------------------------------------------------------
    # PART 2: Why subclass name collision prevention matters
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PART 2: Subclass Name Collision Prevention")
    print("=" * 60)

    base = Base()
    child = Child()

    print(f"Base.get_base_value():   {base.get_base_value()}")
    print(f"Child.get_base_value():  {child.get_base_value()}")  # Accesses Base's __value
    print(f"Child.get_child_value(): {child.get_child_value()}")  # Accesses Child's __value

    # Show the actual attribute names in the child instance
    print("\nvars(child):")
    for attr, val in vars(child).items():
        print(f"  {attr!r}: {val!r}")
    # Output shows both _Base__value and _Child__value — no collision!

    # -------------------------------------------------------------------------
    # PART 3: PasswordManager
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PART 3: PasswordManager")
    print("=" * 60)

    pm = PasswordManager("alice", "securepassword123")
    print(f"Created: {pm}")

    # Verify correct password
    print(f"\nVerify 'securepassword123': {pm.verify_password('securepassword123')}")   # True
    print(f"Verify 'wrongpassword':     {pm.verify_password('wrongpassword')}")         # False

    # Change password
    pm.change_password("securepassword123", "newpassword456")
    print(f"Verify old password after change: {pm.verify_password('securepassword123')}")  # False
    print(f"Verify new password after change: {pm.verify_password('newpassword456')}")     # True

    # Short password is rejected
    try:
        bad = PasswordManager("bob", "short")
    except ValueError as e:
        print(f"\nShort password rejected: {e}")

    # The hash is accessible via the mangled name — but you cannot reverse it
    print(f"\nMangled attribute name: _PasswordManager__password_hash")
    print(f"Hash value: {pm._PasswordManager__password_hash[:20]}...")  # First 20 chars

    # -------------------------------------------------------------------------
    # PART 4: Single underscore convention
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PART 4: Single Underscore Convention")
    print("=" * 60)

    processor = DataProcessor([10, 20, 50, 80, 100])
    print(f"Before process: {processor.get_data()}")
    processor.process()
    print(f"After process:  {processor.get_data()}")
    processor.process()  # Calling again is a no-op

    # We CAN access _raw_data from outside (useful in tests)
    print(f"\nDirect access to _raw_data: {processor._raw_data}")
    # This works — _ is a convention, not a lock.
    # Use it responsibly: don't do this in production code, but it's fine in tests.

    print("\nDone.")
