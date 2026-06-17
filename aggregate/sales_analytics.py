# [VIDEO PLACEHOLDER: 10 min — "Aggregations in action: summarizing sales data with GROUP BY and HAVING"]
# Step 1: Set up the database
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

# Insert products
products = [
    ("Laptop", "Electronics", 999.99),
    ("Mouse", "Electronics", 29.99),
    ("Keyboard", "Electronics", 79.99),
    ("Desk Chair", "Furniture", 249.99),
    ("Standing Desk", "Furniture", 449.99),
    ("Monitor Light", "Accessories", 39.99),
    ("Webcam", "Accessories", 69.99),
    ("Headphones", "Accessories", 149.99),
]
cursor.executemany(
    "INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products
)

# Insert orders
orders = [
    (1, 2, "2025-01-15"), (2, 5, "2025-01-16"), (3, 3, "2025-01-17"),
    (4, 1, "2025-01-20"), (5, 1, "2025-01-25"), (6, 4, "2025-02-01"),
    (1, 1, "2025-02-05"), (7, 2, "2025-02-10"), (2, 3, "2025-02-14"),
    (8, 1, "2025-02-20"), (3, 2, "2025-03-01"), (1, 3, "2025-03-05"),
    (6, 6, "2025-03-10"), (4, 2, "2025-03-12"), (7, 1, "2025-03-15"),
]
cursor.executemany(
    "INSERT INTO orders (product_id, quantity, order_date) VALUES (?, ?, ?)", orders
)
connection.commit()
print("Database ready!\n")

# Step 2: Basic aggregations
# Total number of orders
cursor.execute("SELECT COUNT(*) FROM orders")
print(f"Total orders: {cursor.fetchone()[0]}")

# Step 3: GROUP BY — Sales per category
print("\n=== Revenue by Category ===")
cursor.execute("""
    SELECT p.category, 
           COUNT(o.id) as order_count,
           SUM(o.quantity) as units_sold,
           ROUND(SUM(o.quantity * p.price), 2) as revenue
    FROM orders o
    INNER JOIN products p ON o.product_id = p.id
    GROUP BY p.category
    ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} orders, {row[2]} units, ${row[3]:,.2f} revenue")

# Step 4: HAVING -- Filter Group
# Products ordered more than twice
print("\n=== Popular Products (ordered 2+ times) ===")
cursor.execute("""
    SELECT p.name, COUNT(o.id) as times_ordered, SUM(o.quantity) as total_units
    FROM orders o
    INNER JOIN products p ON o.product_id = p.id
    GROUP BY p.id, p.name
    HAVING COUNT(o.id) >= 2
    ORDER BY times_ordered DESC
""")

for row in cursor.fetchall():
    print(f"  {row[0]}: ordered {row[1]} times ({row[2]} total units)")
    
# Step 5: Subqueries
# Products that cost more than average
print("\n=== Above-Average Price Products ===")
cursor.execute("""
    SELECT name, price 
    FROM products 
    WHERE price > (SELECT AVG(price) FROM products)
    ORDER BY price DESC
""")

for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:.2f}")

# Average price for reference
cursor.execute("SELECT ROUND(AVG(price), 2) FROM products")
avg = cursor.fetchone()[0]
print(f"  (Average price: ${avg})")

# Step 6: Subquery with IN — Products that have never been ordered
# Products with no orders
print("\n=== Products Never Ordered ===")
cursor.execute("""
    SELECT name, category, price 
    FROM products 
    WHERE id NOT IN (SELECT DISTINCT product_id FROM orders)
""")

results = cursor.fetchall()
if results:
    for row in results:
        print(f"  {row[0]} ({row[1]}): ${row[2]:.2f}")
else:
    print("  Every product has been ordered at least once!")

connection.close()