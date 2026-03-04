# Solution Explanation: Library Management System

## Design Patterns Used

### 1. Strategy Pattern — Search
**Problem**: The library needs to support multiple search modes (by title, author, ISBN) without coupling the `Library` class to each mode.

**Solution**: `SearchStrategy` is an abstract base class. `TitleSearchStrategy`, `AuthorSearchStrategy`, and `ISBNSearchStrategy` each implement `search(query, books)`. The `Library.search_book()` method accepts any `SearchStrategy` instance.

**Benefit**: Adding a new search type (e.g., by genre, by year) requires only a new class — no changes to `Library` or `SearchCatalog`.

```python
class TitleSearchStrategy(SearchStrategy):
    def search(self, query: str, books: List[Book]) -> List[Book]:
        q = query.lower()
        return [b for b in books if q in b.title.lower()]
```

### 2. Observer Pattern — Book Availability
**Problem**: When a returned book's availability goes from 0 to 1, we need to notify members on the waiting list.

**Solution**: `Book` maintains a list of `BookAvailabilityObserver` instances. `Member` implements this interface. When `Book.notify_observers()` is called (triggered inside `return_book`), each waiting member's `on_book_available()` is invoked. The observer list is cleared after notification (one-time notification).

```python
def notify_observers(self) -> None:
    for obs in list(self._observers):
        obs.on_book_available(self)
    self._observers.clear()
```

### 3. Facade Pattern — Library Class
**Problem**: Clients shouldn't need to interact with Book, Member, BorrowRecord, and SearchCatalog directly.

**Solution**: `Library` is the single entry point for all operations. It coordinates all domain objects internally.

## Key Design Decisions

### Thread Safety
- A single `threading.Lock` in `Library` guards both `borrow_book` and `return_book`
- This prevents the race condition where two users attempt to borrow the last copy simultaneously
- The lock also guards `_add_book` and `_remove_book` to protect catalog integrity

### BorrowRecord Immutability Convention
- `borrow_date` and `due_date` are set at creation time and never changed
- `return_date` and `fine` are mutable, set only during `return_book`
- This makes auditing straightforward: each record captures the full lifecycle

### Role Separation (Member vs Librarian)
- `Member` can only borrow/return and observe availability
- `Librarian` delegates all operations to `Library` internal methods
- This mirrors real RBAC without complex permission infrastructure

### Fine Calculation
- `BorrowRecord.calculate_fine(return_date)` is a pure function
- `Library.return_book()` calls it and stores the result on the record
- Member's `outstanding_fine` is accumulated and checked in `can_borrow()`

### Observer Clearing After Notification
- The waitlist is cleared after a return so a member is only notified once per return event
- In a real system, you'd re-add the observer if they still can't borrow

## Complexity Analysis

| Operation         | Time Complexity | Notes                          |
|-------------------|-----------------|--------------------------------|
| borrow_book       | O(B)            | B = member's borrow count      |
| return_book       | O(W)            | W = waitlist size for book     |
| search_book       | O(N)            | N = catalog size               |
| add_to_waitlist   | O(1)            | List append                    |

## Possible Extensions
1. **Renewal**: Add `renew_book(record, days)` extending due_date
2. **Fine payment**: `pay_fine(member_id, amount)` reduces outstanding_fine
3. **Reservation**: Reserve a specific copy (BookItem) rather than any copy
4. **Persistence**: Swap in-memory dicts for database repositories
5. **Notification channels**: Email/SMS observers alongside in-memory ones
