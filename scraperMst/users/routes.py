from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from scraperMst.users.forms import SignInForm  # Import the sign-in form
from scraperMst.models import User  # Import the User model
from scraperMst import db, bcrypt  # Assuming you're using Flask-Bcrypt for password hashing
from flask import current_app  # To get the static folder for profile images

# Create a blueprint named 'users' for user-related routes
users = Blueprint('users', __name__)

# Login route
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # If the user is already logged in, redirect to the home page
        return redirect(url_for('main.home'))
    
    form = SignInForm()  # Instantiate the login form
    if form.validate_on_submit():  # Validate the form on submission
        # Query the database to check if the username exists
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            # If the user exists and the password is correct, log the user in
            login_user(user, remember=True)
            # Get the 'next' parameter in case the user was redirected to the login page
            next_page = request.args.get('next')  # Not working (always None)
            print(request.args)
            # TODO: Fix the next page issue
            return redirect(url_for(next_page) if next_page else url_for('main.home'))  # Redirect to 'next' if available, otherwise home page
        else:
            # If login fails, show a flash message
            flash('Invalid username or password', 'danger')
    
    # Render the login page template with the form
    return render_template('users/login.html', form=form)
    
# Logout route
@users.route('/logout')
def logout():
    # Log out the current user and clear the session
    logout_user()
    flash('You have been logged out', 'success')  # Flash a success message
    return redirect(url_for('main.home'))  # Redirect to the home page after logout
