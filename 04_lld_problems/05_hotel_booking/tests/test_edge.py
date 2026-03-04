"""Edge case tests for Hotel Booking System."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)

from datetime import date
import threading
import pytest
from starter import (
    Hotel, SingleRoom, DoubleRoom, Guest, Reservation,
    RoomType, ReservationStatus,
)


@pytest.fixture
def hotel():
    h = Hotel("Edge Hotel")
    h.add_room(SingleRoom("101", price_per_night=100.0))
    h.add_room(SingleRoom("102", price_per_night=100.0))
    h.add_room(DoubleRoom("201", price_per_night=150.0))
    h.register_guest(Guest("Alice", "G001", "alice@test.com"))
    h.register_guest(Guest("Bob", "G002", "bob@test.com"))
    return h


class TestValidationErrors:
    def test_book_unknown_guest_raises(self, hotel):
        with pytest.raises(ValueError):
            hotel.book_room("GHOST", "101", date(2025, 6, 1), date(2025, 6, 3))

    def test_book_unknown_room_raises(self, hotel):
        with pytest.raises(ValueError):
            hotel.book_room("G001", "999", date(2025, 6, 1), date(2025, 6, 3))

    def test_book_invalid_dates_raises(self, hotel):
        with pytest.raises(ValueError):
            hotel.book_room("G001", "101", date(2025, 6, 5), date(2025, 6, 1))

    def test_book_same_day_check_in_out_raises(self, hotel):
        with pytest.raises(ValueError):
            hotel.book_room("G001", "101", date(2025, 6, 1), date(2025, 6, 1))

    def test_double_book_same_room_raises(self, hotel):
        hotel.book_room("G001", "101", date(2025, 7, 1), date(2025, 7, 10))
        with pytest.raises(ValueError):
            hotel.book_room("G002", "101", date(2025, 7, 5), date(2025, 7, 8))

    def test_cancel_checked_in_reservation_raises(self, hotel):
        res = hotel.book_room("G001", "101", date(2025, 8, 1), date(2025, 8, 5))
        hotel.check_in(res.reservation_id)
        with pytest.raises(ValueError):
            hotel.cancel_reservation(res.reservation_id)

    def test_check_in_cancelled_reservation_raises(self, hotel):
        res = hotel.book_room("G001", "101", date(2025, 8, 1), date(2025, 8, 5))
        hotel.cancel_reservation(res.reservation_id)
        with pytest.raises(ValueError):
            hotel.check_in(res.reservation_id)

    def test_check_out_before_check_in_raises(self, hotel):
        res = hotel.book_room("G001", "101", date(2025, 8, 1), date(2025, 8, 5))
        with pytest.raises(ValueError):
            hotel.check_out(res.reservation_id)


class TestConcurrency:
    def test_concurrent_booking_no_double_booking(self, hotel):
        """Only one of N concurrent booking attempts for the same room should succeed."""
        results = []
        errors = []
        lock = threading.Lock()

        def try_book(guest_id):
            try:
                res = hotel.book_room(
                    guest_id, "101", date(2026, 1, 1), date(2026, 1, 5)
                )
                with lock:
                    results.append(res)
            except ValueError:
                with lock:
                    errors.append(guest_id)

        # Register extra guests
        for i in range(3, 13):
            hotel.register_guest(Guest(f"Guest{i}", f"G{i:03}", f"g{i}@test.com"))

        guests = ["G001", "G002"] + [f"G{i:03}" for i in range(3, 13)]
        threads = [threading.Thread(target=try_book, args=(g,)) for g in guests]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Exactly one booking should have succeeded
        assert len(results) == 1, f"Expected 1 booking, got {len(results)}"
        assert len(errors) == len(guests) - 1
