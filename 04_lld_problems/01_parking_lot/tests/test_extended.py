"""
test_extended.py — Parking Lot
================================
Extended functionality tests covering spot fallback, fee calculation, and availability tracking.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
from datetime import datetime, timedelta
from starter import (
    ParkingLot,
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
def lot_no_motorcycle_spots() -> ParkingLot:
    """A lot with ONLY compact and large spots — motorcycle must fall back."""
    return create_parking_lot([{"motorcycle": 0, "compact": 2, "large": 2}])


@pytest.fixture
def lot_only_large() -> ParkingLot:
    """A lot with ONLY large spots — car must fall back to large."""
    return create_parking_lot([{"motorcycle": 0, "compact": 0, "large": 3}])


@pytest.fixture
def mixed_lot() -> ParkingLot:
    """Standard mixed lot for general tests."""
    return create_parking_lot([
        {"motorcycle": 2, "compact": 3, "large": 2},
        {"motorcycle": 1, "compact": 2, "large": 2},
    ])


# ---------------------------------------------------------------------------
# Fallback Spot Tests
# ---------------------------------------------------------------------------

class TestSpotFallback:

    def test_motorcycle_parks_in_compact_when_no_motorcycle_spots(
        self, lot_no_motorcycle_spots: ParkingLot
    ) -> None:
        """Motorcycle falls back to compact spot when motorcycle spots unavailable."""
        moto = Motorcycle("M-100")
        ticket = lot_no_motorcycle_spots.park(moto)
        assert ticket is not None
        assert isinstance(ticket.spot, CompactSpot)

    def test_motorcycle_can_also_park_in_large_spot(self, simple_lot: ParkingLot) -> None:
        """Motorcycle can use large spots as last resort."""
        # Use fixture that only has large spots
        lot = create_parking_lot([{"motorcycle": 0, "compact": 0, "large": 2}])
        moto = Motorcycle("M-101")
        ticket = lot.park(moto)
        assert ticket is not None
        assert isinstance(ticket.spot, LargeSpot)

    def test_car_can_also_park_in_large_spot(self, lot_only_large: ParkingLot) -> None:
        """Car falls back to large spot when no compact spots available."""
        car = Car("C-100")
        ticket = lot_only_large.park(car)
        assert ticket is not None
        assert isinstance(ticket.spot, LargeSpot)

    def test_truck_cannot_park_in_compact_spot(self) -> None:
        """Truck must never be assigned a compact spot, even if that is all that is available."""
        lot = create_parking_lot([{"motorcycle": 2, "compact": 5, "large": 0}])
        truck = Truck("T-100")
        ticket = lot.park(truck)
        # No large spots available → should return None
        assert ticket is None

    def test_car_cannot_park_in_motorcycle_spot(self) -> None:
        """Car must never be assigned a motorcycle spot."""
        lot = create_parking_lot([{"motorcycle": 5, "compact": 0, "large": 0}])
        car = Car("C-101")
        ticket = lot.park(car)
        assert ticket is None


@pytest.fixture
def simple_lot() -> ParkingLot:
    return create_parking_lot([{"motorcycle": 2, "compact": 2, "large": 2}])


# ---------------------------------------------------------------------------
# Fee Calculation Tests
# ---------------------------------------------------------------------------

class TestFeeCalculation:

    def test_fee_calculation_for_exactly_1_hour_car(self) -> None:
        """Car parked for exactly 1 hour → $3.00."""
        calc = HourlyFeeCalculator()
        car = Car("C-200")
        entry = datetime(2024, 1, 1, 10, 0, 0)
        exit_ = datetime(2024, 1, 1, 11, 0, 0)
        fee = calc.calculate(car, entry, exit_)
        assert fee == 3.0

    def test_fee_calculation_for_2_hours_motorcycle(self) -> None:
        """Motorcycle parked for 2 hours → $4.00."""
        calc = HourlyFeeCalculator()
        moto = Motorcycle("M-200")
        entry = datetime(2024, 1, 1, 8, 0, 0)
        exit_ = datetime(2024, 1, 1, 10, 0, 0)
        fee = calc.calculate(moto, entry, exit_)
        assert fee == 4.0

    def test_fee_calculation_ceiling_rounding(self) -> None:
        """1 hour 1 minute → billed as 2 hours for a car → $6.00."""
        calc = HourlyFeeCalculator()
        car = Car("C-201")
        entry = datetime(2024, 1, 1, 10, 0, 0)
        exit_ = datetime(2024, 1, 1, 11, 1, 0)
        fee = calc.calculate(car, entry, exit_)
        assert fee == 6.0

    def test_fee_calculation_minimum_1_hour(self) -> None:
        """Even 1 minute → billed as 1 hour minimum."""
        calc = HourlyFeeCalculator()
        car = Car("C-202")
        entry = datetime(2024, 1, 1, 10, 0, 0)
        exit_ = datetime(2024, 1, 1, 10, 1, 0)
        fee = calc.calculate(car, entry, exit_)
        assert fee == 3.0  # 1 hour minimum

    def test_fee_calculation_for_truck(self) -> None:
        """Truck parked for 3 hours → $15.00."""
        calc = HourlyFeeCalculator()
        truck = Truck("T-200")
        entry = datetime(2024, 1, 1, 9, 0, 0)
        exit_ = datetime(2024, 1, 1, 12, 0, 0)
        fee = calc.calculate(truck, entry, exit_)
        assert fee == 15.0

    def test_unpark_with_controlled_exit_time(self, mixed_lot: ParkingLot) -> None:
        """unpark() with explicit exit_time returns correct fee."""
        car = Car("C-203")
        ticket = mixed_lot.park(car)
        assert ticket is not None
        # Override entry_time for predictable calculation
        ticket.entry_time = datetime(2024, 1, 1, 10, 0, 0)
        exit_time = datetime(2024, 1, 1, 12, 0, 0)  # 2 hours
        fee = mixed_lot.unpark(ticket, exit_time=exit_time)
        assert fee == 6.0  # 2 hrs * $3/hr


# ---------------------------------------------------------------------------
# Availability Tests
# ---------------------------------------------------------------------------

class TestAvailability:

    def test_get_availability_returns_correct_counts(self, mixed_lot: ParkingLot) -> None:
        """Fresh lot returns sum of all spots by type."""
        avail = mixed_lot.get_availability()
        assert avail["motorcycle"] == 3   # 2 + 1
        assert avail["compact"] == 5     # 3 + 2
        assert avail["large"] == 4       # 2 + 2

    def test_availability_decrements_after_park(self, mixed_lot: ParkingLot) -> None:
        """Parking a car reduces compact count by 1."""
        before = mixed_lot.get_availability()["compact"]
        mixed_lot.park(Car("C-300"))
        after = mixed_lot.get_availability()["compact"]
        assert after == before - 1

    def test_availability_increments_after_unpark(self, mixed_lot: ParkingLot) -> None:
        """Unparking a car restores compact count."""
        ticket = mixed_lot.park(Car("C-301"))
        assert ticket is not None
        before_unpark = mixed_lot.get_availability()["compact"]
        mixed_lot.unpark(ticket)
        after_unpark = mixed_lot.get_availability()["compact"]
        assert after_unpark == before_unpark + 1

    def test_full_lot_returns_none_on_park(self) -> None:
        """When all spots are full, park() returns None."""
        # One compact spot only
        lot = create_parking_lot([{"motorcycle": 0, "compact": 1, "large": 0}])
        ticket1 = lot.park(Car("C-400"))
        assert ticket1 is not None
        # Lot is now full for Cars (no more compact or large spots)
        ticket2 = lot.park(Car("C-401"))
        assert ticket2 is None

    def test_availability_all_zeros_when_full(self) -> None:
        """After filling the lot, all relevant counts are zero."""
        lot = create_parking_lot([{"motorcycle": 0, "compact": 1, "large": 0}])
        lot.park(Car("C-402"))
        avail = lot.get_availability()
        assert avail["compact"] == 0
