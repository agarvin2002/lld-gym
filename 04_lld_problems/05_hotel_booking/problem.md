# Problem 05: Hotel Booking System

## Problem Statement

Design a Hotel Booking System that manages rooms of various types, guest reservations,
pricing with weekend surcharges, and supports thread-safe booking to prevent double booking.

---

## Functional Requirements

### Rooms
- Room types: SINGLE, DOUBLE, SUITE (extensible hierarchy)
- Each room has: room_number, room_type, price_per_night, amenities (list), is_available flag
- Room availability is determined by checking reservations, not a simple boolean flag

### Guests
- Each guest has: name, guest_id, contact (phone/email)
- Guests can have multiple reservations over time

### Reservations
- A reservation has: reservation_id, guest, room, check_in_date, check_out_date, total_price, status
- Status lifecycle: PENDING → CONFIRMED → CHECKED_IN → CHECKED_OUT | CANCELLED
- `total_price` is calculated at booking time using the pricing strategy

### Operations
- `search_rooms(check_in, check_out, room_type=None)` → list of available rooms
- `book_room(guest_id, room_number, check_in, check_out)` → Reservation
- `cancel_reservation(reservation_id)` → bool
- `check_in(reservation_id)` → Reservation
- `check_out(reservation_id)` → Reservation

### Pricing
- Base price = room.price_per_night * number_of_nights
- Weekend surcharge: +20% on each night that falls on Saturday or Sunday
- PricingStrategy is injectable (Strategy pattern)

### Thread Safety
- No two guests should be able to book the same room for overlapping dates simultaneously

---

## Non-Functional Requirements

- Clean state machine for reservation status (State pattern)
- Extensible pricing (new strategies without modifying Hotel)
- Thread-safe operations on shared reservation state

---

## Clarifying Questions

1. **Can a guest have multiple active reservations?**
   Yes. A guest can book multiple rooms or the same room for non-overlapping dates.

2. **What happens if you try to cancel a CHECKED_IN reservation?**
   The system raises an error. Only PENDING or CONFIRMED reservations can be cancelled.

3. **Does cancellation refund the guest?**
   Out of scope for this system. Cancellation just changes status to CANCELLED.

4. **Can a room be booked for a single night?**
   Yes. check_in and check_out on consecutive days = 1 night.

5. **How is check_in/check_out date overlap defined?**
   Two reservations overlap if: new_check_in < existing_check_out AND new_check_out > existing_check_in

6. **Is the weekend surcharge per room per night or on the total?**
   Per night. Each night in the date range is evaluated; Saturday/Sunday nights get +20% of the nightly rate.

7. **What is the maximum number of rooms in the hotel?**
   No hard limit; scalable to any number.

---

## Example Usage

```python
hotel = Hotel("Grand Hotel")
hotel.add_room(SingleRoom("101", price_per_night=100.0, amenities=["WiFi"]))
hotel.add_room(SuiteRoom("201", price_per_night=300.0, amenities=["WiFi", "Jacuzzi", "Minibar"]))

guest = Guest("Alice", "G001", "alice@email.com")
hotel.register_guest(guest)

# Search available rooms
available = hotel.search_rooms(date(2025, 6, 1), date(2025, 6, 5), RoomType.SINGLE)

# Book a room
reservation = hotel.book_room("G001", "101", date(2025, 6, 1), date(2025, 6, 5))

# Check in/out
hotel.check_in(reservation.reservation_id)
hotel.check_out(reservation.reservation_id)
```
