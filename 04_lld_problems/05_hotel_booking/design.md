# Design: Hotel Booking System

## ASCII Class Diagram

```
+--------------------+       +--------------------+
|   PricingStrategy  |<------|     Hotel          |
|  (interface/ABC)   |       |--------------------|
|--------------------|       | name: str          |
| + calculate(room,  |       | rooms: dict        |
|   check_in,        |       | guests: dict       |
|   check_out)       |       | reservations: dict |
+--------------------+       | _lock: Lock        |
        ^                    |--------------------|
        |                    | + add_room()       |
+-------+--------+           | + register_guest() |
|StandardPricing |           | + search_rooms()   |
|Strategy        |           | + book_room()      |
|----------------|           | + cancel()         |
|+ calculate()   |           | + check_in()       |
+----------------+           | + check_out()      |
                             +--------------------+
                                     |  manages
              +----------------------+----------+
              |                                 |
    +---------+---------+           +-----------+------+
    |    Room (ABC)     |           |  Reservation     |
    |-------------------|           |------------------|
    | room_number: str  |           | reservation_id   |
    | room_type: Enum   |    uses   | guest: Guest     |
    | price_per_night   |<----------|room: Room        |
    | amenities: list   |           | check_in: date   |
    |-------------------|           | check_out: date  |
    | + is_available()  |           | total_price      |
    +-------------------+           | status: Enum     |
              ^                     |------------------|
    +---------+---------+           | + overlaps()     |
    |         |         |           +------------------+
SingleRoom DoubleRoom SuiteRoom
                                    +------------------+
                                    | ReservationStatus|
                                    | (Enum)           |
                                    |------------------|
                                    | PENDING          |
                                    | CONFIRMED        |
                                    | CHECKED_IN       |
                                    | CHECKED_OUT      |
                                    | CANCELLED        |
                                    +------------------+

    +-----------------+
    |    Guest        |
    |-----------------|
    | guest_id: str   |
    | name: str       |
    | contact: str    |
    +-----------------+

    +-----------------+     +--------------------+
    |   RoomType      |     |  ReservationObserver|
    | (Enum)          |     | (interface)         |
    |-----------------|     |--------------------|
    | SINGLE          |     | + on_status_change()|
    | DOUBLE          |     +--------------------+
    | SUITE           |
    +-----------------+
```

## Design Decisions

### 1. Strategy Pattern for Pricing
- `PricingStrategy` abstract class with `calculate(room, check_in, check_out) -> float`
- `StandardPricingStrategy`: base rate * nights + 20% surcharge for weekend nights
- Hotel stores a reference to the active strategy; can be swapped at runtime
- **Why**: Different seasons (peak/off-peak), loyalty tiers, or room promotions can each be a new strategy

### 2. State Pattern for Reservation Status
- `ReservationStatus` Enum: PENDING → CONFIRMED → CHECKED_IN → CHECKED_OUT | CANCELLED
- Transitions are validated in `Hotel.check_in()` and `Hotel.check_out()`
- Invalid transitions (e.g., checking out a CANCELLED reservation) raise `ValueError`
- **Why**: Makes lifecycle explicit and prevents invalid state transitions

### 3. Room Hierarchy (Inheritance)
- Abstract `Room` class with common attributes
- `SingleRoom`, `DoubleRoom`, `SuiteRoom` inherit from `Room`, setting their `room_type`
- Amenity differences are just data (list of strings), not separate classes
- **Why**: Simple hierarchy that's extensible (add `PenthouseRoom` without changing Hotel)

### 4. Overlap Detection
- `Reservation.overlaps(check_in, check_out)` checks:
  `new_check_in < self.check_out AND new_check_out > self.check_in`
- Called in `search_rooms` and `book_room` (under lock)
- **Why**: Centralized logic prevents duplicating overlap math across the codebase

### 5. Thread Safety
- `threading.Lock` in `Hotel` wraps `book_room` to prevent TOCTOU (Time-of-Check-Time-of-Use) races
- `search_rooms` is read-only and not locked for performance (eventual consistency acceptable)
- **Why**: Double-booking is a critical business error; reads can be slightly stale

## Key Design Patterns

| Pattern   | Applied To               | Benefit                                   |
|-----------|--------------------------|-------------------------------------------|
| Strategy  | Pricing calculation      | Swap pricing rules without changing Hotel |
| State     | Reservation status       | Explicit lifecycle, prevents invalid ops  |
| Template  | Room hierarchy           | Common room behavior, specialized types   |
| Observer  | Reservation status change| Decouple notification from state change   |

## Data Flow: Book Room

```
Client → hotel.book_room(guest_id, room_number, check_in, check_out)
    [acquire lock]
    → validate guest exists
    → validate room exists
    → check no conflicting reservations for room in date range
    → calculate total_price via pricing_strategy
    → create Reservation(id, guest, room, check_in, check_out, price, CONFIRMED)
    → store reservation
    [release lock]
    → return Reservation
```

## Weekend Surcharge Calculation

```
total = 0
current = check_in
while current < check_out:
    night_rate = room.price_per_night
    if current.weekday() in (5, 6):  # Saturday=5, Sunday=6
        night_rate *= 1.20
    total += night_rate
    current += timedelta(days=1)
return total
```
