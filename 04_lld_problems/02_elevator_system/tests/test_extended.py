"""Extended tests for Elevator System."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision
from starter import ElevatorController, ElevatorState, Direction


class TestElevatorMovement:
    def test_elevator_reaches_floor_after_steps(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=1)
        ctrl.select_floor(elevator_id=0, floor=3)
        for _ in range(5):  # allow enough steps
            ctrl.step_all()
        e = ctrl.get_elevator(0)
        assert e.current_floor == 3

    def test_elevator_idle_after_reaching_destination(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=1)
        ctrl.select_floor(elevator_id=0, floor=2)
        for _ in range(5):
            ctrl.step_all()
        e = ctrl.get_elevator(0)
        assert e.state in (ElevatorState.IDLE, ElevatorState.DOOR_OPEN)

    def test_multiple_destinations_served_in_order(self):
        ctrl = ElevatorController(num_floors=20, num_elevators=1)
        ctrl.select_floor(elevator_id=0, floor=2)
        ctrl.select_floor(elevator_id=0, floor=5)
        # Run enough steps to reach both
        for _ in range(20):
            ctrl.step_all()
        e = ctrl.get_elevator(0)
        assert e.current_floor == 5


class TestScheduling:
    def test_nearest_elevator_assigned(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=2)
        # Manually position one elevator closer to request
        ctrl.get_elevator(0).current_floor = 8
        ctrl.get_elevator(1).current_floor = 3
        ctrl.request_elevator(floor=4, direction=Direction.UP)
        # Elevator 1 (floor 3) is closer to floor 4 than elevator 0 (floor 8)
        e1 = ctrl.get_elevator(1)
        assert 4 in e1.destinations

    def test_all_statuses_returns_all_elevators(self):
        ctrl = ElevatorController(num_floors=10, num_elevators=3)
        statuses = ctrl.get_all_statuses()
        assert len(statuses) == 3
        for s in statuses:
            assert "id" in s and "floor" in s and "state" in s
