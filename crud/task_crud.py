# Step 1: Define the model
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional
from datetime import datetime

engine = create_engine("sqlite:///tasks.db", echo=False)

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    completed: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        status = "DONE" if self.completed else "TODO"
        return f"[{status}] {self.title} (priority: {self.priority})"

Base.metadata.create_all(engine)

# Step 2: CREATE — Adding tasks
def create_task(title, description=None, priority="medium"):
    """Create a new task and save it to the database."""
    with Session(engine) as session:
        task = Task(title=title, description=description, priority=priority)
        session.add(task)
        session.commit()
        session.refresh(task)  # Populates the auto-generated id
        print(f"  Created: {task} (id={task.id})")

print("=== Creating Tasks ===")
create_task("Learn SQLAlchemy CRUD", "Complete the guided example", "high")
create_task("Practice joins", "Do the employee joins exercise", "medium")
create_task("Read about ORMs", "Compare SQLAlchemy vs Django ORM", "low")
create_task("Build module project", "Library management system", "high")
create_task("Review SQL syntax", priority="low")

# Step 3: READ — Querying tasks
def get_all_tasks():
    """Retrieve all tasks."""
    with Session(engine) as session:
        return session.query(Task).all()

def get_tasks_by_priority(priority):
    """Retrieve tasks filtered by priority."""
    with Session(engine) as session:
        return session.query(Task).filter_by(priority=priority).all()

def get_incomplete_tasks():
    """Retrieve incomplete tasks, sorted by priority."""
    with Session(engine) as session:
        return session.query(Task)\
            .filter(Task.completed == False)\
            .order_by(Task.priority)\
            .all()

def get_task_by_id(task_id):
    """Retrieve a single task by its ID."""
    with Session(engine) as session:
        return session.get(Task, task_id)

print("\\n=== All Tasks ===")
for task in get_all_tasks():
    print(f"  {task}")

print("\\n=== High Priority ===")
for task in get_tasks_by_priority("high"):
    print(f"  {task}")

# Step 4: UPDATE — Modifying tasks
def complete_task(task_id):
    """Mark a task as completed."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            print(f"  Task {task_id} not found!")
            return
        task.completed = True  # Just change the attribute
        session.commit()
        print(f"  Completed: {task}")

def update_priority(task_id, new_priority):
    """Change a task's priority."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            print(f"  Task {task_id} not found!")
            return
        old = task.priority
        task.priority = new_priority
        session.commit()
        print(f"  Updated: {task.title} ({old} -> {new_priority})")

print("\\n=== Completing Tasks ===")
complete_task(1)
complete_task(3)

print("\\n=== Updating Priority ===")
update_priority(2, "high")

# Step 5: DELETE — Removing tasks
def delete_task(task_id):
    """Delete a task by ID."""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            print(f"  Task {task_id} not found!")
            return
        title = task.title
        session.delete(task)
        session.commit()
        print(f"  Deleted: {title}")

def delete_completed():
    """Delete all completed tasks."""
    with Session(engine) as session:
        completed = session.query(Task).filter_by(completed=True).all()
        count = len(completed)
        for task in completed:
            session.delete(task)
        session.commit()
        print(f"  Deleted {count} completed task(s)")

print("\\n=== Deleting Task #5 ===")
delete_task(5)

print("\\n=== Deleting Completed ===")
delete_completed()

print("\\n=== Remaining Tasks ===")
for task in get_all_tasks():
    print(f"  {task}")
