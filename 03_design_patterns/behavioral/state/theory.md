# State Pattern

## What is it?
An object changes its behaviour when its internal state changes.
Instead of a long chain of `if/elif` checks, each state is its own class (or Enum value).
Adding a new state means adding a new class — existing code stays untouched.

## Analogy
A vending machine. The same "insert coin" button does different things depending
on whether the machine is IDLE, already HAS_MONEY, or is OUT_OF_STOCK.
The button doesn't change — the state does.

## Minimal code
```python
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    ACTIVE = auto()
    DONE = auto()

class Machine:
    _next = {State.IDLE: State.ACTIVE, State.ACTIVE: State.DONE}

    def __init__(self):
        self.state = State.IDLE

    def advance(self):
        if self.state not in self._next:
            raise ValueError("No transition from current state")
        self.state = self._next[self.state]

m = Machine()
m.advance()          # IDLE → ACTIVE
print(m.state)       # State.ACTIVE
```

## Real-world uses
- Zomato order: PLACED → CONFIRMED → PREPARING → PICKED_UP → DELIVERED
- ATM: IDLE → CARD_INSERTED → PIN_VERIFIED → DISPENSING
- Hotel room booking: AVAILABLE → RESERVED → CHECKED_IN → CHECKED_OUT

## One mistake
Putting transition logic inside each state class creates circular imports and
tight coupling. Keep the transition table in the context (the main class), not
scattered across individual state objects.

## What to do next
Two implementations exist — choose based on complexity:
- **Enum + transition table** (`example1_traffic_light.py`): best for simple machines with 3–5
  states and straightforward transitions. Less code, easier to read.
- **State objects** (`example2_document_workflow.py`): best when each state has meaningfully
  different behaviour. Keeps state-specific logic out of one giant class.

Try `exercises/starter.py` — build a vending machine using the Enum approach.
