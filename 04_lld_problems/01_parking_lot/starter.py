"""
Parking Lot — Starter File
===========================
Fill in every TODO. Do NOT look at solution/solution.py until you have
attempted this file and run the tests.

Run tests:
    python -m pytest tests/test_basic.py -v
    python -m pytest tests/test_extended.py -v
    python -m pytest tests/test_edge.py -v
"""

from __future__ import annotations

import math
import uuid
import threading
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Type


# ---------------------------------------------------------------------------
# Enums / Constants
# ---------------------------------------------------------------------------

# Hourly rates by vehicle type (used by HourlyFeeCalculator)
HOURLY_RATES: Dict[str, float] = {
    "Motorcycle": 2.0,
    "Car": 3.0,
    "Truck": 5.0,
}


# ---------------------------------------------------------------------------
# Spot Hierarchy
# ---------------------------------------------------------------------------

class ParkingSpot(ABC):
    """Abstract base class for all parking spot types."""

    def __init__(self, spot_id: str, floor_number: int) -> None:
        self.spot_id: str = spot_id
        self.floor_number: int = floor_number
        self.is_free: bool = True
        self.vehicle: Optional[Vehicle] = None

    @property
    @abstractmethod
    def spot_type(self) -> str:
        """Return the string name of this spot type (e.g., 'motorcycle')."""
        # TODO: implement in each subclass
        ...

    def park(self, vehicle: "Vehicle") -> None:
        """Mark this spot as occupied by the given vehicle.

        Raises:
            ValueError: if the spot is already occupied.
        """
        # TODO: check is_free, set vehicle, set is_free = False
        ...

    def unpark(self) -> None:
        """Mark this spot as free.

        Raises:
            ValueError: if the spot is already free.
        """
        # TODO: check is_free, clear vehicle, set is_free = True
        ...

    def __repr__(self) -> str:
        status = "free" if self.is_free else f"occupied by {self.vehicle}"
        return f"{self.__class__.__name__}(id={self.spot_id}, {status})"


class MotorcycleSpot(ParkingSpot):
    """A spot designed for motorcycles (smallest)."""

    @property
    def spot_type(self) -> str:
        # TODO: return "motorcycle"
        ...


class CompactSpot(ParkingSpot):
    """A spot designed for cars (medium)."""

    @property
    def spot_type(self) -> str:
        # TODO: return "compact"
        ...


class LargeSpot(ParkingSpot):
    """A spot designed for trucks (largest)."""

    @property
    def spot_type(self) -> str:
        # TODO: return "large"
        ...


# ---------------------------------------------------------------------------
# Vehicle Hierarchy
# ---------------------------------------------------------------------------

class Vehicle(ABC):
    """Abstract base class for all vehicle types."""

    def __init__(self, license_plate: str) -> None:
        self.license_plate: str = license_plate

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        """Return the string name of this vehicle type (e.g., 'Car')."""
        ...

    @abstractmethod
    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        """Return spot types this vehicle can use, in preference order (smallest first).

        Example for Car: [CompactSpot, LargeSpot]
        """
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
    """Motorcycle — fits motorcycle, compact, or large spots."""

    @property
    def vehicle_type(self) -> str:
        # TODO: return "Motorcycle"
        ...

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        # TODO: return [MotorcycleSpot, CompactSpot, LargeSpot]
        ...


class Car(Vehicle):
    """Car — fits compact or large spots."""

    @property
    def vehicle_type(self) -> str:
        # TODO: return "Car"
        ...

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        # TODO: return [CompactSpot, LargeSpot]
        ...


class Truck(Vehicle):
    """Truck — fits large spots only."""

    @property
    def vehicle_type(self) -> str:
        # TODO: return "Truck"
        ...

    def compatible_spot_types(self) -> List[Type[ParkingSpot]]:
        # TODO: return [LargeSpot]
        ...


# ---------------------------------------------------------------------------
# Parking Ticket
# ---------------------------------------------------------------------------

