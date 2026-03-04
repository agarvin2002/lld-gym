# Problem 04: Library Management System

## Problem Statement

Design and implement a Library Management System that allows members to borrow and return books,
librarians to manage the catalog, and supports searching for books using various strategies.

---

## Functional Requirements

### Books
- Each book has: title, author, ISBN, genre, total copies, available copies
- A library may hold multiple physical copies of the same book (BookItems)
- Books can be searched by title, author, or ISBN

### Members
- Each member has: name, member_id, email, a list of currently borrowed books
- A member may borrow at most 3 books at a time (configurable max_books)
- Members can only borrow if they have no outstanding fines above a threshold

### Librarians
- Librarians can add/remove books from the catalog
- Librarians can view all borrowings and fines
- Librarians can update member status

### Borrowing & Returns
- `borrow_book(member_id, isbn)` → returns a BorrowRecord or raises an exception
- `return_book(record)` → processes the return, calculates fine if overdue
- A BorrowRecord captures: book, member, borrow_date, due_date (14 days from borrow)
- Fine: $1.00 per day overdue (calculated at time of return)

### Notifications (Observer)
- When an unavailable book becomes available, registered members waiting for it are notified
- Members can place themselves on a waiting list for a book

### Search (Strategy)
- `search_book(query, strategy)` → returns list of matching books
- Strategies: TitleSearchStrategy, AuthorSearchStrategy, ISBNSearchStrategy

---

## Non-Functional Requirements

- The system should be extensible (new search strategies without modifying Library class)
- Thread-safe operations where relevant
- Clean separation of roles (Member vs Librarian)

---

## Clarifying Questions

1. **Can a member borrow multiple copies of the same book?**
   No. A member can only borrow one copy of any given ISBN at a time.

2. **What happens if all copies of a book are checked out?**
   The member can be placed on a waiting list. When a copy is returned, the first waiter is notified.

3. **Is the fine deducted automatically or must it be paid explicitly?**
   Fine is calculated and stored on the BorrowRecord. Member must pay before borrowing more books if total outstanding fines exceed $10.

4. **Can a librarian also be a member?**
   No. For simplicity, Librarian and Member are separate roles.

5. **What is the max waiting list size per book?**
   No limit by default; configurable.

6. **Can the due date be extended?**
   Not in the base system, but the design should allow for it (extendable BorrowRecord).

7. **What ISBN format is used?**
   The system accepts any string as ISBN (ISBN-10 or ISBN-13). Validation is not enforced at the model level.

---

## Example Usage

```python
library = Library("City Library")
librarian = Librarian("Alice", "L001")

# Add books
librarian.add_book(library, Book("Clean Code", "Robert Martin", "978-0132350884"), copies=3)

# Member borrows
member = Member("Bob", "M001", "bob@email.com")
library.register_member(member)
record = library.borrow_book("M001", "978-0132350884")

# Member returns
library.return_book(record)
```
