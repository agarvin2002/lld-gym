"""Tests for DIP Notification Service exercise."""
import sys, os
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    NotificationSenderInterface, SMSSender, EmailSender, SlackSender,
    NotificationService, NotificationRouter
)


class MockSender(NotificationSenderInterface):
    def __init__(self, channel: str = "Mock"):
        self.sent: list[dict] = []
        self._channel = channel

    def send(self, recipient: str, message: str) -> bool:
        self.sent.append({"recipient": recipient, "message": message})
        return True

    def get_channel_name(self) -> str:
        return self._channel


class TestSMSSender:
    def test_send_returns_true(self):
        assert SMSSender().send("123-456", "Test") is True

    def test_channel_name(self):
        assert SMSSender().get_channel_name() == "SMS"


class TestEmailSender:
    def test_send_returns_true(self):
        assert EmailSender().send("a@b.com", "Test") is True

    def test_channel_name(self):
        assert EmailSender().get_channel_name() == "Email"


class TestSlackSender:
    def test_send_returns_true(self):
        assert SlackSender().send("#alerts", "Test") is True

    def test_channel_name(self):
        assert SlackSender().get_channel_name() == "Slack"


class TestNotificationService:
    def test_send_alert_uses_injected_sender(self):
        mock = MockSender()
        service = NotificationService(mock)
        service.send_alert("user@example.com", "Hello")
        assert len(mock.sent) == 1

    def test_send_alert_returns_true(self):
        service = NotificationService(MockSender())
        assert service.send_alert("user", "msg") is True

    def test_set_sender_swaps_sender(self):
        mock1 = MockSender("First")
        mock2 = MockSender("Second")
        service = NotificationService(mock1)
        service.set_sender(mock2)
        service.send_alert("user", "msg")
        assert len(mock1.sent) == 0
        assert len(mock2.sent) == 1

    def test_works_with_sms_sender(self):
        service = NotificationService(SMSSender())
        assert service.send_alert("555-1234", "Alert!") is True

    def test_works_with_email_sender(self):
        service = NotificationService(EmailSender())
        assert service.send_alert("a@b.com", "Alert!") is True


class TestNotificationRouter:
    def test_route_to_correct_sender(self):
        sms = MockSender("SMS")
        router = NotificationRouter({"sms": sms})
        router.route("sms", "555-1234", "Test")
        assert len(sms.sent) == 1

    def test_route_unknown_channel_raises_error(self):
        router = NotificationRouter({})
        with pytest.raises(ValueError):
            router.route("fax", "555", "Test")

    def test_add_sender_registers_channel(self):
        router = NotificationRouter({})
        mock = MockSender()
        router.add_sender("push", mock)
        router.route("push", "device123", "Ping!")
        assert len(mock.sent) == 1
