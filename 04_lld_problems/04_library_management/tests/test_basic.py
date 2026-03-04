"""
Basic tests for Library Management System.
Tests core borrow/return flow and search.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.modules.pop("starter", None)  # prevent cross-test module cache collision

from datetime import date, timedelta
import pytest
from starter import (
    Library, Book, Member, Librarian, BorrowRecord,
    TitleSearchStrategy, AuthorSearchStrategy, ISBNSearchStrategy,
)


@pytest.fixture
def library():
    lib = Library("Test Library")
    librarian = Librarian("Alice", "L001")
    book1 = Book("Clean Code", "Robert Martin", "ISBN001", total_copies=2)
    book2 = Book("The Pragmatic Programmer", "David Thomas", "ISBN002", total_copies=1)
    book3 = Book("Design Patterns", "Gang of Four", "ISBN003", total_copies=3)
    librarian.add_book(lib, book1)
    librarian.add_book(lib, book2)
    librarian.add_book(lib, book3)
    member = Member("Bob", "M001", "bob@test.com")
    lib.register_member(member)
    return lib


def test_borrow_book_returns_record(library):
    """Borrowing a book should return a valid BorrowRecord."""
    record = library.borrow_book("M001", "ISBN001")
    assert isinstance(record, BorrowRecord)
    assert record.book.isbn == "ISBN001"
    assert record.member.member_id == "M001"
    assert record.borrow_date == date.today()
    assert record.due_date == date.today() + timedelta(days=14)
    assert record.return_date is None


def test_borrow_decrements_available_copies(library):
    """Borrowing reduces available copies by 1."""
    book = library.get_book("ISBN001")
    before = book.available_copies
    library.borrow_book("M001", "ISBN001")
    assert book.available_copies == before - 1


def test_return_book_increments_available_copies(library):
    """Returning a book increments available copies."""
    record = library.borrow_book("M001", "ISBN001")
    book = library.get_book("ISBN001")
    copies_after_borrow = book.available_copies
    library.return_book(record)
    assert book.available_copies == copies_after_borrow + 1


def test_return_book_sets_return_date(library):
    """return_book should set the return_date on the record."""
    record = library.borrow_book("M001", "ISBN001")
    library.return_book(record)
    assert record.return_date is not None
    assert record.is_returned()


def test_search_by_title(library):
    """TitleSearchStrategy returns books matching title."""
    results = library.search_book("clean", TitleSearchStrategy())
    assert len(results) == 1
    assert results[0].isbn == "ISBN001"


def test_search_by_author(library):
    """AuthorSearchStrategy returns books matching author."""
    results = library.search_book("martin", AuthorSearchStrategy())
    assert len(results) == 1
    assert results[0].title == "Clean Code"


def test_search_by_isbn(library):
    """ISBNSearchStrategy returns exact ISBN match."""
    results = library.search_book("ISBN002", ISBNSearchStrategy())
    assert len(results) == 1
    assert results[0].title == "The Pragmatic Programmer"
