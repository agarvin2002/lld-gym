"""
Edge case tests for Library Management System.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

import pytest
from starter import (
    Library, Book, Member, Librarian, BorrowRecord,
    ISBNSearchStrategy,
)


@pytest.fixture
def library():
    lib = Library("Edge Library")
    librarian = Librarian("Alice", "L001")
    book = Book("Singleton Book", "One Author", "UNIQUE001", total_copies=1)
    librarian.add_book(lib, book)
    member = Member("Bob", "M001", "bob@test.com")
    lib.register_member(member)
    return lib


def test_borrow_nonexistent_member_raises(library):
    """Borrowing with a nonexistent member_id raises ValueError."""
    with pytest.raises(ValueError):
        library.borrow_book("GHOST", "UNIQUE001")


def test_borrow_nonexistent_isbn_raises(library):
    """Borrowing a nonexistent ISBN raises ValueError."""
    with pytest.raises(ValueError):
        library.borrow_book("M001", "GHOST_ISBN")


def test_no_copies_available_raises(library):
    """Borrowing when no copies are available raises ValueError."""
    library.borrow_book("M001", "UNIQUE001")
    member2 = Member("Dave", "M002", "dave@test.com")
    library.register_member(member2)
    with pytest.raises(ValueError):
        library.borrow_book("M002", "UNIQUE001")


def test_return_already_returned_record_raises(library):
    """Returning an already-returned record should raise ValueError."""
    record = library.borrow_book("M001", "UNIQUE001")
    library.return_book(record)
    with pytest.raises(ValueError):
        library.return_book(record)


def test_cannot_borrow_same_isbn_twice(library):
    """A member cannot borrow two copies of the same book."""
    librarian = Librarian("Alice", "L001")
    extra_book = Book("Singleton Book", "One Author", "UNIQUE001", total_copies=3)
    # Add more copies via librarian
    library._add_book(Book("Singleton Book", "One Author", "UNIQUE001", total_copies=2), copies=2)
    library.borrow_book("M001", "UNIQUE001")
    with pytest.raises(ValueError):
        library.borrow_book("M001", "UNIQUE001")
