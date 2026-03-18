# Advanced topic — registry-based factory that supports runtime registration of new types
"""
Factory Pattern — Example 2: Registry-Based Notification Factory

New channel types register themselves at startup. Adding WhatsApp later
means one register() call — no changes to NotificationFactory.

Real-world use: Swiggy/Zomato order alerts over Email, SMS, or push;
adding a new channel without touching existing factory code.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    recipient: str
    subject: str
    body: str


class Notification(ABC):
    @abstractmethod
    def send(self, message: Message) -> str: ...


class EmailNotification(Notification):
    def send(self, message: Message) -> str:
        return f"[EMAIL] To: {message.recipient} | {message.subject}: {message.body}"


class SMSNotification(Notification):
    def send(self, message: Message) -> str:
        snippet = message.body[:40] + ("…" if len(message.body) > 40 else "")
        return f"[SMS] To: {message.recipient} | {snippet}"


class PushNotification(Notification):
    def send(self, message: Message) -> str:
        return f"[PUSH] → {message.recipient}: {message.subject}"


class NotificationFactory:
    """
    Registry-based factory. New channels are added via register() — the factory
    class itself never needs to change (Open/Closed Principle).
    """
    _registry: dict[str, type[Notification]] = {}

    @classmethod
    def register(cls, channel: str, cls_: type[Notification]) -> None:
        cls._registry[channel.lower()] = cls_

    @classmethod
    def create(cls, channel: str, **kwargs) -> Notification:
        key = channel.lower()
        if key not in cls._registry:
            raise ValueError(f"Unknown channel {channel!r}. Available: {list(cls._registry)}")
        return cls._registry[key](**kwargs)

    @classmethod
    def available_channels(cls) -> list[str]:
        return list(cls._registry)


# Register built-in channels at module load time
NotificationFactory.register("email", EmailNotification)
NotificationFactory.register("sms",   SMSNotification)
NotificationFactory.register("push",  PushNotification)


if __name__ == "__main__":
    msg = Message("alice@example.com", "Order update", "Your order has shipped.")

    for channel in ["email", "sms", "push"]:
        n = NotificationFactory.create(channel)
        print(n.send(msg))

    # Add a new channel at runtime — no factory code changes needed
    class SlackNotification(Notification):
        def send(self, message: Message) -> str:
            return f"[SLACK] {message.subject}: {message.body}"

    NotificationFactory.register("slack", SlackNotification)
    print(NotificationFactory.create("slack").send(msg))
    print("Channels:", NotificationFactory.available_channels())
