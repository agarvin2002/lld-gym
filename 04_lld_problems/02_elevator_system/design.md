# Design: Elevator System

## Clarifying Questions
1. How many elevators? How many floors?
2. Do we model real-time movement or discrete steps?
3. What scheduling algorithm? SCAN (elevator algorithm) vs FCFS vs nearest-car?
4. Do we need door open/close simulation?
5. Is this for testing (deterministic steps) or production (real threading)?

**Decisions**: Discrete `step()` simulation for testability. SCAN-like scheduling (serve requests in current direction before reversing). No threading — single-threaded step model.

## Core Entities

| Entity | Responsibility |
|--------|---------------|
| `Elevator` | Tracks current floor, state, pending floor queue |
| `ElevatorController` | Manages N elevators, dispatches requests |
| `ElevatorState` | Enum: IDLE / MOVING_UP / MOVING_DOWN / DOOR_OPEN |
| `Direction` | Enum: UP / DOWN |

## Relationships

```
ElevatorController
  └── has── Elevator[] (1..N)
               ├── current_floor: int
               ├── state: ElevatorState
               └── _pending: set[int]   ← floors to visit
```

## ASCII Class Diagram

```
┌──────────────────────────────┐
│      ElevatorController      │
│  - _elevators: list[Elevator]│
│  - _num_floors: int          │
├──────────────────────────────┤
│ + request_elevator(floor, dir)│
│ + select_floor(id, floor)    │
│ + step_all()                 │
│ + get_elevator(id)           │
└──────────────────────────────┘
              │ has N
              ▼
┌──────────────────────────────┐
│          Elevator            │
│  - current_floor: int        │
│  - state: ElevatorState      │
│  - _pending: set[int]        │
├──────────────────────────────┤
│ + add_floor(floor: int)      │
│ + step()                     │
└──────────────────────────────┘
```

## Key Design Decisions

**Discrete simulation (`step()`)**: Each call advances the elevator one floor or changes state. This makes the system 100% deterministic and unit-testable without threads or `time.sleep`.

**Nearest-car dispatching**: `request_elevator(floor, direction)` assigns the request to the elevator closest to that floor. Simple and effective for the interview scope.

**Pending set, not queue**: Floors to visit are stored in a `set[int]` — deduplicates repeated requests. Direction is determined dynamically each step: if the elevator has floors above it, go UP; below it, go DOWN.

## Extensibility Points
- **Different scheduling algorithms**: wrap the dispatch logic in a `DispatchStrategy` ABC
- **Capacity limits**: add `max_passengers` to Elevator, track current load
- **Priority floors**: add VIP floor support by inserting at front of priority queue
- **Emergency mode**: add `EMERGENCY` state that overrides scheduling
