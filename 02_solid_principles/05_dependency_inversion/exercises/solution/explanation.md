# Explanation: DIP Notification Service

## The Key Inversion
Without DIP: `NotificationService → SMSSender` (depends on detail)
With DIP: `NotificationService → NotificationSenderInterface ← SMSSender` (both depend on abstraction)

The dependency arrow is "inverted" — now both the high-level service and low-level implementations point toward the abstraction.

## Testability
```python
class MockSender(NotificationSenderInterface):
    def __init__(self): self.sent = []
    def send(self, recipient, message): self.sent.append(...); return True
    def get_channel_name(self): return "Mock"

# Test NotificationService without any real infrastructure:
service = NotificationService(MockSender())
service.send_alert("user", "test message")
assert len(mock.sent) == 1  # verified!
```

## `NotificationRouter` Pattern
The router is essentially a Strategy pattern variant — it picks the right sender based on a key. Notice that `NotificationRouter` also depends only on `NotificationSenderInterface`, never on `SMSSender` directly.

## What Changed vs Tight Coupling
| Before | After |
|--------|-------|
| `self.sms = SMSSender()` | `self._sender = sender` (injected) |
| Can't test without SMS API | Test with MockSender |
| Swap SMS → Email requires edit | `service.set_sender(EmailSender())` |
| UserService knows about SMS | Service knows only about interface |
