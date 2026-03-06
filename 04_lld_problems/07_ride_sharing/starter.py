"""
Ride Sharing System — Starter File
=====================================
Your task: Implement a ride sharing system (Uber/Lyft style).

Read problem.md and design.md before starting.

Design decisions:
  - @dataclass for Location, Vehicle, Driver, Rider, Trip
  - Location.distance_to() uses Euclidean distance
  - Nearest available driver is selected when a ride is requested
  - Fare = base_fee + per_unit_distance * distance (per VehicleType)
  - Driver status: AVAILABLE → ON_TRIP → AVAILABLE (after completion)
  - Use uuid.uuid4() for IDs
"""
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

    def distance_to(self, other: "Location") -> float:
        # TODO: Return Euclidean distance: sqrt((lat diff)^2 + (lon diff)^2)
        pass


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
    # Pricing per vehicle type: (base_fee, per_unit_distance_rate)
    PRICING = {
        VehicleType.STANDARD: (2.0, 1.0),
        VehicleType.PREMIUM:  (5.0, 2.0),
        VehicleType.XL:       (3.0, 1.5),
    }

    def __init__(self) -> None:
        # TODO: Create _drivers, _riders, _trips as empty dicts keyed by their IDs
        pass

    def register_driver(
        self, name: str, license_plate: str, vehicle_type: VehicleType
    ) -> Driver:
        """Register a new driver with a vehicle.

        TODO:
            - Create Vehicle and Driver with driver_id = str(uuid.uuid4())
            - Store in _drivers and return driver
        """
        pass

    def register_rider(self, name: str) -> Rider:
        """Register a new rider.

        TODO:
            - Create Rider with rider_id = str(uuid.uuid4())
            - Store in _riders and return rider
        """
        pass

    def update_driver_location(self, driver_id: str, lat: float, lon: float) -> None:
        """Update a driver's current location.

        TODO:
            - Raise DriverNotFoundError if driver_id not in _drivers
            - Set driver.location = Location(lat, lon)
        """
        pass

    def set_driver_status(self, driver_id: str, status: DriverStatus) -> None:
        """Update a driver's availability status.

        TODO:
            - Raise DriverNotFoundError if driver_id not in _drivers
            - Set driver.status = status
        """
        pass

    def request_ride(
        self, rider_id: str, pickup: Location, dropoff: Location
    ) -> Trip:
        """Match rider to nearest available driver and create a trip.

        TODO:
            - Filter drivers with status == AVAILABLE
            - Raise NoDriverAvailableError if none available
            - Select nearest driver by pickup.distance_to(pickup) from driver.location
            - Calculate fare: base + rate * pickup.distance_to(dropoff), rounded to 2dp
            - Create Trip with trip_id = str(uuid.uuid4())
            - Set driver.status = ON_TRIP
            - Store in _trips and return trip
        """
        pass

    def complete_trip(self, trip_id: str) -> Trip:
        """Mark a trip as completed and free the driver.

        TODO:
            - Raise TripNotFoundError if trip_id not in _trips
            - Set trip.status = COMPLETED
            - Set trip.completed_at = datetime.now()
            - Set trip.driver.status = AVAILABLE
            - Return trip
        """
        pass

    def get_trip(self, trip_id: str) -> Trip:
        """Retrieve a trip by ID.

        TODO:
            - Raise TripNotFoundError if not found
            - Return the trip
        """
        pass

    def get_available_drivers(self) -> list[Driver]:
        # TODO: Return drivers with status == AVAILABLE
        pass
