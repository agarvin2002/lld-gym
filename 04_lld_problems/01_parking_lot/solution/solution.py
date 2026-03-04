"""
Parking Lot — Full Solution
============================
Production-quality implementation with:
  - Abstract base classes for Vehicle and ParkingSpot hierarchies
  - Strategy pattern for fee calculation
  - Best-fit spot assignment
  - Thread-safe parking with a single Lock
  - Proper datetime-based fee calculation (ceiling rounding)
  - UUID-based ticket IDs

Run the full test suite against this file by adjusting the import in tests:
    from solution.solution import ...
Or run via starter.py if you copy implementations there.
"""

from __future__ import annotations

import math
import uuid
import threading
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Type


# ---------------------------------------------------------------------------
# Hourly Rates Constant
# ---------------------------------------------------------------------------

HOURLY_RATES: Dict[str, float] = {
    "Motorcycle": 2.0,
    "Car": 3.0,
    "Truck": 5.0,
}


# ---------------------------------------------------------------------------
# Spot Hierarchy
# ---------------------------------------------------------------------------

class ParkingSpot(ABC):
    """Abstract base class for parking spots."""

    def __init__(self, spot_id: str, floor_number: int) -> None:
        self.spot_id: str = spot_id
        self.floor_number: int = floor_number
        self.is_free: bool = True
        self.vehicle: Optional["Vehicle"] = None

    @property
    @abstractmethod
    def spot_type(self) -> str:
        """String identifier for this spot type."""
        ...

    def park(self, vehicle: "Vehicle") -> None:
        """Occupy this spot with the given vehicle."""
        if not self.is_free:
            raise ValueError(f"Spot {self.spot_id} is already occupied.")
        self.vehicle = vehicle
        self.is_free = False

    def unpark(self) -> None:
        """Free this spot."""
        if self.is_free:
            raise ValueError(f"Spot {self.spot_id} is already free.")
        self.vehicle = None
        self.is_free = True

    def __repr__(self) -> str:
        status = "free" if self.is_free else f"occupied by {self.vehicle}"
        return f"{self.__class__.__name__}(id={self.spot_id}, {status})"


class MotorcycleSpot(ParkingSpot):
    @property
    def spot_type(self) -> str:
        return "motorcycle"


class CompactSpot(ParkingSpot):
    @property
    def spot_type(self) -> str:
        return "compact"


class LargeSpot(ParkingSpot):
    @property
    def spot_type(self) -> str:
        return "large"


# ---------------------------------------------------------------------------
# Vehicle Hierarchy
# ---------------------------------------------------------------------------

