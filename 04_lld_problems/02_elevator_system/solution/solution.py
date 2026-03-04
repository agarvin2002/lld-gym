"""
Elevator System — Reference Solution

Patterns: State (elevator states), Strategy (scheduling)
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"


class ElevatorState(Enum):
    IDLE = "IDLE"
    MOVING_UP = "MOVING_UP"
    MOVING_DOWN = "MOVING_DOWN"
    DOOR_OPEN = "DOOR_OPEN"


class Elevator:
    def __init__(self, elevator_id: int, initial_floor: int = 0) -> None:
        self.elevator_id = elevator_id
        self.current_floor = initial_floor
        self.state = ElevatorState.IDLE
        self.destinations: deque[int] = deque()

    def add_destination(self, floor: int) -> None:
        if floor not in self.destinations:
            self.destinations.append(floor)

    def step(self) -> None:
        if not self.destinations:
            self.state = ElevatorState.IDLE
            return

        next_dest = self.destinations[0]

        if self.current_floor < next_dest:
            self.current_floor += 1
            self.state = ElevatorState.MOVING_UP
        elif self.current_floor > next_dest:
            self.current_floor -= 1
            self.state = ElevatorState.MOVING_DOWN

        if self.current_floor == next_dest:
            self.destinations.popleft()
            self.state = ElevatorState.DOOR_OPEN if not self.destinations else self.state

        if not self.destinations and self.current_floor == next_dest:
            self.state = ElevatorState.IDLE

    @property
    def is_idle(self) -> bool:
        return self.state == ElevatorState.IDLE

    def __repr__(self) -> str:
        return f"Elevator(id={self.elevator_id}, floor={self.current_floor}, state={self.state.value})"


class SchedulingStrategy(ABC):
    @abstractmethod
    def select_elevator(self, elevators: list[Elevator], request_floor: int) -> Elevator | None: ...


class NearestElevatorStrategy(SchedulingStrategy):
    def select_elevator(self, elevators: list[Elevator], request_floor: int) -> Elevator | None:
        if not elevators:
            return None
        # Prefer idle elevators; among those, pick nearest
        idle = [e for e in elevators if e.is_idle]
        candidates = idle if idle else elevators
        return min(candidates, key=lambda e: abs(e.current_floor - request_floor))


class ElevatorController:
    def __init__(self, num_floors: int, num_elevators: int) -> None:
        self.num_floors = num_floors
        self._elevators = [Elevator(i) for i in range(num_elevators)]
        self._scheduler: SchedulingStrategy = NearestElevatorStrategy()

    def _validate_floor(self, floor: int) -> None:
        if floor < 0 or floor >= self.num_floors:
            raise ValueError(f"Floor {floor} out of range [0, {self.num_floors - 1}]")

    def request_elevator(self, floor: int, direction: Direction) -> bool:
        self._validate_floor(floor)
        selected = self._scheduler.select_elevator(self._elevators, floor)
        if selected is None:
            return False
        selected.add_destination(floor)
        return True

    def select_floor(self, elevator_id: int, floor: int) -> None:
        self._validate_floor(floor)
        elevator = self.get_elevator(elevator_id)
        elevator.add_destination(floor)

    def step_all(self) -> None:
        for elevator in self._elevators:
            elevator.step()

    def get_elevator(self, elevator_id: int) -> Elevator:
        for e in self._elevators:
            if e.elevator_id == elevator_id:
                return e
        raise ValueError(f"No elevator with id={elevator_id}")

    def get_all_statuses(self) -> list[dict]:
        return [
            {"id": e.elevator_id, "floor": e.current_floor, "state": e.state.value}
            for e in self._elevators
        ]
