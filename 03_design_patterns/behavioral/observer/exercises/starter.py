"""
WHAT YOU'RE BUILDING
====================
An e-commerce event bus. When an order changes state (placed, shipped,
delivered), the EventBus notifies all services that subscribed to that event.

Services:
- InventoryService — reserves stock when an order is placed
- ShippingService  — schedules delivery when an order is placed
- EmailService     — sends confirmation emails at each status change
- LoyaltyService   — awards points when an order is delivered

You're implementing the EventBus (the subject) and filling in each service.
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
    """Central event bus. Publishers emit events; subscribers handle them."""

    def __init__(self) -> None:
        # HINT: Use defaultdict(list) so you can append handlers without
        #       checking whether the key exists first.
        # TODO: Initialize self._handlers as defaultdict(list)
        pass

    def subscribe(self, event_type: str, handler: Callable[[OrderEvent], None]) -> None:
        # TODO: Append handler to self._handlers[event_type]
        pass

    def unsubscribe(self, event_type: str, handler: Callable[[OrderEvent], None]) -> None:
        # TODO: Remove handler from self._handlers[event_type]; ignore if not found
        pass

    def publish(self, event: OrderEvent) -> None:
        # HINT: Look up self._handlers[event.event_type] and call each handler
        #       with the event object. Iterate over a copy so handlers can safely
        #       unsubscribe themselves during the loop.
        # TODO: Call every handler in self._handlers[event.event_type] with event
        pass


class InventoryService:
    def __init__(self) -> None:
        self.reservations: list[str] = []

    def handle(self, event: OrderEvent) -> None:
        # TODO: Append event.order_id to self.reservations and print a message
        pass


class ShippingService:
    def __init__(self) -> None:
        self.scheduled: list[str] = []

    def handle(self, event: OrderEvent) -> None:
        # TODO: Append event.order_id to self.scheduled and print a message
        pass


class EmailService:
    def __init__(self) -> None:
        self.emails_sent: list[dict] = []

    def on_placed(self, event: OrderEvent) -> None:
        # TODO: Append {"to": event.customer_email, "subject": "Order Confirmed"}
        #       to self.emails_sent and print a message
        pass

    def on_shipped(self, event: OrderEvent) -> None:
        # TODO: Append {"to": event.customer_email, "subject": "Order Shipped"}
        #       to self.emails_sent and print a message
        pass

    def on_delivered(self, event: OrderEvent) -> None:
        # TODO: Append {"to": event.customer_email, "subject": "Order Delivered"}
        #       to self.emails_sent and print a message
        pass


class LoyaltyService:
    def __init__(self) -> None:
        self.points: dict[str, float] = {}

    def handle(self, event: OrderEvent) -> None:
        # HINT: Points = event.total * 0.1. Use self.points.get(email, 0) to
        #       accumulate points across multiple orders for the same customer.
        # TODO: Add event.total * 0.1 to self.points[event.customer_email]
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/behavioral/observer/exercises/tests.py -v
#
# Run all 03_design_patterns exercises at once:
#   /tmp/lld_venv/bin/pytest 03_design_patterns/ -v
# =============================================================================
