from datetime import datetime, timezone
from flask_todolist import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(500), nullable=True, default='1.webp')
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String(100), default='user')
    email_confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(100), nullable=True)
    
    # Relationship
    tasks = db.relationship('Task', backref='user', lazy=True)

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"User('{self.user_id}','{self.username}', '{self.email}')"


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    priority = db.Column(db.Integer, default=3)  # Example: 1=High, 2=Medium, 3=Low
    category = db.Column(db.String(255), nullable=True)  # Simplified category implementation
    time_estimate = db.Column(db.Integer, nullable=True)  # Time in minutes
    recurrence = db.Column(db.String(255), nullable=True)  # Example: daily, weekly, monthly
    attachments = db.Column(db.Text, nullable=True)  # Simplified attachment implementation
    comments = db.Column(db.Text, nullable=True)  # Simplified comments implementation
    status = db.Column(db.String(100), default='Not Started')  # Examples: Not Started, In Progress, On Hold, Completed
    reminder_date = db.Column(db.DateTime, nullable=True)

    # Relationships - assuming simple string fields for categories and attachments for the example
    # For a more complex implementation, these might be separate models with relationships

    def __repr__(self):
        return f'<Task {self.task_id} - {self.title}>'
    
    def __repr__(self):
        return f"Task('{self.task_id}', '{self.title}', '{self.due_date}', '{self.completed}') - User('{self.user_id}')"
