# Ride Sharing — Solution Explanation

## Nearest Driver Matching

```python
nearest = min(available, key=lambda d: d.location.distance_to(pickup))
```

`min()` with a key function is O(n) — acceptable for this problem. A production system would use a geospatial index (KD-tree, S2 geometry library, or PostGIS) for sub-linear lookups over thousands of drivers.

## Fare Calculation

```python
PRICING = {
    VehicleType.STANDARD: (2.0, 1.0),
    VehicleType.PREMIUM:  (5.0, 2.0),
    VehicleType.XL:       (3.0, 1.5),
}
base, rate = self.PRICING[nearest.vehicle.vehicle_type]
fare = round(base + rate * distance, 2)
```

The pricing table is a class-level constant, not hard-coded per method. Adding a new vehicle type only requires adding one entry to `PRICING`. The **Strategy** pattern would be appropriate if fare rules were more complex (surge pricing, time-of-day, etc.).

## Driver State Transitions

```
register_driver → AVAILABLE
request_ride    → ON_TRIP
complete_trip   → AVAILABLE
set_driver_status → any
```

State is stored on the `Driver` object. The system doesn't enforce illegal transitions (e.g., completing a trip from an AVAILABLE driver) — that's a tradeoff for simplicity. A strict system would validate state before transitions.

## Euclidean Distance

`Location.distance_to` uses Euclidean distance. Real lat/lon needs the Haversine formula for spherical Earth. For this problem, Euclidean is fine because the test data uses small coordinate differences.

## Data Relationships

`Trip` holds direct references to `Driver` and `Rider` objects (not just IDs). This means:
- No secondary lookup needed
- Mutations to `Driver.status` are immediately visible through `trip.driver.status`
- But Trip objects hold a strong reference, preventing garbage collection

In a large-scale system, trips would store IDs and the system would resolve them on demand.