class ParkingTicket:
    """Issued when a vehicle parks. Required to exit the lot.

    Attributes:
        ticket_id:  Unique identifier (UUID string).
        vehicle:    The parked vehicle.
        spot:       The assigned parking spot.
        entry_time: When the vehicle entered (datetime.now() at park() call).
        exit_time:  Set when the vehicle exits; None while parked.
        is_active:  True while the vehicle is still parked.
    """

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot) -> None:
        # TODO:
        # - Generate self.ticket_id using uuid.uuid4()
        # - Store vehicle and spot
        # - Set entry_time to datetime.now()
        # - Set exit_time to None
        # - Set is_active to True
        ...

    def close(self, exit_time: Optional[datetime] = None) -> None:
        """Mark ticket as closed (vehicle has exited).

        Args:
            exit_time: Override exit time (useful in tests). Defaults to datetime.now().
        """
        # TODO: set exit_time (use datetime.now() if not provided), set is_active = False
        ...

    def __repr__(self) -> str:
        return (
            f"ParkingTicket(id={self.ticket_id}, "
            f"vehicle={self.vehicle}, "
            f"spot={self.spot.spot_id}, "
            f"active={self.is_active})"
        )


# ---------------------------------------------------------------------------
# Fee Calculator (Strategy Pattern)
# ---------------------------------------------------------------------------

class FeeCalculator(ABC):
    """Strategy interface for fee calculation."""

    @abstractmethod
    def calculate(
        self,
        vehicle: Vehicle,
        entry_time: datetime,
        exit_time: datetime,
    ) -> float:
        """Calculate the parking fee.

        Args:
            vehicle:    The vehicle being charged.
            entry_time: When the vehicle entered.
            exit_time:  When the vehicle exited.

        Returns:
            Fee in dollars as a float, rounded to 2 decimal places.
        """
        ...


class HourlyFeeCalculator(FeeCalculator):
    """Charges by the hour (ceiling), with per-vehicle-type rates.

    Rates: Motorcycle=$2/hr, Car=$3/hr, Truck=$5/hr.
    Minimum charge: 1 hour.
    """

    RATES: Dict[str, float] = HOURLY_RATES

    def calculate(
        self,
        vehicle: Vehicle,
        entry_time: datetime,
        exit_time: datetime,
    ) -> float:
        # TODO:
        # 1. Compute duration in seconds: (exit_time - entry_time).total_seconds()
        # 2. Convert to hours, ceiling: math.ceil(duration_seconds / 3600)
        # 3. Enforce minimum of 1 hour
        # 4. Look up rate by vehicle.vehicle_type in self.RATES
        # 5. Return round(hours * rate, 2)
        ...


# ---------------------------------------------------------------------------
# Parking Floor
# ---------------------------------------------------------------------------

