from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Configure the SQLAlchemy part of the app instance

# Create the SQLAlchemy db instance

# Define models

def init_db():
    """Initializes the database."""
    db.create_all()

if __name__ == '__main__':
    init_db()
