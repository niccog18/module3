from sqlalchemy import create_engine, String, Boolean, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional

engine = create_engine("sqlite:///contacts.db", echo=True)

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"

# 1. Define a Contact model: id, first_name (required), last_name (required), email (unique, required), phone (optional), favorite (boolean, default False)
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(25))
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return (
            f"Contact(id={self.id}, "
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}', "
            f"email='{self.email}', "
            f"phone='{self.phone}', "
            f"favorite={self.favorite})"
            )

Base.metadata.create_all(engine)

#2. Implement these functions:
    # add_contact(first_name, last_name, email, phone=None)
def add_contact(first_name: str,
                last_name: str,
                email: str,
                phone: Optional[str] = None
                ) -> None:
    with Session(engine) as session:
        existing_contact = session.scalar(
            select(Contact).where(Contact.email == email)
        )

        if existing_contact:
            print(f"{email} already exists.")
            return

        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )

        session.add(contact)
        session.commit()

        print(f"Added {first_name} {last_name}")

    # list_contacts() — all contacts, sorted by last name
def list_contacts() -> None:

    with Session(engine) as session:

        contacts = session.scalars(
            select(Contact).order_by(Contact.last_name)
        ).all()

        print("\n=== CONTACTS ===")

        for contact in contacts:
            print(contact)

    # find_contact(email) — single contact by email
def find_contact(email: str) -> Contact | None:

    with Session(engine) as session:

        return session.scalar(
            select(Contact).where(Contact.email == email)
        )

    # update_phone(email, new_phone) — update phone number
def update_phone(
    email: str,
    new_phone: str
) -> None:

    with Session(engine) as session:

        contact = session.scalar(
            select(Contact).where(Contact.email == email)
        )

        if contact:
            contact.phone = new_phone
            session.commit()
            print("Phone updated.")
        else:
            print("Contact not found.")
    
    # toggle_favorite(email) — flip favorite status (True ↔ False)
def toggle_favorite(email: str) -> None:

    with Session(engine) as session:

        contact = session.scalar(
            select(Contact).where(Contact.email == email)
        )

        if contact:
            contact.favorite = not contact.favorite
            session.commit()

            print(
                f"{contact.first_name}'s favorite status "
                f"is now {contact.favorite}"
            )
        else:
            print("Contact not found.")

    # delete_contact(email) — remove a contact
def delete_contact(email: str) -> None:

    with Session(engine) as session:

        contact = session.scalar(
            select(Contact).where(Contact.email == email)
        )

        if contact:
            session.delete(contact)
            session.commit()
            print(f"Deleted {email}")
        else:
            print("Contact not found.")

# 3. Demonstrate all functions: add 5+ contacts, list, update, toggle favorites, delete one, list again.
add_contact(
    "Nicco",
    "Gonzalez",
    "nicco@gmail.com", 
    "111-1111"
)
add_contact(
    "Nayia",
    "Gonzalez",
    "nayia@yahoo.com",
    "222-2222"
)
add_contact(
    "Becca",
    "Gonzalez",
    "becca@hotmail.com",
    "333-3333"
)
add_contact(
    "Kaiden",
    "Gonzalez",
    "kaiden@fakemail.com"
)
add_contact(
    "Capri",
    "Gonzalez",
    "capri@notrealmail.com",
)
add_contact(
    "Julio",
    "Gonzalez",
    "julio@gmail.com",
    "123-4567"
)

list_contacts()

print("\nFinding Julio:")
contact = find_contact("julio@gmail.com")
if contact:
    print(contact)
else:
    print("Contact not found.")

update_phone(
    "kaiden@fakemail.com",
    "987-6543"
)

toggle_favorite("nicco@gmail.com")
toggle_favorite("becca@hotmail.com")

delete_contact("capri@notrealmail.com")

print("\n=== After Updates ===")
list_contacts()