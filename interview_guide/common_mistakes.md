# Common LLD Interview Mistakes

## Top 10 Mistakes (and How to Fix Them)

---

### 1. Starting to Code Before Clarifying

**What it looks like:**
Interviewer says "Design a parking lot" → candidate immediately opens IDE and starts typing `class Vehicle:`.

**Why it's bad:**
The interviewer hasn't told you about multi-level floors, handicap spots, monthly passes, or whether it's a 20-car lot or a 2000-car garage. Your first design might be completely wrong.

**Fix:**
Always spend 3-5 minutes asking clarifying questions first. It shows maturity. Even if your questions seem obvious, asking them communicates that you care about requirements.

---

### 2. Jumping to Implementation Without Design

**What it looks like:**
Writing code for `ParkingLot` with 10 methods, all in one class, no thought about structure.

**Why it's bad:**
Mid-way through, you realize you need a different structure and have to rewrite everything.

**Fix:**
Write class stubs and relationships in 5 minutes before any real logic. "Let me sketch out the main classes before coding."

---

### 3. God Classes (SRP Violation)

**What it looks like:**
```python
class BookingSystem:
    def search_movies(self): ...
    def create_booking(self): ...
    def charge_payment(self): ...
    def send_confirmation_email(self): ...
    def update_inventory(self): ...
    def generate_report(self): ...
```

**Why it's bad:**
Everything is coupled. One change can break everything. Untestable.

**Fix:**
Break into `MovieSearchService`, `BookingService`, `PaymentProcessor`, `NotificationService`, `InventoryService`.

---

### 4. Over-Engineering

**What it looks like:**
Using 5 design patterns for a problem that needs 2. Adding abstract factories for things with one implementation. Premature extensibility.

**Why it's bad:**
Wastes time, makes the code harder to understand, signals lack of judgment.

**Fix:**
Apply patterns only when you have a concrete reason. "I'm using Strategy here because the problem mentions multiple payment types." Not just to show off pattern knowledge.

---

### 5. Ignoring Thread Safety

**What it looks like:**
Designing a booking system where two users can book the same seat without any locking.

**Why it's bad:**
In FAANG, systems run at massive concurrency. "Did you consider concurrent access?" is a common follow-up. Getting it wrong after the question is worse than addressing it proactively.

**Fix:**
When designing any shared resource (seats, spots, stock), mention: "In a real system, I'd add a Lock here to prevent double-booking."

---

### 6. Not Discussing Extensibility

**What it looks like:**
Finishing implementation and saying "done."

**Why it's bad:**
The interviewer wants to see architectural thinking — not just coding ability.

**Fix:**
Always close with: "To extend this, we could add [X]. The Strategy pattern here means adding a new [Y] requires zero changes to [Z]."

---

### 7. Forgetting Edge Cases

**What it looks like:**
`withdraw(amount)` with no check for negative amounts or insufficient balance.

**Why it's bad:**
Production code handles edge cases. It shows incomplete thinking.

**Fix:**
After implementing happy path, say: "Let me also handle edge cases — negative amounts, empty states, concurrent access..."

---

### 8. Naming Patterns Without Understanding Them

**What it looks like:**
"I used the Singleton pattern here" → interviewer: "Why not just a module-level variable in Python?" → silence.

**Why it's bad:**
Pattern name-dropping without reasoning sounds hollow.

**Fix:**
Always explain *why*: "I'm using Strategy because there are multiple payment methods and we need to be able to add new ones without modifying the checkout logic."

---

### 9. Weak Error Handling

**What it looks like:**
No custom exceptions. Using bare `Exception`. No documentation of what can be raised.

**Fix:**
Define custom exceptions: `InsufficientFundsError`, `SeatAlreadyBookedError`, `InvalidStateError`. It shows domain modeling.

---

### 10. Not Explaining Decisions Out Loud

**What it looks like:**
Coding in silence.

**Why it's bad:**
The interviewer can't see your reasoning. A good design done silently scores worse than a slightly flawed design with clear explanation.

**Fix:**
Narrate: "I'm choosing composition over inheritance here because... I'm making this an enum because... I'd normally use a lock here because..."
