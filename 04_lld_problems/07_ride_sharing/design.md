# Design — Ride Sharing System

## Clarifying Questions (Interview Simulation)

Before drawing any class diagram, ask these in an interview:

1. How are drivers matched to riders? → Nearest available driver.
2. What vehicle types exist? → STANDARD, PREMIUM, XL — each with different pricing.
3. How is fare calculated? → Base fee + per-unit-distance rate × Euclidean distance.
4. Can a driver take multiple trips simultaneously? → No, one trip at a time.
5. What happens if no drivers are available? → Raise an error.
6. Thread safety required? → Not for this version (no lock needed in basic implementation).
7. Do we need real GPS? → No, use simple coordinates with Euclidean distance.
8. Trip rating/reviews? → Out of scope for this problem.

---

## Core Entities

### 1. Location (Value Object)
Simple (lat, lon) coordinate pair. `distance_to(other)` uses Euclidean distance.
Immutable — always create a new Location to update position.

### 2. Vehicle (Data Class)
Holds license plate and vehicle type (STANDARD/PREMIUM/XL). Owned by a driver.

### 3. Driver
Has an ID, name, vehicle, current location, and status (AVAILABLE/ON_TRIP/OFFLINE).
Status transitions: AVAILABLE → ON_TRIP (when assigned) → AVAILABLE (after completion).

### 4. Rider
Simple entity: ID and name. Represents the passenger.

### 5. Trip
Captures the full trip lifecycle: driver, rider, pickup/dropoff locations, fare, status, timestamps.
Status: REQUESTED → IN_PROGRESS → COMPLETED.

### 6. RideSharingSystem (Facade)
The central coordinator. Manages driver/rider registries and trip dispatch.
Implements nearest-driver matching and fare calculation.

---

## Class Diagram (ASCII)

```
+-------------------+
| RideSharingSystem |
+-------------------+
| - _drivers: dict  |------>  Driver (1..*)
| - _riders: dict   |------>  Rider (1..*)
| - _trips: dict    |------>  Trip (1..*)
+-------------------+
| + register_driver()       |
| + register_rider()        |
| + request_ride()          |
| + complete_trip()         |
| + get_available_drivers() |
+---------------------------+

+------------------+      +------------------+
|     Driver       |      |      Rider       |
+------------------+      +------------------+
| driver_id: str   |      | rider_id: str    |
| name: str        |      | name: str        |
| vehicle: Vehicle |      +------------------+
| location: Loc    |
| status: Enum     |      +------------------+
+------------------+      |     Location     |
                          +------------------+
+------------------+      | lat: float       |
|     Vehicle      |      | lon: float       |
+------------------+      +------------------+
| license_plate    |      | + distance_to()  |
| vehicle_type     |      +------------------+
+------------------+

+----------------------------+
|           Trip             |
+----------------------------+
| trip_id: str               |
| driver: Driver             |
| rider: Rider               |
| pickup: Location           |
| dropoff: Location          |
| status: TripStatus         |
| fare: float                |
| requested_at: datetime     |
| completed_at: datetime|None|
+----------------------------+
```

---

## Driver Status State Machine

```
    OFFLINE
       ↕
  AVAILABLE  ──request_ride()──>  ON_TRIP
       ↑                             |
       └────── complete_trip() ──────┘
```

---

## Fare Calculation

```
Pricing per VehicleType:
  STANDARD: base=$2.00, rate=$1.00/unit
  PREMIUM:  base=$5.00, rate=$2.00/unit
  XL:       base=$3.00, rate=$1.50/unit

fare = round(base + rate * pickup.distance_to(dropoff), 2)
```

The nearest driver's vehicle type determines the pricing tier.

---

## Driver Matching Algorithm

```
available_drivers = [d for d in drivers if d.status == AVAILABLE]
if not available_drivers:
    raise NoDriverAvailableError

nearest = min(available_drivers,
              key=lambda d: d.location.distance_to(pickup))
```

---

## Design Decisions & Trade-offs

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| Euclidean distance | Simple, testable | Not real-world GPS accuracy |
| Nearest driver selection | Good UX, simple algorithm | Could use smarter dispatch |
| Pricing dict on system | Easy to read/modify | Could be a Strategy pattern |
| @dataclass for entities | Less boilerplate | Less control over validation |
| No thread safety | Keeps scope focused | Not production-ready |

---

## Extensibility

**Add surge pricing:**
- Introduce a `FareStrategy` ABC with `calculate(distance, vehicle_type, demand_factor)`.
- Inject into RideSharingSystem.

**Add ride cancellation:**
- Add `CANCELLED` status to TripStatus.
- Add `cancel_trip(trip_id)` method that frees the driver.

**Add driver ratings:**
- Add `rating` field and `rate_driver(trip_id, score)` method.
- Calculate cumulative moving average (as in Restaurant.update_rating).
