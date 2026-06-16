# Step 1: Set up the database with sample data
import sqlite3

connection = sqlite3.connect("bookstore.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL,
        in_stock INTEGER DEFAULT 1
    )
""")

books = [
    ("Dune", "Frank Herbert", 15.99, 1),
    ("Neuromancer", "William Gibson", 12.99, 1),
    ("Snow Crash", "Neal Stephenson", 14.99, 1),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", 13.99, 0),
    ("Kindred", "Octavia Butler", 11.99, 1),
]
cursor.executemany("""
    INSERT OR IGNORE INTO books (title, author, price, in_stock) 
    VALUES (?, ?, ?, ?)
""", books)
connection.commit()

# Step 2: READ with SELECT
print("=== All Books ===")
cursor.execute("SELECT * FROM books")
for row in cursor.fetchall():
    status = "In Stock" if row[4] else "Out of Stock"
    print(f"  [{row[0]}] {row[1]} by {row[2]} — ${row[3]:.2f} ({status})")

# Step 3: CREATE with INSERT
cursor.execute("""
    INSERT INTO books (title, author, price, in_stock) VALUES (?, ?, ?, ?)
""", ("Foundation", "Isaac Asimov", 13.49, 1))
connection.commit()

# Step 4: UPDATE
cursor.execute("UPDATE books SET price = 17.99 WHERE id = 1")
connection.commit()

# Step 5: DELETE
cursor.execute("DELETE FROM books WHERE id = 3")
connection.commit()

cursor.execute("SELECT id, title FROM books")
for row in cursor.fetchall():
    print(f"  [{row[0]}] {row[1]}")

connection.close()

# Notice that ID 3 is gone after delete. Primary keys don't renumber themselves.

# Key takeaways:

    # fetchall() returns a list of tuples (all matching rows)
    # fetchone() returns a single tuple (or None)
    # Always commit() after INSERT, UPDATE, or DELETE
    # Always use ? placeholders for values
    # Always include WHERE on UPDATE and DELETE