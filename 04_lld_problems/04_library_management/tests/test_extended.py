"""
Extended tests for Library Management System.
Tests fine calculation, observer pattern, librarian operations, member limits.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

from datetime import date, timedelta
import pytest
from starter import (
    Library, Book, Member, Librarian, BorrowRecord,
    TitleSearchStrategy, ISBNSearchStrategy, FINE_PER_DAY,
)


@pytest.fixture
def library():
    lib = Library("Test Library")
    librarian = Librarian("Alice", "L001")
    for i in range(5):
        book = Book(f"Book {i}", f"Author {i}", f"ISBN00{i}", total_copies=1)
        librarian.add_book(lib, book)
    member = Member("Bob", "M001", "bob@test.com", max_books=3)
    lib.register_member(member)
    return lib


def test_overdue_fine_calculated(library):
    """Fine should be $1/day for each day overdue."""
    record = library.borrow_book("M001", "ISBN000")
    overdue_days = 5
    return_date = record.due_date + timedelta(days=overdue_days)
    fine = library.return_book(record, return_date=return_date)
    assert fine == overdue_days * FINE_PER_DAY
    assert record.fine == fine


def test_no_fine_when_returned_on_time(library):
    """No fine when returned on or before due date."""
    record = library.borrow_book("M001", "ISBN000")
    fine = library.return_book(record, return_date=record.due_date)
    assert fine == 0.0


def test_member_borrow_limit(library):
    """Member cannot borrow more than max_books."""
    library.borrow_book("M001", "ISBN000")
    library.borrow_book("M001", "ISBN001")
    library.borrow_book("M001", "ISBN002")
    with pytest.raises(ValueError):
        library.borrow_book("M001", "ISBN003")


def test_observer_notification_on_return(library):
    """Waiting member is notified when a book is returned."""
    # Borrow the only copy
    record = library.borrow_book("M001", "ISBN000")
    # Register a second member on the waitlist
    waiter = Member("Carol", "M002", "carol@test.com")
    library.register_member(waiter)
    library.add_to_waitlist("M002", "ISBN000")
    # Return the book
    library.return_book(record)
    # Carol should have received a notification
    assert len(waiter.notifications) == 1
    assert "ISBN000" in waiter.notifications[0] or "Book 0" in waiter.notifications[0]


def test_librarian_add_book(library):
    """Librarian can add a new book to the catalog."""
    librarian = Librarian("Alice", "L001")
    new_book = Book("Refactoring", "Martin Fowler", "ISBN999")
    librarian.add_book(library, new_book)
    assert library.get_book("ISBN999") is not None


def test_librarian_remove_book(library):
    """Librarian can remove a book from the catalog."""
    librarian = Librarian("Alice", "L001")
    result = librarian.remove_book(library, "ISBN001")
    assert result is True
    assert library.get_book("ISBN001") is None


def test_librarian_get_all_borrowings(library):
    """Librarian can view all active borrowings."""
    librarian = Librarian("Alice", "L001")
    library.borrow_book("M001", "ISBN000")
    library.borrow_book("M001", "ISBN001")
    records = librarian.get_all_borrowings(library)
    assert len(records) == 2
