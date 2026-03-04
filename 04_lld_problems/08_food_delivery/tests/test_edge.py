"""
Edge-case tests for Problem 08: Food Delivery System.
Tests invalid inputs, error conditions, and boundary behavior.
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

from starter import (
    FoodDeliveryApp,
    Location,
    OrderStatus,
    AgentStatus,
)


# ---------- Invalid IDs ----------

def test_place_order_unknown_customer():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    with pytest.raises(ValueError):
        app.place_order("nonexistent-customer", r.restaurant_id, {item.item_id: 1})


def test_place_order_unknown_restaurant():
    app = FoodDeliveryApp()
    c = app.add_customer("C", Location(0, 0))
    with pytest.raises(ValueError):
        app.place_order(c.customer_id, "nonexistent-restaurant", {"some-item": 1})


def test_track_order_unknown_id():
    app = FoodDeliveryApp()
    with pytest.raises(ValueError):
        app.track_order("nonexistent-order")


def test_assign_agent_unknown_order():
    app = FoodDeliveryApp()
    with pytest.raises(ValueError):
        app.assign_delivery_agent("nonexistent-order")


# ---------- Closed Restaurant ----------

def test_place_order_closed_restaurant():
    app = FoodDeliveryApp()
    r = app.add_restaurant("Closed", "Any", Location(0, 0), is_open=False)
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    with pytest.raises(ValueError):
        app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})


# ---------- Invalid Menu Items ----------

def test_place_order_item_not_on_menu():
    app = FoodDeliveryApp()
    r1 = app.add_restaurant("R1", "Any", Location(0, 0))
    r2 = app.add_restaurant("R2", "Any", Location(0, 0))
    item_r2 = r2.add_menu_item("Other Item", 10.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    with pytest.raises(ValueError):
        app.place_order(c.customer_id, r1.restaurant_id, {item_r2.item_id: 1})


def test_place_order_empty_items():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    c = app.add_customer("C", Location(0, 0))
    with pytest.raises(ValueError):
        app.place_order(c.customer_id, r.restaurant_id, {})


# ---------- No Available Agent ----------

def test_assign_agent_none_available():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    # No agents added
    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    with pytest.raises(ValueError):
        app.assign_delivery_agent(order.order_id)


def test_assign_agent_all_offline():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    agent = app.add_delivery_agent("A", Location(0, 0))
    agent.status = AgentStatus.OFFLINE

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    with pytest.raises(ValueError):
        app.assign_delivery_agent(order.order_id)


# ---------- Invalid Status Transitions ----------

def test_invalid_status_transition_placed_to_delivered():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})

    with pytest.raises(ValueError):
        app.update_order_status(order.order_id, OrderStatus.DELIVERED)


def test_invalid_status_transition_delivered_to_cancelled():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    agent = app.add_delivery_agent("A", Location(0, 0))
    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    app.assign_delivery_agent(order.order_id)
    for s in [
        OrderStatus.CONFIRMED, OrderStatus.PREPARING,
        OrderStatus.READY, OrderStatus.PICKED_UP, OrderStatus.DELIVERED,
    ]:
        app.update_order_status(order.order_id, s)

    with pytest.raises(ValueError):
        app.update_order_status(order.order_id, OrderStatus.CANCELLED)


# ---------- Rating Edge Cases ----------

def test_rate_restaurant_before_delivery():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    with pytest.raises(ValueError):
        app.rate_restaurant(order.order_id, 5)


def test_rate_restaurant_invalid_rating_value():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    agent = app.add_delivery_agent("A", Location(0, 0))
    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    app.assign_delivery_agent(order.order_id)
    for s in [
        OrderStatus.CONFIRMED, OrderStatus.PREPARING,
        OrderStatus.READY, OrderStatus.PICKED_UP, OrderStatus.DELIVERED,
    ]:
        app.update_order_status(order.order_id, s)

    with pytest.raises(ValueError):
        app.rate_restaurant(order.order_id, 6)  # out of range

    with pytest.raises(ValueError):
        app.rate_restaurant(order.order_id, 0)  # out of range


def test_rate_agent_no_agent_assigned():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    # Manually bring order to DELIVERED without assigning agent is not possible
    # through normal flow; instead test that an order with no agent raises
    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    # Force-set status to DELIVERED without agent (bypass normal validation)
    order.status = OrderStatus.DELIVERED
    with pytest.raises(ValueError):
        app.rate_agent(order.order_id, 5)


# ---------- Location Distance ----------

def test_location_distance_to_self():
    loc = Location(3.0, 4.0)
    assert loc.distance_to(loc) == 0.0


def test_location_distance_symmetric():
    a = Location(0, 0)
    b = Location(3, 4)
    assert abs(a.distance_to(b) - b.distance_to(a)) < 1e-9
