# Exercise: Notification Service with DIP

## What You'll Build

A `NotificationService` that sends alerts through different channels — SMS, Email, Slack — all swappable without modifying the service.

## Interfaces

### `NotificationSenderInterface` (ABC)
- `send(recipient: str, message: str) -> bool`
- `get_channel_name() -> str`

## Concrete Senders

| Class | Channel | Behavior |
|-------|---------|----------|
| `SMSSender` | SMS | Simulates Twilio — prints and returns True |
| `EmailSender` | Email | Simulates SMTP — prints and returns True |
| `SlackSender` | Slack | Simulates webhook — prints and returns True |

## High-Level Classes

### `NotificationService`
- `__init__(sender: NotificationSenderInterface)`
- `send_alert(recipient: str, message: str) -> bool`
- `set_sender(sender: NotificationSenderInterface) -> None` — swap at runtime

### `NotificationRouter`
- `__init__(senders: dict[str, NotificationSenderInterface])` — map of channel→sender
- `route(channel: str, recipient: str, message: str) -> bool`
- `add_sender(channel: str, sender: NotificationSenderInterface) -> None`

## Constraints
- `NotificationService` must not contain any SMS/Email/Slack specific logic
- All senders must be swappable without modifying `NotificationService`

## Hints
1. Store senders dict as `self._senders: dict[str, NotificationSenderInterface]`
2. `route()` should raise `ValueError` if channel not found
3. A `MockSender` for testing is trivial to implement

## What You'll Practice
- Dependency injection via constructor
- High-level modules depending only on abstractions
- Runtime strategy swapping
- Testability: mock implementations
