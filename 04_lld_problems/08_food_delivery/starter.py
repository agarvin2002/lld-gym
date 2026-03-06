"""
Food Delivery System — Starter File
=====================================
Your task: Implement a food delivery platform (DoorDash/Swiggy style).

Read problem.md and design.md before starting.

Design decisions:
  - Location uses Euclidean distance for proximity calculations
  - Order has a VALID_TRANSITIONS dict — use it to enforce status flow
  - Nearest delivery agent to the restaurant is selected on assignment
  - DeliveryFeeCalculator: flat fee + per-km rate * distance
  - Restaurant and DeliveryAgent have cumulative moving-average ratings
  - Use uuid.uuid4() for all IDs
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
    PLACED    = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY     = "READY"
    PICKED_UP = "PICKED_UP"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class AgentStatus(Enum):
    AVAILABLE  = "AVAILABLE"
    DELIVERING = "DELIVERING"
    OFFLINE    = "OFFLINE"


# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------

@dataclass
class Location:
    x: float
    y: float

    def distance_to(self, other: "Location") -> float:
        # TODO: Return Euclidean distance: sqrt((x diff)^2 + (y diff)^2)
        pass


# ---------------------------------------------------------------------------
# Domain Entities
# ---------------------------------------------------------------------------

class MenuItem:
    def __init__(self, name: str, price: float, category: str) -> None:
        # TODO: Set item_id = str(uuid.uuid4())
        # TODO: Store name, price, category
        pass

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
        # TODO: Set restaurant_id = str(uuid.uuid4())
        # TODO: Store all parameters
        # TODO: Create _menu: Dict[str, MenuItem] = {}
        # TODO: Set rating = 0.0 and _rating_count = 0
        pass

    def add_menu_item(self, name: str, price: float, category: str) -> MenuItem:
        """Create a MenuItem, add to _menu, and return it.

        TODO:
            - Create MenuItem(name, price, category)
            - Store in self._menu[item.item_id]
            - Return item
        """
        pass

    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        # TODO: Return item from _menu or None
        pass

    @property
    def menu(self) -> List[MenuItem]:
        # TODO: Return a list of all items in _menu
        pass

    def update_rating(self, rating: int) -> None:
        """Update cumulative moving average rating.

        TODO:
            - new_rating = (current * count + rating) / (count + 1)
            - Increment _rating_count
        """
        pass

    def __repr__(self) -> str:
        return f"Restaurant({self.name!r}, {'open' if self.is_open else 'closed'})"


@dataclass
class OrderItem:
    menu_item: MenuItem
    quantity: int

    @property
    def subtotal(self) -> float:
        # TODO: Return menu_item.price * quantity
        pass


class Customer:
    def __init__(self, name: str, location: Location) -> None:
        # TODO: Set customer_id = str(uuid.uuid4())
        # TODO: Store name and location
        # TODO: Create order_history: List["Order"] = []
        pass

    def __repr__(self) -> str:
        return f"Customer({self.name!r})"


class DeliveryAgent:
    def __init__(self, name: str, current_location: Location) -> None:
        # TODO: Set agent_id = str(uuid.uuid4())
        # TODO: Store name and current_location
        # TODO: Set status = AgentStatus.AVAILABLE
        # TODO: Set rating = 0.0 and _rating_count = 0
        pass

    def update_rating(self, rating: int) -> None:
        # TODO: Same cumulative average formula as Restaurant
        pass

    def __repr__(self) -> str:
        return f"DeliveryAgent({self.name!r}, {self.status.value})"


class Order:
    # Valid state transitions — do not change this
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
        # TODO: Set order_id = str(uuid.uuid4())
        # TODO: Store customer, restaurant, items, delivery_fee
        # TODO: Set status = OrderStatus.PLACED
        # TODO: Set delivery_agent = None
        pass

    @property
    def total_amount(self) -> float:
        # TODO: Return sum of item subtotals + delivery_fee
        pass

    def transition_to(self, new_status: OrderStatus) -> None:
        """Transition to a new status, enforcing VALID_TRANSITIONS.

        TODO:
            - Look up allowed transitions from VALID_TRANSITIONS[self.status]
            - Raise ValueError if new_status not in allowed list
              (include current status and allowed statuses in message)
            - Set self.status = new_status
        """
        pass

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
        # TODO: Return FLAT_FEE + PER_KM_RATE * distance between locations
        pass


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------

class FoodDeliveryApp:
    def __init__(self) -> None:
        # TODO: Create _restaurants, _customers, _agents, _orders
        #       as empty dicts keyed by their respective IDs
        pass

    def add_restaurant(
        self,
        name: str,
        cuisine_type: str,
        location: Location,
        prep_time: int = 30,
        is_open: bool = True,
    ) -> Restaurant:
        """Create, register, and return a Restaurant.

        TODO:
            - Create Restaurant with given args
            - Store in _restaurants and return it
        """
        pass

    def add_customer(self, name: str, location: Location) -> Customer:
        # TODO: Create Customer, store in _customers, return it
        pass

    def add_delivery_agent(self, name: str, location: Location) -> DeliveryAgent:
        # TODO: Create DeliveryAgent, store in _agents, return it
        pass

    def search_restaurants(
        self,
        cuisine_type: Optional[str] = None,
        max_delivery_time: Optional[int] = None,
    ) -> List[Restaurant]:
        """Search open restaurants by optional filters.

        TODO:
            - Start with all open restaurants
            - If cuisine_type provided: filter case-insensitively
            - If max_delivery_time provided: filter by prep_time <= max_delivery_time
            - Return results
        """
        pass

    def place_order(
        self,
        customer_id: str,
        restaurant_id: str,
        items: Dict[str, int],   # item_id → quantity
    ) -> Order:
        """Place a customer order.

        TODO:
            - Raise ValueError if customer or restaurant not found
            - Raise ValueError if restaurant is closed
            - Raise ValueError if items dict is empty
            - Build List[OrderItem] — raise ValueError if any item_id not on menu
            - Calculate delivery fee via DeliveryFeeCalculator.calculate(...)
            - Create Order, store in _orders, append to customer.order_history
            - Return the order
        """
        pass

    def assign_delivery_agent(self, order_id: str) -> DeliveryAgent:
        """Assign the nearest available agent to an order.

        TODO:
            - Raise ValueError if order not found
            - Filter agents with status == AVAILABLE
            - Raise ValueError if none available
            - Select nearest to order.restaurant.location
            - Set agent.status = DELIVERING and order.delivery_agent = agent
            - Return the agent
        """
        pass

    def update_order_status(self, order_id: str, status: OrderStatus) -> None:
        """Transition order to new status with side effects.

        TODO:
            - Raise ValueError if order not found
            - Call order.transition_to(status)
            - Side effect: if DELIVERED → set delivery_agent.status = AVAILABLE
            - Side effect: if CANCELLED → if agent is DELIVERING, set to AVAILABLE
        """
        pass

    def track_order(self, order_id: str) -> Order:
        # TODO: Raise ValueError if not found; return the order
        pass

    def rate_restaurant(self, order_id: str, rating: int) -> None:
        """Rate restaurant after delivery.

        TODO:
            - Raise ValueError if order not found, not DELIVERED, or rating not 1-5
            - Call restaurant.update_rating(rating)
        """
        pass

    def rate_agent(self, order_id: str, rating: int) -> None:
        """Rate delivery agent after delivery.

        TODO:
            - Raise ValueError if order not found, not DELIVERED,
              no agent assigned, or rating not 1-5
            - Call delivery_agent.update_rating(rating)
        """
        pass
