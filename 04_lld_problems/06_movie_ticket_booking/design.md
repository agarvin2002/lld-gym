# Movie Ticket Booking System — Design

---

## Class Diagram (ASCII)

```
+------------------+        +------------------+
|     Movie        |        |    Theater       |
|------------------|        |------------------|
| movie_id: str    |        | theater_id: str  |
| title: str       |        | name: str        |
| duration_minutes |        | location: str    |
| genre: str       |        +--------+---------+
+------------------+                 |  owns 1..*
                                     |
                            +--------v---------+
                            |     Screen       |
                            |------------------|
                            | screen_id: str   |
                            | theater: Theater |
                            | screen_number    |
                            | seats: list[Seat]|
                            | _lock: Lock      |
                            +--------+---------+
                                     |  contains rows*cols
                                     |
                            +--------v---------+
                            |      Seat        |
                            |------------------|
                            | seat_id: str     |   SeatCategory
                            | row: int         |   +-----------+
                            | col: int         |   | REGULAR   |
                            | category --------+-> | PREMIUM   |
                            | status           |   | VIP       |
                            +------------------+   +-----------+
                                                   SeatStatus
         Movie + Screen + show_time                +-----------+
               |                                   | AVAILABLE |
+-----------------------------+                    | BOOKED    |
|           Show              |                    +-----------+
|-----------------------------|
| show_id: str                |
| movie: Movie                |
| screen: Screen              |
| show_time: datetime         |
| pricing: dict[Cat, float]   |
+-------------+---------------+
              |
              | 1 booking books N seats
              |
+-------------v---------------+
|          Booking            |
|-----------------------------|
| booking_id: str             |
| user_name: str              |
| show: Show                  |
| seats: list[Seat]           |
| total_amount: float         |
| booked_at: datetime         |
+-----------------------------+

+-----------------------------+
|       BookingSystem         |   <<facade>>
|-----------------------------|
| _movies: dict               |
| _theaters: dict             |
| _screens: dict              |
| _shows: dict                |
| _bookings: dict             |
| _lock: Lock                 |
|-----------------------------|
| add_movie(...)  -> Movie    |
| add_theater(..) -> Theater  |
| add_screen(..)  -> Screen   |
| add_show(..)    -> Show     |
| book_seats(..)  -> Booking  |
| get_available_seats(show)   |
| get_booking(id) -> Booking  |
+-----------------------------+
```

---

## Booking Flow

```
User calls book_seats(user_name, show, seat_ids)
  |
  v
1. Validate seat_ids is not empty           -> ValueError if empty
  |
  v
2. Build seat_map from show.screen.seats
  |
  v
3. Validate all seat_ids exist in seat_map  -> ValueError if any missing
  |
  v
4. Acquire show.screen._lock                <- per-screen lock (fine-grained)
  |
  v
5. (Inside lock) Check all seats AVAILABLE  -> ValueError if any BOOKED
  |
  v
6. (Inside lock) Mark all seats BOOKED      <- atomic check-then-set
  |
  v
7. Release lock
  |
  v
8. Calculate total_amount from pricing
  |
  v
9. Create Booking, store in _bookings       <- system-wide lock for dict write
  |
  v
10. Return Booking
```

---

## Thread Safety Design

### Two-level locking strategy

| Lock | Scope | Protects |
|------|-------|----------|
| `Screen._lock` | Per screen | Seat status transitions (step 4-7 above) |
| `BookingSystem._lock` | System-wide | `_bookings` dict reads/writes |

**Why per-screen locking?**

Using a single system-wide lock would serialize all bookings across all screens, eliminating concurrency. By locking at the `Screen` level, two users booking seats in different screens (or even different shows on the same screen at different times, if extended) can proceed concurrently. The seat status map is owned by the screen, so the screen lock is the natural guard.

### Atomic check-then-set

The critical section (steps 5-6) does two things under a single lock acquisition:

1. **Check**: verify all requested seats are `AVAILABLE`
2. **Set**: mark all of them `BOOKED`

This prevents TOCTOU (time-of-check-time-of-use) races: if two threads both pass the availability check before either sets the status, one seat could be double-booked. Holding the lock across both operations eliminates this window.

### All-or-nothing semantics

Validation of seat existence (step 3) happens **before** acquiring the lock. Only the status-check-and-update is inside the lock, keeping the critical section short. If any seat is unavailable, we raise `ValueError` without having modified any seat — the operation is fully rolled back by never having started.

---

## Pricing Model

```
Show.pricing: dict[SeatCategory, float]

Example:
  {
    SeatCategory.REGULAR: 150.0,
    SeatCategory.PREMIUM: 250.0,
    SeatCategory.VIP:     400.0,
  }

total_amount = sum(show.pricing[seat.category] for seat in booked_seats)
```

Pricing is attached to a `Show`, not a `Screen`, so:
- The same screen can run a matinee at lower prices and an evening show at premium prices.
- Different movies on the same screen can have different price points.

---

## Seat Category Assignment (default strategy)

When `add_screen` creates seats for an `rows x cols` grid:

```
Row 0          -> VIP
Rows 1..rows//3 -> PREMIUM
Remaining rows  -> REGULAR
```

This mirrors real-world cinema layouts where front-center or special rows are premium.
