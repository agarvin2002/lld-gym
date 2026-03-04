"""Ride Sharing — Extended Tests: matching, pricing, multiple trips."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import RideSharingSystem, Location, DriverStatus, VehicleType, TripStatus


@pytest.fixture
def system():
    return RideSharingSystem()


class TestNearestDriverMatching:
    def test_nearest_driver_selected(self, system):
        d1 = system.register_driver("Far", "P1", VehicleType.STANDARD)
        d2 = system.register_driver("Near", "P2", VehicleType.STANDARD)
        system.update_driver_location(d1.driver_id, 100.0, 100.0)
        system.update_driver_location(d2.driver_id, 1.0, 1.0)
        rider = system.register_rider("Alice")
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(5, 5))
        assert trip.driver is d2  # Near driver was chosen

    def test_offline_driver_excluded(self, system):
        d1 = system.register_driver("Dave", "P1", VehicleType.STANDARD)
        d2 = system.register_driver("Eve", "P2", VehicleType.STANDARD)
        system.update_driver_location(d1.driver_id, 0.0, 0.0)
        system.update_driver_location(d2.driver_id, 1.0, 1.0)
        system.set_driver_status(d1.driver_id, DriverStatus.OFFLINE)
        rider = system.register_rider("Alice")
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(5, 5))
        assert trip.driver is d2  # offline d1 excluded


class TestFarePricing:
    def test_standard_fare(self, system):
        driver = system.register_driver("D", "P1", VehicleType.STANDARD)
        system.update_driver_location(driver.driver_id, 0.0, 0.0)
        rider = system.register_rider("R")
        # distance = sqrt(3²+4²) = 5.0; fare = 2.0 + 1.0*5.0 = 7.0
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        assert trip.fare == pytest.approx(7.0)

    def test_premium_fare(self, system):
        driver = system.register_driver("D", "P1", VehicleType.PREMIUM)
        system.update_driver_location(driver.driver_id, 0.0, 0.0)
        rider = system.register_rider("R")
        # distance = 5.0; fare = 5.0 + 2.0*5.0 = 15.0
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        assert trip.fare == pytest.approx(15.0)

    def test_xl_fare(self, system):
        driver = system.register_driver("D", "P1", VehicleType.XL)
        system.update_driver_location(driver.driver_id, 0.0, 0.0)
        rider = system.register_rider("R")
        # distance = 5.0; fare = 3.0 + 1.5*5.0 = 10.5
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(3, 4))
        assert trip.fare == pytest.approx(10.5)


class TestMultipleTrips:
    def test_driver_available_for_second_trip_after_first_complete(self, system):
        driver = system.register_driver("D", "P1", VehicleType.STANDARD)
        system.update_driver_location(driver.driver_id, 0.0, 0.0)
        r1 = system.register_rider("Alice")
        r2 = system.register_rider("Bob")

        trip1 = system.request_ride(r1.rider_id, Location(0, 0), Location(1, 1))
        system.complete_trip(trip1.trip_id)

        trip2 = system.request_ride(r2.rider_id, Location(0, 0), Location(2, 2))
        assert trip2.driver is driver

    def test_two_drivers_two_simultaneous_trips(self, system):
        d1 = system.register_driver("D1", "P1", VehicleType.STANDARD)
        d2 = system.register_driver("D2", "P2", VehicleType.STANDARD)
        system.update_driver_location(d1.driver_id, 0.0, 0.0)
        system.update_driver_location(d2.driver_id, 10.0, 10.0)
        r1 = system.register_rider("Alice")
        r2 = system.register_rider("Bob")

        t1 = system.request_ride(r1.rider_id, Location(0, 0), Location(5, 5))
        t2 = system.request_ride(r2.rider_id, Location(10, 10), Location(15, 15))
        assert t1.driver is not t2.driver
        assert system.get_available_drivers() == []

    def test_get_available_drivers_multiple(self, system):
        d1 = system.register_driver("D1", "P1", VehicleType.STANDARD)
        d2 = system.register_driver("D2", "P2", VehicleType.STANDARD)
        available = system.get_available_drivers()
        assert len(available) == 2

    def test_offline_driver_not_in_available_list(self, system):
        d1 = system.register_driver("D1", "P1", VehicleType.STANDARD)
        system.set_driver_status(d1.driver_id, DriverStatus.OFFLINE)
        assert system.get_available_drivers() == []
