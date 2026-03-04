# LLD Problem: Elevator System

## Problem Summary

Design an elevator control system for a building with **N floors** and **M elevators**.

## Clarifying Questions to Ask

1. How many elevators and floors? (configurable)
2. Is there a capacity limit per elevator?
3. What scheduling algorithm? (nearest car, SCAN, LOOK)
4. Can an elevator serve all floors or only certain zones?
5. Do we need door open/close simulation?
6. Real-time or discrete-step simulation?

**Assumptions for this exercise:**
- Configurable floors and elevators
- Nearest elevator scheduling (simplest)
- No zones — all elevators serve all floors
- Door state is part of elevator state
- Discrete steps (call `step()` to advance simulation)

## Functional Requirements

- **Hall button**: `request_elevator(floor: int, direction: Direction)` — pressed outside elevator
- **Cabin button**: `select_floor(elevator_id: int, floor: int)` — pressed inside elevator
- **Status**: `get_elevator_status(elevator_id: int) -> ElevatorStatus`
- **Step**: advance simulation one step (move elevators toward next destination)

## Non-Functional

- Thread-safe request queue
- Extensible scheduling algorithm

## Key Design Decisions

- **State pattern** for elevator state (IDLE, MOVING_UP, MOVING_DOWN)
- **Strategy pattern** for scheduling algorithm
- **Queue** for pending floor requests

## Entities to Identify

```
ElevatorController
Elevator
Request
Direction (Enum)
ElevatorState (Enum)
SchedulingStrategy (ABC)
NearestElevatorStrategy
```

## ASCII Class Diagram

```
ElevatorController
├── elevators: list[Elevator]
├── scheduler: SchedulingStrategy
├── pending_requests: list[Request]
└── request_elevator(floor, direction)

Elevator
├── id: int
├── current_floor: int
├── state: ElevatorState
├── destinations: deque[int]
└── step() → move one floor

Request
├── floor: int
└── direction: Direction

Direction (Enum): UP, DOWN
ElevatorState (Enum): IDLE, MOVING_UP, MOVING_DOWN, DOOR_OPEN
```
