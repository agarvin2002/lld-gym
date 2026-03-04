"""Movie Ticket Booking — Basic Tests: happy path."""
import sys, os
import pytest
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import (
    Movie, Theater, Screen, Seat, Show, Booking,
    BookingSystem, SeatCategory, SeatStatus,
)

SHOW_TIME = datetime(2024, 6, 15, 19, 30)
PRICING = {
    SeatCategory.REGULAR: 10.0,
    SeatCategory.PREMIUM: 15.0,
    SeatCategory.VIP: 25.0,
}


@pytest.fixture
def system():
    return BookingSystem()


@pytest.fixture
def setup(system):
    movie = system.add_movie("Inception", 148, "Sci-Fi")
    theater = system.add_theater("PVR Cinemas", "Mumbai")
    screen = system.add_screen(theater, screen_number=1, rows=5, cols=6)
    show = system.add_show(movie, screen, SHOW_TIME, PRICING)
    return system, movie, theater, screen, show


class TestMovieCreation:
    def test_title(self, system):
        m = system.add_movie("Matrix", 136, "Sci-Fi")
        assert m.title == "Matrix"

    def test_duration(self, system):
        m = system.add_movie("Matrix", 136, "Sci-Fi")
        assert m.duration_minutes == 136

    def test_genre(self, system):
        m = system.add_movie("Matrix", 136, "Sci-Fi")
        assert m.genre == "Sci-Fi"

    def test_id_is_set(self, system):
        m = system.add_movie("Matrix", 136, "Sci-Fi")
        assert m.movie_id and len(m.movie_id) > 0

    def test_returns_movie_instance(self, system):
        m = system.add_movie("Matrix", 136, "Sci-Fi")
        assert isinstance(m, Movie)


class TestTheaterAndScreen:
    def test_theater_name(self, system):
        t = system.add_theater("INOX", "Delhi")
        assert t.name == "INOX"

    def test_theater_location(self, system):
        t = system.add_theater("INOX", "Delhi")
        assert t.location == "Delhi"

    def test_screen_seat_count(self, system):
        t = system.add_theater("INOX", "Delhi")
        screen = system.add_screen(t, screen_number=2, rows=4, cols=5)
        assert len(screen.seats) == 20

    def test_screen_belongs_to_theater(self, system):
        t = system.add_theater("INOX", "Delhi")
        screen = system.add_screen(t, 1, 3, 4)
        assert screen.theater is t

    def test_screen_number(self, system):
        t = system.add_theater("INOX", "Delhi")
        screen = system.add_screen(t, screen_number=3, rows=3, cols=3)
        assert screen.screen_number == 3


class TestSeatGrid:
    def test_all_seats_available(self, setup):
        _, _, _, screen, _ = setup
        for seat in screen.seats:
            assert seat.status == SeatStatus.AVAILABLE

    def test_seat_ids_format(self, setup):
        _, _, _, screen, _ = setup
        ids = {s.seat_id for s in screen.seats}
        assert "R0C0" in ids
        assert "R4C5" in ids

    def test_seat_count_matches(self, setup):
        _, _, _, screen, _ = setup
        assert len(screen.seats) == 30  # 5 rows * 6 cols


class TestShowCreation:
    def test_show_movie(self, setup):
        _, movie, _, _, show = setup
        assert show.movie is movie

    def test_show_screen(self, setup):
        _, _, _, screen, show = setup
        assert show.screen is screen

    def test_show_time(self, setup):
        _, _, _, _, show = setup
        assert show.show_time == SHOW_TIME

    def test_show_pricing(self, setup):
        _, _, _, _, show = setup
        assert show.pricing[SeatCategory.REGULAR] == 10.0
        assert show.pricing[SeatCategory.VIP] == 25.0


class TestBookingHappyPath:
    def test_booking_returned(self, setup):
        system, _, _, _, show = setup
        booking = system.book_seats("Alice", show, ["R2C0", "R2C1"])
        assert isinstance(booking, Booking)

    def test_booked_seats_status(self, setup):
        system, _, _, screen, show = setup
        system.book_seats("Alice", show, ["R2C0", "R2C1"])
        seat_map = {s.seat_id: s for s in screen.seats}
        assert seat_map["R2C0"].status == SeatStatus.BOOKED
        assert seat_map["R2C1"].status == SeatStatus.BOOKED

    def test_available_count_decreases(self, setup):
        system, _, _, _, show = setup
        before = len(system.get_available_seats(show))
        system.book_seats("Alice", show, ["R2C0", "R2C1"])
        after = len(system.get_available_seats(show))
        assert after == before - 2

    def test_booking_user(self, setup):
        system, _, _, _, show = setup
        booking = system.book_seats("Alice", show, ["R3C0"])
        assert booking.user_name == "Alice"

    def test_booking_seats(self, setup):
        system, _, _, _, show = setup
        booking = system.book_seats("Alice", show, ["R2C0", "R2C1"])
        ids = {s.seat_id for s in booking.seats}
        assert ids == {"R2C0", "R2C1"}


class TestGetBooking:
    def test_retrieve_by_id(self, setup):
        system, _, _, _, show = setup
        booking = system.book_seats("Bob", show, ["R4C0"])
        retrieved = system.get_booking(booking.booking_id)
        assert retrieved.booking_id == booking.booking_id

    def test_retrieved_user(self, setup):
        system, _, _, _, show = setup
        booking = system.book_seats("Bob", show, ["R4C0"])
        assert system.get_booking(booking.booking_id).user_name == "Bob"

    def test_unknown_id_raises(self, setup):
        system, *_ = setup
        with pytest.raises(ValueError):
            system.get_booking("nonexistent-id")
