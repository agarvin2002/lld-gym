# Design: Food Delivery System

## ASCII Class Diagram

```
+------------------+         +------------------+
|   FoodDelivery   |         |    Restaurant    |
|      App         |-------->|------------------|
|------------------|   1..*  | restaurant_id    |
| restaurants      |         | name             |
| customers        |         | cuisine_type     |
| agents           |         | location         |
| orders           |         | menu: [MenuItem] |
|------------------|         | is_open          |
| add_restaurant() |         | prep_time        |
| add_customer()   |         | rating           |
| add_agent()      |         |------------------|
| search_rest..()  |         | add_menu_item()  |
| place_order()    |         | get_menu_item()  |
| assign_agent()   |         +------------------+
| update_status()  |                  |
| track_order()    |         +------------------+
| rate_restaurant()|         |    MenuItem      |
| rate_agent()     |         |------------------|
+------------------+         | item_id          |
        |                    | name             |
        |                    | price            |
        |                    | category         |
        |                    +------------------+
        |
        |         +------------------+         +------------------+
        |-------->|    Customer      |         |  DeliveryAgent   |
        |         |------------------|         |------------------|
        |         | customer_id      |         | agent_id         |
        |         | name             |         | name             |
        |         | location         |         | current_location |
        |         | order_history    |         | status           |
        |         +------------------+         | rating           |
        |                                      |------------------|
        |         +------------------+         | AgentStatus(Enum)|
        |-------->|     Order        |         | AVAILABLE        |
                  |------------------|         | DELIVERING       |
                  | order_id         |         | OFFLINE          |
                  | customer         |         +------------------+
                  | restaurant       |
                  | items:[OrderItem]|         +------------------+
                  | status           |         |   OrderItem      |
                  | total_amount     |         |------------------|
                  | delivery_agent   |         | menu_item        |
                  | timestamps       |         | quantity         |
                  |------------------|         | subtotal         |
                  | OrderStatus(Enum)|         +------------------+
                  | PLACED           |
                  | CONFIRMED        |         +------------------+
                  | PREPARING        |         |    Location      |
                  | READY            |         |------------------|
                  | PICKED_UP        |         | x: float         |
                  | DELIVERED        |         | y: float         |
                  | CANCELLED        |         |------------------|
                  +------------------+         | distance_to()    |
                                               +------------------+

+------------------------------+
|   DeliveryFeeCalculator      |
|------------------------------|
| FLAT_FEE = 2.00              |
| PER_KM_RATE = 0.50           |
|------------------------------|
| calculate(loc_a, loc_b)→float|
+------------------------------+
```

---

## Design Patterns Used

### 1. State Pattern — Order Lifecycle
The `Order` object holds its current `OrderStatus`. Valid transitions are enforced:
```
PLACED → CONFIRMED → PREPARING → READY → PICKED_UP → DELIVERED
                                                    ↘ CANCELLED
```
Any illegal jump (e.g., PLACED → DELIVERED) raises a `ValueError`.

### 2. Observer Pattern — Status Notifications
`FoodDeliveryApp` acts as a central coordinator. When `update_order_status()` is called:
- Agent status is updated (AVAILABLE ↔ DELIVERING)
- Customer's order history is updated
- (Extensible: push notifications, emails)

### 3. Strategy Pattern — Agent Assignment
`assign_delivery_agent()` uses a pluggable strategy:
- Default: **Nearest Available** (Euclidean distance from restaurant to agent)
- Extensible: Zone-based, load-balanced, priority-based

---

## Order Status Transition Table

| Current Status | Allowed Next          |
|----------------|-----------------------|
| PLACED         | CONFIRMED, CANCELLED  |
| CONFIRMED      | PREPARING, CANCELLED  |
| PREPARING      | READY, CANCELLED      |
| READY          | PICKED_UP             |
| PICKED_UP      | DELIVERED             |
| DELIVERED      | (terminal)            |
| CANCELLED      | (terminal)            |

---

## Delivery Fee Formula

```
distance_km = sqrt((x2-x1)^2 + (y2-y1)^2)
fee = FLAT_FEE + PER_KM_RATE * distance_km
    = $2.00 + $0.50 * distance_km
```

---

## Data Flow: place_order()

```
place_order(customer_id, restaurant_id, {item_id: qty})
    │
    ├─ Validate customer exists
    ├─ Validate restaurant exists & is_open
    ├─ For each item: validate item belongs to restaurant menu
    ├─ Create OrderItem(menu_item, quantity)
    ├─ Calculate subtotals
    ├─ Calculate delivery fee (restaurant.location → customer.location)
    ├─ total_amount = sum(subtotals) + delivery_fee
    ├─ Create Order(PLACED status)
    └─ Append to customer.order_history, store in app.orders
```

---

## Key Design Decisions

1. **IDs as UUIDs**: Each entity gets a `uuid4()` ID to avoid collisions.
2. **Flat delivery fee model**: Simple and testable; can swap `DeliveryFeeCalculator` for a real pricing engine.
3. **Location as value object**: `Location(x, y)` with `distance_to()` — immutable, hashable.
4. **Rating stored on entity**: `restaurant.rating` and `agent.rating` track cumulative average via `(old * count + new) / (count + 1)`.
5. **No external dependencies**: Pure Python, stdlib only.
