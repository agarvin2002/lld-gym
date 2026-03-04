# State Pattern

## What is it?
Allow an object to alter its behaviour when its internal state changes. The object will appear to change its class.

## Real-world analogy
A traffic light. The same physical box behaves differently depending on state: RED stops traffic, GREEN allows it, YELLOW warns. The same `change()` trigger transitions between states differently depending on current state.

## Why does it matter?
Without State, every method becomes a chain of `if self.state == X: ... elif self.state == Y: ...`. As states grow, the class becomes unmaintainable. With State, each state is its own class; adding a new state doesn't touch existing ones.

## Python-specific notes
- Use `Enum` for state when transitions are simple and you don't need per-state behaviour encapsulation
- Use full State objects (each state as a class) when each state has meaningfully different behaviour
- For LLD interviews, the `Enum` + guard method approach is often cleaner and faster to write

## When to use
- An object's behaviour depends on its state and changes at runtime
- You have many conditional statements based on a state variable
- States have distinct behaviours that go beyond simple flag checks

## When to avoid
- Only 2-3 states with trivial transitions — a simple flag is cleaner
- States share almost all behaviour — subclassing may be simpler

## Quick example (Enum approach — preferred for interviews)
```python
from enum import Enum, auto

class TrafficLightState(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()

class TrafficLight:
    _transitions = {
        TrafficLightState.RED: TrafficLightState.GREEN,
        TrafficLightState.GREEN: TrafficLightState.YELLOW,
        TrafficLightState.YELLOW: TrafficLightState.RED,
    }

    def __init__(self) -> None:
        self.state = TrafficLightState.RED

    def change(self) -> None:
        self.state = self._transitions[self.state]

    def action(self) -> str:
        return {
            TrafficLightState.RED: "Stop",
            TrafficLightState.GREEN: "Go",
            TrafficLightState.YELLOW: "Caution",
        }[self.state]

light = TrafficLight()
print(light.action())   # Stop
light.change()
print(light.action())   # Go
light.change()
print(light.action())   # Caution
```

## Quick example (State objects — for complex per-state logic)
```python
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle(self, context: "Context") -> None: ...

class IdleState(State):
    def handle(self, context):
        print("Idle: starting work")
        context.state = WorkingState()

class WorkingState(State):
    def handle(self, context):
        print("Working: done, going idle")
        context.state = IdleState()

class Context:
    def __init__(self) -> None:
        self.state: State = IdleState()

    def request(self) -> None:
        self.state.handle(self)
```

## Common mistakes
- Hardcoding transitions inside state classes (creates circular dependencies) — keep transition logic in the context
- Forgetting to validate transitions (allowing illegal state jumps)
- Using State when a simple `Enum` flag would do

## Links
- Exercise: `exercises/starter.py` — implement a vending machine with states: IDLE, HAS_MONEY, DISPENSING, OUT_OF_STOCK
