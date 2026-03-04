"""Movie Ticket Booking System — Reference Solution."""
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
        self._movies: dict[str, Movie] = {}
        self._theaters: dict[str, Theater] = {}
        self._screens: dict[str, Screen] = {}
        self._shows: dict[str, Show] = {}
        self._bookings: dict[str, Booking] = {}
        self._lock = threading.Lock()

    def add_movie(self, title: str, duration_minutes: int, genre: str) -> Movie:
        movie = Movie(
            movie_id=str(uuid.uuid4()),
            title=title,
            duration_minutes=duration_minutes,
            genre=genre,
        )
        self._movies[movie.movie_id] = movie
        return movie

    def add_theater(self, name: str, location: str) -> Theater:
        theater = Theater(
            theater_id=str(uuid.uuid4()), name=name, location=location
        )
        self._theaters[theater.theater_id] = theater
        return theater

    def add_screen(
        self, theater: Theater, screen_number: int, rows: int, cols: int
    ) -> Screen:
        seats = []
        for r in range(rows):
            if r == 0:
                cat = SeatCategory.VIP
            elif r <= rows // 3:
                cat = SeatCategory.PREMIUM
            else:
                cat = SeatCategory.REGULAR
            for c in range(cols):
                seats.append(
                    Seat(seat_id=f"R{r}C{c}", row=r, col=c, category=cat)
                )
        screen = Screen(
            screen_id=str(uuid.uuid4()),
            theater=theater,
            screen_number=screen_number,
            seats=seats,
        )
        self._screens[screen.screen_id] = screen
        return screen

    def add_show(
        self,
        movie: Movie,
        screen: Screen,
        show_time: datetime,
        pricing: dict[SeatCategory, float],
    ) -> Show:
        show = Show(
            show_id=str(uuid.uuid4()),
            movie=movie,
            screen=screen,
            show_time=show_time,
            pricing=pricing,
        )
        self._shows[show.show_id] = show
        return show

    def book_seats(self, user_name: str, show: Show, seat_ids: list[str]) -> Booking:
        if not seat_ids:
            raise ValueError("seat_ids cannot be empty.")
        seat_map = {s.seat_id: s for s in show.screen.seats}
        for sid in seat_ids:
            if sid not in seat_map:
                raise ValueError(f"Seat {sid!r} not found on this screen.")
        with show.screen._lock:
            for sid in seat_ids:
                if seat_map[sid].status != SeatStatus.AVAILABLE:
                    raise ValueError(f"Seat {sid!r} is already booked.")
            for sid in seat_ids:
                seat_map[sid].status = SeatStatus.BOOKED
        seats = [seat_map[sid] for sid in seat_ids]
        total = sum(show.pricing.get(s.category, 0.0) for s in seats)
        booking = Booking(
            booking_id=str(uuid.uuid4()),
            user_name=user_name,
            show=show,
            seats=seats,
            total_amount=total,
        )
        with self._lock:
            self._bookings[booking.booking_id] = booking
        return booking

    def get_available_seats(self, show: Show) -> list[Seat]:
        return [s for s in show.screen.seats if s.status == SeatStatus.AVAILABLE]

    def get_booking(self, booking_id: str) -> Booking:
        with self._lock:
            if booking_id not in self._bookings:
                raise ValueError(f"Booking {booking_id!r} not found.")
            return self._bookings[booking_id]
