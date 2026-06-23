# The Translation Challenge
#     Load this dataset into both a SQLite database and a pandas DataFrame:
import sqlite3
import pandas as pd

sales_data = [
    ("Widget A", "Electronics", 29.99, 150, "2025-Q1"),
    ("Widget B", "Electronics", 49.99, 89, "2025-Q1"),
    ("Gadget X", "Accessories", 15.99, 300, "2025-Q1"),
    ("Widget A", "Electronics", 29.99, 200, "2025-Q2"),
    ("Gadget Y", "Accessories", 22.99, 175, "2025-Q2"),
    ("Widget C", "Electronics", 79.99, 50, "2025-Q2"),
    ("Gadget X", "Accessories", 15.99, 280, "2025-Q2"),
    ("Widget B", "Electronics", 49.99, 120, "2025-Q3"),
]
# Columns: product, category, unit_price, quantity, quarter
# SQLite setup
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    product TEXT,
    category TEXT,
    unit_price REAL,
    quantity INTEGER,
    quarter TEXT
)
""")

cursor.execute("DELETE FROM sales")

cursor.executemany("""
INSERT INTO sales
VALUES (?, ?, ?, ?, ?)
""", sales_data)

conn.commit()

# Pandas Setup
df = pd.DataFrame(
    sales_data,
    columns=["product", "category", "unit_price", "quantity", "quarter"]
)

print("\nOriginal DataFrame:")
print(df)

# Answer each question using BOTH SQL and pandas:
# 1. What is the total revenue (price × quantity) per product?
print("\n--- SQL: Total Revenue Per Product ---")

sql_query = """
SELECT
    product,
    SUM(unit_price * quantity) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC
"""

for row in cursor.execute(sql_query):
    print(row)

print("\n--- Pandas: Total Revenue Per Product ---")

df["revenue"] = df["unit_price"] * df["quantity"]

revenue_per_product = (
    df.groupby("product")["revenue"]
      .sum()
      .sort_values(ascending=False)
)

print(revenue_per_product)

# 2. Which quarter had the highest total quantity sold?
print("\n--- SQL: Highest Quantity Quarter ---")

sql_query = """
SELECT
    quarter,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY quarter
ORDER BY total_quantity DESC
LIMIT 1
"""

for row in cursor.execute(sql_query):
    print(row)

print("\n--- Pandas: Highest Quantity Quarter ---")

quantity_by_quarter = (
    df.groupby("quarter")["quantity"]
      .sum()
)

highest_quarter = quantity_by_quarter.idxmax()
highest_quantity = quantity_by_quarter.max()

print(f"{highest_quarter}: {highest_quantity}")

# 3. What is the average unit price per category?
print("\n--- SQL: Average Unit Price Per Category ---")

sql_query = """
SELECT
    category,
    AVG(unit_price) AS avg_price
FROM sales
GROUP BY category
"""

for row in cursor.execute(sql_query):
    print(row)

print("\n--- Pandas: Average Unit Price Per Category ---")

avg_price_category = (
    df.groupby("category")["unit_price"]
      .mean()
)

print(avg_price_category)

# 4. Which products had total quantity over 200 across all quarters?
print("\n--- SQL: Products With Quantity Over 200 ---")

sql_query = """
SELECT
    product,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY product
HAVING SUM(quantity) > 200
"""

for row in cursor.execute(sql_query):
    print(row)

print("\n--- Pandas: Products With Quantity Over 200 ---")

products_over_200 = (
    df.groupby("product")["quantity"]
      .sum()
)

print(products_over_200[products_over_200 > 200])

# BONUS: Use pd.read_sql() to run one of your SQL queries and get the result as a DataFrame.
print("\n--- BONUS: pd.read_sql() ---")

bonus_df = pd.read_sql("""
SELECT
    product,
    SUM(unit_price * quantity) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC
""", conn)

print(bonus_df)

conn.close()