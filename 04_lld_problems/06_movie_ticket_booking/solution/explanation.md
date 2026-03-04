# Movie Ticket Booking — Solution Explanation

## Architecture: Facade Pattern

`BookingSystem` is a Facade that hides the complexity of coordinating `Movie`, `Theater`, `Screen`, `Show`, `Seat`, and `Booking`. Callers only interact with `BookingSystem`.

## Thread Safety: Per-Screen Lock

```python
with show.screen._lock:
    # check all seats available
    # mark all seats booked
```

The lock lives on `Screen`, not on `BookingSystem`. This gives **finer granularity**: two concurrent bookings on different screens don't block each other, while bookings on the same screen serialize correctly.

## All-or-Nothing Booking

```python
# Phase 1: validate ALL seats first (outside lock for ID check)
for sid in seat_ids:
    if sid not in seat_map:
        raise ValueError(...)

# Phase 2: acquire lock, check availability, then book
with show.screen._lock:
    for sid in seat_ids:
        if seat_map[sid].status != SeatStatus.AVAILABLE:
            raise ValueError(...)   # nothing booked yet → consistent state
    for sid in seat_ids:
        seat_map[sid].status = SeatStatus.BOOKED
```

The check and the write are both inside the lock. No seat is partially booked.

## Seat ID Generation

```python
Seat(seat_id=f"R{r}C{c}", row=r, col=c, ...)
```

Deterministic IDs enable callers to reference seats by position without querying first.

## Category Assignment by Row

```python
if r == 0:         cat = VIP
elif r <= rows//3: cat = PREMIUM
else:              cat = REGULAR
```

Row 0 (front row closest to screen) is VIP — counter-intuitive for cinemas but illustrates the pattern. The strategy is encapsulated in `add_screen` and can be changed without touching `book_seats`.

## Pricing per Show

Pricing is attached to `Show`, not `Screen`. The same screen can have `{REGULAR: 10}` for matinee and `{REGULAR: 15}` for evening. `book_seats` computes `total_amount` by looking up each booked seat's category in `show.pricing`.

## `@dataclass` with `threading.Lock` field

```python
_lock: threading.Lock = field(
    default_factory=threading.Lock, repr=False, compare=False
)
```

Using `field(default_factory=...)` avoids the shared-default-argument bug. `repr=False, compare=False` prevents the lock from appearing in `__repr__` or affecting equality comparisons.
