# Exercise: E-Commerce Event Bus

## What You'll Build

A simple event bus for an e-commerce system where order lifecycle events are published and various services react independently.

## Events (as strings or Enum)
- `"order.placed"` — triggered when order is created
- `"order.shipped"` — triggered when order is dispatched
- `"order.delivered"` — triggered when order arrives

## Event Data
```python
@dataclass
class OrderEvent:
    event_type: str
    order_id: str
    customer_email: str
    items: list[str]
    total: float
```

## Components

### `EventBus`
- `subscribe(event_type: str, handler: Callable) -> None`
- `unsubscribe(event_type: str, handler: Callable) -> None`
- `publish(event: OrderEvent) -> None` — calls all handlers for `event.event_type`

### Handlers (simple classes with `handle(event: OrderEvent) -> None`)

| Handler | Reacts to |
|---------|----------|
| `InventoryService` | `order.placed` — reserves stock |
| `ShippingService` | `order.placed` — schedules pickup |
| `EmailService` | all three events — sends confirmation, shipping, delivery emails |
| `LoyaltyService` | `order.delivered` — awards points |

## Constraints
- Handlers must be decoupled from each other
- `EventBus` must not know about `InventoryService`, `ShippingService`, etc.
- Adding a new handler should require zero changes to `EventBus`

## Hints
1. Store handlers as `dict[str, list[Callable]]`
2. Use `defaultdict(list)` to avoid key existence checks
3. The event bus is essentially the same as `EventEmitter` in the example — apply to this domain

## What You'll Practice
- Observer pattern with event-type filtering
- Decoupled event handlers
- Callable-based observers (Pythonic)
