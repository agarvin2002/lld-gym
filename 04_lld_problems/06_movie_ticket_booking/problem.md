# Movie Ticket Booking System

Design a movie ticket booking system (like BookMyShow).

---

## Requirements

### Core Entities

- **Movie**: has a title, duration in minutes, and a genre.
- **Theater**: has a name and a location; owns one or more screens.
- **Screen**: belongs to a theater, has a `screen_number`, and contains a grid of seats (`rows x cols`). Each seat has a `SeatCategory`: `REGULAR`, `PREMIUM`, or `VIP`.
- **Show**: a `(movie, screen, show_time)` tuple with per-category pricing (`dict[SeatCategory, float]`).
- **Seat**: identified by a `seat_id` (e.g., `"R0C2"`), has a `SeatCategory` and a `SeatStatus` (`AVAILABLE` or `BOOKED`).
- **Booking**: records which user booked which seats for which show, along with the `total_amount` and a timestamp.
- **User** (implicit): represented by `user_name` string in bookings.

### Functional Requirements

1. Add movies, theaters, screens, and shows to the system.
2. Query available seats for a show.
3. Book one or more seats for a show atomically — no two users can book the same seat.
4. Retrieve a booking by its ID.

### Constraints & Rules

- Seats transition from `AVAILABLE` to `BOOKED`. There is no cancellation in this version.
- Booking is **all-or-nothing**: if any seat in the requested list is already booked, the whole booking fails with a `ValueError`.
- Booking an empty list of seat IDs raises a `ValueError`.
- Booking a seat ID that does not exist on the screen raises a `ValueError`.
- The system must be **thread-safe**: concurrent booking attempts for the same seat must result in exactly one success.

---

## API (BookingSystem Facade)

```python
class BookingSystem:
    def add_movie(self, title: str, duration_minutes: int, genre: str) -> Movie: ...
    def add_theater(self, name: str, location: str) -> Theater: ...
    def add_screen(self, theater: Theater, screen_number: int, rows: int, cols: int) -> Screen: ...
    def add_show(self, movie: Movie, screen: Screen, show_time: datetime,
                 pricing: dict[SeatCategory, float]) -> Show: ...
    def book_seats(self, user_name: str, show: Show, seat_ids: list[str]) -> Booking: ...
    def get_available_seats(self, show: Show) -> list[Seat]: ...
    def get_booking(self, booking_id: str) -> Booking: ...
```

---

## Enums

```python
class SeatCategory(Enum):
    REGULAR = "REGULAR"
    PREMIUM = "PREMIUM"
    VIP     = "VIP"

class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED    = "BOOKED"
```

---

## Hints

- Seat IDs are generated as `"R{row}C{col}"` (e.g., row 0, col 2 → `"R0C2"`).
- Pricing is per `SeatCategory` per show, so the same screen can have different prices for a matinee vs. an evening show.
- Use `threading.Lock` on the `Screen` to keep locking at the finest possible granularity (per-screen vs. system-wide).
- Use `uuid.uuid4()` for all entity IDs.
- Use `@dataclass` for data-holding classes.

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **State** | `SeatStatus`: AVAILABLE → BOOKED; no cancellation keeps state machine simple |
| **Facade** | `BookingSystem` provides a single interface over movies, theaters, shows, and seats |
| **Thread Safety** | Per-screen `threading.Lock` prevents concurrent double-booking |
| **SRP** | `Show` owns seat map and pricing; `Booking` records the transaction; `BookingSystem` orchestrates |

**See also:** Module 03 → [State](../../03_design_patterns/behavioral/state/), [Facade](../../03_design_patterns/structural/facade/)
