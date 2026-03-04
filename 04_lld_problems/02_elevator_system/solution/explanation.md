# Explanation: Elevator System

## Patterns Used

### State Pattern (implicit)
Each elevator has an `ElevatorState` enum. Behavior in `step()` depends on the current state and next destination. A full GoF State pattern would use State objects, but for this problem the enum + conditional approach is clean and sufficient.

### Strategy Pattern
`SchedulingStrategy` is injected into `ElevatorController`. Swap `NearestElevatorStrategy` for `SCANStrategy` (elevator algorithm) without touching `ElevatorController`.

## Key Design Decisions

### Discrete Simulation via `step()`
Rather than running in real time (with `threading.sleep`), we use a discrete step model. Each `step()` call moves elevators one floor. This makes the system deterministic and easy to test.

### Destination Queue (deque)
Each elevator maintains a `deque` of floor destinations. The elevator serves them in FIFO order. A production system would sort destinations to minimize travel (SCAN/LOOK algorithm).

### `Elevator.step()` Logic
```
if no destinations → IDLE
elif below next_dest → move up
elif above next_dest → move down
if arrived → remove from queue, DOOR_OPEN or IDLE
```

## Extensibility Points

1. **Better scheduling**: implement `SCANStrategy` that sorts destinations to minimize direction changes
2. **Capacity**: add `current_load` and `max_capacity` to `Elevator`, reject requests when full
3. **Priority**: VIP floors get assigned idle elevators preferentially
4. **Zones**: partition floors among elevators (low-rise vs high-rise)

## Thread Safety
Add a `threading.Lock` in `ElevatorController` around `request_elevator` and `step_all` for multi-threaded use.
