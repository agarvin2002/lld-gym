"""
Parking Lot — Starter File
===========================
Your task: Implement a multi-floor parking lot system.

Read problem.md and design.md before starting.

Design decisions to keep in mind:
  - Use the Strategy pattern for fee calculation (makes it swappable)
  - Use abstract base classes for Vehicle and ParkingSpot hierarchies
  - Use a single threading.Lock to make park/unpark thread-safe
  - Best-fit spot assignment: prefer the smallest compatible spot type
  - Use uuid.uuid4() for ticket IDs
  - Fee: ceiling-rounded hours × vehicle rate (min 1 hour)
"""

from __future__ import annotations

import math
import uuid
import threading
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Type


# ---------------------------------------------------------------------------
# Hourly Rates Constant — keep as-is
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
        # TODO: Store spot_id and floor_number as attributes
        # TODO: Set is_free = True and vehicle = None
        pass

    @property
    @abstractmethod
    def spot_type(self) -> str:
        """String identifier for this spot type (e.g. 'motorcycle')."""
        ...

    def park(self, vehicle: "Vehicle") -> None:
        """Occupy this spot with the given vehicle.

        TODO:
            - Raise ValueError if the spot is already occupied
            - Set self.vehicle = vehicle and self.is_free = False
        """
        pass

    def unpark(self) -> None:
        """Free this spot.

        TODO:
            - Raise ValueError if the spot is already free
            - Set self.vehicle = None and self.is_free = True
        """
        pass

    def __repr__(self) -> str:
        status = "free" if self.is_free else f"occupied by {self.vehicle}"
        return f"{self.__class__.__name__}(id={self.spot_id}, {status})"


class MotorcycleSpot(ParkingSpot):
    # TODO: Implement the spot_type property — return "motorcycle"
    pass


class CompactSpot(ParkingSpot):
    # TODO: Implement the spot_type property — return "compact"
    pass


class LargeSpot(ParkingSpot):
    # TODO: Implement the spot_type property — return "large"
    pass


# ---------------------------------------------------------------------------
# Vehicle Hierarchy
# ---------------------------------------------------------------------------

class Vehicle(ABC):
    """Abstract base class for vehicles."""

    def __init__(self, license_plate: str) -> None:
        # TODO: Store license_plate as an attribute
        pass

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        """E.g. 'Motorcycle', 'Car', 'Truck' — must match HOURLY_RATES keys."""
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
    """Motorcycle — can use any spot type (smallest first)."""

    @property
    def vehicle_type(self) -> str:
        return "Motorcycle"

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        # TODO: Return [MotorcycleSpot, CompactSpot, LargeSpot]
        pass


class Car(Vehicle):
    """Car — can use compact or large spots."""

    @property
    def vehicle_type(self) -> str:
        return "Car"

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        # TODO: Return [CompactSpot, LargeSpot]
        pass


class Truck(Vehicle):
    """Truck — large spots only."""

    @property
    def vehicle_type(self) -> str:
        return "Truck"

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        # TODO: Return [LargeSpot]
        pass


# ---------------------------------------------------------------------------
# Parking Ticket
# ---------------------------------------------------------------------------

class ParkingTicket:
    """Issued at vehicle entry. Required for exit processing."""

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot) -> None:
        # TODO: Set ticket_id = str(uuid.uuid4())
        # TODO: Store vehicle and spot
        # TODO: Set entry_time = datetime.now()
        # TODO: Set exit_time = None and is_active = True
        pass

    def close(self, exit_time: Optional[datetime] = None) -> None:
        """Finalize the ticket at exit.

        TODO:
            - Set self.exit_time (use the argument if provided, else datetime.now())
            - Set self.is_active = False
        """
        pass

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
    Minimum: 1 hour. Use math.ceil for partial hours.
    """

    RATES: Dict[str, float] = HOURLY_RATES

    def calculate(
        self,
        vehicle: Vehicle,
        entry_time: datetime,
        exit_time: datetime,
    ) -> float:
        # TODO: Calculate duration in seconds from entry_time to exit_time
        # TODO: Convert to hours using math.ceil (partial hour = full hour)
        # TODO: Enforce minimum of 1 hour
        # TODO: Look up rate via self.RATES[vehicle.vehicle_type]
        # TODO: Return round(hours * rate, 2)
        pass


# ---------------------------------------------------------------------------
# Parking Floor
# ---------------------------------------------------------------------------

class ParkingFloor:
    """A single floor in the parking structure."""

    def __init__(self, floor_number: int, spots: List[ParkingSpot]) -> None:
        # TODO: Store floor_number and spots
        pass

    def find_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find the best (smallest compatible) free spot for the vehicle.

        TODO:
            - Iterate vehicle.compatible_spot_types() in order (smallest first)
            - For each preferred type, scan self.spots for a free spot of that type
            - Return the first match found, or None if no compatible spot is free
        """
        pass

    def get_availability(self) -> Dict[str, int]:
        """Count free spots per type on this floor.

        TODO:
            - Return a dict mapping spot_type string → count of free spots
        """
        pass

    def __repr__(self) -> str:
        return f"ParkingFloor(floor={self.floor_number}, spots={len(self.spots)})"


# ---------------------------------------------------------------------------
# Parking Lot — Main Facade
# ---------------------------------------------------------------------------

class ParkingLot:
    """Central coordinator for the parking lot system.

    Thread-safe: a single Lock guards all mutable state.
    """

    def __init__(
        self,
        floors: List[ParkingFloor],
        fee_calculator: Optional[FeeCalculator] = None,
    ) -> None:
        # TODO: Store floors
        # TODO: Set fee_calculator to the provided one or HourlyFeeCalculator()
        # TODO: Create _active_tickets: Dict[str, ParkingTicket] = {}
        # TODO: Create _parked_vehicles: Dict[str, ParkingTicket] = {}
        # TODO: Create _lock = threading.Lock()
        pass

    def park(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        """Park a vehicle, returning a ticket or None if the lot is full.

        TODO (all under self._lock):
            1. Raise ValueError if vehicle.license_plate is already in _parked_vehicles
            2. Search each floor in order for a compatible spot
            3. If no spot found, return None
            4. Call spot.park(vehicle) to occupy the spot
            5. Create a ParkingTicket(vehicle, spot)
            6. Register ticket in _active_tickets and _parked_vehicles
            7. Return the ticket
        """
        pass

    def unpark(
        self,
        ticket: ParkingTicket,
        exit_time: Optional[datetime] = None,
    ) -> float:
        """Process vehicle exit and return the fee charged.

        TODO (all under self._lock):
            1. Raise ValueError if ticket is not in _active_tickets or not is_active
            2. Call ticket.close(exit_time)
            3. Call ticket.spot.unpark()
            4. Remove ticket from _active_tickets and _parked_vehicles
            5. Calculate fee via self.fee_calculator.calculate(...)
            6. Return the fee
        """
        pass

    def get_availability(self) -> Dict[str, int]:
        """Return total free spots per type across all floors.

        TODO:
            - Sum availability from each floor's get_availability()
        """
        pass

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

    TODO:
        - For each config, create MotorcycleSpot, CompactSpot, LargeSpot instances
        - Name them with IDs like "M-{floor}-{i}", "C-{floor}-{i}", "L-{floor}-{i}"
        - Wrap spots in a ParkingFloor, collect into a list
        - Return ParkingLot(floors, fee_calculator)
    """
    pass
