# Problem 7: Ride Sharing System

## Problem Statement

Design a ride-sharing system (like Uber/Lyft) that matches riders with nearby available drivers, tracks trips, and computes fares.

---

## Core Entities

| Entity | Key Fields |
|--------|-----------|
| `Driver` | id, name, vehicle, location, status (AVAILABLE/ON_TRIP/OFFLINE) |
| `Rider` | id, name |
| `Location` | lat, lon — supports `distance_to(other) -> float` (Euclidean) |
| `Vehicle` | license_plate, vehicle_type (STANDARD/PREMIUM/XL) |
| `Trip` | id, driver, rider, pickup, dropoff, status, fare, timestamps |

---

## API

```python
class RideSharingSystem:
    def register_driver(self, name, license_plate, vehicle_type) -> Driver
    def register_rider(self, name) -> Rider
    def update_driver_location(self, driver_id, lat, lon) -> None
    def set_driver_status(self, driver_id, status) -> None
    def request_ride(self, rider_id, pickup: Location, dropoff: Location) -> Trip
    def complete_trip(self, trip_id) -> Trip
    def get_trip(self, trip_id) -> Trip
    def get_available_drivers(self) -> list[Driver]
```

---

## Matching & Pricing

- `request_ride` finds the **nearest available** driver to the pickup location
- If no available driver exists, raises `NoDriverAvailableError`
- Fare = `base_fare + distance * rate_per_unit`
  - STANDARD: base=2.0, rate=1.0 per distance unit
  - PREMIUM: base=5.0, rate=2.0
  - XL: base=3.0, rate=1.5
- Distance is Euclidean distance between pickup and dropoff `Location`

---

## Trip Status
`REQUESTED → IN_PROGRESS → COMPLETED`

When a trip is requested: driver status → `ON_TRIP`
When a trip is completed: driver status → `AVAILABLE`

---

## Enums
```python
class DriverStatus(Enum): AVAILABLE, ON_TRIP, OFFLINE
class VehicleType(Enum): STANDARD, PREMIUM, XL
class TripStatus(Enum): REQUESTED, IN_PROGRESS, COMPLETED
```

---

## Errors
```python
class NoDriverAvailableError(Exception): pass
class DriverNotFoundError(Exception): pass
class TripNotFoundError(Exception): pass
```

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **State** | `DriverStatus` (AVAILABLE / ON_TRIP / OFFLINE) and `TripStatus` (REQUESTED / IN_PROGRESS / COMPLETED) — two parallel state machines |
| **Strategy** | Fare calculation varies by `VehicleType` (base fare + rate per distance unit) |
| **SRP** | `Driver` tracks location/status; `Trip` records the journey; `RideSharingSystem` handles matching |

**See also:** Module 03 → [Strategy](../../03_design_patterns/behavioral/strategy/), [State](../../03_design_patterns/behavioral/state/)
