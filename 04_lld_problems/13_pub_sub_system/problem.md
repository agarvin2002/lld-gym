# Problem 13: Pub/Sub Messaging System

## Problem Statement

Design a **Publisher-Subscriber (Pub/Sub) messaging system** that allows decoupled communication between publishers and subscribers via named topics. The system must support both synchronous and asynchronous delivery modes, at-least-once delivery, and be fully thread-safe.

---

## Requirements

### Core Entities

- **Topic**: A named channel through which messages flow
- **Message**: Contains `message_id`, `topic`, `payload`, `timestamp`, `publisher_id`
- **Publisher**: Can publish messages to any existing topic
- **Subscriber**: Subscribes to topics and receives messages via a callback

### MessageBroker (Central Coordinator)

```
create_topic(name: str) -> None
delete_topic(name: str) -> None
publish(publisher_id: str, topic: str, payload: Any) -> Message
subscribe(subscriber_id: str, topic: str, callback: Callable[[Message], None]) -> None
unsubscribe(subscriber_id: str, topic: str) -> None
get_messages(topic: str) -> List[Message]
```

### Delivery Modes

1. **Synchronous**: Callbacks are invoked immediately in the publisher's thread
2. **Asynchronous**: Messages are queued and delivered by a background worker thread

### Reliability

- **At-least-once delivery**: If a subscriber callback raises an exception, retry up to a configurable number of times
- Messages delivered in order per topic

### Thread Safety

- Multiple publishers and subscribers can operate concurrently

---

## Constraints

- Publishing to a non-existent topic raises `TopicNotFoundError`
- Subscribing to a non-existent topic raises `TopicNotFoundError`
- A subscriber can subscribe to multiple topics
- A topic can have multiple subscribers
- Deleting a topic stops all deliveries to that topic

---

## Examples

```python
broker = MessageBroker()
broker.create_topic("news")

def on_news(msg: Message) -> None:
    print(f"Received: {msg.payload}")

broker.subscribe("sub1", "news", on_news)
broker.publish("pub1", "news", {"headline": "LLD is fun!"})
# Prints: Received: {'headline': 'LLD is fun!'}

broker.unsubscribe("sub1", "news")
broker.publish("pub1", "news", {"headline": "No one listening now"})
# Nothing printed
```

---

## Follow-up Questions

1. How would you implement **exactly-once** delivery semantics?
2. How would you persist messages to disk for durability (like Kafka)?
3. How would you support **message filtering** (subscribers receive only matching messages)?
4. How would you implement a **dead-letter queue** for repeatedly failing messages?
5. How would you scale this to multiple broker nodes?
