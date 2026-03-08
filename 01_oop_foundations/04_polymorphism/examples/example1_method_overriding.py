"""
example1_method_overriding.py
------------------------------
Shows polymorphism: many classes, one common method name.

We build a notification system. Different channels (Email, SMS, Push) all have
a send() method — but each does it differently. The service that sends
notifications doesn't care which type it is talking to. It just calls send().

Real-world use: this pattern appears in almost every multi-class system.
  Parking lot:  Vehicle.get_parking_fee() — Car, Bike, Truck return different amounts
  Hotel system: Room.calculate_price()    — Single, Double, Suite return different prices

Run this file directly:
    python3 example1_method_overriding.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# The interface — every notification type must implement send()
# ---------------------------------------------------------------------------

class Notification(ABC):
    """Abstract base. Every notification type must implement send()."""

    @abstractmethod
    def send(self, message: str) -> bool:
        """Send the message. Return True if successful."""
        ...

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


# ---------------------------------------------------------------------------
# Three concrete types — each overrides send() differently
# ---------------------------------------------------------------------------

@dataclass
class EmailNotification(Notification):
    recipient: str

    def send(self, message: str) -> bool:
        print(f"[EMAIL] To: {self.recipient} | Message: {message}")
        return True


@dataclass
class SMSNotification(Notification):
    phone_number: str
    max_length: int = 160

    def send(self, message: str) -> bool:
        if len(message) > self.max_length:
            message = message[: self.max_length - 3] + "..."
        print(f"[SMS]   To: {self.phone_number} | Text: {message}")
        return True


@dataclass
class PushNotification(Notification):
    device_token: str
    title: str = "Notification"

    def send(self, message: str) -> bool:
        print(f"[PUSH]  Device: {self.device_token} | {self.title}: {message}")
        return True


# ---------------------------------------------------------------------------
# The service — works with ANY notification type, no isinstance() checks
# ---------------------------------------------------------------------------

@dataclass
class NotificationService:
    """
    Sends messages through all registered channels.

    TIP: This class only knows about Notification (the abstract class).
    It does not know about Email, SMS, or Push specifically.
    You can add new types without changing this class at all.
    """

    channels: list[Notification]

    def notify_all(self, message: str) -> None:
        """Send to all channels. No if/elif needed — just call send()."""
        for channel in self.channels:
            channel.send(message)    # POLYMORPHIC CALL — works for any type


# ---------------------------------------------------------------------------
# ANTI-PATTERN: what NOT to do
# ---------------------------------------------------------------------------

def send_with_isinstance_chain(notification: Notification, message: str) -> bool:
    """
    WRONG WAY — using isinstance() instead of polymorphism.

    Problems:
    1. If you add a new notification type, you must edit this function.
    2. It is easy to forget one type and get a silent failure.
    3. Compare with notify_all() above — same result, zero isinstance checks.
    """
    if isinstance(notification, EmailNotification):
        return notification.send(message)
    elif isinstance(notification, SMSNotification):
        return notification.send(message)
    elif isinstance(notification, PushNotification):
        return notification.send(message)
    # What if someone adds WhatsAppNotification? It falls through here silently!
    else:
        print(f"Unknown type: {type(notification).__name__} — message not sent!")
        return False


# ---------------------------------------------------------------------------
# RUN THIS TO SEE IT IN ACTION
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Part 1: Each type sends differently ===\n")
    notifications: list[Notification] = [
        EmailNotification(recipient="priya@example.com"),
        SMSNotification(phone_number="+91-99999-00000"),
        PushNotification(device_token="TOKEN_ABC123", title="Order Alert"),
    ]

    for notif in notifications:
        notif.send("Your order #42 has been shipped!")

    # -------------------------------------------------------------------------
    print("\n=== Part 2: NotificationService — one call sends to all ===\n")
    service = NotificationService(channels=[
        EmailNotification(recipient="rahul@example.com"),
        SMSNotification(phone_number="+91-88888-00000"),
        PushNotification(device_token="TOKEN_XYZ789"),
    ])
    service.notify_all("Flash sale: 50% off everything today!")

    # -------------------------------------------------------------------------
    print("\n=== Part 3: Anti-pattern — isinstance chains fail silently ===\n")

    # Create a new notification type and add it to the service
    class WhatsAppNotification(Notification):
        def send(self, message: str) -> bool:
            print(f"[WA]    Message: {message}")
            return True

    wa = WhatsAppNotification()

    print("Using notify_all() — works fine:")
    wa.send("Hello from notify_all!")       # works

    print("\nUsing isinstance chain — silently fails:")
    send_with_isinstance_chain(wa, "Hello from isinstance chain")   # falls to else!

    print("\nKey takeaway: notify_all() never needs to change. The isinstance chain does.")
