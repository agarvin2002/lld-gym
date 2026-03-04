"""
Problem 08: Food Delivery System — Complete Solution

Run tests with:
    pytest tests/
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class OrderStatus(Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    PICKED_UP = "PICKED_UP"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class AgentStatus(Enum):
    AVAILABLE = "AVAILABLE"
    DELIVERING = "DELIVERING"
    OFFLINE = "OFFLINE"


# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------

@dataclass
class Location:
    x: float
    y: float

    def distance_to(self, other: "Location") -> float:
        """Return Euclidean distance to another Location."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


# ---------------------------------------------------------------------------
# Domain Entities
# ---------------------------------------------------------------------------

class MenuItem:
    def __init__(self, name: str, price: float, category: str) -> None:
        self.item_id: str = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self) -> str:
        return f"MenuItem({self.name!r}, ${self.price:.2f})"


class Restaurant:
    def __init__(
        self,
        name: str,
        cuisine_type: str,
        location: Location,
        prep_time: int = 30,
        is_open: bool = True,
    ) -> None:
        self.restaurant_id: str = str(uuid.uuid4())
        self.name = name
        self.cuisine_type = cuisine_type
        self.location = location
        self.prep_time = prep_time
        self.is_open = is_open
        self._menu: Dict[str, MenuItem] = {}
        self.rating: float = 0.0
        self._rating_count: int = 0

    def add_menu_item(self, name: str, price: float, category: str) -> MenuItem:
        item = MenuItem(name, price, category)
        self._menu[item.item_id] = item
        return item

    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        return self._menu.get(item_id)

    @property
    def menu(self) -> List[MenuItem]:
        return list(self._menu.values())

    def update_rating(self, rating: int) -> None:
        """Cumulative moving average."""
        self.rating = (self.rating * self._rating_count + rating) / (self._rating_count + 1)
        self._rating_count += 1

    def __repr__(self) -> str:
        return f"Restaurant({self.name!r}, {'open' if self.is_open else 'closed'})"


@dataclass
class OrderItem:
    menu_item: MenuItem
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.menu_item.price * self.quantity


class Customer:
    def __init__(self, name: str, location: Location) -> None:
        self.customer_id: str = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.order_history: List["Order"] = []

    def __repr__(self) -> str:
        return f"Customer({self.name!r})"


class DeliveryAgent:
    def __init__(self, name: str, current_location: Location) -> None:
        self.agent_id: str = str(uuid.uuid4())
        self.name = name
        self.current_location = current_location
        self.status: AgentStatus = AgentStatus.AVAILABLE
        self.rating: float = 0.0
        self._rating_count: int = 0

    def update_rating(self, rating: int) -> None:
        self.rating = (self.rating * self._rating_count + rating) / (self._rating_count + 1)
        self._rating_count += 1

    def __repr__(self) -> str:
        return f"DeliveryAgent({self.name!r}, {self.status.value})"


