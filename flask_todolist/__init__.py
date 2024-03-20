from flask import Flask , Blueprint 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_todolist.config import Config


bcrypt = Bcrypt() # Initialize Bcrypt
db = SQLAlchemy() # Initialize SQLAlchemy
login_manager = LoginManager() # Initialize LoginManager
login_manager.login_view = 'users.login'  # Set the view for login
login_manager.login_message_category = 'warning'  # Set the category for login message


def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(Config)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    from flask_todolist.main.routes import main
    from flask_todolist.users.routes import users
    from flask_todolist.tasks.routes import tasks
    from flask_todolist.todolist.routes import todolist
    from flask_todolist.errors.handlers import errors
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(todolist)
    return app