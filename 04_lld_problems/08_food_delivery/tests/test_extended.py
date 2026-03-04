"""
Extended tests for Problem 08: Food Delivery System.
Tests multi-item orders, multiple agents, search filters, ratings.
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
    DeliveryFeeCalculator,
)


# ---------- Delivery Fee Calculator ----------

def test_delivery_fee_zero_distance():
    fee = DeliveryFeeCalculator.calculate(Location(0, 0), Location(0, 0))
    assert abs(fee - 2.00) < 0.01


def test_delivery_fee_known_distance():
    # distance = sqrt(3^2 + 4^2) = 5 km  →  2.00 + 0.50*5 = 4.50
    fee = DeliveryFeeCalculator.calculate(Location(0, 0), Location(3, 4))
    assert abs(fee - 4.50) < 0.01


def test_delivery_fee_horizontal():
    # distance = 10 km  →  2.00 + 0.50*10 = 7.00
    fee = DeliveryFeeCalculator.calculate(Location(0, 0), Location(10, 0))
    assert abs(fee - 7.00) < 0.01


# ---------- Multi-item Orders ----------

def test_place_order_multiple_items():
    app = FoodDeliveryApp()
    r = app.add_restaurant("Cafe", "Cafe", Location(0, 0))
    item1 = r.add_menu_item("Coffee", 3.00, "veg")
    item2 = r.add_menu_item("Cake", 5.00, "veg")
    c = app.add_customer("Carol", Location(0, 0))

    order = app.place_order(
        c.customer_id, r.restaurant_id,
        {item1.item_id: 2, item2.item_id: 1}
    )
    assert len(order.items) == 2
    # subtotals: 6.00 + 5.00 = 11.00, fee = 2.00, total = 13.00
    assert abs(order.total_amount - 13.00) < 0.01


def test_order_item_subtotals():
    app = FoodDeliveryApp()
    r = app.add_restaurant("Deli", "Deli", Location(0, 0))
    item = r.add_menu_item("Sandwich", 7.50, "veg")
    c = app.add_customer("Dan", Location(0, 0))

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 3})
    oi = order.items[0]
    assert abs(oi.subtotal - 22.50) < 0.01


# ---------- Multiple Agents — Nearest Assignment ----------

def test_nearest_agent_selected():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(10, 10))

    far_agent = app.add_delivery_agent("Far", Location(100, 100))
    near_agent = app.add_delivery_agent("Near", Location(1, 1))

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    assigned = app.assign_delivery_agent(order.order_id)

    assert assigned is near_agent


def test_second_order_gets_next_available_agent():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(1, 1))

    agent1 = app.add_delivery_agent("A1", Location(0.5, 0.5))
    agent2 = app.add_delivery_agent("A2", Location(0.6, 0.6))

    order1 = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    a = app.assign_delivery_agent(order1.order_id)

    order2 = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    b = app.assign_delivery_agent(order2.order_id)

    assert a is not b
    assert {a, b} == {agent1, agent2}


# ---------- Search Filters ----------

def test_search_by_prep_time():
    app = FoodDeliveryApp()
    app.add_restaurant("Fast Food", "American", Location(0, 0), prep_time=10)
    app.add_restaurant("Slow Gourmet", "French", Location(0, 0), prep_time=60)

    results = app.search_restaurants(max_delivery_time=15)
    names = [r.name for r in results]
    assert "Fast Food" in names
    assert "Slow Gourmet" not in names


def test_search_cuisine_case_insensitive():
    app = FoodDeliveryApp()
    app.add_restaurant("Spice Palace", "indian", Location(0, 0))
    results = app.search_restaurants(cuisine_type="Indian")
    assert len(results) == 1


def test_search_combined_filters():
    app = FoodDeliveryApp()
    app.add_restaurant("Quick Indian", "Indian", Location(0, 0), prep_time=20)
    app.add_restaurant("Slow Indian", "Indian", Location(0, 0), prep_time=90)
    app.add_restaurant("Quick Italian", "Italian", Location(0, 0), prep_time=15)

    results = app.search_restaurants(cuisine_type="Indian", max_delivery_time=30)
    assert len(results) == 1
    assert results[0].name == "Quick Indian"


# ---------- Cancellation ----------

def test_cancel_order():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    c = app.add_customer("C", Location(0, 0))
    agent = app.add_delivery_agent("A", Location(0, 0))

    order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
    app.assign_delivery_agent(order.order_id)
    app.update_order_status(order.order_id, OrderStatus.CANCELLED)

    assert order.status == OrderStatus.CANCELLED
    assert agent.status == AgentStatus.AVAILABLE


# ---------- Multiple Ratings / Average ----------

def test_restaurant_rating_average():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")
    agent = app.add_delivery_agent("A", Location(0, 0))

    def make_and_deliver():
        c = app.add_customer("C", Location(0, 0))
        order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 1})
        app.assign_delivery_agent(order.order_id)
        for s in [
            OrderStatus.CONFIRMED, OrderStatus.PREPARING,
            OrderStatus.READY, OrderStatus.PICKED_UP, OrderStatus.DELIVERED,
        ]:
            app.update_order_status(order.order_id, s)
        return order

    o1 = make_and_deliver()
    app.rate_restaurant(o1.order_id, 4)
    o2 = make_and_deliver()
    app.rate_restaurant(o2.order_id, 2)

    # Average of 4 and 2 = 3.0
    assert abs(r.rating - 3.0) < 0.01


# ---------- Multiple Customers ----------

def test_multiple_customers_independent_histories():
    app = FoodDeliveryApp()
    r = app.add_restaurant("R", "Any", Location(0, 0))
    item = r.add_menu_item("X", 5.00, "veg")

    c1 = app.add_customer("Alice", Location(0, 0))
    c2 = app.add_customer("Bob", Location(0, 0))

    app.add_delivery_agent("A", Location(0, 0))

    o1 = app.place_order(c1.customer_id, r.restaurant_id, {item.item_id: 1})
    o2 = app.place_order(c2.customer_id, r.restaurant_id, {item.item_id: 1})

    assert o1 in c1.order_history
    assert o1 not in c2.order_history
    assert o2 in c2.order_history
    assert o2 not in c1.order_history
