"""
Elevator System — Starter

Fill in the TODOs. Test with:
  pytest tests/test_basic.py -v
  pytest tests/test_extended.py -v
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
    """
    Represents a single elevator car.

    Maintains current floor, state, and queue of destinations.
    Call step() to move one floor toward the next destination.
    """

    def __init__(self, elevator_id: int, initial_floor: int = 0) -> None:
        # TODO: store elevator_id, current_floor
        # TODO: initialize state = ElevatorState.IDLE
        # TODO: initialize destinations as deque()
        pass

    def add_destination(self, floor: int) -> None:
        """Add floor to destination queue (ignore duplicates)."""
        # TODO: add floor to destinations if not already there
        pass

    def step(self) -> None:
        """Move one floor toward next destination. Update state."""
        # TODO: if no destinations, state = IDLE, return
        # TODO: next_dest = destinations[0]
        # TODO: if current_floor < next_dest: move up (current_floor += 1, state = MOVING_UP)
        # TODO: elif current_floor > next_dest: move down
        # TODO: if current_floor == next_dest: popleft, state = DOOR_OPEN (or IDLE if empty)
        pass

    @property
    def is_idle(self) -> bool:
        return self.state == ElevatorState.IDLE

    def __repr__(self) -> str:
        return f"Elevator(id={self.elevator_id}, floor={self.current_floor}, state={self.state.value})"


class SchedulingStrategy(ABC):
    @abstractmethod
    def select_elevator(
        self,
        elevators: list[Elevator],
        request_floor: int,
    ) -> Elevator | None:
        """Select best elevator to serve the request."""
        ...


class NearestElevatorStrategy(SchedulingStrategy):
    """Assigns the elevator with the smallest distance to the request floor."""

    def select_elevator(
        self,
        elevators: list[Elevator],
        request_floor: int,
    ) -> Elevator | None:
        # TODO: find elevator with minimum abs(current_floor - request_floor)
        # TODO: prefer idle elevators; if tie, pick first
        pass


class ElevatorController:
    """
    Central controller: manages all elevators, dispatches requests.
    """

    def __init__(self, num_floors: int, num_elevators: int) -> None:
        # TODO: store num_floors
        # TODO: create num_elevators Elevator objects (starting at floor 0)
        # TODO: create NearestElevatorStrategy as default scheduler
        pass

    def request_elevator(self, floor: int, direction: Direction) -> bool:
        """
        Hall button pressed. Assign nearest elevator to serve request.

        Returns:
            True if elevator was assigned, False if no elevators available

        Raises:
            ValueError: if floor is out of range
        """
        # TODO: validate floor range
        # TODO: use scheduler to select elevator
        # TODO: add floor to selected elevator's destinations
        # TODO: return True if assigned, False otherwise
        pass

    def select_floor(self, elevator_id: int, floor: int) -> None:
        """
        Cabin button pressed. Add floor to specific elevator's destinations.

        Raises:
            ValueError: if elevator_id invalid or floor out of range
        """
        # TODO: validate elevator_id and floor
        # TODO: add floor to that elevator's destinations
        pass

    def step_all(self) -> None:
        """Advance all elevators one step."""
        # TODO: call step() on all elevators
        pass

    def get_elevator(self, elevator_id: int) -> Elevator:
        # TODO: return elevator by id, raise ValueError if not found
        pass

    def get_all_statuses(self) -> list[dict]:
        """Return status snapshot of all elevators."""
        # TODO: return list of dicts with id, floor, state for each elevator
        pass
