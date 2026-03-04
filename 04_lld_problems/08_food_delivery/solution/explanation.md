# Explanation: Food Delivery System

## Overview

This solution models a food delivery platform (think DoorDash or Swiggy) using straightforward object-oriented design. Every entity—Restaurant, Customer, DeliveryAgent, Order—is represented as a class with clearly defined responsibilities.

---

## Design Patterns Applied

### 1. State Pattern — Order Lifecycle

The `Order` class owns a `status: OrderStatus` and an explicit transition table:

```python
VALID_TRANSITIONS = {
    OrderStatus.PLACED:    [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
    ...
    OrderStatus.DELIVERED: [],  # terminal
}
```

`order.transition_to(new_status)` checks this table and raises `ValueError` on illegal jumps. This ensures the lifecycle is impossible to corrupt from outside the class.

### 2. Observer (simplified) — Status Side Effects

`FoodDeliveryApp.update_order_status()` acts as the coordinator:
- On `DELIVERED` → agent goes back to `AVAILABLE`
- On `CANCELLED` → agent (if assigned) goes back to `AVAILABLE`

In a production system you would register real observers (push notification services, billing, analytics). Here the app class plays that role directly.

### 3. Strategy Pattern — Agent Assignment

`assign_delivery_agent()` uses a "nearest available" strategy:

```python
nearest = min(available_agents, key=lambda a: a.location.distance_to(restaurant.location))
```

To swap strategies (zone-based, load-balanced, priority queues), you would extract this lambda into a callable `AgentSelectionStrategy` and inject it into `FoodDeliveryApp.__init__`.

---

## Delivery Fee Calculation

```
fee = $2.00 (flat) + $0.50 × distance_km
distance_km = sqrt((x2-x1)^2 + (y2-y1)^2)
```

`DeliveryFeeCalculator` is a stateless utility class (all static methods). It can be replaced with a pricing engine that accounts for surge pricing, peak hours, or distance tiers.

---

## Rating System

Ratings use a cumulative moving average:

```python
new_avg = (old_avg * count + new_rating) / (count + 1)
```

This avoids storing all individual ratings while maintaining correctness. Both `Restaurant` and `DeliveryAgent` implement `update_rating()` this way.

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| UUID IDs | Collision-free without a database sequence |
| `Location` as dataclass | Immutable value object; `distance_to()` is the only behaviour |
| `OrderItem.subtotal` as property | Derived value, not stored; always consistent |
| `order_history` on Customer | Enables per-customer order lookup without a database query |
| Items validated against restaurant menu | Prevents cross-restaurant item injection |
| Raising `ValueError` everywhere | Simple, standard Python exception for invalid business rules |

---

## Extensibility Points

1. **Payment**: Add a `PaymentService` called in `place_order()` before creating the Order.
2. **Notifications**: Register `OrderObserver` callbacks on status changes.
3. **Real GPS**: Replace `Location(x, y)` with `Location(lat, lon)` and swap Euclidean distance for Haversine.
4. **Castling / En Passant analogy**: Promo codes, restaurant discounts — add a `DiscountStrategy` that modifies the order total before creation.
5. **Persistence**: Replace the in-memory dicts with a repository abstraction backed by SQL or NoSQL.
