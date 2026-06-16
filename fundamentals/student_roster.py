import sqlite3

connection = sqlite3.connect("school.db")
print("Connected to database!")

cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Create the Students table:
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade INTEGER NOT NULL,
        gpa REAL
    )
""")

# Write functions for each CRUD operation:
# add_students(name, grade, gpa) - inserts a new student
def add_student(name, grade, gpa):
    cursor.execute("""
        INSERT INTO students (name, grade, gpa)
        VALUES (?, ?, ?)
    """, (name, grade, gpa))
    connection.commit()

# get_all_students() - returns all students
def get_all_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

print("=== All Students ===")

for student in get_all_students():
    print(student)

# get_student_by_id(student_id) - returns a single student
def get_student_by_id(student_id):
    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )
    return cursor.fetchone()

print(get_student_by_id(1))

# update_student_gpa(student_id, new_gpa) - updates a student's GPA
def update_student_gpa(student_id, new_gpa):
    cursor.execute("""
        UPDATE students
        SET gpa = ?
        WHERE id = ?
    """, (new_gpa, student_id))

    connection.commit()
update_student_gpa(2, 3.9)

# delete_students(student_id) - removes a student
def delete_student(student_id):
    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
delete_student(4)

if __name__ == "__main__":

    add_student("Nicco Gonzalez", 95, 3.8)
    add_student("Lanayia Gonzalez", 92, 3.5)
    add_student("Dakota Palmer", 83, 3.0)
    add_student("Dillon Palmer", 85, 3.2)
    add_student("Dean Palmer", 98, 4.0)

    print("=== Before Changes ===")
    for student in get_all_students():
        print(student)

    update_student_gpa(2, 3.9)

    delete_student(4)

    print("\n=== After Changes ===")
    for student in get_all_students():
        print(student)
        
    connection.close()