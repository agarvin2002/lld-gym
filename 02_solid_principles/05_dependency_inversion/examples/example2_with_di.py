# Advanced topic — constructor injection of abstractions to make services testable and swappable
"""
DIP Example 2: Dependency Injection

UserService depends on abstractions injected from outside.
Testable, swappable, and decoupled.
"""
from abc import ABC, abstractmethod


# ─── Abstractions (the interfaces) ───────────────────────────────

class DatabaseInterface(ABC):
    @abstractmethod
    def query(self, sql: str) -> list: ...


class EmailSenderInterface(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None: ...


class LoggerInterface(ABC):
    @abstractmethod
    def log(self, message: str) -> None: ...


# ─── Production Implementations ───────────────────────────────────

class MySQLDatabase(DatabaseInterface):
    def query(self, sql: str) -> list:
        return [{"id": 1, "name": "Alice"}]  # would use real MySQL


class GmailSender(EmailSenderInterface):
    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"[Gmail] Sending to {to}: {subject}")


class ConsoleLogger(LoggerInterface):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


# ─── Test Doubles (no real infrastructure needed) ─────────────────

class MockDatabase(DatabaseInterface):
    def query(self, sql: str) -> list:
        return [{"id": 1, "name": "TestUser"}]


class MockEmailSender(EmailSenderInterface):
    def __init__(self) -> None:
        self.sent: list[dict] = []

    def send_email(self, to: str, subject: str, body: str) -> None:
        self.sent.append({"to": to, "subject": subject})


class NullLogger(LoggerInterface):
    def log(self, message: str) -> None:
        pass  # swallow logs during tests


# ─── High-Level Module ─────────────────────────────────────────────

class UserService:
    """
    Depends ONLY on abstractions. Never creates its own dependencies.
    Swap MySQL → PostgreSQL or Gmail → SendGrid without touching this class.
    """

    def __init__(self, db: DatabaseInterface, email: EmailSenderInterface, logger: LoggerInterface) -> None:
        self._db = db
        self._email = email
        self._logger = logger

    def create_user(self, name: str, email_addr: str) -> dict:
        self._logger.log(f"Creating user {name}")
        user = {"id": 1, "name": name, "email": email_addr}
        self._email.send_email(email_addr, "Welcome!", f"Hello {name}")
        return user

    def get_user(self, user_id: int) -> dict | None:
        results = self._db.query(f"SELECT * FROM users WHERE id={user_id}")
        return results[0] if results else None


if __name__ == "__main__":
    # Production: real implementations injected
    prod = UserService(db=MySQLDatabase(), email=GmailSender(), logger=ConsoleLogger())
    print("=== Production ===")
    print(prod.create_user("Alice", "alice@example.com"))

    # Tests: mock implementations injected — no real DB or email needed
    mock_email = MockEmailSender()
    test = UserService(db=MockDatabase(), email=mock_email, logger=NullLogger())
    print("\n=== Test (no real infrastructure) ===")
    print(test.create_user("Bob", "bob@test.com"))
    print(f"Emails captured: {mock_email.sent}")
