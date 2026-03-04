"""
Basic tests for Problem 08: Food Delivery System.
Tests core happy-path functionality.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

from starter import (
    FoodDeliveryApp,
    Location,
    OrderStatus,
    AgentStatus,
)


def make_app():
    """Return a FoodDeliveryApp populated with one restaurant, one customer, one agent."""
    app = FoodDeliveryApp()

    loc_r = Location(0.0, 0.0)
    r = app.add_restaurant("Burger Palace", "American", loc_r, prep_time=20)
    r.add_menu_item("Cheeseburger", 8.99, "non-veg")
    r.add_menu_item("Fries", 3.49, "veg")

    loc_c = Location(3.0, 4.0)  # 5 km away
    app.add_customer("Alice", loc_c)

    loc_a = Location(1.0, 1.0)
    app.add_delivery_agent("Bob", loc_a)

    return app


# ---------- Restaurant / Search ----------

def test_add_restaurant():
    app = FoodDeliveryApp()
    r = app.add_restaurant("Pizza Place", "Italian", Location(0, 0))
    assert r.name == "Pizza Place"
    assert r.cuisine_type == "Italian"
    assert r.is_open is True


def test_add_menu_item():
    app = FoodDeliveryApp()
    r = app.add_restaurant("Sushi Bar", "Japanese", Location(0, 0))
    item = r.add_menu_item("Salmon Roll", 12.50, "non-veg")
    assert item.name == "Salmon Roll"
    assert item.price == 12.50
    assert item.category == "non-veg"
    assert r.get_menu_item(item.item_id) is item


def test_search_all_open_restaurants():
    app = make_app()
    results = app.search_restaurants()
    assert len(results) == 1
    assert results[0].name == "Burger Palace"


def test_search_by_cuisine():
    app = make_app()
    app.add_restaurant("Taco Town", "Mexican", Location(5, 5))
    american = app.search_restaurants(cuisine_type="American")
    assert len(american) == 1
    assert american[0].name == "Burger Palace"


def test_search_excludes_closed():
    app = make_app()
    app.add_restaurant("Closed Cafe", "Cafe", Location(2, 2), is_open=False)
    results = app.search_restaurants()
    names = [r.name for r in results]
    assert "Closed Cafe" not in names


# ---------- Customer ----------

def test_add_customer():
    app = FoodDeliveryApp()
    c = app.add_customer("Bob", Location(1, 1))
    assert c.name == "Bob"
    assert c.order_history == []


# ---------- Delivery Agent ----------

def test_add_delivery_agent():
    app = FoodDeliveryApp()
    agent = app.add_delivery_agent("Dave", Location(2, 2))
    assert agent.name == "Dave"
    assert agent.status == AgentStatus.AVAILABLE


# ---------- Order Placement ----------

def test_place_order_success():
    app = make_app()
    restaurants = app.search_restaurants()
    r = restaurants[0]
    customers = list(app._customers.values())
    c = customers[0]

    item = r.menu[0]
    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 2})

    assert order is not None
    assert order.status == OrderStatus.PLACED
    assert len(order.items) == 1
    assert order.items[0].quantity == 2


def test_order_total_amount():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]  # $8.99

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    # subtotal = 8.99, delivery_fee = 2.00 + 0.50*5 = 4.50 → total = 13.49
    assert abs(order.total_amount - 13.49) < 0.01


def test_order_added_to_customer_history():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    assert order in c.order_history


# ---------- Tracking ----------

def test_track_order():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    tracked = app.track_order(order.order_id)
    assert tracked is order


# ---------- Agent Assignment ----------

def test_assign_delivery_agent():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    agent = app.assign_delivery_agent(order.order_id)

    assert agent is not None
    assert agent.status == AgentStatus.DELIVERING
    assert order.delivery_agent is agent


# ---------- Status Updates ----------

def test_status_transitions():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    app.assign_delivery_agent(order.order_id)

    for status in [
        OrderStatus.CONFIRMED,
        OrderStatus.PREPARING,
        OrderStatus.READY,
        OrderStatus.PICKED_UP,
        OrderStatus.DELIVERED,
    ]:
        app.update_order_status(order.order_id, status)
        assert order.status == status


def test_agent_freed_on_delivery():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    agent = app.assign_delivery_agent(order.order_id)

    for status in [
        OrderStatus.CONFIRMED,
        OrderStatus.PREPARING,
        OrderStatus.READY,
        OrderStatus.PICKED_UP,
        OrderStatus.DELIVERED,
    ]:
        app.update_order_status(order.order_id, status)

    assert agent.status == AgentStatus.AVAILABLE


# ---------- Rating ----------

def test_rate_restaurant_after_delivery():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    app.assign_delivery_agent(order.order_id)
    for status in [
        OrderStatus.CONFIRMED, OrderStatus.PREPARING,
        OrderStatus.READY, OrderStatus.PICKED_UP, OrderStatus.DELIVERED,
    ]:
        app.update_order_status(order.order_id, status)

    app.rate_restaurant(order.order_id, 5)
    assert r.rating == 5.0


def test_rate_agent_after_delivery():
    app = make_app()
    r = list(app._restaurants.values())[0]
    c = list(app._customers.values())[0]
    item = r.menu[0]

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    agent = app.assign_delivery_agent(order.order_id)
    for status in [
        OrderStatus.CONFIRMED, OrderStatus.PREPARING,
        OrderStatus.READY, OrderStatus.PICKED_UP, OrderStatus.DELIVERED,
    ]:
        app.update_order_status(order.order_id, status)

    app.rate_agent(order.order_id, 4)
    assert agent.rating == 4.0
