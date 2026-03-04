"""Edge case tests for Elevator System."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision
from starter import ElevatorController, Direction, ElevatorState


class TestEdgeCases:
    def test_request_floor_zero_valid(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=1)
        assert ctrl.request_elevator(floor=0, direction=Direction.UP) is True

    def test_request_top_floor_valid(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=1)
        assert ctrl.request_elevator(floor=9, direction=Direction.DOWN) is True

    def test_negative_floor_raises_error(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=1)
        with pytest.raises(ValueError):
            ctrl.request_elevator(floor=-1, direction=Direction.UP)

    def test_invalid_elevator_id_raises_error(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=2)
        with pytest.raises(ValueError):
            ctrl.select_floor(elevator_id=99, floor=5)

    def test_step_idle_elevator_stays_idle(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=1)
        ctrl.step_all()
        e = ctrl.get_elevator(0)
        assert e.state == ElevatorState.IDLE

    def test_same_floor_request_handled(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=1)
        e = ctrl.get_elevator(0)
        e.current_floor = 5
        ctrl.request_elevator(floor=5, direction=Direction.UP)
        ctrl.step_all()
        assert e.current_floor == 5  # already there, no movement
