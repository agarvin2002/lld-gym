"""
Movie Ticket Booking System — Starter File
===========================================
Your task: Implement a movie ticket booking system.

Read problem.md and design.md before starting.

Design decisions:
  - @dataclass for simple value objects (Movie, Theater, Seat, Screen, Show, Booking)
  - SeatStatus tracks AVAILABLE/BOOKED per seat
  - SeatCategory determines pricing (REGULAR, PREMIUM, VIP)
  - Row 0 = VIP, rows 1..rows//3 = PREMIUM, rest = REGULAR
  - Book seats atomically using Screen._lock (per-screen threading.Lock)
  - Use uuid.uuid4() for all IDs
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import threading
import uuid
from datetime import datetime


class SeatCategory(Enum):
    REGULAR = "REGULAR"
    PREMIUM = "PREMIUM"
    VIP     = "VIP"


class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED    = "BOOKED"


@dataclass
class Movie:
    movie_id: str
    title: str
    duration_minutes: int
    genre: str


@dataclass
class Theater:
    theater_id: str
    name: str
    location: str


@dataclass
class Seat:
    seat_id: str
    row: int
    col: int
    category: SeatCategory = SeatCategory.REGULAR
    status: SeatStatus = SeatStatus.AVAILABLE


@dataclass
class Screen:
    screen_id: str
    theater: Theater
    screen_number: int
    seats: list[Seat] = field(default_factory=list)
    _lock: threading.Lock = field(
        default_factory=threading.Lock, repr=False, compare=False
    )


@dataclass
class Show:
    show_id: str
    movie: Movie
    screen: Screen
    show_time: datetime
    pricing: dict[SeatCategory, float] = field(default_factory=dict)


@dataclass
class Booking:
    booking_id: str
    user_name: str
    show: Show
    seats: list[Seat]
    total_amount: float
    booked_at: datetime = field(default_factory=datetime.now)


class BookingSystem:
    def __init__(self) -> None:
        # TODO: Create _movies, _theaters, _screens, _shows, _bookings
        #       as empty dicts keyed by their respective IDs
        # TODO: Create _lock = threading.Lock()
        pass

    def add_movie(self, title: str, duration_minutes: int, genre: str) -> Movie:
        """Create and register a Movie.

        TODO:
            - Create Movie with movie_id = str(uuid.uuid4())
            - Store in _movies and return it
        """
        pass

    def add_theater(self, name: str, location: str) -> Theater:
        """Create and register a Theater.

        TODO:
            - Create Theater with theater_id = str(uuid.uuid4())
            - Store in _theaters and return it
        """
        pass

    def add_screen(
        self, theater: Theater, screen_number: int, rows: int, cols: int
    ) -> Screen:
        """Create a Screen with auto-generated seats.

        Seat category rules:
          - Row 0 → VIP
          - Rows 1 to rows//3 → PREMIUM
          - Remaining rows → REGULAR

        TODO:
            - Create seats with seat_id = f"R{r}C{c}", assign category per rules above
            - Create Screen with screen_id = str(uuid.uuid4())
            - Store in _screens and return it
        """
        pass

    def add_show(
        self,
        movie: Movie,
        screen: Screen,
        show_time: datetime,
        pricing: dict[SeatCategory, float],
    ) -> Show:
        """Create and register a Show.

        TODO:
            - Create Show with show_id = str(uuid.uuid4())
            - Store in _shows and return it
        """
        pass

    def book_seats(self, user_name: str, show: Show, seat_ids: list[str]) -> Booking:
        """Book one or more seats for a show (thread-safe per screen).

        TODO:
            - Raise ValueError if seat_ids is empty
            - Build a seat_map from show.screen.seats
            - Raise ValueError if any seat_id is not in seat_map
            - Under show.screen._lock:
                - Raise ValueError if any seat is already BOOKED
                - Mark all requested seats as BOOKED
            - Calculate total from show.pricing per seat category
            - Create Booking with booking_id = str(uuid.uuid4())
            - Store in _bookings (under self._lock) and return it
        """
        pass

    def get_available_seats(self, show: Show) -> list[Seat]:
        # TODO: Return seats with status == AVAILABLE from show.screen.seats
        pass

    def get_booking(self, booking_id: str) -> Booking:
        """Retrieve a booking by ID.

        TODO:
            - Under _lock: raise ValueError if not found
            - Return the Booking
        """
        pass
