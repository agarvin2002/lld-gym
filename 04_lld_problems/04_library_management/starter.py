"""
Problem 04: Library Management System
Starter file with class stubs and type hints.
Complete all TODO sections.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Optional, Dict
import threading


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BORROW_DURATION_DAYS: int = 14
FINE_PER_DAY: float = 1.0          # dollars
MAX_OUTSTANDING_FINE: float = 10.0 # member cannot borrow if fine > this
DEFAULT_MAX_BOOKS: int = 3


# ---------------------------------------------------------------------------
# Observer interface
# ---------------------------------------------------------------------------
class BookAvailabilityObserver(ABC):
    """Observer notified when a book becomes available."""

    @abstractmethod
    def on_book_available(self, book: "Book") -> None:
        """Called when the observed book has at least one available copy."""
        # TODO: implement in concrete classes
        pass


# ---------------------------------------------------------------------------
# Search Strategy
# ---------------------------------------------------------------------------
class SearchStrategy(ABC):
    """Abstract strategy for searching books."""

    @abstractmethod
    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        """Return books matching the query."""
        # TODO: implement in concrete classes
        pass


class TitleSearchStrategy(SearchStrategy):
    """Search books by title (case-insensitive substring match)."""

    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        # TODO: return books whose title contains query (case-insensitive)
        pass


class AuthorSearchStrategy(SearchStrategy):
    """Search books by author (case-insensitive substring match)."""

    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        # TODO: return books whose author contains query (case-insensitive)
        pass


class ISBNSearchStrategy(SearchStrategy):
    """Search books by exact ISBN match."""

    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        # TODO: return books whose isbn exactly matches query
        pass


# ---------------------------------------------------------------------------
# Core Domain Models
# ---------------------------------------------------------------------------
class Book:
    """Represents a book in the library catalog."""

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        genre: str = "General",
        total_copies: int = 1,
    ) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies
        self._observers: List[BookAvailabilityObserver] = []
        # TODO: any additional initialization

    def add_observer(self, observer: BookAvailabilityObserver) -> None:
        """Register an observer for availability notifications."""
        # TODO: add observer to internal list (avoid duplicates)
        pass

    def remove_observer(self, observer: BookAvailabilityObserver) -> None:
        """Unregister an observer."""
        # TODO: remove observer if present
        pass

    def notify_observers(self) -> None:
        """Notify all observers that the book is available."""
        # TODO: call on_book_available on each observer, then clear the list
        pass

    def __repr__(self) -> str:
        return f"Book('{self.title}', isbn={self.isbn}, available={self.available_copies}/{self.total_copies})"


class BorrowRecord:
    """Records a single borrowing transaction."""

    def __init__(
        self,
        book: Book,
        member: "Member",
        borrow_date: Optional[date] = None,
    ) -> None:
        self.book = book
        self.member = member
        self.borrow_date: date = borrow_date or date.today()
        self.due_date: date = self.borrow_date + timedelta(days=BORROW_DURATION_DAYS)
        self.return_date: Optional[date] = None
        self.fine: float = 0.0
        # TODO: any additional fields

    def calculate_fine(self, return_date: Optional[date] = None) -> float:
        """Calculate fine based on return_date vs due_date."""
        # TODO: fine = max(0, (return_date - due_date).days) * FINE_PER_DAY
        pass

    def is_returned(self) -> bool:
        """Return True if the book has been returned."""
        # TODO: check if return_date is set
        pass

    def __repr__(self) -> str:
        return (
            f"BorrowRecord(book={self.book.isbn}, member={self.member.member_id}, "
            f"due={self.due_date}, returned={self.return_date})"
        )


class Member(BookAvailabilityObserver):
    """A library member who can borrow books."""

    def __init__(
        self,
        name: str,
        member_id: str,
        email: str,
        max_books: int = DEFAULT_MAX_BOOKS,
    ) -> None:
        self.name = name
        self.member_id = member_id
        self.email = email
        self.max_books = max_books
        self.borrowed_records: List[BorrowRecord] = []
        self.outstanding_fine: float = 0.0
        self.notifications: List[str] = []  # for testing observer
        # TODO: any additional fields

    def can_borrow(self) -> bool:
        """Return True if member can borrow more books."""
        # TODO: check borrow limit and outstanding fine
        pass

    def active_borrow_count(self) -> int:
        """Return number of currently borrowed (not yet returned) books."""
        # TODO: count records where return_date is None
        pass

    def on_book_available(self, book: Book) -> None:
        """Observer callback when a book becomes available."""
        # TODO: add a notification message to self.notifications
        pass

    def __repr__(self) -> str:
        return f"Member('{self.name}', id={self.member_id})"


class Librarian:
    """A library staff member with admin privileges."""

    def __init__(self, name: str, staff_id: str) -> None:
        self.name = name
        self.staff_id = staff_id

    def add_book(
        self,
        library: "Library",
        book: Book,
        copies: int = 1,
    ) -> None:
        """Add a book (or additional copies) to the library catalog."""
        # TODO: call library internal method to add book
        pass

    def remove_book(self, library: "Library", isbn: str) -> bool:
        """Remove a book from the catalog by ISBN. Returns True if removed."""
        # TODO: call library internal method to remove book
        pass

    def get_all_borrowings(self, library: "Library") -> List[BorrowRecord]:
        """Return all active borrow records across all members."""
        # TODO: aggregate all borrowed_records from all members
        pass


# ---------------------------------------------------------------------------
# Search Catalog (Facade over list of books)
# ---------------------------------------------------------------------------
class SearchCatalog:
    """Provides search functionality over the book catalog."""

    def __init__(self, books: List[Book]) -> None:
        self._books = books

    def search(self, query: str, strategy: SearchStrategy) -> List[Book]:
        """Execute search using the given strategy."""
        # TODO: delegate to strategy.search(query, self._books)
        pass

    def update_books(self, books: List[Book]) -> None:
        """Update the catalog reference."""
        # TODO: update self._books
        pass


# ---------------------------------------------------------------------------
# Library (Facade / main entry point)
# ---------------------------------------------------------------------------
class Library:
    """Main library system. Thread-safe borrow/return operations."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._catalog: Dict[str, Book] = {}   # isbn -> Book
        self._members: Dict[str, Member] = {} # member_id -> Member
        self._search_catalog: SearchCatalog = SearchCatalog([])
        self._lock = threading.Lock()
        # TODO: any additional initialization

    # ------------------------------------------------------------------
    # Catalog management (called by Librarian)
    # ------------------------------------------------------------------
    def _add_book(self, book: Book, copies: int = 1) -> None:
        """Internal: add book or increase copies."""
        # TODO:
        #   If isbn already in catalog, increase total_copies and available_copies
        #   Else add book to catalog
        #   Update search catalog
        pass

    def _remove_book(self, isbn: str) -> bool:
        """Internal: remove book from catalog. Returns True if removed."""
        # TODO: remove from self._catalog, update search catalog
        pass

    # ------------------------------------------------------------------
    # Member management
    # ------------------------------------------------------------------
    def register_member(self, member: Member) -> None:
        """Register a new member."""
        # TODO: add to self._members
        pass

    def get_member(self, member_id: str) -> Optional[Member]:
        """Return member by ID or None."""
        # TODO: lookup in self._members
        pass

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------
    def borrow_book(self, member_id: str, isbn: str) -> BorrowRecord:
        """
        Borrow a book.
        Raises:
            ValueError: if member not found, book not found, no copies available,
                        member at borrow limit, or member has excessive fines.
        """
        # TODO (thread-safe):
        #   1. Get member → validate exists
        #   2. Get book → validate exists
        #   3. Validate member.can_borrow()
        #   4. Validate book.available_copies > 0
        #   5. Check member hasn't already borrowed this ISBN
        #   6. Decrement book.available_copies
        #   7. Create BorrowRecord
        #   8. Add record to member.borrowed_records
        #   9. Return record
        pass

    def return_book(self, record: BorrowRecord, return_date: Optional[date] = None) -> float:
        """
        Process a book return.
        Returns the fine amount charged.
        """
        # TODO (thread-safe):
        #   1. Validate record is not already returned
        #   2. Set return_date
        #   3. Calculate and store fine on record
        #   4. Add fine to member.outstanding_fine
        #   5. Increment book.available_copies
        #   6. If book was at 0 before return, notify observers
        #   7. Return fine amount
        pass

    def search_book(self, query: str, strategy: SearchStrategy) -> List[Book]:
        """Search books using the given strategy."""
        # TODO: delegate to self._search_catalog
        pass

    def add_to_waitlist(self, member_id: str, isbn: str) -> None:
        """Add member to the book's observer list (waiting list)."""
        # TODO: get member and book, call book.add_observer(member)
        pass

    def get_book(self, isbn: str) -> Optional[Book]:
        """Return book by ISBN or None."""
        # TODO: lookup in self._catalog
        pass

    def __repr__(self) -> str:
        return f"Library('{self.name}', books={len(self._catalog)}, members={len(self._members)})"
