"""Solution: Notification Service with DIP"""
from abc import ABC, abstractmethod


class NotificationSenderInterface(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool: ...

    @abstractmethod
    def get_channel_name(self) -> str: ...


class SMSSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        print(f"[SMS → {recipient}]: {message}")
        return True

    def get_channel_name(self) -> str:
        return "SMS"


class EmailSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        print(f"[Email → {recipient}]: {message}")
        return True

    def get_channel_name(self) -> str:
        return "Email"


class SlackSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        print(f"[Slack → {recipient}]: {message}")
        return True

    def get_channel_name(self) -> str:
        return "Slack"


class NotificationService:
    def __init__(self, sender: NotificationSenderInterface) -> None:
        self._sender = sender

    def send_alert(self, recipient: str, message: str) -> bool:
        return self._sender.send(recipient, message)

    def set_sender(self, sender: NotificationSenderInterface) -> None:
        self._sender = sender


class NotificationRouter:
    def __init__(self, senders: dict[str, NotificationSenderInterface]) -> None:
        self._senders = dict(senders)

    def add_sender(self, channel: str, sender: NotificationSenderInterface) -> None:
        self._senders[channel] = sender

    def route(self, channel: str, recipient: str, message: str) -> bool:
        if channel not in self._senders:
            raise ValueError(f"Unknown channel: {channel!r}")
        return self._senders[channel].send(recipient, message)