class ParkingFloor:
    """A single floor in the parking structure.

    Holds a list of spots and provides spot-finding logic.
    """

    def __init__(self, floor_number: int, spots: List[ParkingSpot]) -> None:
        self.floor_number: int = floor_number
        self.spots: List[ParkingSpot] = spots

    def find_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find the best available spot for this vehicle (smallest compatible, first available).

        Args:
            vehicle: The vehicle looking for a spot.

        Returns:
            A free ParkingSpot, or None if no compatible spot is available.
        """
        # TODO:
        # Iterate vehicle.compatible_spot_types() (preference order: smallest first)
        # For each preferred type, scan self.spots for a free spot of that type
        # Return the first match found, or None if none found
        ...

    def get_availability(self) -> Dict[str, int]:
        """Return count of free spots per type on this floor.

        Returns:
            e.g., {"motorcycle": 2, "compact": 3, "large": 1}
        """
        # TODO: count free spots grouped by spot_type
        ...

    def __repr__(self) -> str:
        return f"ParkingFloor(floor={self.floor_number}, spots={len(self.spots)})"


# ---------------------------------------------------------------------------
# Parking Lot (Main Facade)
# ---------------------------------------------------------------------------

class ParkingLot:
    """The top-level parking lot system.

    Coordinates multiple floors, issues tickets, processes exits, and
    reports availability. Thread-safe.

    Usage:
        lot = ParkingLot(floors=[...], fee_calculator=HourlyFeeCalculator())
        ticket = lot.park(Car("ABC-123"))
        fee = lot.unpark(ticket)
        availability = lot.get_availability()
    """

    def __init__(
        self,
        floors: List[ParkingFloor],
        fee_calculator: Optional[FeeCalculator] = None,
    ) -> None:
        self.floors: List[ParkingFloor] = floors
        self.fee_calculator: FeeCalculator = fee_calculator or HourlyFeeCalculator()
        # Active tickets: maps ticket_id -> ParkingTicket
        self._active_tickets: Dict[str, ParkingTicket] = {}
        # Tracks which vehicles are currently parked (by license plate)
        self._parked_vehicles: Dict[str, ParkingTicket] = {}
        self._lock: threading.Lock = threading.Lock()

    def park(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        """Park a vehicle in the best available spot.

        Args:
            vehicle: The vehicle to park.

        Returns:
            A ParkingTicket if a spot was found, or None if the lot is full.

        Raises:
            ValueError: If the vehicle is already parked in this lot.
        """
        # TODO:
        # 1. Acquire self._lock
        # 2. Check if vehicle.license_plate is in self._parked_vehicles → raise ValueError
        # 3. Iterate self.floors to find a spot (call floor.find_spot(vehicle))
        # 4. If no spot found anywhere, return None
        # 5. Call spot.park(vehicle)
        # 6. Create ParkingTicket(vehicle, spot)
        # 7. Store ticket in self._active_tickets and self._parked_vehicles
        # 8. Return the ticket
        # (Remember to release the lock — use a try/finally or 'with' statement)
        ...

    def unpark(self, ticket: ParkingTicket, exit_time: Optional[datetime] = None) -> float:
        """Process vehicle exit.

        Args:
            ticket:    The ticket issued at entry.
            exit_time: Override exit time for testing. Defaults to datetime.now().

        Returns:
            The fee charged, in dollars.

        Raises:
            ValueError: If the ticket is invalid, already used, or not from this lot.
        """
        # TODO:
        # 1. Acquire self._lock
        # 2. Validate: ticket.ticket_id in self._active_tickets AND ticket.is_active
        #    → raise ValueError if not
        # 3. Close the ticket (ticket.close(exit_time))
        # 4. Call ticket.spot.unpark()
        # 5. Remove from self._active_tickets and self._parked_vehicles
        # 6. Calculate fee using self.fee_calculator.calculate(vehicle, entry, exit)
        # 7. Return fee
        ...

    def get_availability(self) -> Dict[str, int]:
        """Return total free spots per type across all floors.

        Returns:
            e.g., {"motorcycle": 5, "compact": 8, "large": 3}
        """
        # TODO:
        # Aggregate each floor's get_availability() dict
        # Sum values for matching keys across all floors
        ...

    def __repr__(self) -> str:
        return f"ParkingLot(floors={len(self.floors)})"


# ---------------------------------------------------------------------------
# Factory Helper (optional convenience)
# ---------------------------------------------------------------------------

def create_parking_lot(
    floor_configs: List[Dict[str, int]],
    fee_calculator: Optional[FeeCalculator] = None,
) -> ParkingLot:
    """Convenience factory to build a ParkingLot from a config list.

    Args:
        floor_configs: List of dicts, one per floor. Each dict:
            {"motorcycle": N, "compact": N, "large": N}
        fee_calculator: Optional custom fee calculator.

    Returns:
        A fully configured ParkingLot.

    Example:
        lot = create_parking_lot([
            {"motorcycle": 2, "compact": 3, "large": 1},
            {"motorcycle": 1, "compact": 2, "large": 2},
        ])
    """
    # TODO:
    # For each floor_config (with index = floor_number):
    #   Create spots:
    #     - "motorcycle" count of MotorcycleSpot with IDs like "M-{floor}-{i}"
    #     - "compact" count of CompactSpot with IDs like "C-{floor}-{i}"
    #     - "large" count of LargeSpot with IDs like "L-{floor}-{i}"
    #   Create ParkingFloor(floor_number, spots)
    # Return ParkingLot(floors, fee_calculator)
    ...
