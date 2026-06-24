"""
Module 3 Project: Library Management System
seed.py — Populate the database with sample data for testing.

Run after implementing your models and CRUD functions:
    python seed.py

Sample data is loaded from sample_data.json.
"""

import json
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import (init_db, engine, Author, Book, Member)
from crud import (add_author, add_book, add_member, add_author_to_book, checkout_book, return_book)


def seed():
    """Load sample data from sample_data.json and insert it into the database."""
    init_db()

    with open("sample_data.json") as f:
        data = json.load(f)

    # Authors
    for author_data in data["authors"]:
        add_author(
            author_data["name"],
            author_data["bio"]
        )
    # Books
    for book_data in data["books"]:

        add_book(
            title=book_data["title"],
            isbn=book_data["isbn"],
            year_published=book_data["year_published"],
            available_copies=book_data["available_copies"]
        )
    # Author - Book
    with Session(engine) as session:

        for book_data in data["books"]:

            book = session.scalar(
                select(Book).where(
                    Book.isbn == book_data["isbn"]
                )
            )

            for author_name in book_data["authors"]:

                author = session.scalar(
                    select(Author).where(
                        Author.name == author_name
                    )
                )

                add_author_to_book(
                    book.id,
                    author.id
                )
    # MEMBERS

    for member_data in data["members"]:

        add_member(
            member_data["name"],
            member_data["email"]
        )

    # BORROWINGS

    with Session(engine) as session:

        for borrowing_data in data["borrowings"]:

            book = session.scalar(
                select(Book).where(
                    Book.isbn == borrowing_data["book_isbn"]
                )
            )

            member = session.scalar(
                select(Member).where(
                    Member.email ==
                    borrowing_data["member_email"]
                )
            )

            checkout_dt = date.fromisoformat(
                borrowing_data["checkout_date"]
            )

            borrowing = checkout_book(
                book.id,
                member.id,
                checkout_dt
            )

            if borrowing_data["return_date"]:

                return_dt = date.fromisoformat(
                    borrowing_data["return_date"]
                )

                return_book(
                    borrowing.id,
                    return_dt
                )

    print("Seed complete!")

if __name__ == "__main__":
    seed()
