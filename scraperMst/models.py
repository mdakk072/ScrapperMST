from datetime import datetime, timezone
from scraperMst import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(500), nullable=True, default='1.webp')
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String(100), default='user')
    confirmation_token = db.Column(db.String(100), nullable=True)
    

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"User('{self.user_id}','{self.username}')"

