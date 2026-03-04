"""
Problem 05: Hotel Booking System
Starter file with class stubs and type hints.
Complete all TODO sections.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, timedelta
from enum import Enum, auto
from typing import List, Optional, Dict
import threading
import uuid


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class RoomType(Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    SUITE = "SUITE"


class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"


# ---------------------------------------------------------------------------
# Pricing Strategy (Strategy Pattern)
# ---------------------------------------------------------------------------
class PricingStrategy(ABC):
    """Abstract pricing strategy."""

    @abstractmethod
    def calculate(self, room: "Room", check_in: date, check_out: date) -> float:
        """Calculate total price for a stay."""
        # TODO: implement in concrete classes
        pass


class StandardPricingStrategy(PricingStrategy):
    """
    Standard pricing:
    - Base rate per night
    - +20% surcharge for Saturday and Sunday nights
    """
    WEEKEND_SURCHARGE = 0.20

    def calculate(self, room: "Room", check_in: date, check_out: date) -> float:
        # TODO:
        #   Iterate each night from check_in to check_out (exclusive)
        #   If night is Saturday (weekday=5) or Sunday (weekday=6), add 20% surcharge
        #   Return total price
        pass


# ---------------------------------------------------------------------------
# Room hierarchy
# ---------------------------------------------------------------------------
class Room(ABC):
    """Abstract base class for hotel rooms."""

    def __init__(
        self,
        room_number: str,
        room_type: RoomType,
        price_per_night: float,
        amenities: Optional[List[str]] = None,
    ) -> None:
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.amenities: List[str] = amenities or []
        # TODO: any additional fields

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.room_number}, ${self.price_per_night}/night)"


class SingleRoom(Room):
    """A single occupancy room."""

    def __init__(
        self,
        room_number: str,
        price_per_night: float,
        amenities: Optional[List[str]] = None,
    ) -> None:
        # TODO: call super().__init__ with RoomType.SINGLE
        pass


class DoubleRoom(Room):
    """A double occupancy room."""

    def __init__(
        self,
        room_number: str,
        price_per_night: float,
        amenities: Optional[List[str]] = None,
    ) -> None:
        # TODO: call super().__init__ with RoomType.DOUBLE
        pass


class SuiteRoom(Room):
    """A luxury suite room."""

    def __init__(
        self,
        room_number: str,
        price_per_night: float,
        amenities: Optional[List[str]] = None,
    ) -> None:
        # TODO: call super().__init__ with RoomType.SUITE
        pass


# ---------------------------------------------------------------------------
# Guest
# ---------------------------------------------------------------------------
class Guest:
    """Represents a hotel guest."""

    def __init__(self, name: str, guest_id: str, contact: str) -> None:
        self.name = name
        self.guest_id = guest_id
        self.contact = contact
        # TODO: any additional fields

    def __repr__(self) -> str:
        return f"Guest('{self.name}', id={self.guest_id})"


# ---------------------------------------------------------------------------
# Reservation
# ---------------------------------------------------------------------------
class Reservation:
    """Represents a hotel room reservation."""

    def __init__(
        self,
        guest: Guest,
        room: Room,
        check_in: date,
        check_out: date,
        total_price: float,
        status: ReservationStatus = ReservationStatus.CONFIRMED,
    ) -> None:
        self.reservation_id: str = str(uuid.uuid4())
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.total_price = total_price
        self.status = status
        # TODO: any additional fields

    def overlaps(self, check_in: date, check_out: date) -> bool:
        """
        Return True if this reservation's dates overlap with the given range.
        Overlap condition: new_check_in < self.check_out AND new_check_out > self.check_in
        Only active reservations (not CANCELLED/CHECKED_OUT) should be considered.
        """
        # TODO: implement overlap detection
        pass

    def nights(self) -> int:
        """Return number of nights in this reservation."""
        # TODO: return (check_out - check_in).days
        pass

    def __repr__(self) -> str:
        return (
            f"Reservation(id={self.reservation_id[:8]}, room={self.room.room_number}, "
            f"guest={self.guest.name}, {self.check_in}→{self.check_out}, "
            f"status={self.status.value})"
        )


# ---------------------------------------------------------------------------
# Hotel (Facade / main entry point)
# ---------------------------------------------------------------------------
class Hotel:
    """Main hotel booking system. Thread-safe for concurrent bookings."""

    def __init__(
        self,
        name: str,
        pricing_strategy: Optional[PricingStrategy] = None,
    ) -> None:
        self.name = name
        self._pricing_strategy: PricingStrategy = pricing_strategy or StandardPricingStrategy()
        self._rooms: Dict[str, Room] = {}             # room_number -> Room
        self._guests: Dict[str, Guest] = {}           # guest_id -> Guest
        self._reservations: Dict[str, Reservation] = {}  # reservation_id -> Reservation
        self._lock = threading.Lock()
        # TODO: any additional initialization

    def add_room(self, room: Room) -> None:
        """Add a room to the hotel."""
        # TODO: add to self._rooms
        pass

    def register_guest(self, guest: Guest) -> None:
        """Register a new guest."""
        # TODO: add to self._guests
        pass

    def get_guest(self, guest_id: str) -> Optional[Guest]:
        """Return guest by ID or None."""
        # TODO: lookup in self._guests
        pass

    def get_room(self, room_number: str) -> Optional[Room]:
        """Return room by number or None."""
        # TODO: lookup in self._rooms
        pass

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Return reservation by ID or None."""
        # TODO: lookup in self._reservations
        pass

    def search_rooms(
        self,
        check_in: date,
        check_out: date,
        room_type: Optional[RoomType] = None,
    ) -> List[Room]:
        """
        Return list of rooms available for the given date range and optional room type.
        A room is available if no active (non-cancelled, non-checked-out) reservation overlaps.
        """
        # TODO:
        #   1. Filter rooms by room_type if specified
        #   2. For each room, check if any active reservation overlaps with dates
        #   3. Return rooms with no conflicting reservations
        pass

    def book_room(
        self,
        guest_id: str,
        room_number: str,
        check_in: date,
        check_out: date,
    ) -> Reservation:
        """
        Book a room for a guest.
        Raises:
            ValueError: if guest not found, room not found, dates invalid,
                        or room not available for the dates.
        Thread-safe: uses lock to prevent double booking.
        """
        # TODO (thread-safe):
        #   1. Validate guest exists
        #   2. Validate room exists
        #   3. Validate check_in < check_out
        #   4. Acquire lock
        #   5. Check no conflicting active reservations
        #   6. Calculate total_price via pricing strategy
        #   7. Create Reservation
        #   8. Store reservation
        #   9. Return reservation
        pass

    def cancel_reservation(self, reservation_id: str) -> bool:
        """
        Cancel a reservation.
        Only PENDING or CONFIRMED reservations can be cancelled.
        Returns True if cancelled, raises ValueError for invalid state.
        """
        # TODO:
        #   1. Get reservation
        #   2. Validate status is PENDING or CONFIRMED
        #   3. Set status to CANCELLED
        #   4. Return True
        pass

    def check_in(self, reservation_id: str) -> Reservation:
        """
        Mark a reservation as CHECKED_IN.
        Only CONFIRMED reservations can be checked into.
        """
        # TODO: validate status is CONFIRMED, set to CHECKED_IN, return reservation
        pass

    def check_out(self, reservation_id: str) -> Reservation:
        """
        Mark a reservation as CHECKED_OUT.
        Only CHECKED_IN reservations can be checked out.
        """
        # TODO: validate status is CHECKED_IN, set to CHECKED_OUT, return reservation
        pass

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        """Swap the pricing strategy at runtime."""
        # TODO: update self._pricing_strategy
        pass

    def __repr__(self) -> str:
        return f"Hotel('{self.name}', rooms={len(self._rooms)}, reservations={len(self._reservations)})"