class Vehicle(ABC):
    """Abstract base class for vehicles."""

    def __init__(self, license_plate: str) -> None:
        self.license_plate: str = license_plate

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        ...

    @abstractmethod
    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        """Spot types this vehicle can use, smallest/preferred first."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(plate={self.license_plate})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.license_plate == other.license_plate

    def __hash__(self) -> int:
        return hash(self.license_plate)


class Motorcycle(Vehicle):
    """Motorcycle — can use any spot type."""

    @property
    def vehicle_type(self) -> str:
        return "Motorcycle"

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        # Preference: smallest first
        return [MotorcycleSpot, CompactSpot, LargeSpot]


class Car(Vehicle):
    """Car — can use compact or large spots."""

    @property
    def vehicle_type(self) -> str:
        return "Car"

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        return [CompactSpot, LargeSpot]


class Truck(Vehicle):
    """Truck — large spots only."""

    @property
    def vehicle_type(self) -> str:
        return "Truck"

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        return [LargeSpot]


# ---------------------------------------------------------------------------
# Parking Ticket
# ---------------------------------------------------------------------------

class ParkingTicket:
    """Issued at vehicle entry. Required for exit processing."""

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot) -> None:
        self.ticket_id: str = str(uuid.uuid4())
        self.vehicle: Vehicle = vehicle
        self.spot: ParkingSpot = spot
        self.entry_time: datetime = datetime.now()
        self.exit_time: Optional[datetime] = None
        self.is_active: bool = True

    def close(self, exit_time: Optional[datetime] = None) -> None:
        """Finalize the ticket at exit."""
        self.exit_time = exit_time if exit_time is not None else datetime.now()
        self.is_active = False

    def __repr__(self) -> str:
        return (
            f"ParkingTicket(id={self.ticket_id[:8]}..., "
            f"vehicle={self.vehicle}, "
            f"spot={self.spot.spot_id}, "
            f"active={self.is_active})"
        )


# ---------------------------------------------------------------------------
# Fee Calculator — Strategy Pattern
# ---------------------------------------------------------------------------

class FeeCalculator(ABC):
    """Abstract strategy for parking fee calculation."""

    @abstractmethod
    def calculate(
        self,
        vehicle: Vehicle,
        entry_time: datetime,
        exit_time: datetime,
    ) -> float:
        ...


class HourlyFeeCalculator(FeeCalculator):
    """Standard hourly rate calculator with ceiling rounding.

    Rates: Motorcycle=$2/hr, Car=$3/hr, Truck=$5/hr.
    Minimum: 1 hour.
    """

    RATES: Dict[str, float] = HOURLY_RATES

    def calculate(
        self,
        vehicle: Vehicle,
        entry_time: datetime,
        exit_time: datetime,
    ) -> float:
        duration_seconds = (exit_time - entry_time).total_seconds()
        # Ceiling division: any partial hour counts as a full hour
        hours = math.ceil(duration_seconds / 3600)
        # Minimum 1 hour
        hours = max(hours, 1)
        rate = self.RATES[vehicle.vehicle_type]
        return round(hours * rate, 2)


# ---------------------------------------------------------------------------
# Parking Floor
# ---------------------------------------------------------------------------

class ParkingFloor:
    """A single floor in the parking structure."""

    def __init__(self, floor_number: int, spots: List[ParkingSpot]) -> None:
        self.floor_number: int = floor_number
        self.spots: List[ParkingSpot] = spots

    def find_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find the best (smallest compatible) free spot for the vehicle.

        Iterates vehicle.compatible_spot_types() in preference order (smallest first)
        and returns the first free spot of each type before trying larger ones.
        This implements the "best fit" strategy.
        """
        for preferred_type in vehicle.compatible_spot_types():
            for spot in self.spots:
                if isinstance(spot, preferred_type) and spot.is_free:
                    return spot
        return None

    def get_availability(self) -> Dict[str, int]:
        """Count free spots per type on this floor."""
        counts: Dict[str, int] = {}
        for spot in self.spots:
            key = spot.spot_type
            if key not in counts:
                counts[key] = 0
            if spot.is_free:
                counts[key] += 1
        return counts

    def __repr__(self) -> str:
        return f"ParkingFloor(floor={self.floor_number}, spots={len(self.spots)})"


# ---------------------------------------------------------------------------
# Parking Lot — Main Facade
# ---------------------------------------------------------------------------