class Order:
    VALID_TRANSITIONS: Dict[OrderStatus, List[OrderStatus]] = {
        OrderStatus.PLACED:    [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
        OrderStatus.PREPARING: [OrderStatus.READY,     OrderStatus.CANCELLED],
        OrderStatus.READY:     [OrderStatus.PICKED_UP],
        OrderStatus.PICKED_UP: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    def __init__(
        self,
        customer: Customer,
        restaurant: Restaurant,
        items: List[OrderItem],
        delivery_fee: float,
    ) -> None:
        self.order_id: str = str(uuid.uuid4())
        self.customer = customer
        self.restaurant = restaurant
        self.items = items
        self.delivery_fee = delivery_fee
        self.status: OrderStatus = OrderStatus.PLACED
        self.delivery_agent: Optional[DeliveryAgent] = None

    @property
    def total_amount(self) -> float:
        return sum(oi.subtotal for oi in self.items) + self.delivery_fee

    def transition_to(self, new_status: OrderStatus) -> None:
        allowed = self.VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Cannot transition from {self.status.value} to {new_status.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        self.status = new_status

    def __repr__(self) -> str:
        return f"Order({self.order_id[:8]}…, {self.status.value})"


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

class DeliveryFeeCalculator:
    FLAT_FEE: float = 2.00
    PER_KM_RATE: float = 0.50

    @staticmethod
    def calculate(restaurant_location: Location, customer_location: Location) -> float:
        distance = restaurant_location.distance_to(customer_location)
        return DeliveryFeeCalculator.FLAT_FEE + DeliveryFeeCalculator.PER_KM_RATE * distance


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------

class FoodDeliveryApp:
    def __init__(self) -> None:
        self._restaurants: Dict[str, Restaurant] = {}
        self._customers: Dict[str, Customer] = {}
        self._agents: Dict[str, DeliveryAgent] = {}
        self._orders: Dict[str, Order] = {}

    # --- Setup helpers ---

    def add_restaurant(
        self,
        name: str,
        cuisine_type: str,
        location: Location,
        prep_time: int = 30,
        is_open: bool = True,
    ) -> Restaurant:
        r = Restaurant(name, cuisine_type, location, prep_time, is_open)
        self._restaurants[r.restaurant_id] = r
        return r

    def add_customer(self, name: str, location: Location) -> Customer:
        c = Customer(name, location)
        self._customers[c.customer_id] = c
        return c

    def add_delivery_agent(self, name: str, location: Location) -> DeliveryAgent:
        agent = DeliveryAgent(name, location)
        self._agents[agent.agent_id] = agent
        return agent

    # --- Core operations ---

    def search_restaurants(
        self,
        cuisine_type: Optional[str] = None,
        max_delivery_time: Optional[int] = None,
    ) -> List[Restaurant]:
        results = [r for r in self._restaurants.values() if r.is_open]
        if cuisine_type is not None:
            results = [
                r for r in results
                if r.cuisine_type.lower() == cuisine_type.lower()
            ]
        if max_delivery_time is not None:
            results = [r for r in results if r.prep_time <= max_delivery_time]
        return results

    def place_order(
        self,
        customer_id: str,
        restaurant_id: str,
        items: Dict[str, int],
    ) -> Order:
        customer = self._customers.get(customer_id)
        if customer is None:
            raise ValueError(f"Customer '{customer_id}' not found.")

        restaurant = self._restaurants.get(restaurant_id)
        if restaurant is None:
            raise ValueError(f"Restaurant '{restaurant_id}' not found.")

        if not restaurant.is_open:
            raise ValueError(f"Restaurant '{restaurant.name}' is currently closed.")

        if not items:
            raise ValueError("Order must contain at least one item.")

        order_items: List[OrderItem] = []
        for item_id, qty in items.items():
            menu_item = restaurant.get_menu_item(item_id)
            if menu_item is None:
                raise ValueError(
                    f"Item '{item_id}' is not on the menu of '{restaurant.name}'."
                )
            order_items.append(OrderItem(menu_item=menu_item, quantity=qty))

        fee = DeliveryFeeCalculator.calculate(restaurant.location, customer.location)
        order = Order(customer=customer, restaurant=restaurant, items=order_items, delivery_fee=fee)

        self._orders[order.order_id] = order
        customer.order_history.append(order)
        return order

    def assign_delivery_agent(self, order_id: str) -> DeliveryAgent:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found.")

        available = [
            a for a in self._agents.values()
            if a.status == AgentStatus.AVAILABLE
        ]
        if not available:
            raise ValueError("No delivery agents currently available.")

        # Pick nearest agent to the restaurant
        nearest = min(
            available,
            key=lambda a: a.current_location.distance_to(order.restaurant.location),
        )
        nearest.status = AgentStatus.DELIVERING
        order.delivery_agent = nearest
        return nearest

    def update_order_status(self, order_id: str, status: OrderStatus) -> None:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found.")

        order.transition_to(status)

        # Side effects
        if status == OrderStatus.DELIVERED:
            if order.delivery_agent:
                order.delivery_agent.status = AgentStatus.AVAILABLE

        elif status == OrderStatus.CANCELLED:
            if order.delivery_agent and order.delivery_agent.status == AgentStatus.DELIVERING:
                order.delivery_agent.status = AgentStatus.AVAILABLE

    def track_order(self, order_id: str) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found.")
        return order

    def rate_restaurant(self, order_id: str, rating: int) -> None:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found.")
        if order.status != OrderStatus.DELIVERED:
            raise ValueError("Can only rate a DELIVERED order.")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        order.restaurant.update_rating(rating)

    def rate_agent(self, order_id: str, rating: int) -> None:
        order = self._orders.get(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found.")
        if order.status != OrderStatus.DELIVERED:
            raise ValueError("Can only rate a DELIVERED order.")
        if order.delivery_agent is None:
            raise ValueError("No delivery agent assigned to this order.")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        order.delivery_agent.update_rating(rating)
