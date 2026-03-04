"""
test_edge.py — Parking Lot
============================
Edge case tests: error conditions, concurrency, and boundary behavior.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
import threading
from datetime import datetime
from starter import (
    ParkingLot,
    ParkingTicket,
    Motorcycle,
    Car,
    Truck,
    HourlyFeeCalculator,
    create_parking_lot,
    CompactSpot,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def lot() -> ParkingLot:
    return create_parking_lot([{"motorcycle": 5, "compact": 5, "large": 5}])


@pytest.fixture
def small_lot() -> ParkingLot:
    return create_parking_lot([{"motorcycle": 2, "compact": 2, "large": 2}])


# ---------------------------------------------------------------------------
# Error Condition Tests
# ---------------------------------------------------------------------------

class TestErrorConditions:

    def test_park_same_vehicle_twice_raises_error(self, lot: ParkingLot) -> None:
        """Attempting to park a vehicle that is already parked raises ValueError."""
        car = Car("DUPE-001")
        ticket = lot.park(car)
        assert ticket is not None
        with pytest.raises(ValueError, match="already parked"):
            lot.park(car)

    def test_unpark_invalid_ticket_raises_error(self, lot: ParkingLot) -> None:
        """Presenting a ticket that was never issued raises ValueError."""
        car = Car("CAR-FAKE")
        # Create a ticket manually without going through lot.park()
        fake_spot = CompactSpot("FAKE-SPOT", 0)
        fake_ticket = ParkingTicket(car, fake_spot)
        with pytest.raises(ValueError):
            lot.unpark(fake_ticket)

    def test_unpark_already_used_ticket_raises_error(self, lot: ParkingLot) -> None:
        """Using the same ticket twice raises ValueError on the second attempt."""
        car = Car("CAR-USED")
        ticket = lot.park(car)
        assert ticket is not None
        lot.unpark(ticket)
        with pytest.raises(ValueError):
            lot.unpark(ticket)

    def test_ticket_is_inactive_after_unpark(self, lot: ParkingLot) -> None:
        """Ticket is_active must be False after unpark."""
        car = Car("CAR-DONE")
        ticket = lot.park(car)
        assert ticket is not None
        lot.unpark(ticket)
        assert ticket.is_active is False

    def test_ticket_has_exit_time_after_unpark(self, lot: ParkingLot) -> None:
        """Ticket exit_time must be set after unpark."""
        car = Car("CAR-EXIT")
        ticket = lot.park(car)
        assert ticket is not None
        lot.unpark(ticket)
        assert ticket.exit_time is not None


# ---------------------------------------------------------------------------
# Availability Consistency Tests
# ---------------------------------------------------------------------------

class TestAvailabilityConsistency:

    def test_availability_decrements_on_park_increments_on_unpark(
        self, small_lot: ParkingLot
    ) -> None:
        """Availability accurately tracks park/unpark cycles."""
        initial = small_lot.get_availability()["compact"]

        ticket1 = small_lot.park(Car("C-CYCLE-1"))
        assert small_lot.get_availability()["compact"] == initial - 1

        ticket2 = small_lot.park(Car("C-CYCLE-2"))
        assert small_lot.get_availability()["compact"] == initial - 2

        small_lot.unpark(ticket1)
        assert small_lot.get_availability()["compact"] == initial - 1

        small_lot.unpark(ticket2)
        assert small_lot.get_availability()["compact"] == initial

    def test_motorcycle_fallback_reduces_correct_spot_type(
        self, small_lot: ParkingLot
    ) -> None:
        """When motorcycle uses a compact spot (fallback), compact count decreases."""
        # Fill all motorcycle spots
        lot = create_parking_lot([{"motorcycle": 1, "compact": 2, "large": 1}])
        lot.park(Motorcycle("M-FILL"))  # takes motorcycle spot

        compact_before = lot.get_availability()["compact"]
        moto_before = lot.get_availability()["motorcycle"]

        # Next motorcycle must use compact spot
        ticket = lot.park(Motorcycle("M-FALLBACK"))
        assert ticket is not None

        # Compact count should decrease, motorcycle count stays at 0
        assert lot.get_availability()["compact"] == compact_before - 1
        assert lot.get_availability()["motorcycle"] == moto_before  # already 0


# ---------------------------------------------------------------------------
# Concurrency Test
# ---------------------------------------------------------------------------

class TestConcurrency:

    def test_concurrent_parking_no_double_booking(self, lot: ParkingLot) -> None:
        """Multiple threads parking simultaneously must not double-book any spot.

        Strategy: 10 threads each try to park 1 car simultaneously.
        All spot IDs collected from successful tickets must be unique.
        """
        num_threads = 10
        tickets = []
        errors = []
        lock = threading.Lock()

        def park_car(plate: str) -> None:
            try:
                ticket = lot.park(Car(plate))
                if ticket is not None:
                    with lock:
                        tickets.append(ticket)
            except Exception as e:
                with lock:
                    errors.append(str(e))

        threads = [
            threading.Thread(target=park_car, args=(f"CONC-{i:03d}",))
            for i in range(num_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No unexpected errors
        assert len(errors) == 0, f"Unexpected errors: {errors}"

        # All assigned spot IDs must be unique (no double-booking)
        spot_ids = [t.spot.spot_id for t in tickets]
        assert len(spot_ids) == len(set(spot_ids)), (
            f"Double-booking detected! Spot IDs: {spot_ids}"
        )

        # Count should match parked vehicles
        assert len(tickets) == num_threads

    def test_concurrent_park_and_unpark(self) -> None:
        """Concurrent park and unpark operations maintain consistency."""
        lot = create_parking_lot([{"motorcycle": 0, "compact": 20, "large": 0}])
        tickets = []
        errors = []
        lock = threading.Lock()

        # Pre-park 10 cars
        for i in range(10):
            t = lot.park(Car(f"PRE-{i:03d}"))
            assert t is not None
            tickets.append(t)

        def unpark_car(ticket: ParkingTicket) -> None:
            try:
                lot.unpark(ticket)
            except Exception as e:
                with lock:
                    errors.append(str(e))

        def park_new_car(plate: str) -> None:
            try:
                ticket = lot.park(Car(plate))
                if ticket is not None:
                    with lock:
                        tickets.append(ticket)
            except Exception as e:
                with lock:
                    errors.append(str(e))

        # Simultaneously unpark 10 and park 10 new ones
        threads = []
        for t in tickets[:10]:
            threads.append(threading.Thread(target=unpark_car, args=(t,)))
        for i in range(10):
            threads.append(threading.Thread(target=park_new_car, args=(f"NEW-{i:03d}",)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Concurrent errors: {errors}"

        # Total spots: 20. After unparking 10 and parking 10, should still have 10 occupied.
        avail = lot.get_availability()
        assert avail["compact"] == 10
