"""
test_basic.py — Parking Lot
============================
Basic functionality tests. These should pass with a minimal correct implementation.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
from starter import (
    ParkingLot,
    ParkingFloor,
    ParkingTicket,
    MotorcycleSpot,
    CompactSpot,
    LargeSpot,
    Motorcycle,
    Car,
    Truck,
    HourlyFeeCalculator,
    create_parking_lot,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def simple_lot() -> ParkingLot:
    """A small lot: 2 motorcycle spots, 2 compact spots, 2 large spots on one floor."""
    return create_parking_lot([{"motorcycle": 2, "compact": 2, "large": 2}])


@pytest.fixture
def two_floor_lot() -> ParkingLot:
    """Two-floor lot."""
    return create_parking_lot([
        {"motorcycle": 1, "compact": 2, "large": 1},
        {"motorcycle": 1, "compact": 1, "large": 2},
    ])


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestInitialization:

    def test_parking_lot_initializes_with_correct_capacity(self, simple_lot: ParkingLot) -> None:
        """Lot should report full availability on init."""
        availability = simple_lot.get_availability()
        assert availability["motorcycle"] == 2
        assert availability["compact"] == 2
        assert availability["large"] == 2

    def test_two_floor_lot_aggregates_availability(self, two_floor_lot: ParkingLot) -> None:
        """Multi-floor availability should be summed across floors."""
        availability = two_floor_lot.get_availability()
        assert availability["motorcycle"] == 2
        assert availability["compact"] == 3
        assert availability["large"] == 3

    def test_lot_has_correct_number_of_floors(self, two_floor_lot: ParkingLot) -> None:
        assert len(two_floor_lot.floors) == 2


class TestParking:

    def test_motorcycle_can_park_in_motorcycle_spot(self, simple_lot: ParkingLot) -> None:
        """Motorcycle should prefer motorcycle spots."""
        moto = Motorcycle("M-001")
        ticket = simple_lot.park(moto)
        assert ticket is not None
        assert isinstance(ticket.spot, MotorcycleSpot)

    def test_car_can_park_in_compact_spot(self, simple_lot: ParkingLot) -> None:
        """Car should prefer compact spots."""
        car = Car("C-001")
        ticket = simple_lot.park(car)
        assert ticket is not None
        assert isinstance(ticket.spot, CompactSpot)

    def test_truck_can_park_in_large_spot(self, simple_lot: ParkingLot) -> None:
        """Truck must use large spots."""
        truck = Truck("T-001")
        ticket = simple_lot.park(truck)
        assert ticket is not None
        assert isinstance(ticket.spot, LargeSpot)

    def test_park_returns_ticket(self, simple_lot: ParkingLot) -> None:
        """park() must return a ParkingTicket instance."""
        car = Car("C-002")
        ticket = simple_lot.park(car)
        assert isinstance(ticket, ParkingTicket)

    def test_ticket_has_vehicle_reference(self, simple_lot: ParkingLot) -> None:
        """Ticket must reference the correct vehicle."""
        car = Car("C-003")
        ticket = simple_lot.park(car)
        assert ticket is not None
        assert ticket.vehicle == car

    def test_ticket_has_entry_time(self, simple_lot: ParkingLot) -> None:
        """Ticket must have a non-None entry_time."""
        from datetime import datetime
        car = Car("C-004")
        ticket = simple_lot.park(car)
        assert ticket is not None
        assert ticket.entry_time is not None
        assert isinstance(ticket.entry_time, datetime)

    def test_ticket_is_active_after_park(self, simple_lot: ParkingLot) -> None:
        """Ticket is_active must be True immediately after parking."""
        car = Car("C-005")
        ticket = simple_lot.park(car)
        assert ticket is not None
        assert ticket.is_active is True


class TestSpotState:

    def test_spot_is_occupied_after_parking(self, simple_lot: ParkingLot) -> None:
        """After park(), the assigned spot must be marked as not free."""
        car = Car("C-006")
        ticket = simple_lot.park(car)
        assert ticket is not None
        assert ticket.spot.is_free is False
        assert ticket.spot.vehicle == car

    def test_unpark_clears_spot(self, simple_lot: ParkingLot) -> None:
        """After unpark(), the spot must be free again."""
        car = Car("C-007")
        ticket = simple_lot.park(car)
        assert ticket is not None
        simple_lot.unpark(ticket)
        assert ticket.spot.is_free is True
        assert ticket.spot.vehicle is None

    def test_unpark_returns_positive_fee(self, simple_lot: ParkingLot) -> None:
        """unpark() must return a positive fee (at least minimum 1 hour)."""
        car = Car("C-008")
        ticket = simple_lot.park(car)
        assert ticket is not None
        fee = simple_lot.unpark(ticket)
        assert fee > 0
