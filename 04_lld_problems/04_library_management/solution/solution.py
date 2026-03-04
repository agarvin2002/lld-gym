"""
Problem 04: Library Management System — Full Solution

Design Patterns:
  - Strategy: SearchStrategy (title, author, ISBN)
  - Observer: BookAvailabilityObserver (notify waiters on book return)
  - Facade: Library class (single entry point)
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
FINE_PER_DAY: float = 1.0
MAX_OUTSTANDING_FINE: float = 10.0
DEFAULT_MAX_BOOKS: int = 3


# ---------------------------------------------------------------------------
# Observer interface
# ---------------------------------------------------------------------------
class BookAvailabilityObserver(ABC):
    @abstractmethod
    def on_book_available(self, book: "Book") -> None:
        pass


# ---------------------------------------------------------------------------
# Search Strategy
# ---------------------------------------------------------------------------
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        pass


class TitleSearchStrategy(SearchStrategy):
    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        q = query.lower()
        return [b for b in books if q in b.title.lower()]


class AuthorSearchStrategy(SearchStrategy):
    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        q = query.lower()
        return [b for b in books if q in b.author.lower()]


class ISBNSearchStrategy(SearchStrategy):
    def search(self, query: str, books: List["Book"]) -> List["Book"]:
        return [b for b in books if b.isbn == query]


# ---------------------------------------------------------------------------
# Core Domain Models
# ---------------------------------------------------------------------------
class Book:
    """Represents a book title in the library catalog with copy tracking."""

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

    def add_observer(self, observer: BookAvailabilityObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: BookAvailabilityObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self) -> None:
        for obs in list(self._observers):
            obs.on_book_available(self)
        self._observers.clear()

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

    def calculate_fine(self, return_date: Optional[date] = None) -> float:
        rd = return_date or date.today()
        overdue_days = max(0, (rd - self.due_date).days)
        return overdue_days * FINE_PER_DAY

    def is_returned(self) -> bool:
        return self.return_date is not None

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
        self.notifications: List[str] = []

    def can_borrow(self) -> bool:
        if self.active_borrow_count() >= self.max_books:
            return False
        if self.outstanding_fine > MAX_OUTSTANDING_FINE:
            return False
        return True

    def active_borrow_count(self) -> int:
        return sum(1 for r in self.borrowed_records if not r.is_returned())

    def on_book_available(self, book: Book) -> None:
        msg = f"Book '{book.title}' (ISBN: {book.isbn}) is now available."
        self.notifications.append(msg)

    def __repr__(self) -> str:
        return f"Member('{self.name}', id={self.member_id})"


class Librarian:
    """Library staff with administrative privileges."""

    def __init__(self, name: str, staff_id: str) -> None:
        self.name = name
        self.staff_id = staff_id

    def add_book(self, library: "Library", book: Book, copies: int = 1) -> None:
        library._add_book(book, copies)

    def remove_book(self, library: "Library", isbn: str) -> bool:
        return library._remove_book(isbn)

    def get_all_borrowings(self, library: "Library") -> List[BorrowRecord]:
        records: List[BorrowRecord] = []
        for member in library._members.values():
            records.extend(r for r in member.borrowed_records if not r.is_returned())
        return records


# ---------------------------------------------------------------------------
# Search Catalog
# ---------------------------------------------------------------------------
class SearchCatalog:
    def __init__(self, books: List[Book]) -> None:
        self._books = books

    def search(self, query: str, strategy: SearchStrategy) -> List[Book]:
        return strategy.search(query, self._books)

    def update_books(self, books: List[Book]) -> None:
        self._books = books


# ---------------------------------------------------------------------------
# Library (Facade / main entry point)
# ---------------------------------------------------------------------------
class Library:
    """Main library system facade. Thread-safe borrow/return operations."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._catalog: Dict[str, Book] = {}
        self._members: Dict[str, Member] = {}
        self._search_catalog: SearchCatalog = SearchCatalog([])
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Catalog management
    # ------------------------------------------------------------------
    def _add_book(self, book: Book, copies: int = 1) -> None:
        with self._lock:
            if book.isbn in self._catalog:
                existing = self._catalog[book.isbn]
                existing.total_copies += copies
                existing.available_copies += copies
            else:
                # Use the book as-is (copies already set via total_copies)
                self._catalog[book.isbn] = book
            self._search_catalog.update_books(list(self._catalog.values()))

    def _remove_book(self, isbn: str) -> bool:
        with self._lock:
            if isbn in self._catalog:
                del self._catalog[isbn]
                self._search_catalog.update_books(list(self._catalog.values()))
                return True
            return False

    # ------------------------------------------------------------------
    # Member management
    # ------------------------------------------------------------------
    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member

    def get_member(self, member_id: str) -> Optional[Member]:
        return self._members.get(member_id)

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------
    def borrow_book(self, member_id: str, isbn: str) -> BorrowRecord:
        with self._lock:
            member = self._members.get(member_id)
            if member is None:
                raise ValueError(f"Member '{member_id}' not found.")

            book = self._catalog.get(isbn)
            if book is None:
                raise ValueError(f"Book with ISBN '{isbn}' not found.")

            if not member.can_borrow():
                raise ValueError(
                    f"Member '{member_id}' cannot borrow: at limit or has outstanding fines."
                )

            if book.available_copies <= 0:
                raise ValueError(f"No available copies of ISBN '{isbn}'.")

            # Prevent borrowing the same book twice
            for record in member.borrowed_records:
                if record.book.isbn == isbn and not record.is_returned():
                    raise ValueError(
                        f"Member '{member_id}' has already borrowed ISBN '{isbn}'."
                    )

            book.available_copies -= 1
            record = BorrowRecord(book=book, member=member)
            member.borrowed_records.append(record)
            return record

    def return_book(self, record: BorrowRecord, return_date: Optional[date] = None) -> float:
        with self._lock:
            if record.is_returned():
                raise ValueError("This book has already been returned.")

            rd = return_date or date.today()
            record.return_date = rd
            fine = record.calculate_fine(rd)
            record.fine = fine
            record.member.outstanding_fine += fine

            was_zero = record.book.available_copies == 0
            record.book.available_copies += 1

            if was_zero:
                record.book.notify_observers()

            return fine

    def search_book(self, query: str, strategy: SearchStrategy) -> List[Book]:
        return self._search_catalog.search(query, strategy)

    def add_to_waitlist(self, member_id: str, isbn: str) -> None:
        member = self._members.get(member_id)
        book = self._catalog.get(isbn)
        if member is None:
            raise ValueError(f"Member '{member_id}' not found.")
        if book is None:
            raise ValueError(f"Book with ISBN '{isbn}' not found.")
        book.add_observer(member)

    def get_book(self, isbn: str) -> Optional[Book]:
        return self._catalog.get(isbn)

    def __repr__(self) -> str:
        return f"Library('{self.name}', books={len(self._catalog)}, members={len(self._members)})"
