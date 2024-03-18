import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app) # Initialize Bcrypt
db = SQLAlchemy(app) # Initialize SQLAlchemy
login_manager = LoginManager(app) # Initialize LoginManager
login_manager.login_view = 'login'  # Set the view for login
login_manager.login_message_category = 'warning'  # Set the category for login message
from flask_todolist.services import load_users, load_todos  # Adjusted import
from flask_todolist import models



users = load_users()  # Use the function from services.py
data= load_todos()  # Use the function from services.py
from flask_todolist import routes
