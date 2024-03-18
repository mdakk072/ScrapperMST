#!/bin/bash

# Start MySQL directly
mysqld_safe &

# Wait for MySQL to become available
while ! mysqladmin ping -h localhost --silent; do
    echo 'Waiting for MySQL to become available...'
    sleep 1
done

# Initialize the MySQL database and user
# (Ensure these commands are idempotent or handle already exists cases)
mysql -u root -e "CREATE USER IF NOT EXISTS 'myuser'@'localhost' IDENTIFIED BY 'mypassword';"
mysql -u root -e "CREATE DATABASE IF NOT EXISTS mydatabase;"
mysql -u root -e "GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"

# Start your Flask application with Gunicorn
gunicorn -w 1 -b 0.0.0.0:8000 app:app
