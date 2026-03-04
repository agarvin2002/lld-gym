# Design: Library Management System

## ASCII Class Diagram

```
+------------------+          +-------------------+
|   SearchStrategy |<---------|  Library          |
|  (interface)     |          |-------------------|
|------------------|          | name              |
| + search(query,  |          | catalog: dict     |
|   books) -> list |          | members: dict     |
+------------------+          | waiting_lists     |
        ^                     |-------------------|
        |                     | + add_book()      |
   +---------+-----------+    | + borrow_book()   |
   |         |           |    | + return_book()   |
TitleSearch AuthorSearch ISBNSearch | + search_book()  |
Strategy    Strategy     Strategy   | + notify_waiters()|
                                    +-------------------+
                                           |  uses
                                           |
              +----------------------------+----------------+
              |                                             |
    +---------+--------+                       +-----------+------+
    |    Book          |                       |  BorrowRecord    |
    |------------------|    1         *        |------------------|
    | isbn: str        |<---------contains---->| book: Book       |
    | title: str       |                       | member: Member   |
    | author: str      |                       | borrow_date: date|
    | genre: str       |                       | due_date: date   |
    | total_copies: int|                       | return_date: date|
    | avail_copies: int|                       | fine: float      |
    | observers: list  |                       |------------------|
    |------------------|                       | + calculate_fine()|
    | + notify()       |                       +------------------+
    | + add_observer() |
    +------------------+
              |
    +---------+------+
    |                |
+---+------+   +-----+-----+
|  Member  |   | Librarian |
|----------|   |-----------|
| member_id|   | staff_id  |
| name     |   | name      |
| email    |   |-----------|
| borrowed |   |+ add_book()|
| fines    |   |+ remove_book()|
|----------|   +-----------+
|+borrow() |
|+return() |
+----------+
    ^
    |
+---+------+
| Observer |  (BookAvailabilityObserver interface)
|----------|
|+update() |
+----------+
```

## Design Decisions

### 1. Strategy Pattern for Search
- `SearchStrategy` is an abstract base class with a `search(query, books)` method
- Three concrete strategies: `TitleSearchStrategy`, `AuthorSearchStrategy`, `ISBNSearchStrategy`
- `Library.search_book(query, strategy)` accepts any strategy, making it open for extension
- **Why**: Adding a new search criterion (e.g., by genre) requires only a new Strategy class, no changes to `Library`

### 2. Observer Pattern for Book Availability
- `Book` maintains a list of observers (waiting members)
- When a copy is returned and `available_copies` goes from 0 → 1, `Book.notify_observers()` is called
- Members implement `BookAvailabilityObserver` with an `update(book)` method
- **Why**: Decouples the notification logic from the borrowing logic

### 3. Separation of Roles (Member vs Librarian)
- `Member` can only borrow/return books
- `Librarian` can add/remove books and has access to admin operations
- This models real-world RBAC (Role-Based Access Control)

### 4. BorrowRecord as a Value Object
- Captures the full context of a borrowing transaction
- Immutable fields: book, member, borrow_date, due_date
- Mutable fields: return_date, fine (set at return time)
- **Why**: Makes auditing and fine calculation straightforward

### 5. Fine Calculation
- Fine = max(0, (return_date - due_date).days) * FINE_PER_DAY
- FINE_PER_DAY = $1.00
- Stored on the BorrowRecord for record-keeping

### 6. Thread Safety
- `threading.Lock` in `Library` for borrow/return operations
- Prevents double-borrowing the last copy

## Key Design Patterns

| Pattern   | Applied To                         | Benefit                              |
|-----------|------------------------------------|--------------------------------------|
| Strategy  | Search (title/author/isbn)         | Add new search types without changes |
| Observer  | Book availability notifications    | Decouple book from member logic      |
| Facade    | Library class                      | Single entry point for all ops       |

## Data Flow: Borrow Book

```
Client → library.borrow_book(member_id, isbn)
    → validate member exists
    → validate member borrow limit not exceeded
    → validate member outstanding fines ≤ threshold
    → find book by isbn
    → check available_copies > 0
    → decrement available_copies
    → create BorrowRecord(book, member, today, today+14)
    → add record to member.borrowed_books
    → return BorrowRecord
```

## Data Flow: Return Book

```
Client → library.return_book(record)
    → set record.return_date = today
    → calculate fine
    → increment book.available_copies
    → remove record from member.borrowed_books
    → if available_copies was 0 before → notify_observers
```
