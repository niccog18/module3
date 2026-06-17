# Library Analytics
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Create Tables
cursor.execute("""
    CREATE TABLE members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        join_date TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        year_published INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE checkouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        book_id TEXT,
        checkout_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
""")

# Insert Sample data
# Sample Members
members = [
    ("Nicco", "2023-01-10"),
    ("Nayia", "2023-02-15"),
    ("Becca", "2023-03-20"),
    ("Kaiden", "2023-04-05"),
    ("Capri", "2023-05-12")
]

cursor.executemany("""
INSERT INTO members (name, join_date)
VALUES (?, ?)
""", members)

# Sample Books
books = [
    ("The Hobbit", "Fantasy", 1937),
    ("Harry Potter", "Fantasy", 1997),
    ("Dune", "Science Fiction", 1965),
    ("Foundation", "Science Fiction", 1951),
    ("1984", "Dystopian", 1949),
    ("Brave New World", "Dystopian", 1932),
    ("The Catcher in the Rye", "Classic", 1951),
    ("To Kill a Mockingbird", "Classic", 1960),
    ("Never Checked Out Book", "Fantasy", 2020)
]

cursor.executemany("""
INSERT INTO books (title, genre, year_published)
VALUES (?, ?, ?)
""", books)

# Sample Checkouts
checkouts = [
    (1, 1, "2024-01-01", "2024-01-10"),
    (1, 2, "2024-01-15", "2024-01-25"),
    (1, 3, "2024-02-01", None),
    (2, 1, "2024-02-05", "2024-02-15"),
    (2, 4, "2024-02-20", None),
    (2, 5, "2024-03-01", "2024-03-10"),
    (3, 2, "2024-03-05", None),
    (3, 3, "2024-03-12", "2024-03-20"),
    (3, 6, "2024-03-25", None),
    (4, 4, "2024-04-01", None),
    (4, 5, "2024-04-10", "2024-04-18"),
    (4, 7, "2024-04-20", None),
    (5, 1, "2024-05-01", None),
    (5, 8, "2024-05-10", "2024-05-18"),
    (5, 3, "2024-05-20", None)
]

cursor.executemany("""
INSERT INTO checkouts (member_id, book_id, checkout_date, return_date)
VALUES (?, ?, ?, ?)
""", checkouts)

connection.commit()

# 1)Books per Genre
print("\n=== Books Per Genre ===")

cursor.execute("""
SELECT genre, COUNT(*)
FROM books
GROUP BY genre
""")

for genre, count in cursor.fetchall():
    print(f"{genre}: {count}")

# 2) Member with the Most Checkouts
print("\n=== Member With Most Checkouts ===")

cursor.execute("""
SELECT m.name, COUNT(*) AS total_checkouts
FROM members m
JOIN checkouts c
    ON m.id = c.member_id
GROUP BY m.id
ORDER BY total_checkouts DESC
LIMIT 1
""")

name, total = cursor.fetchone()
print(f"{name} checked out {total} books")

# 3) Average Checkouts per Member
print("\n=== Average Checkouts Per Member ===")

cursor.execute("""
SELECT AVG(checkout_count)
FROM (
    SELECT COUNT(*) AS checkout_count
    FROM checkouts
    GROUP BY member_id
)
""")

avg_checkouts = cursor.fetchone()[0]
print(f"Average checkouts per member: {avg_checkouts:.2f}")

# 4) Genres with More than 3 Checkouts
print("\n=== Genres With More Than 3 Checkouts ===")

cursor.execute("""
SELECT b.genre, COUNT(*) AS total_checkouts
FROM books b
JOIN checkouts c
    ON b.id = c.book_id
GROUP BY b.genre
HAVING COUNT(*) > 3
""")

for genre, total in cursor.fetchall():
    print(f"{genre}: {total} checkouts")

# 5) Books Never Checked Out
print("\n=== Books Never Checked Out ===")

cursor.execute("""
SELECT title
FROM books
WHERE id NOT IN (
    SELECT DISTINCT book_id
    FROM checkouts
)
""")

for (title,) in cursor.fetchall():
    print(title)

connection.close()