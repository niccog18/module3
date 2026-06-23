# Step 1: Set up both a database and a DataFrame with the same data
import sqlite3
import pandas as pd

# --- Set up the SQLite database ---
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        years_exp INTEGER NOT NULL
    )
""")

employees_data = [
    (1, "Alice", "Engineering", 95000, 5),
    (2, "Bob", "Engineering", 88000, 3),
    (3, "Carol", "Marketing", 72000, 7),
    (4, "David", "Engineering", 105000, 8),
    (5, "Eva", "Marketing", 68000, 2),
    (6, "Frank", "Sales", 62000, 4),
    (7, "Grace", "Sales", 71000, 6),
    (8, "Henry", "Engineering", 92000, 4),
    (9, "Iris", "Marketing", 78000, 5),
    (10, "Jack", "Sales", 58000, 1),
]

cursor.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees_data
)
conn.commit()

# --- Set up the same data as a pandas DataFrame ---
df = pd.DataFrame(employees_data, columns=["id", "name", "department", "salary", "years_exp"])

print("Data loaded in both SQL and pandas!\\n")

# Step 2: Question 1 — "Who earns more than $80,000?"
# --- SQL ---
print("=== SQL: Salary > $80,000 ===")
cursor.execute("SELECT name, salary FROM employees WHERE salary > 80000 ORDER BY salary DESC")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:,.0f}")

# --- pandas ---
print("\\n=== pandas: Salary > $80,000 ===")
high_earners = df[df["salary"] > 80000][["name", "salary"]].sort_values("salary", ascending=False)
for _, row in high_earners.iterrows():
    print(f"  {row['name']}: ${row['salary']:,.0f}")

# Same result, different syntax. SQL uses WHERE salary > 80000. pandas uses df[df["salary"] > 80000].

# Step 3: Question 2 — "What's the average salary per department?"
# --- SQL ---
print("\\n=== SQL: Average Salary by Department ===")
cursor.execute("""
    SELECT department, ROUND(AVG(salary), 0) as avg_salary, COUNT(*) as headcount
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:,.0f} avg ({row[2]} employees)")

# --- pandas ---
print("\\n=== pandas: Average Salary by Department ===")
dept_stats = df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    headcount=("id", "count")
).sort_values("avg_salary", ascending=False)

for dept, row in dept_stats.iterrows():
    print(f"  {dept}: ${row['avg_salary']:,.0f} avg ({row['headcount']} employees)")

# SQL uses GROUP BY department with AVG() and COUNT(). pandas uses groupby("department").agg().

# Step 4: The bridge — Loading SQL results directly into pandas
# Use pandas.read_sql() to query the database and get a DataFrame
print("\\n=== pandas.read_sql(): Best of Both Worlds ===")

query = """
    SELECT department, name, salary,
           salary - (SELECT AVG(salary) FROM employees) as vs_average
    FROM employees 
    WHERE salary > 75000
    ORDER BY salary DESC
"""

# read_sql runs the SQL query and returns a DataFrame
result_df = pd.read_sql(query, conn)
print(result_df.to_string(index=False))

# pd.read_sql() is the bridge. You write SQL to filter and shape the data in the database, and pandas receives the result as a DataFrame — ready for further analysis, visualization, or export.

# Step 5: Going the other direction — DataFrame to SQL table
# Create a new DataFrame
new_hires = pd.DataFrame({
    "name": ["Kate", "Leo", "Maya"],
    "department": ["Engineering", "Sales", "Marketing"],
    "salary": [85000, 60000, 70000],
    "years_exp": [2, 1, 3],
})

# Write the DataFrame directly to a SQL table
new_hires.to_sql("new_hires", conn, if_exists="replace", index=False)

# Verify it worked
cursor.execute("SELECT * FROM new_hires")
print("\\n=== New Hires Table (created from DataFrame) ===")
for row in cursor.fetchall():
    print(f"  {row}")

conn.close()

# df.to_sql() creates a table from a DataFrame. This is useful for loading CSVs into a database, or for saving analysis results.