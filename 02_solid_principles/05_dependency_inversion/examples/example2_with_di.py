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

    @abstractmethod
    def execute(self, sql: str) -> None: ...


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

    def execute(self, sql: str) -> None:
        pass  # would execute real SQL


class GmailSender(EmailSenderInterface):
    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"[Gmail] Sending to {to}: {subject}")


class ConsoleLogger(LoggerInterface):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


# ─── Test Doubles (for testing without real infrastructure) ───────

class MockDatabase(DatabaseInterface):
    def __init__(self) -> None:
        self.executed: list[str] = []

    def query(self, sql: str) -> list:
        return [{"id": 1, "name": "TestUser"}]

    def execute(self, sql: str) -> None:
        self.executed.append(sql)


class MockEmailSender(EmailSenderInterface):
    def __init__(self) -> None:
        self.sent: list[dict] = []

    def send_email(self, to: str, subject: str, body: str) -> None:
        self.sent.append({"to": to, "subject": subject})


class NullLogger(LoggerInterface):
    def log(self, message: str) -> None:
        pass  # swallow all logs during tests


# ─── High-Level Module ─────────────────────────────────────────────

class UserService:
    """
    UserService depends ONLY on abstractions.
    Never creates its own dependencies — they're injected.
    """

    def __init__(
        self,
        db: DatabaseInterface,
        email: EmailSenderInterface,
        logger: LoggerInterface,
    ) -> None:
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


# ─── Factory for Production Setup ─────────────────────────────────

def create_production_service() -> UserService:
    return UserService(
        db=MySQLDatabase(),
        email=GmailSender(),
        logger=ConsoleLogger(),
    )


def create_test_service() -> tuple[UserService, MockDatabase, MockEmailSender]:
    db = MockDatabase()
    email = MockEmailSender()
    service = UserService(db=db, email=email, logger=NullLogger())
    return service, db, email


if __name__ == "__main__":
    print("=== Production Setup ===")
    prod_service = create_production_service()
    user = prod_service.create_user("Alice", "alice@example.com")
    print(f"Created: {user}")

    print("\n=== Test Setup (no real infrastructure) ===")
    test_service, mock_db, mock_email = create_test_service()
    user = test_service.create_user("Bob", "bob@test.com")
    print(f"Created: {user}")
    print(f"Emails sent: {mock_email.sent}")
    print("No real database or email server needed! ✅")
