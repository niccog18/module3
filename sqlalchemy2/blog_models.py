# Step 1: Install SQLAlchemy

# In your terminal (with your virtual environment activated):
# pip install sqlalchemy

# Step 2: Set up the engine and base
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional
from datetime import datetime

# --- Engine: connects to a SQLite database file ---
engine = create_engine(
    "sqlite:///blog.db",
    echo=True  # Prints the SQL that SQLAlchemy generates (great for learning!)
)

# --- Base class: all models inherit from this ---
class Base(DeclarativeBase):
    pass

# The echo=True parameter is incredibly useful while learning — it prints every SQL statement that SQLAlchemy generates. You'll see the actual CREATE TABLE and INSERT commands it's running behind the scenes. Turn it off in production.

# Step 3: Define the Author model
class Author(Base):
    __tablename__ = "authors"  # The actual table name in the database

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))  # Optional — can be NULL

    # This helps when you print an Author object
    def __repr__(self) -> str:
        return f"Author(id={self.id}, name='{self.name}', email='{self.email}')"
    
# Let's walk through each piece:

    # __tablename__ — Required. Tells SQLAlchemy what to name the table. Convention is lowercase, plural.
    # Mapped[int] — Type annotation saying this column holds integers
    # mapped_column(primary_key=True) — This is the primary key, auto-incrementing by default in SQLite
    # String(100) — Optional length hint. SQLite doesn't enforce string length, but PostgreSQL does, so it's good practice.
    # nullable=False — This column cannot be NULL (maps to SQL NOT NULL)
    # unique=True — No two rows can have the same value (maps to SQL UNIQUE)
    # __repr__ — Not required by SQLAlchemy, but makes debugging much easier

# Step 4: Define the Post model
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)  # TEXT — no length limit
    published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self) -> str:
        status = "published" if self.published else "draft"
        return f"Post(id={self.id}, title='{self.title}', status={status})"

# Notice default=False and default=datetime.now — these set Python-side defaults. If you create a Post without specifying published, it defaults to False. [VERIFY: datetime.now without parentheses — confirm this works correctly as a callable default in SQLAlchemy 2.0]

# Step 5: Create the tables
# This creates all tables that inherit from Base
Base.metadata.create_all(engine)
print("\nTables created successfully!")

# Step 6: Add some data using the session
# Create a session
with Session(engine) as session:
    # Create Author objects — just regular Python objects
    alice = Author(name="Alice Park", email="alice@blog.com", bio="Python enthusiast")
    bob = Author(name="Bob Martinez", email="bob@blog.com")  # bio is optional

    # Add them to the session
    session.add(alice)
    session.add(bob)

    # Create posts
    post1 = Post(title="Getting Started with Python", content="Python is a great language...")
    post2 = Post(title="SQL vs NoSQL", content="When to use each...", published=True)

    session.add_all([post1, post2])  # add_all for multiple objects

    # Commit — this is when the INSERT statements actually run
    session.commit()

    print(f"\nCreated: {alice}")
    print(f"Created: {bob}")
    print(f"Created: {post1}")
    print(f"Created: {post2}")

# Step 7: Query data back
with Session(engine) as session:
    # Get all authors
    print("\n=== All Authors ===")
    authors = session.query(Author).all()
    for author in authors:
        print(f"  {author}")

    # Get a specific author by email
    print("\n=== Find by Email ===")
    alice = session.query(Author).filter_by(email="alice@blog.com").first()
    print(f"  Found: {alice}")
    print(f"  Bio: {alice.bio}")

    # Get published posts only
    print("\n=== Published Posts ===")
    published = session.query(Post).filter_by(published=True).all()
    for post in published:
        print(f"  {post}")

