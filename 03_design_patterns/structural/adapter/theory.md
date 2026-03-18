# Adapter Pattern

## What is it?
The Adapter pattern wraps an incompatible object so it looks compatible to the caller.
You cannot change the object you are wrapping. So you create a thin class that translates calls.
The caller only ever sees the interface it already understands.

## Analogy
A travel power adapter lets your Indian charger plug into a European socket.
The charger has not changed. The wall socket has not changed.
The adapter sits in between and makes the connection possible.

## Minimal code
```python
# Legacy class you cannot modify
class OldSMS:
    def send_sms(self, mobile: str, msg: str) -> None:
        print(f"Sending '{msg}' to {mobile}")

# Interface your app expects
class Notifier:
    def notify(self, user_id: str, message: str) -> None:
        raise NotImplementedError

# Adapter bridges the two
class SMSAdapter(Notifier):
    def __init__(self, old_sms: OldSMS) -> None:
        self._old = old_sms

    def notify(self, user_id: str, message: str) -> None:
        self._old.send_sms(mobile=user_id, msg=message)

# Client code only knows Notifier
notifier = SMSAdapter(OldSMS())
notifier.notify("9876543210", "Your Zomato order is on the way!")
```

## Real-world uses
- Wrapping a legacy payment gateway (like a bank's old SOAP API) behind a clean `charge()` interface
- Adapting multiple third-party SMS providers (Twilio, MSG91, Exotel) so your app treats them identically
- Connecting an old database access layer to a new repository interface during a migration

## One mistake
Modifying the adaptee instead of writing an adapter.
If you own the old code and can safely change it, do that.
The Adapter pattern is for code you cannot or should not touch.

## What to do next
- Read `examples/example1_legacy_adapter.py` to see a printer adapter in action.
- Read `examples/example2_third_party_adapter.py` to see a third-party weather API adapted.
- Then open `exercises/starter.py` and build your own adapter.
