# LLD Interview Approach Framework

## The 6-Step Framework (Memorize This)

### Step 1: Clarify Requirements (5 minutes)
Ask before writing a single line of code. This shows seniority.

**Template questions:**
1. **Scope**: "What are the core operations? What's out of scope?"
2. **Scale**: "How many users/floors/vehicles are we designing for?"
3. **Constraints**: "Any specific rules I should model?"
4. **Edge cases**: "What happens when [edge case]?"
5. **Non-functional**: "Do we need thread safety? Persistence?"

**Example (Parking Lot):**
> "Before I start — what types of vehicles should I support? And do I need to handle pricing, or just availability? Any specific spot types?"

---

### Step 2: Identify Entities (2 minutes)
Read the problem. **Underline nouns** → these become classes.
**Underline verbs** → these become methods.

**Example:**
> "A **library** manages **books**. **Members** can **borrow** and **return** books. Each **book** has a **title**, **author**, and **ISBN**."

Entities: `Library`, `Book`, `Member`, `BorrowRecord`
Methods: `borrow()`, `return_book()`

---

### Step 3: Define Relationships (2 minutes)
Map how entities relate:
- **is-a** (inheritance): `Car is-a Vehicle`
- **has-a** (composition): `ParkingLot has-a list[Floor]`
- **uses** (dependency): `ParkingService uses FeeCalculator`

Draw a quick ASCII diagram:
```
ParkingLot ──has──> Floor[] ──has──> ParkingSpot[]
                                          ↑
Vehicle ──────────────────────────────parks_in
```

---

### Step 4: Define Interfaces First (3 minutes)
Write ABCs before implementations. This shows clean thinking.

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def get_type(self) -> str: ...

class ParkingSpot(ABC):
    @abstractmethod
    def can_fit(self, vehicle: Vehicle) -> bool: ...
```

**Why**: It separates "what" from "how", and shows you're thinking about extensibility.

---

### Step 5: Implement (15-20 minutes)
Start with the core entity, then add complexity:
1. Core data classes first (enums, dataclasses)
2. Base classes / ABCs
3. Concrete implementations
4. Service/orchestrator class last

**Narrate as you code:**
> "I'm creating a `ParkingFloor` class that holds a list of spots. The `park()` method finds the first available spot for the vehicle type..."

---

### Step 6: Review and Extend (3 minutes)
After basic implementation:
1. State which design patterns you used and why
2. Identify thread safety concerns
3. Suggest 2-3 extensions

**Example closing:**
> "I used Strategy for fee calculation so we can add new pricing models without touching ParkingLot. For thread safety, I'd add a Lock around the spot assignment. We could extend this with reservations, multi-level pricing, and an API layer."

---

## Worked Example: Movie Ticket Booking

**Step 1: Clarify**
> "I'll model: movies, shows (movie + theater + time), seats with categories, and bookings. Out of scope: payments, reviews, recommendations. Thread safety needed for seat booking."

**Step 2: Entities**
`Movie`, `Theater`, `Show`, `Seat`, `Booking`, `User`, `SeatCategory` (enum)

**Step 3: Relationships**
```
Show ──has──> Theater, Movie, list[Seat]
Booking ──has──> User, Show, list[Seat]
Seat ──has──> SeatCategory, is_reserved (bool)
```

**Step 4: Interfaces**
```python
class SeatReservationService(ABC):
    @abstractmethod
    def reserve(self, show_id: str, seat_ids: list[str]) -> Booking: ...
```

**Step 5: Implement core flow**
```python
def book_seats(self, user_id, show_id, seat_ids, payment):
    with self._lock:  # thread safety
        seats = [self._get_seat(s) for s in seat_ids]
        if any(s.is_reserved for s in seats):
            raise SeatAlreadyBookedError(...)
        for seat in seats:
            seat.is_reserved = True
        booking = Booking(user_id, show_id, seats, payment)
        self._bookings[booking.id] = booking
        return booking
```

**Step 6: Review**
> "I used State for booking status (PENDING→CONFIRMED→CANCELLED), Observer to notify users on status changes. The main extension would be seat release on payment timeout."
