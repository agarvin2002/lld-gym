"""
example2_duck_typing.py
-----------------------
Advanced topic — shows duck typing, Python's structural polymorphism.

What's in here:
  - Duck typing: "if an object has the right method, it can be used"
  - How to write functions that work with any compatible object, without ABC

Run this file directly:
    python3 example2_duck_typing.py
"""


# =============================================================================
# Duck typing — no inheritance needed
# =============================================================================
#
# In Python, if an object has the method you need, you can use it.
# You don't HAVE to inherit from a common base class.
# This is called "duck typing": if it walks like a duck and quacks like a duck,
# it IS a duck.

class ConsoleLogger:
    """Prints messages to the screen."""

    def log(self, msg: str) -> None:
        print(f"[CONSOLE] {msg}")


class FileLogger:
    """Saves messages to a file (simulated here as a list)."""

    def __init__(self) -> None:
        self._entries: list[str] = []

    def log(self, msg: str) -> None:
        self._entries.append(msg)
        # in real code: write to a file

    def get_entries(self) -> list[str]:
        return list(self._entries)


class NullLogger:
    """Silently ignores all messages. Useful in tests."""

    def log(self, msg: str) -> None:
        pass   # do nothing — intentionally silent


# =============================================================================
# A function that accepts ANY logger — no ABC needed
# =============================================================================

def process_payment(amount: float, logger) -> bool:
    """
    Process a payment and log the steps.
    Works with ConsoleLogger, FileLogger, or NullLogger — or any object with log().
    No isinstance() check. No ABC. Just duck typing.
    """
    logger.log(f"Starting payment of ₹{amount:.2f}")
    logger.log("Contacting payment gateway...")
    logger.log(f"Payment of ₹{amount:.2f} successful")
    return True


# =============================================================================
# RUN THIS TO SEE IT IN ACTION
# =============================================================================

if __name__ == "__main__":
    print("=== Duck Typing Demo ===\n")

    print("--- ConsoleLogger (visible output) ---")
    process_payment(599.0, ConsoleLogger())

    print("\n--- FileLogger (saved in memory) ---")
    file_log = FileLogger()
    process_payment(299.0, file_log)
    print(f"Captured {len(file_log.get_entries())} log entries")

    print("\n--- NullLogger (silent) ---")
    process_payment(199.0, NullLogger())
    print("(no output — NullLogger swallowed everything)")

    print("\nKey takeaway:")
    print("All three loggers have log(). That's enough — no ABC needed.")
    print("Use ABC when you design and own the classes.")
    print("Duck typing is useful when working with classes from external libraries.")
