from datetime import datetime, timezone
from scraperMst.models import User
from scraperMst import db, bcrypt

def create_database(app):
    """
    Create database tables from SQLAlchemy models and populate them if empty.
    This function will create the database schema and ensure that a default admin user
    is present if the User table is empty.
    """
    with app.app_context():  # Ensure the function runs within the Flask app context
        db.create_all()  # Create all tables defined in the SQLAlchemy models

        # Check if the User table is empty
        if User.query.first() is None:
            print("User table is empty. Adding default admin user...")
            
            # Hash the password for the admin user using Bcrypt
            hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
            
            # Create an instance of the User model for the admin user
            admin_user = User(
                username='admin',  # Set admin username
                password_hash=hashed_password,  # Set the hashed password
                profile_image='6.webp',  # Default profile image for the admin user
                registered_on=datetime.now(timezone.utc),  # Set the current time for registration
                last_login=datetime.now(timezone.utc),  # Set the current time for last login
                role='admin',  # Assign 'admin' role
            )
            
            # Add the new admin user to the session and commit the changes to the database
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user added successfully.")