class ParkingLot:
    """Central coordinator for the parking lot system.

    Thread-safe: a single Lock guards all mutable state.

    Attributes:
        floors:          All parking floors.
        fee_calculator:  Strategy for computing fees.
        _active_tickets: Maps ticket_id → ParkingTicket for O(1) lookup.
        _parked_vehicles: Maps license_plate → ParkingTicket to prevent double-parking.
        _lock:           Threading lock for all mutations.
    """

    def __init__(
        self,
        floors: List[ParkingFloor],
        fee_calculator: Optional[FeeCalculator] = None,
    ) -> None:
        self.floors: List[ParkingFloor] = floors
        self.fee_calculator: FeeCalculator = fee_calculator or HourlyFeeCalculator()
        self._active_tickets: Dict[str, ParkingTicket] = {}
        self._parked_vehicles: Dict[str, ParkingTicket] = {}
        self._lock: threading.Lock = threading.Lock()

    def park(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        """Park a vehicle, returning a ticket or None if the lot is full.

        Raises:
            ValueError: If the vehicle's license plate is already parked.
        """
        with self._lock:
            if vehicle.license_plate in self._parked_vehicles:
                raise ValueError(
                    f"Vehicle {vehicle.license_plate} is already parked in this lot."
                )

            # Find a spot across all floors
            assigned_spot: Optional[ParkingSpot] = None
            for floor in self.floors:
                spot = floor.find_spot(vehicle)
                if spot is not None:
                    assigned_spot = spot
                    break

            if assigned_spot is None:
                return None  # Lot is full for this vehicle type

            assigned_spot.park(vehicle)
            ticket = ParkingTicket(vehicle, assigned_spot)
            self._active_tickets[ticket.ticket_id] = ticket
            self._parked_vehicles[vehicle.license_plate] = ticket
            return ticket

    def unpark(
        self,
        ticket: ParkingTicket,
        exit_time: Optional[datetime] = None,
    ) -> float:
        """Process vehicle exit and return the fee charged.

        Args:
            ticket:    The ticket issued at entry.
            exit_time: Override exit time (for testing). Defaults to datetime.now().

        Raises:
            ValueError: If the ticket is invalid or already used.
        """
        with self._lock:
            if ticket.ticket_id not in self._active_tickets or not ticket.is_active:
                raise ValueError(
                    f"Ticket {ticket.ticket_id} is invalid or has already been processed."
                )

            # Close the ticket (records exit_time and sets is_active = False)
            ticket.close(exit_time)

            # Free the spot
            ticket.spot.unpark()

            # Remove from registries
            del self._active_tickets[ticket.ticket_id]
            del self._parked_vehicles[ticket.vehicle.license_plate]

            # Calculate and return fee
            fee = self.fee_calculator.calculate(
                ticket.vehicle,
                ticket.entry_time,
                ticket.exit_time,  # type: ignore[arg-type]  # set by ticket.close()
            )
            return fee

    def get_availability(self) -> Dict[str, int]:
        """Return total free spots per type across all floors."""
        totals: Dict[str, int] = {}
        for floor in self.floors:
            floor_avail = floor.get_availability()
            for spot_type, count in floor_avail.items():
                totals[spot_type] = totals.get(spot_type, 0) + count
        return totals

    def __repr__(self) -> str:
        return f"ParkingLot(floors={len(self.floors)})"


# ---------------------------------------------------------------------------
# Factory Helper
# ---------------------------------------------------------------------------

def create_parking_lot(
    floor_configs: List[Dict[str, int]],
    fee_calculator: Optional[FeeCalculator] = None,
) -> ParkingLot:
    """Build a ParkingLot from a declarative floor configuration.

    Args:
        floor_configs: List of dicts, one per floor:
            {"motorcycle": N, "compact": N, "large": N}
        fee_calculator: Optional custom fee calculator.

    Returns:
        A fully configured ParkingLot instance.

    Example:
        lot = create_parking_lot([
            {"motorcycle": 2, "compact": 3, "large": 1},
            {"motorcycle": 1, "compact": 2, "large": 2},
        ])
    """
    floors: List[ParkingFloor] = []
    for floor_number, config in enumerate(floor_configs):
        spots: List[ParkingSpot] = []

        moto_count = config.get("motorcycle", 0)
        compact_count = config.get("compact", 0)
        large_count = config.get("large", 0)

        for i in range(moto_count):
            spots.append(MotorcycleSpot(f"M-{floor_number}-{i}", floor_number))
        for i in range(compact_count):
            spots.append(CompactSpot(f"C-{floor_number}-{i}", floor_number))
        for i in range(large_count):
            spots.append(LargeSpot(f"L-{floor_number}-{i}", floor_number))

        floors.append(ParkingFloor(floor_number, spots))

    return ParkingLot(floors, fee_calculator)


# ---------------------------------------------------------------------------
# Demo / Manual Test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from datetime import timedelta

    lot = create_parking_lot([
        {"motorcycle": 2, "compact": 3, "large": 1},
        {"motorcycle": 1, "compact": 2, "large": 2},
    ])

    print("Initial availability:", lot.get_availability())

    car = Car("CAR-ABC")
    truck = Truck("TRUCK-XYZ")
    moto = Motorcycle("MOTO-111")

    t1 = lot.park(car)
    t2 = lot.park(truck)
    t3 = lot.park(moto)

    print(f"\nParked {car} → {t1}")
    print(f"Parked {truck} → {t2}")
    print(f"Parked {moto} → {t3}")
    print("Availability after parking:", lot.get_availability())

    # Simulate 2-hour stay for car
    assert t1 is not None
    t1.entry_time = datetime.now() - timedelta(hours=2)
    fee = lot.unpark(t1, exit_time=datetime.now())
    print(f"\nUnparked {car}, fee = ${fee:.2f}")
    print("Availability after unpark:", lot.get_availability())
