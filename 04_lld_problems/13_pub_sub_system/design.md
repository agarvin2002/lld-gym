# Design: Pub/Sub Messaging System

## Class Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      DeliveryMode (Enum)                     │
├──────────────────────────────────────────────────────────────┤
│  SYNCHRONOUS                                                 │
│  ASYNCHRONOUS                                                │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                         Message                              │
├──────────────────────────────────────────────────────────────┤
│ + message_id: str                                            │
│ + topic: str                                                 │
│ + payload: Any                                               │
│ + timestamp: float                                           │
│ + publisher_id: str                                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                          Topic                               │
├──────────────────────────────────────────────────────────────┤
│ + name: str                                                  │
│ - _subscribers: Dict[str, Callable[[Message], None]]         │
│ - _message_history: List[Message]                            │
│ - _lock: threading.Lock                                      │
├──────────────────────────────────────────────────────────────┤
│ + add_subscriber(sub_id, callback) -> None                   │
│ + remove_subscriber(sub_id) -> None                          │
│ + get_subscribers() -> Dict[str, Callable]                   │
│ + add_message(message) -> None                               │
│ + get_messages() -> List[Message]                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                       MessageBroker                          │
├──────────────────────────────────────────────────────────────┤
│ - _topics: Dict[str, Topic]                                  │
│ - _delivery_mode: DeliveryMode                               │
│ - _max_retries: int                                          │
│ - _queue: queue.Queue[Tuple[Message, Callable]]  (async)     │
│ - _worker_thread: threading.Thread               (async)     │
│ - _lock: threading.RLock                                     │
│ - _running: bool                                             │
├──────────────────────────────────────────────────────────────┤
│ + create_topic(name) -> None                                 │
│ + delete_topic(name) -> None                                 │
│ + publish(publisher_id, topic, payload) -> Message           │
│ + subscribe(subscriber_id, topic, callback) -> None          │
│ + unsubscribe(subscriber_id, topic) -> None                  │
│ + get_messages(topic) -> List[Message]                       │
│ + shutdown() -> None                                         │
│ - _deliver(message, callback) -> None                        │
│ - _async_worker() -> None                                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    TopicNotFoundError                        │
├──────────────────────────────────────────────────────────────┤
│  (extends Exception)                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## Message Flow Diagram

### Synchronous Delivery

```
Publisher                MessageBroker               Subscribers
    |                         |                           |
    |--- publish(topic, msg) ->|                           |
    |                         |--- deliver(msg, cb1) ---> cb1()
    |                         |--- deliver(msg, cb2) ---> cb2()
    |<--- returns Message -----|                           |
```

### Asynchronous Delivery

```
Publisher                MessageBroker            Queue      Worker Thread   Subscribers
    |                         |                    |              |               |
    |--- publish(topic, msg) ->|                    |              |               |
    |                         |--- enqueue(msg,cb)->|              |               |
    |<--- returns Message -----|                    |              |               |
    |                         |                    |<-- dequeue --|               |
    |                         |                    |              |-- deliver --> cb()
```

---

## Design Patterns

### 1. Observer Pattern (Core)
- **Subject**: Topic — maintains a list of subscriber callbacks
- **Observers**: Subscriber callbacks — invoked when a message is published
- The broker acts as the mediator coordinating subjects and observers

### 2. Strategy Pattern (Delivery Mode)
- `DeliveryMode.SYNCHRONOUS` — inline delivery strategy
- `DeliveryMode.ASYNCHRONOUS` — queued delivery strategy
- Broker selects strategy at publish time based on `_delivery_mode`

### 3. Singleton Pattern (Optional for Broker)
- A single `MessageBroker` instance typically coordinates the entire application
- Can be enforced with metaclass or module-level singleton if needed

---

## At-Least-Once Delivery

```
deliver(message, callback):
  for attempt in range(max_retries + 1):
    try:
      callback(message)
      return  # success
    except Exception:
      if attempt == max_retries:
        log error and give up
      else:
        continue retry
```

---

## Thread Safety Design

- `Topic._lock` protects subscriber list modifications and message history
- `MessageBroker._lock` (RLock) protects topic dictionary
- `queue.Queue` is thread-safe by design — no extra lock needed for async queue
- Worker thread runs as daemon — exits when main thread exits
