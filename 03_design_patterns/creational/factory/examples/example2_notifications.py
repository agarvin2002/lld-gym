"""Factory Pattern — Example 2: Notification Factory.

Shows a registry-based factory that supports runtime registration
of new types without modifying the factory class (Open/Closed Principle).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ── Product Interface ─────────────────────────────────────────────────────────

@dataclass
class Message:
    recipient: str
    subject: str
    body: str


class Notification(ABC):
    @abstractmethod
    def send(self, message: Message) -> str:
        """Send the message and return a delivery receipt string."""


# ── Concrete Products ─────────────────────────────────────────────────────────

class EmailNotification(Notification):
    def send(self, message: Message) -> str:
        return (
            f"[EMAIL] To: {message.recipient} | "
            f"Subject: {message.subject} | Body: {message.body}"
        )


class SMSNotification(Notification):
    def send(self, message: Message) -> str:
        # SMS is short: truncate body
        snippet = message.body[:40] + ("…" if len(message.body) > 40 else "")
        return f"[SMS] To: {message.recipient} | {snippet}"


class PushNotification(Notification):
    def send(self, message: Message) -> str:
        return f"[PUSH] → {message.recipient}: {message.subject}"


class SlackNotification(Notification):
    def __init__(self, channel: str = "#general") -> None:
        self._channel = channel

    def send(self, message: Message) -> str:
        return f"[SLACK {self._channel}] {message.subject}: {message.body}"


# ── Registry-Based Factory ─────────────────────────────────────────────────────

class NotificationFactory:
    """
    Registry-based factory: supports registering new channel types at runtime.
    New channels don't require touching existing factory code.
    """
    _registry: dict[str, type[Notification]] = {}

    @classmethod
    def register(cls, channel: str, notification_class: type[Notification]) -> None:
        cls._registry[channel.lower()] = notification_class

    @classmethod
    def create(cls, channel: str, **kwargs) -> Notification:
        key = channel.lower()
        if key not in cls._registry:
            available = list(cls._registry)
            raise ValueError(f"Unknown channel {channel!r}. Available: {available}")
        return cls._registry[key](**kwargs)

    @classmethod
    def available_channels(cls) -> list[str]:
        return list(cls._registry)


# Register built-in channels
NotificationFactory.register("email", EmailNotification)
NotificationFactory.register("sms",   SMSNotification)
NotificationFactory.register("push",  PushNotification)


# ── Notification Service (uses factory) ───────────────────────────────────────

class NotificationService:
    """High-level service; depends only on the factory + Notification interface."""

    def notify(self, channel: str, recipient: str, subject: str, body: str) -> str:
        notification = NotificationFactory.create(channel)
        message = Message(recipient=recipient, subject=subject, body=body)
        return notification.send(message)

    def broadcast(self, channels: list[str], recipient: str, subject: str, body: str) -> list[str]:
        """Send on multiple channels, collecting receipts."""
        message = Message(recipient=recipient, subject=subject, body=body)
        receipts = []
        for channel in channels:
            notification = NotificationFactory.create(channel)
            receipts.append(notification.send(message))
        return receipts


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    service = NotificationService()

    print("=== Single channel ===")
    for channel in ["email", "sms", "push"]:
        receipt = service.notify(channel, "alice@example.com", "Hello", "Your order has shipped.")
        print(receipt)

    print("\n=== Broadcast ===")
    receipts = service.broadcast(
        ["email", "sms"],
        "bob@example.com",
        "Reminder",
        "Your meeting starts in 15 minutes.",
    )
    for r in receipts:
        print(r)

    print("\n=== Register custom channel ===")
    NotificationFactory.register("slack", SlackNotification)
    receipt = service.notify("slack", "team", "Deploy done", "v2.3.1 is live.")
    print(receipt)
    print("Available channels:", NotificationFactory.available_channels())
