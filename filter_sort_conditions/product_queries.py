# Step: Set up the database with realistic data
import sqlite3

connection = sqlite3.connect(":memory:")  # In-memory DB — disappears when script ends
cursor = connection.cursor()

# Create a products table
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        rating REAL,
        in_stock INTEGER DEFAULT 1
    )
""")

# Insert sample data — a small electronics store
products = [
    ("Wireless Mouse", "Accessories", 29.99, 4.5, 1),
    ("Mechanical Keyboard", "Accessories", 89.99, 4.8, 1),
    ("USB-C Hub", "Accessories", 34.99, 4.2, 0),
    ("27-inch Monitor", "Displays", 299.99, 4.6, 1),
    ("24-inch Monitor", "Displays", 179.99, 4.3, 1),
    ("Webcam HD", "Accessories", 49.99, 3.9, 1),
    ("Noise-Canceling Headphones", "Audio", 199.99, 4.7, 1),
    ("Bluetooth Speaker", "Audio", 59.99, 4.1, 0),
    ("Laptop Stand", "Accessories", 39.99, 4.4, 1),
    ("External SSD 1TB", "Storage", 89.99, 4.6, 1),
    ("External SSD 2TB", "Storage", 149.99, 4.5, 1),
    ("Flash Drive 64GB", "Storage", 12.99, 4.0, 1),
]

cursor.executemany("""
    INSERT INTO products (name, category, price, rating, in_stock) 
    VALUES (?, ?, ?, ?, ?)
""", products)
connection.commit()
# Note: :memory: creates a temporary database that lives in RAM. Perfect for practice — no file cleanup needed.

# Step 2: Basic filtering with WHERE
# Products under $50
print("=== Products Under $50 ===")
cursor.execute("SELECT name, price FROM products WHERE price < 50.00")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:.2f}")

# Step 3: Combining conditions with AND and OR
# In-stock accessories under $50
print("\n=== In-Stock Accessories Under $50 ===")
cursor.execute("""
    SELECT name, price, rating 
    FROM products 
    WHERE category = 'Accessories' 
      AND price < 50.00 
      AND in_stock = 1
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:.2f} (Rating: {row[2]})")

# Step 4: Pattern matching with LIKE and set membership with IN
# Products with "SSD" in the name
print("\n=== SSD Products ===")
cursor.execute("SELECT name, price FROM products WHERE name LIKE '%SSD%'")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:.2f}")

# Products in Audio or Storage categories
print("\n=== Audio & Storage Products ===")
cursor.execute("""
    SELECT name, category, price 
    FROM products 
    WHERE category IN ('Audio', 'Storage')
""")
for row in cursor.fetchall():
    print(f"  [{row[1]}] {row[0]}: ${row[2]:.2f}")

# Step 5: Sorting and limiting
# Top 5 highest-rated products
print("\n=== Top 5 by Rating ===")
cursor.execute("""
    SELECT name, rating, price 
    FROM products 
    WHERE in_stock = 1 
    ORDER BY rating DESC 
    LIMIT 5
""")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"  {i}. {row[0]} — Rating: {row[1]}, ${row[2]:.2f}")

# Cheapest 3 products
print("\n=== 3 Cheapest Products ===")
cursor.execute("""
    SELECT name, price 
    FROM products 
    ORDER BY price ASC 
    LIMIT 3
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:.2f}")

# Step 6: BETWEEN and complex condtions
# Products priced between $50 and $200, in stock, sorted by price
print("\n=== Mid-Range In-Stock Products ===")
cursor.execute("""
    SELECT name, category, price 
    FROM products 
    WHERE price BETWEEN 50.00 AND 200.00 
      AND in_stock = 1 
    ORDER BY price
""")
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[1]}): ${row[2]:.2f}")

connection.close()