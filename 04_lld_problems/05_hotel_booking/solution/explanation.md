# Explanation: Hotel Booking System

## Patterns Used

### Strategy — `PricingStrategy`
`StandardPricingStrategy` is injected into `Hotel` at construction. Swap it for `DiscountPricingStrategy` or `SeasonalPricingStrategy` without changing any booking logic.

```
Hotel ──uses──> PricingStrategy (ABC)
                     ↑
           StandardPricingStrategy   (base rate + 20% weekend surcharge)
```

### State — `ReservationStatus`
A reservation moves through: `CONFIRMED → CHECKED_IN → CHECKED_OUT`. It can also go `CONFIRMED → CANCELLED`. Each transition is validated — you can't check in a cancelled reservation.

### Facade — `Hotel`
`Hotel` is the single entry point. Clients call `hotel.book_room()`, `hotel.check_in()`, etc. without knowing about rooms, guests, or pricing internals.

## Key Design Decisions

**Overlap detection in `Reservation.overlaps()`**: Uses the standard interval overlap formula — `new_check_in < self.check_out AND new_check_out > self.check_in`. Only active reservations (not CANCELLED/CHECKED_OUT) count.

**Thread safety via `Lock` in `book_room()`**: Validation (guest exists, room exists, dates valid) happens outside the lock. Only the conflict check + reservation creation is inside — minimises contention while preventing double-booking.

**Weekend surcharge per-night**: `StandardPricingStrategy.calculate()` iterates each night in the stay and adds 20% for Saturday/Sunday. This gives correct pricing for mixed weekday/weekend stays.

## Trade-offs

| Decision | Benefit | Cost |
|----------|---------|------|
| Per-room conflict check (O(reservations)) | Simple, no extra data structure | Slow for huge datasets — add index in prod |
| Lock on entire book_room | No double-booking | Slight throughput reduction under concurrency |
| Strategy injected at Hotel level | Easy to swap pricing globally | All rooms use same strategy; per-room pricing needs refactor |

## Extensibility Points
- **New room types**: subclass `Room`, no other changes
- **New pricing logic**: implement `PricingStrategy`, inject it
- **Loyalty points**: add `LoyaltyService` observer on successful bookings
- **Cancellation policy**: inject a `CancellationPolicy` strategy to compute refund amount
