from datetime import date, timedelta

import pytest

from library import Library


@pytest.fixture
def lib():
    l = Library()
    l.add_book("978-5-00000-001-1", "Мастер и Маргарита", "Булгаков", copies=2)
    l.add_book("978-5-00000-002-8", "Преступление и наказание", "Достоевский", copies=1)
    return l


# ---------- add_book ----------

def test_add_book_ok(lib):
    lib.add_book("123", "Тест", "Автор", copies=3)
    assert lib.available("123") == 3


def test_add_book_duplicate_raises(lib):
    with pytest.raises(ValueError):
        lib.add_book("978-5-00000-001-1", "Дубль", "Автор", copies=1)


# ---------- borrow ----------

def test_borrow_returns_due_date(lib):
    today = date(2026, 1, 10)
    due = lib.borrow("978-5-00000-001-1", on=today)
    assert due == today + timedelta(days=14)
    assert lib.available("978-5-00000-001-1") == 1


def test_borrow_all_copies_then_fail(lib):
    isbn = "978-5-00000-002-8"  # 1 экземпляр
    lib.borrow(isbn)
    with pytest.raises(ValueError):
        lib.borrow(isbn)  # больше нет свободных


def test_borrow_unknown_raises(lib):
    with pytest.raises(KeyError):
        lib.borrow("нет-такого")


# ---------- return_book ----------

def test_return_on_time_no_fine(lib):
    isbn = "978-5-00000-001-1"
    due = lib.borrow(isbn, on=date(2026, 1, 1))
    fine = lib.return_book(isbn, on=due)
    assert fine == 0
    assert lib.available(isbn) == 2


def test_return_late_charges_fine(lib):
    isbn = "978-5-00000-001-1"
    due = lib.borrow(isbn, on=date(2026, 1, 1))
    late = due + timedelta(days=3)
    fine = lib.return_book(isbn, on=late)
    assert fine == 30  # 3 дня * 10 руб


# ---------- search ----------

def test_search_by_title(lib):
    res = lib.search("мастер")
    assert len(res) == 1
    assert res[0].author == "Булгаков"


def test_search_by_author(lib):
    res = lib.search("достоевский")
    assert len(res) == 1
    assert res[0].title == "Преступление и наказание"