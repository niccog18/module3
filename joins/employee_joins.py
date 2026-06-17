import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# 3 Tables
cursor.execute("""
    CREATE TABLE departments (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT NOT NULL, 
               location TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        salary REAL NOT NULL,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
""")

cursor.execute("""
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        employee_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
""")

print("Tables created succesfully!")

# Populate with sample data:
# At least 3 departments
cursor.executemany("""
                   INSERT INTO departments (name, location) VALUES (?, ?)
                   """, [(" Engineering", "Irvine"), ("Finance", "Hollywood"), ("Human Resources", "San Francisco"), ("Legal", "Sacramento")
    ])

# At least 8 employees across different departments (at least one department should have 3+ employees)
cursor.executemany("""
                   INSERT INTO employees (name, role, salary, department_id) VALUES (?, ?, ?, ?) """, [("Robert Baker", "Software Engineer", 95000, 1), ("Rebecca Gonzalez", "Analyst", 85000, 2), ("Dillon Palmer", "Finance Manager", 100000, 2), ("Nicco Gonzalez", "Senior Developer", 120000, 1), ("Kaiden Gonzalez", "Assistant Manager", 65000, 3), ("Capri Angel", "DevOps Engineer", 83000, 1), ("Yvette Gonzalez", "Human Resource Manager", 76000, 3), ("Kristian Branson", "Auditor", 87000, 2), ("Julio Gonzalez", "AI Engineer", 105000, 1)])    

# At least 4 projects (some employees should lead projects, some should not)

cursor.executemany("""
                   INSERT INTO projects (title, employee_id) VALUES (?, ?) """, [("Website Redesign", 4), ("Marketing Campaign", 3), ("Employee Onboarding", 5), ("Quarterly Audit", 8)])

connection.commit()

print("Sample data inserted!")

# Query Lists
# Query 1: List all employees with their department name (INNER JOIN)
print("\n=== Employees with Departments ===")
cursor.execute("""
SELECT
    employees.name,
    employees.role,
    departments.name AS department
FROM employees
INNER JOIN departments
    ON employees.department_id = departments.id;
""")

for row in cursor.fetchall():
    print(row)

# Query 2: List all departments, even those with no employees (LEFT JOIN)
print("\n=== Departments and Employees ===")
cursor.execute("""
SELECT
    departments.name,
    employees.name
FROM departments
LEFT JOIN employees
    ON departments.id = employees.department_id;
""")

for row in cursor.fetchall():
    print(row)

# Query 3: List all employees and the projects they lead, including employees who don't lead any project (LEFT JOIN)
print("\n=== Employees and their Projects ===")
cursor.execute("""
SELECT
     employees.name,
    projects.title
FROM employees
LEFT JOIN projects
    ON employees.id = projects.employee_id;
""")

for row in cursor.fetchall():
    print(row)

# Query 4: Find employees who don't lead any project (LEFT JOIN + IS NULL)
print("\n=== Employees without Projects ===")
cursor.execute("""
SELECT
    employees.name
FROM employees
LEFT JOIN projects
    ON employees.id = projects.employee_id
WHERE projects.id IS NULL;
""")

for row in cursor.fetchall():
    print(row)

# Query 5: List all projects with the project lead's name AND their department name (requires joining 3 tables)
print("\n=== Projects, Leads and their Departments ===")
cursor.execute("""
SELECT
    projects.title,
    employees.name AS project_lead,
    departments.name AS department
FROM projects
INNER JOIN employees
    ON projects.employee_id = employees.id
INNER JOIN departments
    ON employees.department_id = departments.id;
""")

for row in cursor.fetchall():
    print(row)

connection.close()