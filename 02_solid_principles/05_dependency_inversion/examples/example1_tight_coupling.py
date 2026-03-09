"""
DIP Example 1: Tight Coupling Violation

UserService hardcodes all its dependencies — can't test, can't swap.

Real-world use: This pattern appears in backend services (hotel booking,
ride-sharing) where the service class directly instantiates the database
and email client. When the team switches from MySQL to PostgreSQL or from
Gmail to SendGrid, they must edit the business logic class itself — a DIP
violation. See example2_with_di.py for the injected version.
"""


# ─── Low-Level Modules (implementation details) ───────────────────

class MySQLDatabase:
    def __init__(self) -> None:
        print("Connecting to MySQL...")  # would need real MySQL

    def query(self, sql: str) -> list:
        return [{"id": 1, "name": "Alice"}]  # simulated


class GmailSender:
    def __init__(self) -> None:
        print("Initializing Gmail SMTP...")  # would need real credentials

    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"Sending Gmail to {to}: {subject}")


class FileLogger:
    def __init__(self) -> None:
        print("Opening log file...")  # would need file system

    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


# ─── High-Level Module — the problem ─────────────────────────────

class UserServiceTightlyCoupled:
    """
    UserService that creates its own dependencies.

    PROBLEMS:
    1. To test this, you need a real MySQL database
    2. To switch to PostgreSQL, you must edit UserService
    3. To use SendGrid instead of Gmail, you must edit UserService
    4. UserService knows too much about infrastructure
    """

    def __init__(self) -> None:
        # Hardcoded dependencies — DIP violation!
        self.db = MySQLDatabase()       # ❌ hardcoded
        self.email = GmailSender()      # ❌ hardcoded
        self.logger = FileLogger()      # ❌ hardcoded

    def create_user(self, name: str, email: str) -> dict:
        self.logger.log(f"Creating user {name}")
        # In real code: INSERT into DB, send welcome email
        user = {"id": 1, "name": name, "email": email}
        self.email.send_email(email, "Welcome!", f"Hello {name}")
        return user

    def get_user(self, user_id: int) -> dict | None:
        results = self.db.query(f"SELECT * FROM users WHERE id={user_id}")
        return results[0] if results else None


if __name__ == "__main__":
    print("=== Tight Coupling Demonstration ===\n")
    service = UserServiceTightlyCoupled()
    user = service.create_user("Alice", "alice@example.com")
    print(f"Created: {user}")

    print("\n=== Why This Is a Problem ===")
    print("1. Can't test without real MySQL + Gmail credentials")
    print("2. Switching databases = editing UserService source code")
    print("3. Adding CloudLogger = editing UserService source code")
    print("4. UserService violates both DIP and SRP")
