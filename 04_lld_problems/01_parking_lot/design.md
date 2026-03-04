# Design — Parking Lot

## Clarifying Questions (Interview Simulation)

Before drawing any class diagram, ask these in an interview:

1. How many floors and spots? → Multi-floor, configurable at init.
2. What vehicle types exist? → Motorcycle, Car, Truck.
3. Vehicle-spot compatibility rules? → Motorcycle fits any; Car fits compact+large; Truck fits large only.
4. Pricing model? → Per-vehicle-type hourly rate, ceiling rounding.
5. What does park() return on success/failure? → Ticket on success, None if full.
6. Thread safety required? → Yes, multiple gates.
7. Can I assume license plates are unique? → Yes.
8. Do we need persistence? → No, in-memory is fine.

---

## Core Entities

### 1. Vehicle (Abstract Base Class)
Represents any vehicle entering the lot. Subclasses define which spot types they are compatible with.

### 2. ParkingSpot (Abstract Base Class)
Represents a physical parking space. Subclasses define the spot type.

### 3. ParkingTicket
Issued when a vehicle parks. Carries all information needed to process exit: vehicle reference, spot reference, entry time. UUID-based ID for uniqueness.

### 4. ParkingFloor
One floor of the building. Holds a list of spots. Responsible for finding available spots on that floor.

### 5. FeeCalculator (Strategy Interface)
Abstract strategy for calculating fees. Default implementation uses hourly rates. Swap out for flat-rate pricing without touching parking logic.

### 6. ParkingLot (Singleton-like Facade)
Central coordinator. Owns all floors and the fee calculator. Exposes `park()`, `unpark()`, `get_availability()`. Manages the active-ticket registry. Thread-safe.

---

## Class Diagram (ASCII)

```
                        +------------------+
                        |   ParkingLot     |
                        +------------------+
                        | - floors         |---------->  ParkingFloor  (1..*)
                        | - fee_calculator |---------->  FeeCalculator
                        | - active_tickets |
                        | - _lock: Lock    |
                        +------------------+
                        | + park(vehicle)  |
                        | + unpark(ticket) |
                        | + get_availability() |
                        +------------------+
                                |
                    +-----------+-----------+
                    |                       |
           +----------------+    +---------------------+
           |  ParkingFloor  |    |    FeeCalculator     | (ABC)
           +----------------+    +---------------------+
           | - floor_num    |    | + calculate(vehicle, |
           | - spots: List  |    |   entry, exit): float|
           +----------------+    +---------------------+
           | + find_spot    |              |
           |   (vehicle)    |    +---------------------+
           +----------------+    | HourlyFeeCalculator |
                    |            +---------------------+
                    |            | RATES: dict         |
           +--------+-------+   | + calculate(...)    |
           |                |    +---------------------+
    +-----------+    +-----------+
    |ParkingSpot| (ABC)          |
    +-----------+                |
    | - spot_id |         Vehicle (ABC)
    | - floor   |         +----------+
    | - is_free |         | - plate  |
    | - vehicle |         | - type   |
    +-----------+         +----------+
    | + park()  |              |
    | + unpark()|    +---------+---------+
    +-----------+    |         |         |
         |       Motorcycle   Car      Truck
    +----+----+
    |    |    |
  Moto Compact Large
  Spot  Spot   Spot

                    +------------------+
                    |  ParkingTicket   |
                    +------------------+
                    | - ticket_id: str |
                    | - vehicle        |
                    | - spot           |
                    | - entry_time     |
                    | - is_active: bool|
                    +------------------+
```

---

## Vehicle-Spot Compatibility Matrix

| Vehicle Type | Motorcycle Spot | Compact Spot | Large Spot |
|-------------|-----------------|--------------|------------|
| Motorcycle  | YES             | YES          | YES        |
| Car         | NO              | YES          | YES        |
| Truck       | NO              | NO           | YES        |

Implementation: Each `Vehicle` subclass defines `compatible_spot_types()` returning a list of spot type classes in **preference order** (smallest first → best fit).

---

## Spot Assignment Algorithm (Best Fit)

```
def find_spot(vehicle):
    for preferred_spot_type in vehicle.compatible_spot_types():   # smallest first
        for spot in self.spots:
            if isinstance(spot, preferred_spot_type) and spot.is_free:
                return spot
    return None
```

The ParkingLot iterates floors and calls `floor.find_spot(vehicle)`. First match wins.

---

## State: ParkingSpot Lifecycle

```
     is_free = True
          |
    park(vehicle)
          |
     is_free = False
     vehicle = <Vehicle>
          |
    unpark()
          |
     is_free = True
     vehicle = None
```

---

## Fee Calculation (Strategy Pattern)

```python
class FeeCalculator(ABC):
    @abstractmethod
    def calculate(self, vehicle, entry_time, exit_time) -> float: ...

class HourlyFeeCalculator(FeeCalculator):
    RATES = {Motorcycle: 2.0, Car: 3.0, Truck: 5.0}

    def calculate(self, vehicle, entry_time, exit_time) -> float:
        duration_seconds = (exit_time - entry_time).total_seconds()
        hours = math.ceil(duration_seconds / 3600)
        hours = max(hours, 1)  # minimum 1 hour
        return hours * self.RATES[type(vehicle)]
```

**Why Strategy?**
- The fee algorithm is independent of parking logic.
- You can inject `FlatRateFeeCalculator` or `WeekendFeeCalculator` at construction time.
- Testing: inject a mock calculator that returns fixed values.

---

## Thread Safety Design

The `ParkingLot` holds a single `threading.Lock`. It is acquired for the duration of `park()` and `unpark()`. This prevents two threads from assigning the same spot simultaneously.

```
Thread A (Gate 1): park(Car)     │ Thread B (Gate 2): park(Car)
─────────────────────────────────┼──────────────────────────────
acquire lock                     │ waiting for lock...
find spot → Compact-0-0          │
mark spot as occupied            │
issue ticket                     │
release lock                     │ acquire lock
                                 │ find spot → Compact-0-1 (next)
                                 │ ...
```

Trade-off: A global lock is simple and correct. At very high throughput you could use per-floor locks, but a single lock is appropriate for an interview solution.

---

## Design Decisions & Trade-offs

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| Strategy for fee | Swappable pricing without touching core logic | Slight complexity vs. simple if/else |
| Best-fit spot assignment | Conserves premium spots | Slightly slower than first-fit |
| Global Lock | Simple, correct | Bottleneck under extreme concurrency |
| UUID ticket IDs | Globally unique, no state counter needed | Slightly heavier than int counter |
| Abstract base classes | Enforces contract on Vehicle/Spot subclasses | More files/boilerplate |
| Ticket registry in ParkingLot | Single source of truth for active tickets | Memory grows with active tickets |

---

## Extensibility

**Add a new vehicle type (e.g., Bus):**
1. Create `class Bus(Vehicle)` with `compatible_spot_types()` returning `[LargeSpot]` (or a new `BusSpot`).
2. Add `Bus: 8.0` to `HourlyFeeCalculator.RATES`.
3. No changes to `ParkingLot`, `ParkingFloor`, or any existing class.

**Add a new spot type (e.g., EV Charging Spot):**
1. Create `class EVSpot(ParkingSpot)`.
2. Update `compatible_spot_types()` on vehicles that can use it.
3. No changes to ParkingLot or FeeCalculator.

**Add flat-rate pricing:**
1. Create `class FlatRateFeeCalculator(FeeCalculator)`.
2. Pass it at `ParkingLot` construction time.
3. Zero changes to existing code.
