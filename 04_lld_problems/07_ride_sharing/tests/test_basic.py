"""Ride Sharing — Basic Tests."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import (
    RideSharingSystem, Driver, Rider, Trip, Location,
    DriverStatus, VehicleType, TripStatus,
    NoDriverAvailableError, DriverNotFoundError, TripNotFoundError,
)


@pytest.fixture
def system():
    return RideSharingSystem()


@pytest.fixture
def setup(system):
    driver = system.register_driver("Dave", "ABC123", VehicleType.STANDARD)
    rider = system.register_rider("Alice")
    system.update_driver_location(driver.driver_id, 0.0, 0.0)
    return system, driver, rider


class TestRegistration:
    def test_register_driver_returns_driver(self, system):
        d = system.register_driver("Dave", "ABC", VehicleType.STANDARD)
        assert isinstance(d, Driver)
        assert d.name == "Dave"

    def test_driver_starts_available(self, system):
        d = system.register_driver("Dave", "ABC", VehicleType.STANDARD)
        assert d.status == DriverStatus.AVAILABLE

    def test_register_rider(self, system):
        r = system.register_rider("Alice")
        assert isinstance(r, Rider)
        assert r.name == "Alice"

    def test_driver_has_id(self, system):
        d = system.register_driver("Dave", "ABC", VehicleType.STANDARD)
        assert d.driver_id and len(d.driver_id) > 0


class TestLocationAndStatus:
    def test_update_location(self, setup):
        system, driver, _ = setup
        system.update_driver_location(driver.driver_id, 10.0, 20.0)
        assert driver.location.lat == pytest.approx(10.0)
        assert driver.location.lon == pytest.approx(20.0)

    def test_update_location_unknown_driver(self, system):
        with pytest.raises(DriverNotFoundError):
            system.update_driver_location("bad-id", 0.0, 0.0)

    def test_set_driver_offline(self, setup):
        system, driver, _ = setup
        system.set_driver_status(driver.driver_id, DriverStatus.OFFLINE)
        assert driver.status == DriverStatus.OFFLINE

    def test_set_status_unknown_driver(self, system):
        with pytest.raises(DriverNotFoundError):
            system.set_driver_status("bad-id", DriverStatus.OFFLINE)


class TestRequestRide:
    def test_trip_returned(self, setup):
        system, _, rider = setup
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        assert isinstance(trip, Trip)

    def test_driver_set_on_trip(self, setup):
        system, driver, rider = setup
        system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        assert driver.status == DriverStatus.ON_TRIP

    def test_driver_not_in_available_after_ride(self, setup):
        system, _, rider = setup
        system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        assert system.get_available_drivers() == []

    def test_no_available_driver_raises(self, system):
        rider = system.register_rider("Alice")
        with pytest.raises(NoDriverAvailableError):
            system.request_ride(rider.rider_id, Location(0, 0), Location(1, 1))

    def test_fare_is_positive(self, setup):
        system, _, rider = setup
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        assert trip.fare > 0


class TestCompleteTrip:
    def test_complete_trip_status(self, setup):
        system, _, rider = setup
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        system.complete_trip(trip.trip_id)
        assert trip.status == TripStatus.COMPLETED

    def test_driver_available_after_completion(self, setup):
        system, driver, rider = setup
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        system.complete_trip(trip.trip_id)
        assert driver.status == DriverStatus.AVAILABLE

    def test_completed_at_is_set(self, setup):
        system, _, rider = setup
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        system.complete_trip(trip.trip_id)
        assert trip.completed_at is not None

    def test_complete_unknown_trip(self, system):
        with pytest.raises(TripNotFoundError):
            system.complete_trip("bad-trip-id")

    def test_get_trip_by_id(self, setup):
        system, _, rider = setup
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(1, 1))
        retrieved = system.get_trip(trip.trip_id)
        assert retrieved.trip_id == trip.trip_id

    def test_get_unknown_trip(self, system):
        with pytest.raises(TripNotFoundError):
            system.get_trip("nonexistent")
