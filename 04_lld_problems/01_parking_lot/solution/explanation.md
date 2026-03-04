# Explanation: Parking Lot Solution

## Patterns Used

### Strategy — `FeeCalculator`
`HourlyFeeCalculator` is injected into `ParkingLot` rather than hardcoded. Swap it for `FlatRateFeeCalculator` or `DailyRateCalculator` without touching the lot logic.

```
ParkingLot ──uses──> FeeCalculator (ABC)
                         ↑
                  HourlyFeeCalculator
```

### Polymorphism — Vehicle and Spot hierarchies
`can_fit(vehicle)` is implemented differently per spot type, making spot assignment purely polymorphic. No `isinstance` checks anywhere in the service layer.

```
Vehicle (ABC)
  ├── Motorcycle
  ├── Car
  └── Truck

ParkingSpot (ABC)
  ├── MotorcycleSpot   ← fits Motorcycle
  ├── CompactSpot      ← fits Car, Motorcycle
  └── LargeSpot        ← fits all
```

## Key Design Decisions

**Best-fit assignment**: When a car can fit in both a compact and a large spot, it always takes the compact first. This keeps large spots available for trucks. Implemented by ordering spots: motorcycle → compact → large.

**Thread safety**: A single `threading.Lock` wraps the entire `park()` operation. Per-spot locks would allow more parallelism but add complexity; for a parking lot the coarser lock is justified.

**Ticket as receipt**: `ParkingTicket` carries `entry_time` and `exit_time`. Fee calculation lives in `FeeCalculator`, not in the ticket — single responsibility.

**`create_parking_lot` factory function**: Takes a list of dicts `[{"motorcycle": 2, "compact": 5, "large": 3}]` per floor. Keeps test setup concise.

## Trade-offs

| Decision | Benefit | Cost |
|----------|---------|------|
| Single global lock | Simple, no deadlocks | Reduced throughput under high concurrency |
| Best-fit assignment | Efficient spot utilisation | Slightly more complex search |
| Fee ceiling rounding | Fairer to the business | Slightly unfair to customer for short stays |

## Extensibility Points

- **New vehicle type**: subclass `Vehicle`, add a new `ParkingSpot` subclass with the right `can_fit`
- **New pricing model**: implement `FeeCalculator`, inject at construction
- **Reservations**: add a `ReservationService` that pre-assigns spots with a hold expiry
- **Multi-entry/exit gates**: the lock already makes this safe; just expose `park()`/`unpark()` via HTTP
