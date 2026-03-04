"""Ride Sharing — Edge Cases."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop('starter', None)
from starter import (
    RideSharingSystem, Location, DriverStatus, VehicleType, TripStatus,
    NoDriverAvailableError, DriverNotFoundError, TripNotFoundError,
)


@pytest.fixture
def system():
    return RideSharingSystem()


class TestEdgeCases:
    def test_zero_distance_trip_has_base_fare(self, system):
        d = system.register_driver("D", "P1", VehicleType.STANDARD)
        system.update_driver_location(d.driver_id, 0.0, 0.0)
        rider = system.register_rider("R")
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(0, 0))
        # distance=0; fare = 2.0 + 1.0*0 = 2.0
        assert trip.fare == pytest.approx(2.0)

    def test_all_drivers_on_trip_raises(self, system):
        d = system.register_driver("D", "P1", VehicleType.STANDARD)
        system.update_driver_location(d.driver_id, 0.0, 0.0)
        r1 = system.register_rider("Alice")
        r2 = system.register_rider("Bob")
        system.request_ride(r1.rider_id, Location(0, 0), Location(1, 1))
        with pytest.raises(NoDriverAvailableError):
            system.request_ride(r2.rider_id, Location(0, 0), Location(2, 2))

    def test_trip_rider_matches(self, system):
        d = system.register_driver("D", "P1", VehicleType.STANDARD)
        system.update_driver_location(d.driver_id, 0.0, 0.0)
        rider = system.register_rider("Alice")
        trip = system.request_ride(rider.rider_id, Location(0, 0), Location(1, 1))
        assert trip.rider is rider

    def test_trip_pickup_and_dropoff_stored(self, system):
        d = system.register_driver("D", "P1", VehicleType.STANDARD)
        system.update_driver_location(d.driver_id, 0.0, 0.0)
        rider = system.register_rider("R")
        pickup = Location(1.0, 2.0)
        dropoff = Location(5.0, 6.0)
        trip = system.request_ride(rider.rider_id, pickup, dropoff)
        assert trip.pickup is pickup
        assert trip.dropoff is dropoff

    def test_location_distance(self):
        a = Location(0, 0)
        b = Location(3, 4)
        assert a.distance_to(b) == pytest.approx(5.0)

    def test_vehicle_type_stored_on_driver(self, system):
        d = system.register_driver("D", "P1", VehicleType.PREMIUM)
        assert d.vehicle.vehicle_type == VehicleType.PREMIUM

    def test_driver_reusable_after_multiple_trips(self, system):
        d = system.register_driver("D", "P1", VehicleType.STANDARD)
        system.update_driver_location(d.driver_id, 0.0, 0.0)
        for i in range(3):
            rider = system.register_rider(f"Rider{i}")
            trip = system.request_ride(rider.rider_id, Location(0, 0), Location(1, 1))
            system.complete_trip(trip.trip_id)
        assert d.status == DriverStatus.AVAILABLE
