"""Extended tests for Hotel Booking System."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)

from datetime import date
import pytest
from starter import (
    Hotel, SingleRoom, DoubleRoom, SuiteRoom, Guest, Reservation,
    RoomType, ReservationStatus, StandardPricingStrategy, PricingStrategy,
)


@pytest.fixture
def hotel():
    h = Hotel("Grand Hotel")
    h.add_room(SingleRoom("101", price_per_night=100.0))
    h.add_room(SingleRoom("102", price_per_night=100.0))
    h.add_room(DoubleRoom("201", price_per_night=150.0))
    h.add_room(SuiteRoom("301", price_per_night=300.0))
    for gid, name in [("G001", "Alice"), ("G002", "Bob"), ("G003", "Carol")]:
        h.register_guest(Guest(name, gid, f"{name.lower()}@test.com"))
    return h


class TestSearchRooms:
    def test_search_all_rooms_no_filter(self, hotel):
        results = hotel.search_rooms(date(2025, 7, 1), date(2025, 7, 3))
        assert len(results) == 4

    def test_search_double_rooms(self, hotel):
        results = hotel.search_rooms(date(2025, 7, 1), date(2025, 7, 3), RoomType.DOUBLE)
        assert len(results) == 1
        assert results[0].room_number == "201"

    def test_search_suite_rooms(self, hotel):
        results = hotel.search_rooms(date(2025, 7, 1), date(2025, 7, 3), RoomType.SUITE)
        assert len(results) == 1
        assert results[0].room_number == "301"

    def test_booked_room_excluded_from_overlapping_search(self, hotel):
        hotel.book_room("G001", "101", date(2025, 8, 1), date(2025, 8, 10))
        results = hotel.search_rooms(date(2025, 8, 5), date(2025, 8, 8), RoomType.SINGLE)
        ids = {r.room_number for r in results}
        assert "101" not in ids
        assert "102" in ids

    def test_booked_room_appears_in_non_overlapping_search(self, hotel):
        hotel.book_room("G001", "101", date(2025, 8, 1), date(2025, 8, 5))
        # Search after the booking ends
        results = hotel.search_rooms(date(2025, 8, 5), date(2025, 8, 8), RoomType.SINGLE)
        ids = {r.room_number for r in results}
        assert "101" in ids

    def test_cancelled_booking_room_reappears(self, hotel):
        res = hotel.book_room("G001", "101", date(2025, 9, 1), date(2025, 9, 5))
        hotel.cancel_reservation(res.reservation_id)
        results = hotel.search_rooms(date(2025, 9, 2), date(2025, 9, 4), RoomType.SINGLE)
        ids = {r.room_number for r in results}
        assert "101" in ids


class TestMultipleBookings:
    def test_two_guests_can_book_different_rooms_same_dates(self, hotel):
        r1 = hotel.book_room("G001", "101", date(2025, 10, 1), date(2025, 10, 5))
        r2 = hotel.book_room("G002", "201", date(2025, 10, 1), date(2025, 10, 5))
        assert r1.status == ReservationStatus.CONFIRMED
        assert r2.status == ReservationStatus.CONFIRMED

    def test_same_room_sequential_bookings_allowed(self, hotel):
        r1 = hotel.book_room("G001", "101", date(2025, 11, 1), date(2025, 11, 5))
        r2 = hotel.book_room("G002", "101", date(2025, 11, 5), date(2025, 11, 10))
        assert r1.status == ReservationStatus.CONFIRMED
        assert r2.status == ReservationStatus.CONFIRMED


class TestPricing:
    def test_nights_count_correct(self, hotel):
        res = hotel.book_room("G001", "101", date(2025, 6, 1), date(2025, 6, 8))
        assert res.nights() == 7

    def test_weekday_total_price(self, hotel):
        # Mon Jun 2 to Fri Jun 6 = 4 nights all weekdays = 4 * 100
        res = hotel.book_room("G001", "101", date(2025, 6, 2), date(2025, 6, 6))
        assert res.total_price == pytest.approx(400.0)

    def test_custom_pricing_strategy(self, hotel):
        """Flat rate strategy: always charges 50.0 regardless of dates."""
        class FlatRateStrategy(PricingStrategy):
            def calculate(self, room, check_in, check_out):
                return 50.0

        hotel.set_pricing_strategy(FlatRateStrategy())
        res = hotel.book_room("G001", "101", date(2025, 6, 1), date(2025, 6, 10))
        assert res.total_price == pytest.approx(50.0)


class TestReservationLifecycle:
    def test_full_lifecycle(self, hotel):
        res = hotel.book_room("G001", "101", date(2025, 7, 1), date(2025, 7, 3))
        assert res.status == ReservationStatus.CONFIRMED
        hotel.check_in(res.reservation_id)
        assert res.status == ReservationStatus.CHECKED_IN
        hotel.check_out(res.reservation_id)
        assert res.status == ReservationStatus.CHECKED_OUT

    def test_get_reservation_by_id(self, hotel):
        res = hotel.book_room("G001", "101", date(2025, 7, 1), date(2025, 7, 3))
        fetched = hotel.get_reservation(res.reservation_id)
        assert fetched is res

    def test_get_nonexistent_reservation_returns_none(self, hotel):
        assert hotel.get_reservation("nonexistent-id") is None
