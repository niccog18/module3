"""
Module 3 Project: Library Management System
main.py — Command-line interface

Your job: Implement each menu handler function below.
The main menu loop is already provided — just fill in the handlers.
"""

from models import init_db
from crud import (
    add_book, add_author, add_member, checkout_book, return_book,
    list_books, search_books_by_title, find_books_by_author,
    list_member_borrowings, list_overdue_books,
)

def handle_add_book():
    title = input("Title: ").strip()
    isbn = input("ISBN: ").strip()

    year = input("Year Published (optional): ").strip()
    copies = input("Available Copies [1]: ").strip()

    year_published = int(year) if year else None
    available_copies = int(copies) if copies else 1

    try:
        book = add_book(
            title=title,
            isbn=isbn,
            year_published=year_published,
            available_copies=available_copies
        )

        print(f"Added book: {book.title}")

    except ValueError as e:
        print(f"Error: {e}")
        
def handle_add_author():
    """Prompt for author details and add to the database."""

    name = input("Author Name: ").strip()
    bio = input("Bio (optional): ").strip()

    bio = bio if bio else None

    author = add_author(name, bio)

    print(f"Added author: {author.name}")

def handle_add_member():
    """Prompt for member details and register in the database."""
    name = input("Member Name: ").strip()
    email = input("Email: ").strip()

    member = add_member(name, email)

    print(f"Registered member: {member.name}")

def handle_search_books():
    """Prompt for a search term and display matching books."""
    keyword = input("Search title: ").strip()

    books = search_books_by_title(keyword)

    if not books:
        print("No books found.")
        return

    print("\nResults:")

    for book in books:
        print(
            f"ID: {book.id} | "
            f"{book.title} | "
            f"ISBN: {book.isbn} | "
            f"Copies: {book.available_copies}"
        )

def handle_find_books_by_author():
    """Prompt for an author name and display matching books."""

    author_name = input("Author Name: ").strip()

    books = find_books_by_author(author_name)

    if not books:
        print("No books found.")
        return

    print("\nBooks:")

    for book in books:
        print(
            f"ID: {book.id} | "
            f"{book.title} | "
            f"ISBN: {book.isbn}"
        )

def handle_checkout():
    """Prompt for book ID and member ID, then check out the book."""
    print("\nAvailable Books")

    for book in list_books():
        print(
            f"ID: {book.id} | "
            f"{book.title} | "
            f"Copies Available: {book.available_copies}"
        )

    try:
        book_id = int(input("\nBook ID: "))
        member_id = int(input("Member ID: "))

        borrowing = checkout_book(book_id, member_id)

        print(
            f"Checkout successful. "
            f"Borrowing ID: {borrowing.id}"
        )

    except ValueError as e:
        print(f"Error: {e}")

def handle_return():
    """Prompt for a borrowing ID and return the book."""
    try:
        borrowing_id = int(
            input("Borrowing ID: ")
        )

        return_book(borrowing_id)

        print("Book returned successfully.")

    except ValueError as e:
        print(f"Error: {e}")

def handle_member_borrowings():
    """Display all active borrowings for a member."""
    member_id = int(
        input("Member ID: ")
    )

    borrowings = list_member_borrowings(member_id)

    if not borrowings:
        print("No active borrowings.")
        return

    for borrowing in borrowings:
        print(
            f"Borrowing ID: {borrowing.id} | "
            f"Book: {borrowing.book.title} | "
            f"Checked Out: {borrowing.checkout_date}"
        )

def handle_overdue():
    """Display all overdue borrowings."""
    overdue = list_overdue_books()

    if not overdue:
        print("No overdue books.")
        return

    print("\nOverdue Borrowings:")

    for borrowing in overdue:
        print(
            f"Borrowing ID: {borrowing.id} | "
            f"Book: {borrowing.book.title} | "
            f"Member ID: {borrowing.member_id} | "
            f"Checkout Date: {borrowing.checkout_date}"
        )

def main():
    init_db()

    while True:
        print("\n📚 Library Management System")
        print("1. Add a book")
        print("2. Add Author")
        print("3. Add a member")
        print("4. Search books")
        print("5. Find book by author")
        print("6. Check out a book")
        print("7. Return a book")
        print("8. View member's borrowings")
        print("9. View overdue books")
        print("10. Exit")

        choice = input("\nChoose an option (1-10): ").strip()

        if choice == "1":
            handle_add_book()
        elif choice == "2":
            handle_add_author()
        elif choice == "3":
            handle_add_member()
        elif choice == "4":
            handle_search_books()
        elif choice == "5":
            handle_find_books_by_author()
        elif choice == "6":
            handle_checkout()
        elif choice == "7":
            handle_return()
        elif choice == "8":
            handle_member_borrowings()
        elif choice == "9":
            handle_overdue()
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-10.")

if __name__ == "__main__":
    main()
