from datetime import datetime, timedelta, timezone
import json
import os
import random
from flask_todolist.models import User, Task
from flask_todolist import db, bcrypt
from faker import Faker

def load_todos():
    try:
        with open("todo.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def save_todos(todos):
    with open("todo.json", "w") as file:
        json.dump(todos, file, indent=4)
# Function to load users from JSON file
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save users to JSON file
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


fake = Faker()

def add_mock_tasks_for_each_user(app,n):
    """Adds n mock tasks for each user in the database."""
    with app.app_context():
        users = User.query.all()
        for user in users:
            for _ in range(n):
                start_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=timezone.utc)
                due_date = start_date + timedelta(days=random.randint(1, 90))  # Random due date between 1 to 90 days from start date
                task = Task(
                    user_id=user.user_id,
                    title=fake.sentence(nb_words=6),
                    description=fake.text(max_nb_chars=200),
                    start_date=start_date,
                    due_date=due_date,
                    completed=fake.boolean(chance_of_getting_true=25),  # 25% chance that the task is completed
                    priority=random.choice([1, 2, 3]),  # Randomly choose between high (1), medium (2), and low (3) priority
                    category=random.choice(['Work', 'Personal', 'Home', 'Study']),
                    time_estimate=random.randint(15, 180),  # Random time estimate between 15 to 180 minutes
                    recurrence=random.choice(['None', 'Daily', 'Weekly', 'Monthly']),
                    attachments=random.choice(['file1.pdf', 'file2.jpg', 'file3.docx', 'file4.txt']) if fake.boolean(chance_of_getting_true=25) else None,  # 25% chance of having an attachment
                    comments=fake.sentence(nb_words=12),
                    status=random.choice(['Not Started', 'In Progress', 'On Hold', 'Completed']),
                    reminder_date=due_date - timedelta(days=random.randint(1, 5)) if fake.boolean(chance_of_getting_true=50) else None  # 50% chance of having a reminder date
                )
                db.session.add(task)
            print(f"Added {n} mock tasks for user {user.username}.")
        db.session.commit()

def create_database(app):
    """Create database tables from SQLAlchemy models and populate them if empty."""
    with app.app_context():
        db.create_all()

        # Check if User table is empty and initialize admin user if so
        if User.query.first() is None:
            print("User table is empty. Adding default admin user...")
            # Hash the password for the admin user
            hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password_hash=hashed_password,
                profile_image='6.webp',  # Assuming you have a default image named '6.webp'
                registered_on=datetime.now(timezone.utc),
                last_login=datetime.now(timezone.utc),
                role='admin',  # Setting the role to 'admin'
                email_confirmed=True  # Assuming the admin's email is auto-confirmed
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user added successfully.")

            # Adding default tasks associated with the admin user
            print("Adding default tasks for admin user...")
            default_tasks = [
                {
                    'title': 'Complete Project Proposal',
                    'description': 'Finalize the project proposal for the upcoming quarter.',
                    'start_date': datetime.now(timezone.utc),
                    'due_date': datetime.now(timezone.utc) + timedelta(days=30),
                    'completed': False,
                    'priority': 1,
                    'category': 'Work',
                    'time_estimate': 120,
                    'recurrence': 'None',
                    'attachments': 'proposal_draft.pdf',
                    'comments': 'Need to discuss with the team.',
                    'status': 'In Progress',
                    'reminder_date': datetime.now(timezone.utc) + timedelta(days=25)
                },
                {
                    'title': 'Gym Membership Renewal',
                    'description': 'Renew the annual gym membership.',
                    'start_date': datetime.now(timezone.utc),
                    'due_date': datetime.now(timezone.utc) + timedelta(days=7),
                    'completed': False,
                    'priority': 2,
                    'category': 'Personal',
                    'time_estimate': 30,
                    'recurrence': 'Yearly',
                    'attachments': 'None',
                    'comments': 'Check for any available discounts.',
                    'status': 'Not Started',
                    'reminder_date': datetime.now(timezone.utc) + timedelta(days=5)
                }
            ]

            for task_info in default_tasks:
                task = Task(
                    user_id=admin_user.user_id,
                    title=task_info['title'],
                    description=task_info['description'],
                    start_date=task_info['start_date'],
                    due_date=task_info['due_date'],
                    completed=task_info['completed'],
                    priority=task_info['priority'],
                    category=task_info['category'],
                    time_estimate=task_info['time_estimate'],
                    recurrence=task_info['recurrence'],
                    attachments=task_info['attachments'],
                    comments=task_info['comments'],
                    status=task_info['status'],
                    reminder_date=task_info['reminder_date']
                )
                db.session.add(task)
            db.session.commit()
            print("Default tasks for admin user added successfully.")
        else:
            print("User table is not empty. Skipping initialization.")
        