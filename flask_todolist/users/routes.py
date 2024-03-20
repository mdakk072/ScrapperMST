from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from flask_todolist.users.forms import SignInForm, SignUpForm  
from flask_todolist.models import User  
from flask_todolist import db, bcrypt  # Assuming you're using Flask-Bcrypt for password hashing
from datetime import datetime, timezone
from flask_todolist.users.utils import get_profile_images
from flask_todolist.users.forms import AccountUpdateForm
from flask import current_app
users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next') # This is not working (always None)
            print(request.args)
            #TODO: Fix the next page issue
            return redirect(url_for(next_page) if next_page else url_for('main.home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)
    
@users.route('/logout')
def logout():
    logout_user()  # This will log out the user and clear the session
    flash('You have been logged out', 'success')
    return redirect(url_for('main.home'))

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Include the full_name and bio fields in the new user creation
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            bio=form.bio.data,
            password_hash=hashed_password,
            profile_image='1.webp',  # Assuming a default image
            registered_on=datetime.now(timezone.utc),
            role='user',  # Default role
            email_confirmed=False  # Assuming email confirmation is required
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('signup.html', form=form)

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Generate the list of filenames for profile images stored in static/profile_pics/
    profile_images = get_profile_images(current_app.static_folder)

    # Instantiate the form and populate the profile_image field's choices
    form = AccountUpdateForm(obj=current_user)
    form.profile_image.choices = [(image, image) for image in profile_images]

    if form.validate_on_submit():
        print(form.profile_image.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.full_name = form.full_name.data
        current_user.bio = form.bio.data
        current_user.profile_image = form.profile_image.data  # Update the profile_image field
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # Pre-populate the form with the current user's information
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.full_name.data = current_user.full_name
        form.bio.data = current_user.bio
        form.profile_image.data = current_user.profile_image

    return render_template('account.html', title='Account', form=form, user=current_user)

