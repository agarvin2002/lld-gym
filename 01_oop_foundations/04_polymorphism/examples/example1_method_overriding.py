"""
Example 1: Polymorphism via Method Overriding
=============================================

This example demonstrates subtype polymorphism — the classical OOP form where
subclasses override a method defined in a base class.

We build a notification system where EmailNotification, SMSNotification, and
PushNotification each implement send() differently, but the rest of the code
treats them identically through the shared Notification interface.

Key ideas demonstrated:
- Same interface (send), different behavior per subclass
- NotificationService works with any Notification without knowing which type
- Why isinstance() chains are an anti-pattern
- How adding a new notification type requires zero changes to existing code
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Base class — defines the interface
# ---------------------------------------------------------------------------

class Notification(ABC):
    """
    Abstract base for all notification types.

    Every concrete notification must implement send(). The caller only
    ever interacts with this interface — it never cares about the
    concrete type underneath.
    """

    @abstractmethod
    def send(self, message: str) -> bool:
        """
        Deliver a message via this notification channel.

        Args:
            message: The text to deliver.

        Returns:
            True if delivery succeeded, False otherwise.
        """
        ...

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


# ---------------------------------------------------------------------------
# Concrete implementations — each overrides send() differently
# ---------------------------------------------------------------------------

@dataclass
class EmailNotification(Notification):
    """Sends notifications via email."""

    recipient: str
    sender: str = "noreply@example.com"

    def send(self, message: str) -> bool:
        """Override: formats and 'sends' an email."""
        print(f"[EMAIL] To: {self.recipient}")
        print(f"        From: {self.sender}")
        print(f"        Body: {message}")
        # In reality: call an SMTP library here
        return True


@dataclass
class SMSNotification(Notification):
    """Sends notifications via SMS."""

    phone_number: str
    max_length: int = 160

    def send(self, message: str) -> bool:
        """Override: truncates long messages and 'sends' an SMS."""
        if len(message) > self.max_length:
            message = message[: self.max_length - 3] + "..."
            print(f"[SMS ] Warning: message truncated to {self.max_length} characters")

        print(f"[SMS ] To: {self.phone_number}")
        print(f"       Text: {message}")
        # In reality: call Twilio / AWS SNS here
        return True


@dataclass
class PushNotification(Notification):
    """Sends mobile push notifications."""

    device_token: str
    title: str = "Notification"

    def send(self, message: str) -> bool:
        """Override: packages a push payload and 'sends' it."""
        payload = {
            "to": self.device_token,
            "title": self.title,
            "body": message,
            "timestamp": int(time.time()),
        }
        print(f"[PUSH] Payload: {payload}")
        # In reality: call Firebase Cloud Messaging / APNs here
        return True


@dataclass
class SlackNotification(Notification):
    """
    Sends notifications to a Slack channel.

    This is a NEW notification type added later — notice that
    NotificationService requires ZERO changes to accommodate it.
    This is the open/closed principle in action.
    """

    channel: str
    webhook_url: str = "https://hooks.slack.com/services/..."

    def send(self, message: str) -> bool:
        """Override: posts a message to a Slack channel."""
        print(f"[SLACK] Channel: #{self.channel}")
        print(f"        Message: {message}")
        print(f"        Webhook: {self.webhook_url}")
        # In reality: HTTP POST to webhook_url here
        return True


# ---------------------------------------------------------------------------
# Service that uses polymorphism — works with any Notification
# ---------------------------------------------------------------------------

@dataclass
class NotificationService:
    """
    Dispatches messages through a collection of notification channels.

    This class only knows about the Notification interface. It does NOT
    know about EmailNotification, SMSNotification, etc. — and it never
    needs to.
    """

    channels: list[Notification] = field(default_factory=list)

    def add_channel(self, channel: Notification) -> None:
        """Register a notification channel."""
        self.channels.append(channel)

    def notify_all(self, message: str) -> dict[str, bool]:
        """
        Send message through all registered channels.

        Returns a dict mapping channel repr to success/failure.
        """
        results: dict[str, bool] = {}
        for channel in self.channels:
            print(f"\n--- Sending via {channel!r} ---")
            success = channel.send(message)    # POLYMORPHIC CALL
            results[repr(channel)] = success
        return results

    def notify_first_available(self, message: str) -> Optional[str]:
        """
        Try each channel in order; return the name of the first that succeeds.
        Useful for fallback chains (email → SMS → push).
        """
        for channel in self.channels:
            if channel.send(message):
                return repr(channel)
        return None


# ---------------------------------------------------------------------------
# Anti-pattern demonstration: isinstance() chains
# ---------------------------------------------------------------------------

def send_with_isinstance_chain(notification: Notification, message: str) -> bool:
    """
    ANTI-PATTERN: Using isinstance() chains instead of polymorphism.

    Problems with this approach:
    1. Every new notification type requires editing this function.
    2. This function must import every concrete class.
    3. It violates the open/closed principle.
    4. The real send() logic is split across two places.
    5. It is impossible to add a new type without changing existing code.

    Compare to NotificationService.notify_all() — identical behavior,
    zero isinstance() calls, zero changes needed for new types.
    """
    if isinstance(notification, EmailNotification):
        # duplicated logic — calling send() anyway, so why bother?
        print(f"[isinstance chain] Detected EmailNotification, calling send...")
        return notification.send(message)
    elif isinstance(notification, SMSNotification):
        print(f"[isinstance chain] Detected SMSNotification, calling send...")
        return notification.send(message)
    elif isinstance(notification, PushNotification):
        print(f"[isinstance chain] Detected PushNotification, calling send...")
        return notification.send(message)
    # SlackNotification? Forgot to add it! Silent failure.
    else:
        print(f"[isinstance chain] Unknown type: {type(notification).__name__}")
        return False


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: Polymorphism via Method Overriding")
    print("=" * 60)

    # --- Part 1: Basic polymorphism ---
    print("\n[Part 1] Each subclass implements send() differently")
    print("-" * 50)

    notifications: list[Notification] = [
        EmailNotification(recipient="alice@example.com"),
        SMSNotification(phone_number="+1-555-0100"),
        PushNotification(device_token="abc123token", title="Alert"),
    ]

    message = "Your order #42 has shipped!"

    for notif in notifications:
        print()
        notif.send(message)

    # --- Part 2: NotificationService — same interface, many types ---
    print("\n\n[Part 2] NotificationService — polymorphic dispatch")
    print("-" * 50)

    service = NotificationService()
    service.add_channel(EmailNotification(recipient="bob@example.com"))
    service.add_channel(SMSNotification(phone_number="+1-555-0200"))
    service.add_channel(PushNotification(device_token="xyz789token"))

    results = service.notify_all("Flash sale: 50% off everything!")
    print(f"\nResults: {results}")

    # --- Part 3: Adding a new type — zero changes to existing code ---
    print("\n\n[Part 3] New type: SlackNotification — zero changes to service")
    print("-" * 50)

    service.add_channel(SlackNotification(channel="engineering-alerts"))
    service.notify_first_available("Server CPU usage at 95%!")

    # --- Part 4: Long SMS truncation ---
    print("\n\n[Part 4] SMS truncates long messages automatically")
    print("-" * 50)

    long_message = "A" * 200
    sms = SMSNotification(phone_number="+1-555-0300")
    sms.send(long_message)

    # --- Part 5: Anti-pattern contrast ---
    print("\n\n[Part 5] Anti-pattern: isinstance() chain (for contrast)")
    print("-" * 50)

    email = EmailNotification(recipient="carol@example.com")
    slack = SlackNotification(channel="general")   # NOT in the chain!

    print("Sending via isinstance chain:")
    send_with_isinstance_chain(email, "Hello from isinstance chain")
    print()
    send_with_isinstance_chain(slack, "This will silently fail!")

    print("\n--- End of demo ---")
    print("\nKey takeaway: NotificationService.notify_all() never changes.")
    print("The isinstance chain breaks every time a new type is added.")
