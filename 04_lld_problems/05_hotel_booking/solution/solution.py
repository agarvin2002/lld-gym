"""
Hotel Booking System — Reference Solution
==========================================
Patterns: Strategy (pricing), State (reservation status), Facade (Hotel)
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional, Dict
import threading
import uuid


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
    @abstractmethod
    def calculate(self, room: "Room", check_in: date, check_out: date) -> float: ...


class StandardPricingStrategy(PricingStrategy):
    WEEKEND_SURCHARGE = 0.20

    def calculate(self, room: "Room", check_in: date, check_out: date) -> float:
        total = 0.0
        current = check_in
        while current < check_out:
            price = room.price_per_night
            if current.weekday() in (5, 6):  # Saturday=5, Sunday=6
                price *= (1 + self.WEEKEND_SURCHARGE)
            total += price
            current += timedelta(days=1)
        return round(total, 2)


# ---------------------------------------------------------------------------
# Room hierarchy
# ---------------------------------------------------------------------------

class Room(ABC):
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.room_number}, ${self.price_per_night}/night)"


class SingleRoom(Room):
    def __init__(self, room_number: str, price_per_night: float,
                 amenities: Optional[List[str]] = None) -> None:
        super().__init__(room_number, RoomType.SINGLE, price_per_night, amenities)


class DoubleRoom(Room):
    def __init__(self, room_number: str, price_per_night: float,
                 amenities: Optional[List[str]] = None) -> None:
        super().__init__(room_number, RoomType.DOUBLE, price_per_night, amenities)


class SuiteRoom(Room):
    def __init__(self, room_number: str, price_per_night: float,
                 amenities: Optional[List[str]] = None) -> None:
        super().__init__(room_number, RoomType.SUITE, price_per_night, amenities)


# ---------------------------------------------------------------------------
# Guest
# ---------------------------------------------------------------------------

class Guest:
    def __init__(self, name: str, guest_id: str, contact: str) -> None:
        self.name = name
        self.guest_id = guest_id
        self.contact = contact

    def __repr__(self) -> str:
        return f"Guest('{self.name}', id={self.guest_id})"


# ---------------------------------------------------------------------------
# Reservation
# ---------------------------------------------------------------------------

class Reservation:
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

    def overlaps(self, check_in: date, check_out: date) -> bool:
        """True if this active reservation overlaps with the given date range."""
        if self.status in (ReservationStatus.CANCELLED, ReservationStatus.CHECKED_OUT):
            return False
        return check_in < self.check_out and check_out > self.check_in

    def nights(self) -> int:
        return (self.check_out - self.check_in).days

    def __repr__(self) -> str:
        return (
            f"Reservation(id={self.reservation_id[:8]}, room={self.room.room_number}, "
            f"guest={self.guest.name}, {self.check_in}→{self.check_out}, "
            f"status={self.status.value})"
        )


# ---------------------------------------------------------------------------
# Hotel (Facade)
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
        self._rooms: Dict[str, Room] = {}
        self._guests: Dict[str, Guest] = {}
        self._reservations: Dict[str, Reservation] = {}
        self._lock = threading.Lock()

    def add_room(self, room: Room) -> None:
        self._rooms[room.room_number] = room

    def register_guest(self, guest: Guest) -> None:
        self._guests[guest.guest_id] = guest

    def get_guest(self, guest_id: str) -> Optional[Guest]:
        return self._guests.get(guest_id)

    def get_room(self, room_number: str) -> Optional[Room]:
        return self._rooms.get(room_number)

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        return self._reservations.get(reservation_id)

    def search_rooms(
        self,
        check_in: date,
        check_out: date,
        room_type: Optional[RoomType] = None,
    ) -> List[Room]:
        rooms = list(self._rooms.values())
        if room_type:
            rooms = [r for r in rooms if r.room_type == room_type]
        available = []
        for room in rooms:
            booked = any(
                res.room.room_number == room.room_number and res.overlaps(check_in, check_out)
                for res in self._reservations.values()
            )
            if not booked:
                available.append(room)
        return available

    def book_room(
        self,
        guest_id: str,
        room_number: str,
        check_in: date,
        check_out: date,
    ) -> Reservation:
        guest = self._guests.get(guest_id)
        if not guest:
            raise ValueError(f"Guest not found: {guest_id}")
        room = self._rooms.get(room_number)
        if not room:
            raise ValueError(f"Room not found: {room_number}")
        if check_in >= check_out:
            raise ValueError("check_in must be before check_out")

        with self._lock:
            for res in self._reservations.values():
                if res.room.room_number == room_number and res.overlaps(check_in, check_out):
                    raise ValueError(f"Room {room_number} is not available for {check_in} to {check_out}")
            total = self._pricing_strategy.calculate(room, check_in, check_out)
            reservation = Reservation(guest, room, check_in, check_out, total)
            self._reservations[reservation.reservation_id] = reservation
            return reservation

    def cancel_reservation(self, reservation_id: str) -> bool:
        res = self._reservations.get(reservation_id)
        if not res:
            raise ValueError(f"Reservation not found: {reservation_id}")
        if res.status not in (ReservationStatus.PENDING, ReservationStatus.CONFIRMED):
            raise ValueError(f"Cannot cancel reservation with status: {res.status.value}")
        res.status = ReservationStatus.CANCELLED
        return True

    def check_in(self, reservation_id: str) -> Reservation:
        res = self._reservations.get(reservation_id)
        if not res:
            raise ValueError(f"Reservation not found: {reservation_id}")
        if res.status != ReservationStatus.CONFIRMED:
            raise ValueError(f"Cannot check in with status: {res.status.value}")
        res.status = ReservationStatus.CHECKED_IN
        return res

    def check_out(self, reservation_id: str) -> Reservation:
        res = self._reservations.get(reservation_id)
        if not res:
            raise ValueError(f"Reservation not found: {reservation_id}")
        if res.status != ReservationStatus.CHECKED_IN:
            raise ValueError(f"Cannot check out with status: {res.status.value}")
        res.status = ReservationStatus.CHECKED_OUT
        return res

    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        self._pricing_strategy = strategy

    def __repr__(self) -> str:
        return f"Hotel('{self.name}', rooms={len(self._rooms)}, reservations={len(self._reservations)})"
