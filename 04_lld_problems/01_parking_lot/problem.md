# Problem 01 — Parking Lot

## Problem Summary

Design a parking lot system for a multi-floor building. The system should manage vehicle entry and exit, assign appropriate spots based on vehicle type, issue tickets, calculate fees, and report availability.

---

## Functional Requirements

1. The parking lot has **multiple floors**, each with a fixed set of spots.
2. There are **three spot types**: Motorcycle spot, Compact spot, Large spot.
3. There are **three vehicle types** with different spot compatibility:
   - **Motorcycle** → fits in Motorcycle spot, Compact spot, or Large spot
   - **Car** → fits in Compact spot or Large spot
   - **Truck** → fits in Large spot only
4. On **entry**, the system assigns the best available spot (smallest fitting spot) and issues a **ticket**.
5. On **exit**, the system accepts a ticket, calculates the **fee**, frees the spot, and returns the fee.
6. Fees are time-based:
   - Motorcycle: $2.00 / hour
   - Car: $3.00 / hour
   - Truck: $5.00 / hour
   - Partial hours are rounded up to the next full hour.
7. The system tracks **real time** using `datetime` (not simulated ticks).
8. `get_availability()` returns the count of free spots per type across the entire lot.
9. The system must be **thread-safe** (multiple entry/exit gates can operate simultaneously).

---

## Non-Functional Requirements

- Thread safety for concurrent park/unpark operations.
- The fee strategy should be **replaceable** without changing the core parking logic (e.g., switch to flat-rate pricing for a special event).
- Adding a new vehicle or spot type should require minimal changes.

---

## Clarifying Questions (with Answers)

**Q1: Can a vehicle park in a spot larger than the minimum required?**
A: Yes. A motorcycle can park in a compact or large spot if motorcycle spots are full. A car can park in a large spot if compact spots are full. This is the "best fit" strategy — smallest available spot first.

**Q2: What happens if the lot is full?**
A: `park(vehicle)` returns `None` when no compatible spot is available.

**Q3: Can the same vehicle park twice (without unparking first)?**
A: No. Attempting to park an already-parked vehicle raises a `ValueError`.

**Q4: What if an invalid/already-used ticket is presented at exit?**
A: `unpark(ticket)` raises a `ValueError` for invalid or already-processed tickets.

**Q5: How is entry time tracked?**
A: The ticket records `entry_time = datetime.now()` at the moment `park()` is called.

**Q6: Is there a maximum capacity per floor?**
A: Capacity is fixed at initialization time. Each floor is initialized with a specific number of each spot type.

**Q7: Do we need to track which gate a vehicle entered from?**
A: Not required for this problem. Gates are abstracted — the lot simply processes entry/exit.

**Q8: How is fee rounded?**
A: Ceiling to the next full hour. 1 hour 1 minute = 2 hours billed. Minimum 1 hour.

**Q9: Can we have only one type of spot on a floor?**
A: Yes. Floor configuration is flexible at init time.

**Q10: Do different floors have different pricing?**
A: No. Pricing is based solely on vehicle type, not floor or spot type.

---

## Constraints

- 1 ≤ number of floors ≤ 10
- 1 ≤ spots per floor ≤ 1000
- Vehicle license plates are unique strings
- All spot IDs are unique across the entire lot

---

## Example Walkthrough

```
Setup:
  ParkingLot with 2 floors:
    Floor 0: 2 motorcycle spots, 3 compact spots, 1 large spot
    Floor 1: 1 motorcycle spot, 2 compact spots, 2 large spots

Action 1: park(Car(plate="ABC-123"))
  → Assigns to Floor 0, Compact Spot C-0-0
  → Returns ParkingTicket(id="T1", spot=C-0-0, entry_time=10:00)

Action 2: park(Truck(plate="XYZ-999"))
  → Assigns to Floor 0, Large Spot L-0-0 (only large spot on floor 0)
  → Returns ParkingTicket(id="T2", spot=L-0-0, entry_time=10:05)

Action 3: get_availability()
  → {"motorcycle": 3, "compact": 4, "large": 1}

Action 4: unpark(T1, exit_time=11:30)
  → Fee = ceil(1.5) * $3.00 = 2 * $3.00 = $6.00
  → Spot C-0-0 is now free

Action 5: get_availability()
  → {"motorcycle": 3, "compact": 5, "large": 1}
```

---

## What a Good Solution Covers

- [ ] Abstract base classes for Vehicle and ParkingSpot
- [ ] Compatibility matrix (vehicle can use which spot types)
- [ ] Best-fit spot assignment (smallest compatible spot first)
- [ ] Thread-safe parking (Lock per spot or global lock)
- [ ] Ticket issuance with UUID and datetime
- [ ] Fee calculation with ceiling rounding (Strategy pattern)
- [ ] `get_availability()` aggregating across all floors
- [ ] Error handling for double-park and invalid ticket

---

## Patterns & Principles Used

| Pattern / Principle | Where |
|---------------------|-------|
| **Strategy** | `FeeCalculator` ABC — swap pricing without touching lot logic |
| **Polymorphism / LSP** | `ParkingSpot.can_fit(vehicle)` — no isinstance checks in service layer |
| **Factory Function** | `create_parking_lot()` — encapsulates multi-floor construction |
| **Thread Safety** | `threading.Lock` in `ParkingLot.park()` / `unpark()` |
| **SRP** | `ParkingTicket` stores receipt data; `FeeCalculator` owns fee logic |

**See also:** Module 03 → [Strategy](../../03_design_patterns/behavioral/strategy/), Module 02 → [LSP](../../02_solid_principles/03_liskov_substitution/), [SRP](../../02_solid_principles/01_single_responsibility/)
