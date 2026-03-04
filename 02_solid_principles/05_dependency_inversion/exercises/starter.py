"""
Exercise: Notification Service with DIP
Fill in the TODOs. Run: pytest tests.py -v
"""
from abc import ABC, abstractmethod


class NotificationSenderInterface(ABC):
    """Abstraction — NotificationService depends on this, not on SMS/Email/Slack."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Send notification. Returns True on success."""
        ...

    @abstractmethod
    def get_channel_name(self) -> str:
        """Return the channel name, e.g. 'SMS', 'Email', 'Slack'."""
        ...


class SMSSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        # TODO: print f"[SMS → {recipient}]: {message}", return True
        pass

    def get_channel_name(self) -> str:
        # TODO: return "SMS"
        pass


class EmailSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        # TODO: print f"[Email → {recipient}]: {message}", return True
        pass

    def get_channel_name(self) -> str:
        # TODO: return "Email"
        pass


class SlackSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        # TODO: print f"[Slack → {recipient}]: {message}", return True
        pass

    def get_channel_name(self) -> str:
        # TODO: return "Slack"
        pass


class NotificationService:
    """
    High-level service. Depends on abstraction, not implementation.
    Never contains SMS/Email/Slack specific logic.
    """

    def __init__(self, sender: NotificationSenderInterface) -> None:
        # TODO: store sender
        pass

    def send_alert(self, recipient: str, message: str) -> bool:
        # TODO: delegate to self._sender.send()
        pass

    def set_sender(self, sender: NotificationSenderInterface) -> None:
        # TODO: swap the sender
        pass


class NotificationRouter:
    """Routes notifications to the correct sender based on channel."""

    def __init__(self, senders: dict[str, NotificationSenderInterface]) -> None:
        # TODO: store senders dict
        pass

    def add_sender(self, channel: str, sender: NotificationSenderInterface) -> None:
        # TODO: add to senders dict
        pass

    def route(self, channel: str, recipient: str, message: str) -> bool:
        """
        Send via the specified channel.

        Raises:
            ValueError: if channel is not registered
        """
        # TODO: look up channel in senders, raise ValueError if not found, then send
        pass
