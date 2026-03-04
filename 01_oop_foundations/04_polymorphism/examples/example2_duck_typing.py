"""
Example 2: Duck Typing and typing.Protocol
==========================================

"If it walks like a duck and quacks like a duck, it's a duck."

This example demonstrates Python's structural polymorphism: objects are
compatible not because they share a base class, but because they share the
right methods. No inheritance is required.

We also show typing.Protocol — Python 3.8+'s way to make duck typing explicit
and statically checkable, without forcing classes into an inheritance hierarchy.

Key ideas demonstrated:
- Duck typing: functions that accept anything with the right method
- Three loggers with no common base class
- typing.Protocol for structural subtyping with type annotations
- runtime_checkable: using isinstance() with a Protocol
- How duck typing differs from Java-style interface requirements
- When to prefer Protocol vs ABC
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# typing.Protocol: define the expected "shape" of a Logger
# ---------------------------------------------------------------------------

@runtime_checkable
class LoggerProtocol(Protocol):
    """
    Structural type: anything with a log(msg: str) method is a Logger.

    This is NOT an ABC. Classes do NOT inherit from this.
    The Protocol simply describes what interface we expect.

    With @runtime_checkable, isinstance(obj, LoggerProtocol) works
    at runtime (checks only for method presence, not signatures).
    """

    def log(self, msg: str) -> None:
        """Log a message."""
        ...


# ---------------------------------------------------------------------------
# Concrete loggers — no common base class, no explicit interface
# ---------------------------------------------------------------------------

class ConsoleLogger:
    """
    Logs messages to stdout with timestamps.

    Does NOT inherit from LoggerProtocol or any ABC.
    It "is" a logger purely because it has a log() method.
    """

    def __init__(self, prefix: str = "APP") -> None:
        self.prefix = prefix

    def log(self, msg: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] [{self.prefix}] {msg}")


@dataclass
class FileLogger:
    """
    Appends log messages to a file.

    Also does NOT inherit from any base class.
    Compatible with LoggerProtocol because it has log().
    """

    filepath: str
    _entries: list[str] = field(default_factory=list, repr=False)

    def log(self, msg: str) -> None:
        timestamp = datetime.now().isoformat()
        entry = f"{timestamp} | {msg}"
        self._entries.append(entry)
        # In a real implementation: write to self.filepath
        # Here we keep it in memory for demo purposes
        print(f"[FILE:{self.filepath}] {entry}")

    def get_entries(self) -> list[str]:
        return list(self._entries)


class NullLogger:
    """
    Silently discards all log messages.

    Useful for testing, or when logging is optional. Follows the
    Null Object pattern: the caller never needs to check 'if logger:'.
    """

    def log(self, msg: str) -> None:
        pass  # intentionally silent


@dataclass
class BufferedLogger:
    """
    Collects log messages in memory and flushes on demand.
    Good for testing — lets you assert what was logged.
    """

    _buffer: list[str] = field(default_factory=list)

    def log(self, msg: str) -> None:
        self._buffer.append(msg)

    def flush(self) -> list[str]:
        """Return all buffered messages and clear the buffer."""
        messages = list(self._buffer)
        self._buffer.clear()
        return messages

    def get_buffer(self) -> list[str]:
        return list(self._buffer)


# ---------------------------------------------------------------------------
# Functions that accept anything with a .log() method
# ---------------------------------------------------------------------------

def run_database_migration(logger: LoggerProtocol) -> bool:
    """
    Simulates a database migration that logs its progress.

    The parameter type is LoggerProtocol — any object with log() works.
    Notice: no isinstance() check anywhere in this function.
    """
    logger.log("Starting database migration...")
    logger.log("Backing up existing data...")
    logger.log("Applying schema changes...")
    logger.log("Verifying data integrity...")
    logger.log("Migration complete.")
    return True


def process_items(items: list[str], logger: LoggerProtocol) -> list[str]:
    """
    Processes items and logs each step.
    Works with any logger: console, file, null, buffered, or custom.
    """
    results: list[str] = []
    for item in items:
        logger.log(f"Processing: {item}")
        processed = item.upper().strip()
        results.append(processed)
        logger.log(f"Result: {processed}")
    return results


def create_user(
    username: str,
    email: str,
    logger: Optional[LoggerProtocol] = None,
) -> dict:
    """
    Creates a user record.

    Logger is optional — if not provided, uses NullLogger internally
    (instead of checking 'if logger is not None' everywhere).
    """
    effective_logger: LoggerProtocol = logger if logger is not None else NullLogger()

    effective_logger.log(f"Creating user: {username}")
    user = {"username": username, "email": email, "active": True}
    effective_logger.log(f"User created: {user}")
    return user


# ---------------------------------------------------------------------------
# Contrast: Java-style vs Python duck typing
# ---------------------------------------------------------------------------

def java_style_explanation() -> None:
    """
    In Java or C#, you MUST declare that a class implements an interface:

        // Java
        public interface Logger {
            void log(String msg);
        }

        public class ConsoleLogger implements Logger {  // explicit
            public void log(String msg) { ... }
        }

        public class FileLogger implements Logger {     // explicit
            public void log(String msg) { ... }
        }

    If you forget 'implements Logger', the compiler rejects it even if
    the method is perfectly compatible.

    In Python, the connection is implicit:
    - No 'implements' keyword needed
    - The runtime checks for the method at call time
    - typing.Protocol makes this EXPLICIT for type checkers (mypy/pyright)
      without requiring any inheritance

    This means you can use third-party classes as loggers without modifying
    them — as long as they have a log() method, they fit the protocol.
    """
    print("[Note] See docstring for Java vs Python comparison")


# ---------------------------------------------------------------------------
# Demonstrate runtime_checkable
# ---------------------------------------------------------------------------

def show_runtime_isinstance_with_protocol() -> None:
    """
    With @runtime_checkable, isinstance() checks for method presence.

    IMPORTANT: This only checks that the method NAME exists, not its
    signature. A type checker like mypy does the full signature check.
    """
    console = ConsoleLogger()
    file_log = FileLogger(filepath="/tmp/app.log")
    null_log = NullLogger()
    buffered = BufferedLogger()

    loggers = [console, file_log, null_log, buffered]
    print("isinstance(obj, LoggerProtocol) checks:")
    for logger in loggers:
        result = isinstance(logger, LoggerProtocol)
        print(f"  {type(logger).__name__:20} -> {result}")

    # An object WITHOUT log() fails the check
    class NotALogger:
        def write(self, msg: str) -> None:
            print(msg)

    not_a_logger = NotALogger()
    print(f"  {'NotALogger':20} -> {isinstance(not_a_logger, LoggerProtocol)}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: Duck Typing and typing.Protocol")
    print("=" * 60)

    # --- Part 1: All loggers work in run_database_migration() ---
    print("\n[Part 1] ConsoleLogger — visible output")
    print("-" * 50)
    run_database_migration(ConsoleLogger(prefix="DB"))

    print("\n[Part 2] FileLogger — writes to file (simulated)")
    print("-" * 50)
    file_logger = FileLogger(filepath="/tmp/migration.log")
    run_database_migration(file_logger)
    print(f"Captured {len(file_logger.get_entries())} log entries")

    print("\n[Part 3] NullLogger — silent (no output)")
    print("-" * 50)
    null_logger = NullLogger()
    result = run_database_migration(null_logger)
    print(f"Migration returned: {result} (logger was silent)")

    # --- Part 2: BufferedLogger for testing ---
    print("\n[Part 4] BufferedLogger — capture output for assertions")
    print("-" * 50)
    buffered = BufferedLogger()
    items = ["  hello  ", "world", "python"]
    processed = process_items(items, buffered)
    print(f"Processed items: {processed}")
    messages = buffered.flush()
    print(f"Captured {len(messages)} log messages:")
    for msg in messages:
        print(f"  >> {msg}")

    # --- Part 3: Optional logger with NullLogger fallback ---
    print("\n[Part 5] Optional logger — NullLogger as default")
    print("-" * 50)
    user_a = create_user("alice", "alice@example.com")
    print(f"Created (no logger): {user_a}")

    user_b = create_user("bob", "bob@example.com", logger=ConsoleLogger("AUTH"))
    print(f"Created (with logger): {user_b}")

    # --- Part 4: runtime_checkable isinstance ---
    print("\n[Part 6] runtime_checkable Protocol isinstance() check")
    print("-" * 50)
    show_runtime_isinstance_with_protocol()

    # --- Part 5: Third-party "duck" logger (no inheritance) ---
    print("\n[Part 7] Third-party class with log() — fits the protocol")
    print("-" * 50)

    class ThirdPartyLibraryLogger:
        """Imagine this comes from a library we cannot modify."""

        def log(self, msg: str) -> None:
            print(f"[THIRD-PARTY] {msg}")

    third_party = ThirdPartyLibraryLogger()
    print(f"isinstance check: {isinstance(third_party, LoggerProtocol)}")
    run_database_migration(third_party)   # works perfectly — duck typing

    print("\n--- End of demo ---")
    print("\nKey takeaway: LoggerProtocol defines WHAT is needed.")
    print("Classes don't inherit from it — they just need the method.")
    print("This lets you use any compatible object without modifying it.")
