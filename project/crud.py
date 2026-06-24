"""
Module 3 Project: Library Management System
crud.py — Create, Read, Update, Delete operations

Your job: Implement every function below.
Import your models and engine from models.py.
"""

from models import engine, Book, Author, Member, Borrowing
from sqlalchemy.orm import Session, joinedload
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError

# ────────────────────────────────────
# CREATE
# ────────────────────────────────────

def add_book(title: str, isbn: str, year_published: int = None,
             available_copies: int = 1):
    """Add a new book to the database. Returns the created Book object."""
    # TODO: open a Session, create a Book, add + commit, return it
    with Session(engine) as session:
        book = Book(
            title=title, isbn=isbn, year_published=year_published, available_copies=available_copies
            )
        session.add(book)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError(
                "A book with this ISBN already exists."
            )
        
        session.refresh(book)
        return book

def add_author(name: str, bio: str = None):
    """Add a new author. Returns the created Author object."""
    with Session(engine) as session:
        author = Author(name=name,bio=bio)
        session.add(author)
        session.commit()
        session.refresh(author)
        return author

def add_member(name: str, email: str):
    """
    Register a new member with today's date as membership_date.
    Returns the created Member object.
    """
    with Session(engine) as session:
        member = Member(
            name=name,
            email=email,membership_date=date.today()
        )
        session.add(member)
        session.commit()
        session.refresh(member)
        return member

def add_author_to_book(book_id: int, author_id: int):
    with Session(engine) as session:

        book = session.get(Book, book_id)
        author = session.get(Author, author_id)

        if not book:
            raise ValueError("Book not found")

        if not author:
            raise ValueError("Author not found")

        if author not in book.authors:
            book.authors.append(author)

        session.commit()

        return book
    
def checkout_book(
        book_id: int, 
        member_id: int,
        checkout_date: date | None = None):
    """
    Check out a book to a member.
    Decrements available_copies by 1 and sets checkout_date to today.
    Raises ValueError if available_copies == 0.
    Returns the created Borrowing object.
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)

        if not book:
            raise ValueError("Book not found")

        if book.available_copies <= 0:
            raise ValueError("No copies available")

        borrowing = Borrowing(
            book_id=book_id,
            member_id=member_id,
            checkout_date=checkout_date or date.today()
        )

        book.available_copies -= 1

        session.add(borrowing)
        session.commit()
        session.refresh(borrowing)
        return borrowing
    
# ──────────────────────────────────────────
# READ
# ──────────────────────────────────────────

def list_books():
    """Return a list of all Book objects."""
    with Session(engine) as session:
        return session.query(Book).all()

def search_books_by_title(title: str):
    """Return books whose title contains the given string (case-insensitive)."""
    with Session(engine) as session:
        return (
            session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()
        )

def find_books_by_author(author_name: str):
    """Return all books associated with an author whose name contains author_name."""
    with Session(engine) as session:
        return (
            session.query(Book)
            .join(Book.authors)
            .filter(Author.name.ilike(f"%{author_name}%"))
            .all()
        )

def list_member_borrowings(member_id: int):
    """Return all active (unreturned) Borrowing objects for the given member."""
    with Session(engine) as session:
        return (
            session.query(Borrowing)
            .options(joinedload(Borrowing.book))
            .filter(
                Borrowing.member_id == member_id,
                Borrowing.return_date.is_(None)
            )
            .all()
        )

def list_overdue_books(days: int = 14):
    """
    Return Borrowing objects where return_date is NULL and
    checkout_date is more than `days` days ago.
    """
    cutoff_date = date.today() - timedelta(days=days)

    with Session(engine) as session:
        return (
            session.query(Borrowing)
            .options(joinedload(Borrowing.book))
            .filter(
                Borrowing.return_date.is_(None),
                Borrowing.checkout_date < cutoff_date
            )
            .all()
        )

# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────

def return_book(borrowing_id: int, return_date: date | None = None):
    """
    Mark a borrowing as returned.
    Sets return_date to today and increments book.available_copies by 1.
    Raises ValueError if the borrowing is not found or already returned.
    """
    with Session(engine) as session:
        borrowing = session.get(Borrowing, borrowing_id)

        if borrowing is None:
            raise ValueError("Borrowing not found")

        if borrowing.return_date is not None:
            raise ValueError("Book already returned")

        borrowing.return_date = return_date or date.today()
        borrowing.book.available_copies += 1

        session.commit()
        session.refresh(borrowing)
        return borrowing


def update_member_email(member_id: int, new_email: str):
    """Update the email address for a member. Returns the updated Member object."""
    with Session(engine) as session:
        member = session.get(Member, member_id)

        if member is None:
            raise ValueError("Member not found")

        member.email = new_email

        session.commit()
        session.refresh(member)
        return member


# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────

def delete_book(book_id: int):
    """
    Delete a book from the database.
    Raises ValueError if the book has any active (unreturned) borrowings.
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)

        if book is None:
            raise ValueError("Book not found")

        active_borrowing = (
            session.query(Borrowing)
            .filter(
                Borrowing.book_id == book_id,
                Borrowing.return_date.is_(None)
            )
            .first()
        )

        if active_borrowing:
            raise ValueError(
                "Cannot delete a book with active borrowings"
            )

        session.delete(book)
        session.commit()

def delete_member(member_id: int):
    """
    Delete a member from the database.
    Raises ValueError if the member has any active (unreturned) borrowings.
    """
    with Session(engine) as session:
        member = session.get(Member, member_id)

        if member is None:
            raise ValueError("Member not found")

        active_borrowing = (
            session.query(Borrowing)
            .filter(
                Borrowing.member_id == member_id,
                Borrowing.return_date.is_(None)
            )
            .first()
        )

        if active_borrowing:
            raise ValueError(
                "Cannot delete a member with active borrowings"
            )

        session.delete(member)
        session.commit()

print("Crud complete!")
