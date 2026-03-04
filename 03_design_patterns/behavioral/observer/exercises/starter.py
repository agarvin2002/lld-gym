"""
Exercise: E-Commerce Event Bus (Observer Pattern)
Fill in the TODOs. Run: pytest tests.py -v
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable


@dataclass
class OrderEvent:
    event_type: str
    order_id: str
    customer_email: str
    items: list[str]
    total: float


class EventBus:
    """Central event bus. Publishers emit, subscribers listen."""

    def __init__(self) -> None:
        # TODO: initialize self._handlers as defaultdict(list)
        pass

    def subscribe(self, event_type: str, handler: Callable[[OrderEvent], None]) -> None:
        # TODO: append handler to self._handlers[event_type]
        pass

    def unsubscribe(self, event_type: str, handler: Callable[[OrderEvent], None]) -> None:
        # TODO: remove handler from self._handlers[event_type], ignore if not found
        pass

    def publish(self, event: OrderEvent) -> None:
        # TODO: call all handlers in self._handlers[event.event_type] with event
        pass


class InventoryService:
    def __init__(self) -> None:
        self.reservations: list[str] = []

    def handle(self, event: OrderEvent) -> None:
        # TODO: append order_id to self.reservations, print reservation message
        pass


class ShippingService:
    def __init__(self) -> None:
        self.scheduled: list[str] = []

    def handle(self, event: OrderEvent) -> None:
        # TODO: append order_id to self.scheduled, print scheduling message
        pass


class EmailService:
    def __init__(self) -> None:
        self.emails_sent: list[dict] = []

    def on_placed(self, event: OrderEvent) -> None:
        # TODO: record {"to": email, "subject": "Order Confirmed"}, print
        pass

    def on_shipped(self, event: OrderEvent) -> None:
        # TODO: record {"to": email, "subject": "Order Shipped"}, print
        pass

    def on_delivered(self, event: OrderEvent) -> None:
        # TODO: record {"to": email, "subject": "Order Delivered"}, print
        pass


class LoyaltyService:
    def __init__(self) -> None:
        self.points: dict[str, float] = {}

    def handle(self, event: OrderEvent) -> None:
        # TODO: award points = total * 0.1, store in self.points[customer_email]
        pass
