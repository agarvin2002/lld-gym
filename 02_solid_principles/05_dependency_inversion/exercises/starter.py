"""
WHAT YOU'RE BUILDING
====================
A notification service that can send messages via SMS, Email, or Slack —
without the service knowing which one it's using.

NotificationService accepts any NotificationSenderInterface. You can swap
SMSSender for EmailSender or SlackSender without touching the service.
That's DIP: the high-level service depends on the abstraction, not the concrete sender.

NotificationRouter maps channel names (e.g. "SMS", "Email") to sender
instances and routes messages to the right one.

Fill in the TODOs below. Run the tests to verify your work.
"""
from abc import ABC, abstractmethod


class NotificationSenderInterface(ABC):
    """Abstraction — NotificationService depends on this, not on SMS/Email/Slack."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Send notification. Return True on success."""
        ...

    @abstractmethod
    def get_channel_name(self) -> str:
        """Return the channel name, e.g. 'SMS', 'Email', 'Slack'."""
        ...


class SMSSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        # TODO: Print f"[SMS → {recipient}]: {message}" and return True
        pass

    def get_channel_name(self) -> str:
        # TODO: Return "SMS"
        pass


class EmailSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        # TODO: Print f"[Email → {recipient}]: {message}" and return True
        pass

    def get_channel_name(self) -> str:
        # TODO: Return "Email"
        pass


class SlackSender(NotificationSenderInterface):
    def send(self, recipient: str, message: str) -> bool:
        # TODO: Print f"[Slack → {recipient}]: {message}" and return True
        pass

    def get_channel_name(self) -> str:
        # TODO: Return "Slack"
        pass


class NotificationService:
    """High-level service. Depends on abstraction, not implementation."""

    def __init__(self, sender: NotificationSenderInterface) -> None:
        # TODO: Store sender as self._sender
        pass

    def send_alert(self, recipient: str, message: str) -> bool:
        # TODO: Delegate to self._sender.send(recipient, message) and return the result
        pass

    def set_sender(self, sender: NotificationSenderInterface) -> None:
        # TODO: Replace self._sender with the new sender
        pass


class NotificationRouter:
    """Routes notifications to the correct sender based on channel name."""

    def __init__(self, senders: dict[str, NotificationSenderInterface]) -> None:
        # TODO: Store senders as self._senders
        # HINT: The senders dict maps channel name → sender, e.g. {"SMS": SMSSender(), "Email": EmailSender()}
        pass

    def add_sender(self, channel: str, sender: NotificationSenderInterface) -> None:
        # TODO: Add channel → sender to self._senders
        pass

    def route(self, channel: str, recipient: str, message: str) -> bool:
        """
        Send via the specified channel.

        Raises:
            ValueError: if the channel is not registered
        """
        # TODO: Look up channel in self._senders
        #   If not found: raise ValueError(f"Unknown channel: {channel}")
        #   If found: call sender.send(recipient, message) and return the result
        # HINT: Use self._senders.get(channel) to look up the sender.
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/05_dependency_inversion/exercises/tests.py -v
#
# Run all SOLID exercises at once:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/ -v
# =============================================================================
