# Step 1 & 2: Create python and connect to SQLite database
import sqlite3

connection = sqlite3.connect("music_db")
print("Connected to database!")

cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Step 3: Create two tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        genre TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER,
        artist_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists(id)      
    )
""")

# Step 4: Insert 3 artists and 5 albums
artists = [
    ("Morgan Wallen", "Country"),
    ("Michael Jackson", "Pop"),
    ("Peabo Bryson", "R&B")
]

cursor.executemany("""
    INSERT INTO artists (name, genre)
    VALUES (?, ?)
""", artists)

cursor.execute(
    "SELECT id FROM artists WHERE name = ?",("Morgan Wallen",)
)
morgan_id = cursor.fetchone()[0]

cursor.execute(
    "SELECT id FROM artists WHERE name = ?",
    ("Michael Jackson",)
)
michael_id = cursor.fetchone()[0]

cursor.execute(
    "SELECT id FROM artists WHERE name = ?",
    ("Peabo Bryson",)
)
peabo_id = cursor.fetchone()[0]

albums = [
    ("One Thing at a Time", 2023, morgan_id),
    ("Dangerous", 2021, morgan_id),
    ("Thriller", 1982, michael_id),
    ("Bad", 1987, michael_id),
    ("Straight from the Heart", 1984, peabo_id)
]

cursor.executemany("""
    INSERT INTO albums (title, year, artist_id)
    VALUES (?, ?, ?)
""", albums)

connection.commit()
print("Tables created. Artists and their albums inserted!")

# Step 5: Query and print all albums(along with a message showing which artists they belong to)
cursor.execute("""
    SELECT albums.title, artists.name
    FROM albums
    JOIN artists
    ON albums.artist_id = artists.id
""")

rows = cursor.fetchall()

print("\nAlbums and their artists:")
for row in rows:
    print(f"'{row[0]}' belongs to {row[1]}")

# Step 6: Close the connection
connection.close()