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

## Links
- [Example 1: Event system →](examples/example1_event_system.py)
- [Example 2: Stock ticker →](examples/example2_stock_ticker.py)
- [Exercise →](exercises/problem.md)
