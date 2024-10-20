from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from scraperMst.config import Config

# Initialize instances of the Flask extensions
bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing
db = SQLAlchemy()  # Initialize SQLAlchemy to handle the database
login_manager = LoginManager()  # Initialize LoginManager for session management and authentication
login_manager.login_view = 'users.login'  # Set the login view to the 'login' route in the users blueprint
login_manager.login_message_category = 'warning'  # Set the category for the login message flash to 'warning'

# Application factory function to create an instance of the Flask app with configuration
def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Load configuration from the Config class
    app.config.from_object(config_class)
    
    # Initialize Flask extensions with the app
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import and register blueprints
    from scraperMst.main.routes import main
    from scraperMst.users.routes import users
    from scraperMst.errors.handlers import errors
    
    app.register_blueprint(errors)  # Register the error handler blueprint
    app.register_blueprint(main)    # Register the main routes blueprint
    app.register_blueprint(users)   # Register the users routes blueprint
    
    return app
