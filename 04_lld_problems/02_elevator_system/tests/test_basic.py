"""Basic tests for Elevator System."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision
from starter import Elevator, ElevatorController, ElevatorState, Direction


class TestElevator:
    def test_elevator_initializes_at_given_floor(self):
        e = Elevator(elevator_id=0, initial_floor=0)
        assert e.current_floor == 0

    def test_elevator_starts_idle(self):
        e = Elevator(elevator_id=0)
        assert e.state == ElevatorState.IDLE

    def test_elevator_moves_up_toward_destination(self):
        e = Elevator(elevator_id=0, initial_floor=0)
        e.add_destination(3)
        e.step()
        assert e.current_floor == 1
        assert e.state == ElevatorState.MOVING_UP

    def test_elevator_moves_down_toward_destination(self):
        e = Elevator(elevator_id=0, initial_floor=5)
        e.add_destination(2)
        e.step()
        assert e.current_floor == 4
        assert e.state == ElevatorState.MOVING_DOWN

    def test_elevator_reaches_destination(self):
        e = Elevator(elevator_id=0, initial_floor=0)
        e.add_destination(1)
        e.step()  # floor 0 → 1, arrives
        assert e.current_floor == 1

    def test_elevator_no_duplicate_destinations(self):
        e = Elevator(elevator_id=0)
        e.add_destination(5)
        e.add_destination(5)
        assert list(e.destinations).count(5) == 1


class TestElevatorController:
    def test_controller_creates_correct_number_of_elevators(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=3)
        assert len(ctrl.get_all_statuses()) == 3

    def test_request_elevator_assigns_elevator(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=2)
        result = ctrl.request_elevator(floor=5, direction=Direction.UP)
        assert result is True

    def test_request_elevator_invalid_floor_raises_error(self):
        import pytest
        ctrl = ElevatorController(num_floors=10, num_elevators=2)
        with pytest.raises(ValueError):
            ctrl.request_elevator(floor=15, direction=Direction.UP)

    def test_select_floor_adds_destination(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=2)
        ctrl.select_floor(elevator_id=0, floor=7)
        elevator = ctrl.get_elevator(0)
        assert 7 in elevator.destinations
