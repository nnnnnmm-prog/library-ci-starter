from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    total_copies: int
    available_copies: int
    borrow_days: int = 14


class Library:
    """Учёт книг, выдача и возврат, штрафы за просрочку."""

    def __init__(self):
        self._books: dict[str, Book] = {}
        self._loans: dict[str, list[date]] = {}

    def add_book(self, isbn: str, title: str, author: str, copies: int) -> None:
        """Добавить книгу в фонд."""
        if isbn in self._books:
            raise ValueError(f"Книга с ISBN {isbn} уже есть")
        self._books[isbn] = Book(
            isbn=isbn, title=title, author=author,
            total_copies=copies, available_copies=copies,
        )
        self._loans[isbn] = []

    def borrow(self, isbn: str, on: date | None = None) -> date:
        """Выдать книгу, вернуть дату возврата."""
        if isbn not in self._books:
            raise KeyError(f"Книга {isbn} не найдена")
        book = self._books[isbn]
        # БАГ ДЛЯ СТУДЕНТОВ: не проверяем наличие свободных экземпляров
        book.available_copies -= 1
        on = on or date.today()
        due = on + timedelta(days=book.borrow_days)
        self._loans[isbn].append(due)
        return due

    def return_book(self, isbn: str, on: date | None = None) -> int:
        """Вернуть книгу. Вернуть штраф (руб)."""
        if isbn not in self._books:
            raise KeyError(f"Книга {isbn} не найдена")
        book = self._books[isbn]
        if not self._loans[isbn]:
            raise ValueError("Нет активных выдач этой книги")
        due = self._loans[isbn].pop(0)
        on = on or date.today()
        book.available_copies += 1

        # БАГ ДЛЯ СТУДЕНТОВ: штраф считается наоборот (до срока)
        overdue = (due - on).days
        if overdue > 0:
            return overdue * 10  # 10 руб/день
        return 0

    def available(self, isbn: str) -> int:
        """Сколько свободных экземпляров."""
        if isbn not in self._books:
            raise KeyError(f"Книга {isbn} не найдена")
        return self._books[isbn].available_copies

    def search(self, query: str) -> list[Book]:
        """Поиск по автору или названию (без учёта регистра)."""
        q = query.lower()
        # БАГ ДЛЯ СТУДЕНТОВ: ищем только по названию
        return [b for b in self._books.values() if q in b.title]