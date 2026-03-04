# Explanation: Pub/Sub Messaging System

## Design Overview

The implementation follows the **Observer pattern**: a `Topic` acts as the
subject, subscriber callbacks are the observers, and `MessageBroker` is the
mediator that decouples publishers from subscribers.

---

## Key Design Decisions

### 1. Synchronous vs Asynchronous Delivery (Strategy Pattern)

The `DeliveryMode` enum selects one of two delivery strategies at broker
construction time:

| Mode | Behaviour | Trade-off |
|------|-----------|-----------|
| `SYNCHRONOUS` | Callbacks execute inline in the publisher's thread before `publish()` returns | Simple, ordered, but a slow callback blocks the publisher |
| `ASYNCHRONOUS` | `(message, callback)` pairs are enqueued; a daemon worker thread drains the queue | Publisher returns immediately; ordering is still preserved (single worker, FIFO queue) |

```python
if self._delivery_mode == DeliveryMode.SYNCHRONOUS:
    self._deliver(message, callback)
else:
    self._queue.put((message, callback))
```

### 2. Two-Level Locking: Broker Lock + Topic Lock

Rather than a single global lock, each `Topic` owns its own `threading.Lock`.
`MessageBroker` uses a `threading.RLock` (re-entrant) to protect the topic
registry (`_topics` dict).

**Why two levels?**

* Finer granularity — concurrent publishes to *different* topics do not
  contend on a single lock.
* The broker lock is released before invoking callbacks, so subscriber code
  (which may call broker methods itself) does not deadlock.

```python
# Broker lock: protect topic-registry lookup only
with self._lock:
    t = self._topics[topic]

# Then release broker lock before calling topic methods or callbacks
subscribers = t.get_subscribers()   # uses topic lock internally
for callback in subscribers.values():
    self._deliver(message, callback)  # lock free
```

### 3. Snapshot Before Delivery

`get_subscribers()` and `get_messages()` both return **copies** of the
internal collections.  This is critical:

* The broker can iterate `subscribers.values()` outside any lock, so a slow
  or blocking callback does not hold the lock and starve other threads.
* Callers that mutate the returned dict/list do not corrupt the topic's
  internal state.

```python
def get_subscribers(self) -> Dict[str, Callable[[Message], None]]:
    with self._lock:
        return dict(self._subscribers)   # <-- copy
```

### 4. Retry Pattern — At-Least-Once Delivery

`_deliver` attempts the callback up to `max_retries + 1` times total.  On
each failure it catches the exception and tries again.  After exhausting all
retries it gives up silently so that one faulty subscriber cannot crash the
broker or starve other subscribers.

```python
def _deliver(self, message, callback):
    for attempt in range(self._max_retries + 1):
        try:
            callback(message)
            return          # success
        except Exception:
            if attempt == self._max_retries:
                break       # give up — do not propagate
```

This gives **at-least-once** semantics (a successful delivery is guaranteed
to have happened at least once).  It does **not** guarantee exactly-once
delivery; a retry could call the callback multiple times if early attempts
partially succeeded (e.g. network-delivered side-effects).

### 5. Async Shutdown with a Sentinel

The `None` sentinel pattern provides a clean shutdown:

```python
def shutdown(self) -> None:
    self._queue.put(None)      # wake the worker
    self._worker.join(timeout=3)

def _async_worker(self) -> None:
    while True:
        item = self._queue.get()
        if item is None:        # sentinel
            break
        message, callback = item
        self._deliver(message, callback)
```

Advantages:
* No busy-polling; the worker blocks cheaply on `queue.Queue.get()`.
* The sentinel is guaranteed to be processed *after* all messages already in
  the queue (FIFO order), so in-flight messages are delivered before exit.
* The worker is a daemon thread, so if `shutdown()` is never called the
  process can still exit normally.

---

## Thread Safety Guarantees

| Operation | Protected by |
|-----------|-------------|
| Topic registry (`_topics`) reads/writes | `MessageBroker._lock` (RLock) |
| Subscriber dict reads/writes | `Topic._lock` |
| Message history reads/writes | `Topic._lock` |
| Async queue operations | `queue.Queue` (internally thread-safe) |
| Callback invocation | No lock held (snapshot used) |

---

## At-Least-Once vs Exactly-Once

This implementation provides **at-least-once** delivery:

* A message is retried if the callback raises, so it will be delivered at
  least once on success.
* If a callback succeeds on attempt N > 1 it means the callback was called N
  times total.

**Exactly-once** would require:

1. Idempotency tokens so the subscriber can deduplicate re-deliveries.
2. A persistent acknowledgement store (e.g. a database) to record which
   `(message_id, subscriber_id)` pairs have been successfully processed.
3. Two-phase commit or transactional outbox pattern to atomically mark a
   message as delivered.

---

## Follow-up: Dead-Letter Queue

For messages that exhaust all retries without success, the broker could move
them to a `DeadLetterQueue` topic:

```python
# In _deliver, after all retries exhausted:
if self._dlq_topic:
    dlq_message = Message(
        topic=self._dlq_topic,
        payload={"original": message, "error": last_exc},
        publisher_id="broker",
    )
    self._topics[self._dlq_topic].add_message(dlq_message)
```

---

## Complexity

| Method | Time | Space |
|--------|------|-------|
| `create_topic` | O(1) | O(1) |
| `delete_topic` | O(1) | O(1) |
| `publish` | O(S) where S = subscriber count | O(1) extra |
| `subscribe` | O(1) | O(1) |
| `unsubscribe` | O(1) | O(1) |
| `get_messages` | O(M) where M = message count | O(M) |
