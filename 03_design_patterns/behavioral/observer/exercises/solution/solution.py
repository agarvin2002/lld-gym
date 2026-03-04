"""Solution: E-Commerce Event Bus (Observer Pattern)"""
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
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[OrderEvent], None]) -> None:
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[OrderEvent], None]) -> None:
        try:
            self._handlers[event_type].remove(handler)
        except ValueError:
            pass

    def publish(self, event: OrderEvent) -> None:
        for handler in list(self._handlers[event.event_type]):
            handler(event)


class InventoryService:
    def __init__(self) -> None:
        self.reservations: list[str] = []

    def handle(self, event: OrderEvent) -> None:
        self.reservations.append(event.order_id)
        print(f"[Inventory] Reserved stock for order {event.order_id}")


class ShippingService:
    def __init__(self) -> None:
        self.scheduled: list[str] = []

    def handle(self, event: OrderEvent) -> None:
        self.scheduled.append(event.order_id)
        print(f"[Shipping] Pickup scheduled for order {event.order_id}")


class EmailService:
    def __init__(self) -> None:
        self.emails_sent: list[dict] = []

    def on_placed(self, event: OrderEvent) -> None:
        self.emails_sent.append({"to": event.customer_email, "subject": "Order Confirmed"})
        print(f"[Email] Confirmation sent to {event.customer_email}")

    def on_shipped(self, event: OrderEvent) -> None:
        self.emails_sent.append({"to": event.customer_email, "subject": "Order Shipped"})
        print(f"[Email] Shipping notification sent to {event.customer_email}")

    def on_delivered(self, event: OrderEvent) -> None:
        self.emails_sent.append({"to": event.customer_email, "subject": "Order Delivered"})
        print(f"[Email] Delivery notification sent to {event.customer_email}")


class LoyaltyService:
    def __init__(self) -> None:
        self.points: dict[str, float] = {}

    def handle(self, event: OrderEvent) -> None:
        earned = event.total * 0.1
        self.points[event.customer_email] = self.points.get(event.customer_email, 0) + earned
        print(f"[Loyalty] {earned:.1f} points awarded to {event.customer_email}")
