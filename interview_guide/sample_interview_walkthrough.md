# Sample Interview Walkthrough: Movie Ticket Booking

> This is a full simulation of an LLD interview, showing what to say and do at each step.

---

## Interview Setup

**Interviewer:** "Design a movie ticket booking system like BookMyShow."

**Candidate thought:** *Don't start coding yet. Start clarifying.*

---

## Step 1: Clarify (5 minutes)

**Candidate says:**
> "Before I start designing, let me clarify a few things.

> 1. What operations do we need? I'm thinking: search movies, list shows, select seats, book, cancel.
> 2. Do we need user accounts and authentication?
> 3. What seat categories do we support — regular, premium, VIP?
> 4. Do we need concurrent seat booking safety?
> 5. Is payment processing in scope, or just booking flow?

**Interviewer says:** "Yes to all operations. Skip auth. Three seat categories: REGULAR, PREMIUM, VIP. Thread safety is important. Payment — just model it as an interface."

---

## Step 2: Identify Entities (2 minutes)

**Candidate says:**
> "Let me identify the main entities. Reading the problem:
> - **Movie**: title, language, duration, genre
> - **Theater**: name, location, screens
> - **Show**: a specific movie at a specific theater at a specific time
> - **Seat**: belongs to a show, has a category and reserved status
> - **Booking**: user, show, seats, payment
> - **SeatCategory**: Enum — REGULAR, PREMIUM, VIP
>
> I'll also need a **BookingService** as the main orchestrator."

---

## Step 3: Define Relationships (2 minutes)

**Candidate says:**
> "Let me map the relationships:
> - Movie and Theater are independent — a Show connects them
> - Show has-a list of Seats
> - Booking has-a list of Seats (the reserved ones)
> - Seat has-a SeatCategory

```
Movie ──────────────────────────────────────┐
                                             ↓
Theater ──has──> Show[] ──has──> Seat[]  ←── Booking
                                               ↑
                                            User, Payment
```

---

## Step 4: Define Interfaces (3 minutes)

**Candidate writes:**
```python
from abc import ABC, abstractmethod
from enum import Enum

class SeatCategory(Enum):
    REGULAR = "REGULAR"
    PREMIUM = "PREMIUM"
    VIP = "VIP"

class PaymentInterface(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool: ...
    @abstractmethod
    def refund(self, amount: float) -> bool: ...
```

**Candidate says:**
> "I'm defining PaymentInterface as an ABC so we can plug in CreditCardPayment, UPIPayment, etc. without changing the booking logic."

---

## Step 5: Implement (20 minutes)

**Candidate writes core classes:**

```python
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
import uuid

@dataclass
class Movie:
    movie_id: str
    title: str
    duration_minutes: int
    language: str

@dataclass
class Seat:
    seat_id: str
    row: str
    number: int
    category: SeatCategory
    is_reserved: bool = False

    def get_price(self) -> float:
        prices = {SeatCategory.REGULAR: 200, SeatCategory.PREMIUM: 350, SeatCategory.VIP: 500}
        return prices[self.category]

@dataclass
class Show:
    show_id: str
    movie: Movie
    start_time: datetime
    theater_name: str
    seats: list[Seat] = field(default_factory=list)

    def get_available_seats(self, category: SeatCategory | None = None) -> list[Seat]:
        seats = [s for s in self.seats if not s.is_reserved]
        if category:
            seats = [s for s in seats if s.category == category]
        return seats

@dataclass
class Booking:
    booking_id: str
    user_id: str
    show: Show
    seats: list[Seat]
    total_amount: float
    status: str = "CONFIRMED"

class BookingService:
    def __init__(self):
        self._shows: dict[str, Show] = {}
        self._bookings: dict[str, Booking] = {}
        self._lock = Lock()  # thread safety for seat reservation

    def add_show(self, show: Show) -> None:
        self._shows[show.show_id] = show

    def get_available_seats(self, show_id: str) -> list[Seat]:
        show = self._shows[show_id]
        return show.get_available_seats()

    def book_seats(
        self,
        user_id: str,
        show_id: str,
        seat_ids: list[str],
        payment: PaymentInterface,
    ) -> Booking:
        with self._lock:  # prevent concurrent double-booking
            show = self._shows.get(show_id)
            if not show:
                raise ValueError(f"Show not found: {show_id}")

            seats = [s for s in show.seats if s.seat_id in seat_ids]
            if len(seats) != len(seat_ids):
                raise ValueError("One or more seats not found")

            # Check availability
            for seat in seats:
                if seat.is_reserved:
                    raise ValueError(f"Seat {seat.seat_id} already reserved")

            total = sum(s.get_price() for s in seats)

            # Charge payment
            if not payment.charge(total):
                raise ValueError("Payment failed")

            # Reserve seats
            for seat in seats:
                seat.is_reserved = True

            booking = Booking(
                booking_id=str(uuid.uuid4()),
                user_id=user_id,
                show=show,
                seats=seats,
                total_amount=total,
            )
            self._bookings[booking.booking_id] = booking
            return booking

    def cancel_booking(self, booking_id: str) -> None:
        booking = self._bookings.get(booking_id)
        if not booking:
            raise ValueError(f"Booking not found: {booking_id}")
        with self._lock:
            for seat in booking.seats:
                seat.is_reserved = False
            booking.status = "CANCELLED"
```

**Candidate says while writing:**
> "I'm wrapping seat reservation in a Lock — this ensures two users can't book the same seat simultaneously. The lock is at BookingService level, not per-show, which is simpler but slightly reduces concurrency. For production, a per-show lock would be better."

---

## Step 6: Review and Extend (5 minutes)

**Candidate says:**
> "Let me review what I've built:
>
> **Patterns used:**
> - **Strategy** (implicit): PaymentInterface lets us plug in any payment method
> - **State**: Booking status (CONFIRMED → CANCELLED) — could formalize with State pattern
>
> **Thread safety:** I used a Lock in `book_seats` to prevent race conditions on seat reservation.
>
> **Extensibility:**
> - New seat categories: add to Enum + price dict
> - New payment methods: implement PaymentInterface
> - Cancellation policy: extract to a `CancellationPolicy` strategy
> - Notifications: add Observer pattern — emit `booking.created` event for email/SMS
>
> **What I'd add with more time:**
> - Seat hold timeout (hold for 10 minutes during payment, release if not completed)
> - Show search by movie, date, city
> - Booking history per user

---

## What Made This Candidate Stand Out

1. ✅ Asked clarifying questions before coding
2. ✅ Identified entities systematically
3. ✅ Drew a relationship diagram
4. ✅ Wrote interfaces before implementations
5. ✅ Mentioned thread safety unprompted and implemented it correctly
6. ✅ Named patterns with reasons, not just buzzwords
7. ✅ Closed with extensions and trade-offs
8. ✅ Narrated reasoning throughout
