from flask import Flask, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from scraperMst.config import Config
from flask_cors import CORS
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
    CORS(app)
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
    
    
        # Add an endpoint in your Flask app to serve this data
    @app.route('/api/status', methods=['GET'])
    def get_status():
        """
        This endpoint will return the latest scraper and profiles status as JSON.
        """
        from scraperMst.ipc_listener import scraper_status_data, profiles_status_data  # Import the status data
        
        print("API call to get_status")
        print(f"Scraper status: {scraper_status_data}")
        print(f"Profiles status: {profiles_status_data}")
        return jsonify({
            'scraper_status': scraper_status_data,
            'profiles_status': profiles_status_data
        }), 200
    return app
