# Observer Pattern

## What is it?
The Observer pattern lets one object (the subject) automatically notify many other objects (observers) when its state changes. Observers subscribe and unsubscribe without the subject knowing anything about them. It decouples the thing that changes from the things that react.

## Analogy
A Swiggy order. You place an order and several things subscribe to it: your phone shows a status update, the delivery partner app gets a ping, and the restaurant's kitchen display lights up. The order (subject) just publishes events — it doesn't care who is listening.

## Minimal code
```python
# Callback-based Observer — the Pythonic style used by Django signals,
# Node.js EventEmitter, and most modern Python frameworks.

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list] = {}

    def subscribe(self, event: str, fn) -> None:
        self._handlers.setdefault(event, []).append(fn)

    def unsubscribe(self, event: str, fn) -> None:
        self._handlers.get(event, []).remove(fn)

    def publish(self, event: str, data=None) -> None:
        for fn in self._handlers.get(event, []):
            fn(data)

bus = EventBus()
bus.subscribe("order.placed", lambda d: print(f"Email: {d}"))
bus.subscribe("order.placed", lambda d: print(f"SMS:   {d}"))
bus.publish("order.placed", "Order #42")
```

> example2 shows the classic GoF ABC approach (Subject + Observer abstract class).
> Use that style when you need a strict contract — every observer must implement
> a specific `update()` method and you want the type checker to enforce it.

## Real-world uses
- Razorpay payment webhooks — every payment status change notifies subscribed services
- Flipkart "Notify Me" for out-of-stock items — observers get pinged when stock arrives
- Real-time chat apps — a message sent to a channel notifies all connected clients

## One mistake
Not unsubscribing observers that are no longer needed. The subject keeps a reference to every observer, so they can never be garbage-collected. This is a memory leak. Always call `unsubscribe()` when a listener is done.

## What to do next
See `examples/example1_event_system.py` for a callback-based EventEmitter (the Pythonic approach).
See `examples/example2_stock_ticker.py` for the classic ABC-based Subject/Observer structure.
Then try `exercises/starter.py` — build an e-commerce event bus with multiple subscriber services.
