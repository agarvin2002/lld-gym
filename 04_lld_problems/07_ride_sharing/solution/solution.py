"""Ride Sharing System — Reference Solution."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
import math
import uuid
from datetime import datetime


class NoDriverAvailableError(Exception):
    pass


class DriverNotFoundError(Exception):
    pass


class TripNotFoundError(Exception):
    pass


class DriverStatus(Enum):
    AVAILABLE = auto()
    ON_TRIP   = auto()
    OFFLINE   = auto()


class VehicleType(Enum):
    STANDARD = auto()
    PREMIUM  = auto()
    XL       = auto()


class TripStatus(Enum):
    REQUESTED   = auto()
    IN_PROGRESS = auto()
    COMPLETED   = auto()


@dataclass
class Location:
    lat: float
    lon: float

    def distance_to(self, other: Location) -> float:
        return math.sqrt((self.lat - other.lat) ** 2 + (self.lon - other.lon) ** 2)


@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType


@dataclass
class Driver:
    driver_id: str
    name: str
    vehicle: Vehicle
    location: Location = field(default_factory=lambda: Location(0.0, 0.0))
    status: DriverStatus = DriverStatus.AVAILABLE


@dataclass
class Rider:
    rider_id: str
    name: str


@dataclass
class Trip:
    trip_id: str
    driver: Driver
    rider: Rider
    pickup: Location
    dropoff: Location
    status: TripStatus = TripStatus.REQUESTED
    fare: float = 0.0
    requested_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None


class RideSharingSystem:
    PRICING = {
        VehicleType.STANDARD: (2.0, 1.0),
        VehicleType.PREMIUM:  (5.0, 2.0),
        VehicleType.XL:       (3.0, 1.5),
    }

    def __init__(self) -> None:
        self._drivers: dict[str, Driver] = {}
        self._riders: dict[str, Rider] = {}
        self._trips: dict[str, Trip] = {}

    def register_driver(
        self, name: str, license_plate: str, vehicle_type: VehicleType
    ) -> Driver:
        vehicle = Vehicle(license_plate=license_plate, vehicle_type=vehicle_type)
        driver = Driver(driver_id=str(uuid.uuid4()), name=name, vehicle=vehicle)
        self._drivers[driver.driver_id] = driver
        return driver

    def register_rider(self, name: str) -> Rider:
        rider = Rider(rider_id=str(uuid.uuid4()), name=name)
        self._riders[rider.rider_id] = rider
        return rider

    def update_driver_location(self, driver_id: str, lat: float, lon: float) -> None:
        if driver_id not in self._drivers:
            raise DriverNotFoundError(f"Driver {driver_id!r} not found.")
        self._drivers[driver_id].location = Location(lat, lon)

    def set_driver_status(self, driver_id: str, status: DriverStatus) -> None:
        if driver_id not in self._drivers:
            raise DriverNotFoundError(f"Driver {driver_id!r} not found.")
        self._drivers[driver_id].status = status

    def request_ride(
        self, rider_id: str, pickup: Location, dropoff: Location
    ) -> Trip:
        available = [d for d in self._drivers.values() if d.status == DriverStatus.AVAILABLE]
        if not available:
            raise NoDriverAvailableError("No drivers available.")
        nearest = min(available, key=lambda d: d.location.distance_to(pickup))

        distance = pickup.distance_to(dropoff)
        base, rate = self.PRICING[nearest.vehicle.vehicle_type]
        fare = round(base + rate * distance, 2)

        trip = Trip(
            trip_id=str(uuid.uuid4()),
            driver=nearest,
            rider=self._riders[rider_id],
            pickup=pickup,
            dropoff=dropoff,
            fare=fare,
        )
        nearest.status = DriverStatus.ON_TRIP
        self._trips[trip.trip_id] = trip
        return trip

    def complete_trip(self, trip_id: str) -> Trip:
        if trip_id not in self._trips:
            raise TripNotFoundError(f"Trip {trip_id!r} not found.")
        trip = self._trips[trip_id]
        trip.status = TripStatus.COMPLETED
        trip.completed_at = datetime.now()
        trip.driver.status = DriverStatus.AVAILABLE
        return trip

    def get_trip(self, trip_id: str) -> Trip:
        if trip_id not in self._trips:
            raise TripNotFoundError(f"Trip {trip_id!r} not found.")
        return self._trips[trip_id]

    def get_available_drivers(self) -> list[Driver]:
        return [d for d in self._drivers.values() if d.status == DriverStatus.AVAILABLE]
