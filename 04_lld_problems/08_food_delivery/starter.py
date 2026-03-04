"""
Problem 08: Food Delivery System (DoorDash / Swiggy Style)

Starter file — implement every class and method marked with TODO.
Run tests with:
    pytest tests/
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
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
        # TODO: implement
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Domain Entities
# ---------------------------------------------------------------------------

class MenuItem:
    def __init__(self, name: str, price: float, category: str) -> None:
        self.item_id: str = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.category = category  # e.g. "veg", "non-veg", "dessert"

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
        self.prep_time = prep_time          # minutes
        self.is_open = is_open
        self._menu: Dict[str, MenuItem] = {}
        self.rating: float = 0.0
        self._rating_count: int = 0

    def add_menu_item(self, name: str, price: float, category: str) -> MenuItem:
        """Create and store a MenuItem; return it."""
        # TODO: implement
        raise NotImplementedError

    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        """Return MenuItem by ID or None."""
        # TODO: implement
        raise NotImplementedError

    @property
    def menu(self) -> List[MenuItem]:
        return list(self._menu.values())

    def update_rating(self, rating: int) -> None:
        """Update cumulative average rating."""
        # TODO: implement
        raise NotImplementedError

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
        """Update cumulative average rating."""
        # TODO: implement
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"DeliveryAgent({self.name!r}, {self.status.value})"


class Order:
    # Valid status transitions
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
        """Sum of all item subtotals + delivery fee."""
        # TODO: implement
        raise NotImplementedError

    def transition_to(self, new_status: OrderStatus) -> None:
        """Validate and apply status transition. Raise ValueError on invalid."""
        # TODO: implement
        raise NotImplementedError

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
        """Return flat_fee + per_km_rate * euclidean_distance."""
        # TODO: implement
        raise NotImplementedError


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
        """Create, store, and return a Restaurant."""
        # TODO: implement
        raise NotImplementedError

    def add_customer(self, name: str, location: Location) -> Customer:
        """Create, store, and return a Customer."""
        # TODO: implement
        raise NotImplementedError

    def add_delivery_agent(self, name: str, location: Location) -> DeliveryAgent:
        """Create, store, and return a DeliveryAgent."""
        # TODO: implement
        raise NotImplementedError

    # --- Core operations ---

    def search_restaurants(
        self,
        cuisine_type: Optional[str] = None,
        max_delivery_time: Optional[int] = None,
    ) -> List[Restaurant]:
        """
        Return open restaurants filtered by:
        - cuisine_type (case-insensitive, if provided)
        - max_delivery_time in minutes (uses restaurant.prep_time, if provided)
        """
        # TODO: implement
        raise NotImplementedError

    def place_order(
        self,
        customer_id: str,
        restaurant_id: str,
        items: Dict[str, int],  # {item_id: quantity}
    ) -> Order:
        """
        Validate inputs, build OrderItems, calculate fee, create Order.
        Raise ValueError for unknown IDs, closed restaurant, or unknown items.
        """
        # TODO: implement
        raise NotImplementedError

    def assign_delivery_agent(self, order_id: str) -> DeliveryAgent:
        """
        Find nearest AVAILABLE agent to the order's restaurant.
        Assign agent to order, set agent status to DELIVERING.
        Raise ValueError if no agent available or order not found.
        """
        # TODO: implement
        raise NotImplementedError

    def update_order_status(self, order_id: str, status: OrderStatus) -> None:
        """
        Transition order to new status.
        When DELIVERED: set agent back to AVAILABLE.
        When CANCELLED (before PICKED_UP): set agent back to AVAILABLE if assigned.
        """
        # TODO: implement
        raise NotImplementedError

    def track_order(self, order_id: str) -> Order:
        """Return Order by ID. Raise ValueError if not found."""
        # TODO: implement
        raise NotImplementedError

    def rate_restaurant(self, order_id: str, rating: int) -> None:
        """
        Rate the restaurant for a DELIVERED order.
        rating must be 1-5. Raise ValueError otherwise.
        """
        # TODO: implement
        raise NotImplementedError

    def rate_agent(self, order_id: str, rating: int) -> None:
        """
        Rate the delivery agent for a DELIVERED order.
        rating must be 1-5. Raise ValueError if order not delivered or no agent.
        """
        # TODO: implement
        raise NotImplementedError
