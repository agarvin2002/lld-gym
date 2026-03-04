# Problem 08: Food Delivery System (DoorDash / Swiggy Style)

## Problem Statement

Design a food delivery platform where customers can browse restaurants, place orders, and track deliveries. Delivery agents pick up orders and deliver them to customers.

---

## Functional Requirements

1. **Restaurants**
   - Each restaurant has: name, cuisine type, menu, open/closed status, estimated prep time (minutes), location
   - Menu contains `MenuItem` objects: name, price, category (e.g., "veg", "non-veg", "dessert")

2. **Customers**
   - Attributes: customer_id, name, address (Location), order_history

3. **Delivery Agents**
   - Attributes: agent_id, name, current_location, status (AVAILABLE / DELIVERING / OFFLINE)

4. **Orders**
   - Attributes: order_id, customer, restaurant, items (list of OrderItem), status, total_amount
   - `OrderItem`: references a MenuItem, quantity, subtotal (price × quantity)

5. **Operations**
   - `search_restaurants(cuisine_type=None, max_delivery_time=None)` → list of open restaurants
   - `place_order(customer_id, restaurant_id, items: dict[item_id, qty])` → Order
   - `assign_delivery_agent(order_id)` → DeliveryAgent (nearest available agent)
   - `update_order_status(order_id, status)` → None
   - `track_order(order_id)` → Order
   - `rate_restaurant(order_id, rating: int)` → None
   - `rate_agent(order_id, rating: int)` → None

6. **Order Status Lifecycle**
   ```
   PLACED → CONFIRMED → PREPARING → READY → PICKED_UP → DELIVERED
                                                        ↘ CANCELLED (at any point before PICKED_UP)
   ```

7. **Delivery Fee Calculation**
   - Flat fee: $2.00
   - Distance fee: $0.50 per km (Euclidean distance between restaurant and customer)
   - `DeliveryFeeCalculator.calculate(restaurant_location, customer_location)` → float

---

## Non-Functional Requirements

- In-memory data store (no database)
- Thread-safety is a bonus (not required)
- Extensible for real GPS, payment systems, notifications

---

## Constraints

- Items must belong to the restaurant's menu
- Cannot place order at a closed restaurant
- Agent assignment uses nearest-available heuristic
- Rating only allowed on DELIVERED orders

---

## Example Usage

```python
app = FoodDeliveryApp()

# Add restaurant
loc_r = Location(0, 0)
r = app.add_restaurant("Burger Palace", "American", loc_r, prep_time=20)
item = r.add_menu_item("Cheeseburger", 8.99, "non-veg")

# Add customer
loc_c = Location(3, 4)   # 5 km away
c = app.add_customer("Alice", loc_c)

# Add delivery agent
loc_a = Location(1, 1)
agent = app.add_delivery_agent("Bob", loc_a)

# Search and order
results = app.search_restaurants(cuisine_type="American")
order = app.place_order(c.customer_id, r.restaurant_id, {item.item_id: 2})
# total = 2*8.99 + 2.00 + 0.50*5 = 17.98 + 2.00 + 2.50 = 22.48

app.assign_delivery_agent(order.order_id)
app.update_order_status(order.order_id, OrderStatus.CONFIRMED)
app.update_order_status(order.order_id, OrderStatus.DELIVERED)
app.rate_restaurant(order.order_id, 5)
app.rate_agent(order.order_id, 4)
```
