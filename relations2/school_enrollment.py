# 1. Define these models:
from sqlalchemy import create_engine, String, ForeignKey, Table, Column, Integer, select
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, 
    relationship, Session
)
from typing import Optional

engine = create_engine("sqlite:///enrollment.db", echo=False)

class Base(DeclarativeBase):
    pass

# Association table student_courses for the Student-Course many-to-many.
student_courses = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)

    # Department: id, name (unique). Has many teachers (one-to-many).
class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    teachers: Mapped[list["Teacher"]] = relationship(back_populates="department")

    def __repr__(self):
        return f"Department(id={self.id}, name='{self.name}')"
    
    # Teacher: id, name, department_id (foreign key). Belongs to one department. Teaches many courses (one-to-many).
class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped["Department"] = relationship(
        back_populates="teachers"
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="teacher"
    )

    def __repr__(self):
        return f"Teacher(id={self.id}, name='{self.name}')"

    # Course: id, title, teacher_id (foreign key). Belongs to one teacher. Has many students (many-to-many).
class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id")
    )

    teacher: Mapped["Teacher"] = relationship(
        back_populates="courses"
    )

    students: Mapped[list["Student"]] = relationship(
        secondary=student_courses,
        back_populates="courses"
    )

    def __repr__(self):
        return f"Course(id={self.id}, title='{self.title}')"

    # Student: id, name, email (unique). Enrolled in many courses (many-to-many).
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    email: Mapped[str] = mapped_column(
        String,
        unique=True
    )

    courses: Mapped[list["Course"]] = relationship(
        secondary=student_courses,
        back_populates="students"
    )

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}')"

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# 2.Populate with sample data: 2+ departments, 4+ teachers, 5+ courses, 6+ students with various enrollments.
with Session(engine) as session:

    # Departments
    math = Department(name="Mathematics")
    cs = Department(name="Computer Science")

    session.add_all([math, cs])

    # Teachers
    t1 = Teacher(name="Dr. Smith", department=math)
    t2 = Teacher(name="Dr. Johnson", department=math)
    t3 = Teacher(name="Prof. Brown", department=cs)
    t4 = Teacher(name="Prof. Davis", department=cs)

    session.add_all([t1, t2, t3, t4])

    # Courses
    c1 = Course(title="Algebra", teacher=t1)
    c2 = Course(title="Calculus", teacher=t2)
    c3 = Course(title="Statistics", teacher=t1)
    c4 = Course(title="Python Programming", teacher=t3)
    c5 = Course(title="Databases", teacher=t4)

    session.add_all([c1, c2, c3, c4, c5])

    # Students
    s1 = Student(name="Alice", email="alice@email.com")
    s2 = Student(name="Bob", email="bob@email.com")
    s3 = Student(name="Charlie", email="charlie@email.com")
    s4 = Student(name="Diana", email="diana@email.com")
    s5 = Student(name="Ethan", email="ethan@email.com")
    s6 = Student(name="Fiona", email="fiona@email.com")

    session.add_all([s1, s2, s3, s4, s5, s6])

    # Enrollments
    c1.students.extend([s1, s2, s3])
    c2.students.extend([s2, s4])
    c3.students.extend([s1, s5])

    # More than 3 students
    c4.students.extend([s1, s2, s3, s4, s5])

    c5.students.extend([s3, s4, s6])

    session.commit()

# 3. Write and run these demonstrations:
with Session(engine) as session:
    # Print each department and its teachers
    print("\n=== Departments and Teachers ===")
    departments = session.scalars(select(Department)).all()

    for dept in departments:
        print(f"\n{dept.name}")
        for teacher in dept.teachers:
            print(f"  - {teacher.name}")
   
    # Print each teacher and the courses they teach
    print("\n=== Teachers and Courses ===")
    teachers = session.scalars(select(Teacher)).all()

    for teacher in teachers:
        print(f"\n{teacher.name}")
        for course in teacher.courses:
            print(f"  - {course.title}")
    # Print each course with its enrolled students
    print("\n=== Courses and Students ===")
    courses = session.scalars(select(Course)).all()

    for course in courses:
        print(f"\n{course.title}")
        for student in course.students:
            print(f"  - {student.name}")
    # Print each student and the courses they're enrolled in
    print("\n=== Students and Enrolled Courses ===")
    students = session.scalars(select(Student)).all()

    for student in students:
        print(f"\n{student.name}")
        for course in student.courses:
            print(f"  - {course.title}")
    # Find and print any course with more than 3 students
    print("\n=== Courses With More Than 3 Students ===")

    for course in courses:
        if len(course.students) > 3:
            print(
                f"{course.title} "
                f"({len(course.students)} students)"
            )