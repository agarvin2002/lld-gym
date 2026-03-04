# Explanation: Observer Event Bus

## Core Insight
The `EventBus` knows nothing about `InventoryService` or `EmailService`. It just stores callbacks and calls them. This is pure decoupling.

## Why Callable Instead of Observer ABC?
In Python, functions are first-class objects. Using a callable interface (`Callable[[OrderEvent], None]`) is more Pythonic than requiring subclasses to implement an Observer ABC:
```python
bus.subscribe("order.placed", inventory.handle)  # clean!
# vs ABC approach: bus.subscribe("order.placed", inventory)  # then inventory.update() is called
```

## The Pattern in Real Systems
- **Django signals**: `post_save.connect(handler, sender=MyModel)`
- **PyQt/Tkinter**: button.clicked.connect(callback)
- **Node.js**: EventEmitter (same concept in JS)
- **Redis Pub/Sub**: subscribers get messages pushed to them

## Adding a New Service
To add `FraudDetectionService` that reacts to `order.placed`:
1. Write `FraudDetectionService` with a `handle()` method
2. `bus.subscribe("order.placed", fraud_service.handle)`
3. Zero changes to `EventBus`, `InventoryService`, `EmailService`

That's the power of Observer.
