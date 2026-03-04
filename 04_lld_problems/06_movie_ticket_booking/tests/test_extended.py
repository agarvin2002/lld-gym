"""Movie Ticket Booking — Extended Tests: pricing, multiple bookings, full show."""
import sys, os
import pytest
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import BookingSystem, SeatCategory, SeatStatus

SHOW_TIME = datetime(2024, 7, 1, 20, 0)
PRICING = {
    SeatCategory.REGULAR: 10.0,
    SeatCategory.PREMIUM: 18.0,
    SeatCategory.VIP: 30.0,
}


@pytest.fixture
def setup():
    system = BookingSystem()
    movie = system.add_movie("Dune", 155, "Sci-Fi")
    theater = system.add_theater("Cineplex", "Bangalore")
    screen = system.add_screen(theater, screen_number=1, rows=6, cols=5)
    show = system.add_show(movie, screen, SHOW_TIME, PRICING)
    return system, movie, theater, screen, show


class TestAvailableSeats:
    def test_all_available_initially(self, setup):
        system, _, _, screen, show = setup
        avail = system.get_available_seats(show)
        assert len(avail) == len(screen.seats)

    def test_available_excludes_booked(self, setup):
        system, _, _, _, show = setup
        system.book_seats("Alice", show, ["R2C0"])
        avail = system.get_available_seats(show)
        avail_ids = {s.seat_id for s in avail}
        assert "R2C0" not in avail_ids

    def test_available_includes_unbooked(self, setup):
        system, _, _, _, show = setup
        system.book_seats("Alice", show, ["R2C0"])
        avail = system.get_available_seats(show)
        avail_ids = {s.seat_id for s in avail}
        assert "R2C1" in avail_ids


class TestPricing:
    def test_total_amount_regular(self, setup):
        system, _, _, _, show = setup
        # Find a REGULAR seat (rows 3-5 in a 6-row screen)
        regular_ids = [
            s.seat_id for s in show.screen.seats
            if s.category == SeatCategory.REGULAR
        ]
        assert len(regular_ids) >= 2
        booking = system.book_seats("Alice", show, regular_ids[:2])
        assert booking.total_amount == pytest.approx(20.0)

    def test_total_amount_vip(self, setup):
        system, _, _, _, show = setup
        vip_ids = [
            s.seat_id for s in show.screen.seats
            if s.category == SeatCategory.VIP
        ]
        booking = system.book_seats("Alice", show, vip_ids[:1])
        assert booking.total_amount == pytest.approx(30.0)

    def test_mixed_category_total(self, setup):
        system, _, _, _, show = setup
        vip = next(s for s in show.screen.seats if s.category == SeatCategory.VIP)
        reg = next(s for s in show.screen.seats if s.category == SeatCategory.REGULAR)
        booking = system.book_seats("Alice", show, [vip.seat_id, reg.seat_id])
        assert booking.total_amount == pytest.approx(40.0)  # 30 + 10


class TestMultipleBookings:
    def test_two_users_different_seats(self, setup):
        system, _, _, _, show = setup
        b1 = system.book_seats("Alice", show, ["R2C0"])
        b2 = system.book_seats("Bob", show, ["R2C1"])
        assert b1.booking_id != b2.booking_id
        assert {s.seat_id for s in b1.seats} == {"R2C0"}
        assert {s.seat_id for s in b2.seats} == {"R2C1"}

    def test_bookings_are_stored_independently(self, setup):
        system, _, _, _, show = setup
        b1 = system.book_seats("Alice", show, ["R3C0"])
        b2 = system.book_seats("Bob", show, ["R3C1"])
        assert system.get_booking(b1.booking_id).user_name == "Alice"
        assert system.get_booking(b2.booking_id).user_name == "Bob"


class TestSeatCategories:
    def test_vip_seats_exist(self, setup):
        _, _, _, screen, _ = setup
        vip = [s for s in screen.seats if s.category == SeatCategory.VIP]
        assert len(vip) > 0

    def test_regular_seats_exist(self, setup):
        _, _, _, screen, _ = setup
        reg = [s for s in screen.seats if s.category == SeatCategory.REGULAR]
        assert len(reg) > 0

    def test_row0_is_vip(self, setup):
        _, _, _, screen, _ = setup
        row0 = [s for s in screen.seats if s.row == 0]
        assert all(s.category == SeatCategory.VIP for s in row0)


class TestFullShow:
    def test_book_all_seats(self, setup):
        system, _, _, screen, show = setup
        all_ids = [s.seat_id for s in screen.seats]
        # Book in batches of 5
        for i in range(0, len(all_ids), 5):
            batch = all_ids[i:i+5]
            system.book_seats("user", show, batch)
        assert system.get_available_seats(show) == []
