"""Movie Ticket Booking — Edge Cases and Concurrency."""
import sys, os
import threading
import pytest
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import BookingSystem, SeatCategory, SeatStatus

PRICING = {
    SeatCategory.REGULAR: 10.0,
    SeatCategory.PREMIUM: 15.0,
    SeatCategory.VIP: 25.0,
}


@pytest.fixture
def setup():
    system = BookingSystem()
    movie = system.add_movie("Interstellar", 169, "Sci-Fi")
    theater = system.add_theater("IMAX", "Delhi")
    screen = system.add_screen(theater, 1, rows=5, cols=5)
    show = system.add_show(movie, screen, datetime(2024, 8, 10, 21, 0), PRICING)
    return system, show


class TestValidation:
    def test_double_booking_raises(self, setup):
        system, show = setup
        system.book_seats("Alice", show, ["R2C2"])
        with pytest.raises(ValueError):
            system.book_seats("Bob", show, ["R2C2"])

    def test_invalid_seat_id_raises(self, setup):
        system, show = setup
        with pytest.raises(ValueError):
            system.book_seats("Alice", show, ["R99C99"])

    def test_empty_seat_list_raises(self, setup):
        system, show = setup
        with pytest.raises(ValueError):
            system.book_seats("Alice", show, [])

    def test_partial_invalid_raises_and_no_seats_booked(self, setup):
        """If one seat in a batch is invalid, no seats should be booked."""
        system, show = setup
        with pytest.raises(ValueError):
            system.book_seats("Alice", show, ["R2C0", "R99C99"])
        # R2C0 should still be available (all-or-nothing)
        avail_ids = {s.seat_id for s in system.get_available_seats(show)}
        assert "R2C0" in avail_ids

    def test_partial_booked_raises_and_available_unchanged(self, setup):
        """If one seat in batch is already booked, no others are booked."""
        system, show = setup
        system.book_seats("Alice", show, ["R1C0"])
        with pytest.raises(ValueError):
            # R1C0 already booked; R1C1 is fine
            system.book_seats("Bob", show, ["R1C0", "R1C1"])
        avail_ids = {s.seat_id for s in system.get_available_seats(show)}
        assert "R1C1" in avail_ids  # R1C1 should not have been booked


class TestConcurrentBooking:
    def test_single_seat_race(self, setup):
        """10 threads race to book the same seat — exactly 1 must succeed."""
        system, show = setup
        successes = []
        errors = []
        lock = threading.Lock()

        def try_book():
            try:
                booking = system.book_seats("user", show, ["R0C0"])
                with lock:
                    successes.append(booking)
            except ValueError:
                with lock:
                    errors.append(True)

        threads = [threading.Thread(target=try_book) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(successes) == 1
        assert len(errors) == 9

    def test_different_seats_no_interference(self, setup):
        """5 threads each book a different seat — all 5 must succeed."""
        system, show = setup
        seats = ["R2C0", "R2C1", "R2C2", "R2C3", "R2C4"]
        successes = []
        lock = threading.Lock()

        def try_book(seat_id):
            try:
                booking = system.book_seats("user", show, [seat_id])
                with lock:
                    successes.append(booking)
            except ValueError:
                pass

        threads = [threading.Thread(target=try_book, args=(sid,)) for sid in seats]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(successes) == 5
