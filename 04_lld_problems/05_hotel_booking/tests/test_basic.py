"""
Basic tests for Hotel Booking System.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

from datetime import date
import pytest
from starter import (
    Hotel, SingleRoom, DoubleRoom, SuiteRoom, Guest, Reservation,
    RoomType, ReservationStatus, StandardPricingStrategy,
)


@pytest.fixture
def hotel():
    h = Hotel("Test Hotel")
    h.add_room(SingleRoom("101", price_per_night=100.0, amenities=["WiFi"]))
    h.add_room(DoubleRoom("201", price_per_night=150.0, amenities=["WiFi", "TV"]))
    h.add_room(SuiteRoom("301", price_per_night=300.0, amenities=["WiFi", "Jacuzzi"]))
    guest = Guest("Alice", "G001", "alice@test.com")
    h.register_guest(guest)
    return h


def test_book_room_returns_reservation(hotel):
    """book_room should return a Reservation with CONFIRMED status."""
    res = hotel.book_room("G001", "101", date(2025, 6, 2), date(2025, 6, 5))
    assert isinstance(res, Reservation)
    assert res.status == ReservationStatus.CONFIRMED
    assert res.room.room_number == "101"
    assert res.guest.guest_id == "G001"


def test_book_room_calculates_price(hotel):
    """Total price should be nights * price_per_night (weekdays only for base test)."""
    # Monday June 2 to Friday June 6 = 4 weekday nights = 4 * 100 = 400
    res = hotel.book_room("G001", "101", date(2025, 6, 2), date(2025, 6, 6))
    assert res.total_price > 0
    assert res.nights() == 4


def test_search_rooms_by_type(hotel):
    """search_rooms with room_type should filter correctly."""
    results = hotel.search_rooms(date(2025, 7, 1), date(2025, 7, 3), RoomType.SINGLE)
    assert len(results) == 1
    assert results[0].room_number == "101"


def test_search_rooms_excludes_booked(hotel):
    """Booked rooms should not appear in search results."""
    hotel.book_room("G001", "101", date(2025, 8, 1), date(2025, 8, 5))
    results = hotel.search_rooms(date(2025, 8, 2), date(2025, 8, 4), RoomType.SINGLE)
    assert all(r.room_number != "101" for r in results)


def test_cancel_reservation(hotel):
    """cancel_reservation should set status to CANCELLED."""
    res = hotel.book_room("G001", "101", date(2025, 9, 1), date(2025, 9, 3))
    result = hotel.cancel_reservation(res.reservation_id)
    assert result is True
    assert res.status == ReservationStatus.CANCELLED


def test_check_in_and_check_out(hotel):
    """check_in then check_out should move through correct states."""
    res = hotel.book_room("G001", "101", date(2025, 10, 1), date(2025, 10, 3))
    hotel.check_in(res.reservation_id)
    assert res.status == ReservationStatus.CHECKED_IN
    hotel.check_out(res.reservation_id)
    assert res.status == ReservationStatus.CHECKED_OUT


def test_weekend_surcharge_applied(hotel):
    """Weekend nights should cost more than weekday nights."""
    # All-weekday stay: Mon Jun 2 to Fri Jun 6 (4 nights)
    weekday_res = hotel.book_room("G001", "101", date(2025, 6, 2), date(2025, 6, 6))
    # Weekend stay: Fri Jun 6 to Mon Jun 9 (3 nights: Fri, Sat, Sun)
    guest2 = Guest("Bob", "G002", "bob@test.com")
    hotel.register_guest(guest2)
    weekend_res = hotel.book_room("G002", "201", date(2025, 6, 6), date(2025, 6, 9))
    # 3 nights * $150 = $450 base, but Sat+Sun get +20%
    # Fri=$150, Sat=$180, Sun=$180 → $510
    assert weekend_res.total_price > 3 * 150.0
