"""Tests for Observer Event Bus exercise."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import EventBus, OrderEvent, InventoryService, ShippingService, EmailService, LoyaltyService


def make_event(event_type: str, order_id: str = "ORD-001", total: float = 100.0) -> OrderEvent:
    return OrderEvent(event_type=event_type, order_id=order_id,
                      customer_email="test@example.com", items=["Widget"], total=total)


class TestEventBus:
    def test_subscriber_receives_event(self):
        bus = EventBus()
        received = []
        bus.subscribe("order.placed", lambda e: received.append(e))
        bus.publish(make_event("order.placed"))
        assert len(received) == 1

    def test_subscriber_only_receives_matching_event(self):
        bus = EventBus()
        received = []
        bus.subscribe("order.placed", lambda e: received.append(e))
        bus.publish(make_event("order.shipped"))
        assert len(received) == 0

    def test_multiple_subscribers_same_event(self):
        bus = EventBus()
        count = [0]
        bus.subscribe("order.placed", lambda e: count.__setitem__(0, count[0] + 1))
        bus.subscribe("order.placed", lambda e: count.__setitem__(0, count[0] + 1))
        bus.publish(make_event("order.placed"))
        assert count[0] == 2

    def test_unsubscribe_stops_delivery(self):
        bus = EventBus()
        received = []
        handler = lambda e: received.append(e)
        bus.subscribe("order.placed", handler)
        bus.unsubscribe("order.placed", handler)
        bus.publish(make_event("order.placed"))
        assert len(received) == 0


class TestServices:
    def setup_method(self):
        self.bus = EventBus()
        self.inventory = InventoryService()
        self.shipping = ShippingService()
        self.email = EmailService()
        self.loyalty = LoyaltyService()

        self.bus.subscribe("order.placed", self.inventory.handle)
        self.bus.subscribe("order.placed", self.shipping.handle)
        self.bus.subscribe("order.placed", self.email.on_placed)
        self.bus.subscribe("order.shipped", self.email.on_shipped)
        self.bus.subscribe("order.delivered", self.email.on_delivered)
        self.bus.subscribe("order.delivered", self.loyalty.handle)

    def test_inventory_reserves_on_placed(self):
        self.bus.publish(make_event("order.placed"))
        assert "ORD-001" in self.inventory.reservations

    def test_shipping_scheduled_on_placed(self):
        self.bus.publish(make_event("order.placed"))
        assert "ORD-001" in self.shipping.scheduled

    def test_email_sent_on_placed(self):
        self.bus.publish(make_event("order.placed"))
        assert any(e["subject"] == "Order Confirmed" for e in self.email.emails_sent)

    def test_email_sent_on_shipped(self):
        self.bus.publish(make_event("order.shipped"))
        assert any(e["subject"] == "Order Shipped" for e in self.email.emails_sent)

    def test_loyalty_points_awarded_on_delivered(self):
        self.bus.publish(make_event("order.delivered", total=200.0))
        email = "test@example.com"
        assert self.loyalty.points.get(email, 0) == 20.0  # 200 * 0.1

    def test_inventory_not_called_on_delivered(self):
        self.bus.publish(make_event("order.delivered"))
        assert len(self.inventory.reservations) == 0
