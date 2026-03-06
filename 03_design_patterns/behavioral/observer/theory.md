# Observer Pattern

## What Is It?
Define a **one-to-many** dependency: when one object (Subject) changes state, all its dependents (Observers) are notified automatically.

## Real-World Analogy
A YouTube channel (Subject) has subscribers (Observers). When a new video is uploaded, all subscribers are notified. Subscribers can unsubscribe at any time. The channel doesn't know how many subscribers it has or what they do with the notification.

## When to Use
- Event systems and callbacks
- MVC: Model notifies Views when data changes
- Pub/Sub messaging
- Real-time feeds (stock tickers, notifications)
- Decoupling components that need to react to state changes

## Python Implementation

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: any) -> None: ...

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: str, data=None) -> None:
        for observer in self._observers:
            observer.update(event, data)
```

## Push vs Pull Model
- **Push**: Subject sends data to observers (`update(data)`)
- **Pull**: Subject notifies observers, they pull what they need (`update(subject)`)

Push is simpler. Pull is more flexible (observers choose what to read).

## Key Components
| Component | Role |
|-----------|------|
| Subject (Observable) | Maintains list of observers, notifies on change |
| Observer | Interface with `update()` |
| ConcreteObserver | Specific reaction to events |

## Common Mistakes
- **Memory leaks**: not unsubscribing (observer holds reference to subject)
- **Synchronous notifications**: slow observers block the subject
- **Order dependency**: observers shouldn't depend on notification order
- **Cascade notifications**: observer → changes subject → notifies again → infinite loop

---

## LLD Problems That Use This Pattern

| Problem | Subject | Observers |
|---------|---------|-----------|
| [13 Pub/Sub System](../../../04_lld_problems/13_pub_sub_system/) | `Topic` | Subscriber callbacks — Observer taken to its logical conclusion |
| [04 Library Management](../../../04_lld_problems/04_library_management/) | `ReservationQueue` | Waiting members notified when a book becomes available |
| [08 Food Delivery](../../../04_lld_problems/08_food_delivery/) | `Order` | Customer and delivery agent react to status changes |
| [07 Ride Sharing](../../../04_lld_problems/07_ride_sharing/) | `Trip` | Driver and rider react to trip lifecycle events |

**Best example:** Pub/Sub System — the entire system is one big Observer mechanism. Study it after the exercise.