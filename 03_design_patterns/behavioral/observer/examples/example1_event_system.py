"""
Observer Pattern — Example 1: Generic Event System

An EventEmitter that supports subscribing/unsubscribing to named events.
Observers are plain callbacks (functions) — no ABC class needed.

Real-world use: Node.js EventEmitter, browser addEventListener, and most
backend frameworks (Django signals, Flask hooks) follow this exact structure.
Zomato's order service emits "order.placed" and multiple microservices react.
"""
from typing import Callable, Any
from collections import defaultdict


class EventEmitter:
    """Subject: stores named event → [callbacks] mappings."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable]] = defaultdict(list)

    def on(self, event: str, callback: Callable) -> None:
        """Subscribe callback to event."""
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable) -> None:
        """Unsubscribe callback from event."""
        try:
            self._listeners[event].remove(callback)
        except ValueError:
            pass  # wasn't subscribed — safe to ignore

    def emit(self, event: str, data: Any = None) -> None:
        """Notify all callbacks for this event."""
        # Copy list so a callback can safely unsubscribe itself during emit
        for callback in list(self._listeners[event]):
            callback(data)

    def once(self, event: str, callback: Callable) -> None:
        """Subscribe a callback that fires only once, then auto-unsubscribes."""
        def one_time_wrapper(data):
            callback(data)
            self.off(event, one_time_wrapper)
        self.on(event, one_time_wrapper)


# ── Example: user service emits events; downstream services react ──────────────

class UserService(EventEmitter):
    def __init__(self) -> None:
        super().__init__()
        self._users: dict[int, dict] = {}
        self._next_id = 1

    def create_user(self, name: str, email: str) -> dict:
        user = {"id": self._next_id, "name": name, "email": email}
        self._users[self._next_id] = user
        self._next_id += 1
        self.emit("user.created", user)
        return user

    def delete_user(self, user_id: int) -> None:
        user = self._users.pop(user_id, None)
        if user:
            self.emit("user.deleted", user)


class EmailService:
    def on_user_created(self, user: dict) -> None:
        print(f"[EmailService] Sending welcome email to {user['email']}")


class AuditLogger:
    def __init__(self) -> None:
        self.log: list[str] = []

    def on_user_created(self, user: dict) -> None:
        entry = f"User created: {user['name']} (id={user['id']})"
        self.log.append(entry)
        print(f"[AuditLogger] {entry}")

    def on_user_deleted(self, user: dict) -> None:
        entry = f"User deleted: {user['name']} (id={user['id']})"
        self.log.append(entry)
        print(f"[AuditLogger] {entry}")


if __name__ == "__main__":
    service = UserService()
    email_svc = EmailService()
    audit = AuditLogger()

    service.on("user.created", email_svc.on_user_created)
    service.on("user.created", audit.on_user_created)
    service.on("user.deleted", audit.on_user_deleted)

    print("=== Creating users ===")
    alice = service.create_user("Alice", "alice@example.com")
    service.create_user("Bob", "bob@example.com")

    print("\n=== Deleting user ===")
    service.delete_user(alice["id"])

    print("\n=== Unsubscribe email service, create another user ===")
    service.off("user.created", email_svc.on_user_created)
    service.create_user("Carol", "carol@example.com")

    print(f"\n=== Audit log ({len(audit.log)} entries) ===")
    for entry in audit.log:
        print(f"  {entry}")
