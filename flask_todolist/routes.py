import os
from flask_login import login_required, login_user , current_user, logout_user
from flask_todolist import app, db , bcrypt
from flask_todolist.forms import SignUpForm, SignInForm, AccountUpdateForm, TaskCreateForm, TaskModifyForm
from flask_todolist.models import User, Task
from flask import abort, render_template,redirect, request,url_for,flash 
from datetime import datetime, timezone
# Home page route
@app.route('/')
@app.route('/home')
def home():
    # Assuming your background images are stored in 'static/background'
    backgrounds_dir = os.path.join(app.static_folder, 'background')
    background_images = [os.path.join('background', filename) for filename in os.listdir(backgrounds_dir)]
    print(background_images)
    return render_template('home.html', background_images=background_images)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Generate the list of filenames for profile images stored in static/profile_pics/
    profile_pics_dir = os.path.join(app.static_folder, 'profile_pics')
    profile_images = [filename for filename in os.listdir(profile_pics_dir) if os.path.isfile(os.path.join(profile_pics_dir, filename))]
    profile_images.sort()  # Sort the filenames if necessary

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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Pre-populate the form with the current user's information
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.full_name.data = current_user.full_name
        form.bio.data = current_user.bio
        form.profile_image.data = current_user.profile_image

    return render_template('account.html', title='Account', form=form, user=current_user)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next') # This is not working (always None)
            print(request.args)
            #TODO: Fix the next page issue
            return redirect(url_for(next_page) if next_page else url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)
    


@app.route('/logout')
def logout():
    logout_user()  # This will log out the user and clear the session
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)


@app.route('/my_todolist')
@login_required
def my_todolist():
    page = request.args.get('page', 1, type=int)
    per_page = 8
    sort_by = request.args.get('sort_by', 'due_date', type=str)
    direction = request.args.get('direction', 'desc', type=str)

    # Define the mapping from sort_by value to model attribute
    sort_attributes = {
        'title': Task.title,
        'due_date': Task.due_date,
        'start_date': Task.start_date,
        'priority': Task.priority,
        'status': Task.status,
        'category': Task.category,
        'time_estimate': Task.time_estimate,
        'reminder_date': Task.reminder_date
    }

    # Determine the sorting direction
    if direction.lower() == 'desc':
        query = Task.query.filter_by(user_id=current_user.get_id()).order_by(sort_attributes[sort_by].desc())
    else:
        query = Task.query.filter_by(user_id=current_user.get_id()).order_by(sort_attributes[sort_by])

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    todos = pagination.items

    return render_template('my_todolist.html', todos=todos, pagination=pagination, sort_by=sort_by, direction=direction)



@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskCreateForm()
    if form.validate_on_submit():
        # Convert form data to model instance
        task = Task(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            due_date=form.due_date.data,
            completed=form.completed.data,
            priority=form.priority.data,
            category=form.category.data,
            time_estimate=form.time_estimate.data,
            recurrence=form.recurrence.data,
            attachments=form.attachments.data,
            comments=form.comments.data,
            status=form.status.data,
            reminder_date=form.reminder_date.data,
            user_id=current_user.user_id  # Assuming you have a user_id attribute in your User model
        )
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('my_todolist'))

    return render_template('create_task.html', title='New Task', form=form, legend='New Task')




@app.route('/task/modify/<int:task_id>', methods=['GET', 'POST'])
@login_required
def modify_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.user_id and 0:
        #TODO: Decide if admin can modify any task
        abort(403)  # Ensure the current user owns the task or has permission to modify it
    
    form = TaskModifyForm(obj=task)
    if form.validate_on_submit():
        # Update task with form data
        task.title = form.title.data
        task.description = form.description.data
        task.start_date = form.start_date.data
        task.due_date = form.due_date.data
        task.completed = form.completed.data
        task.priority = form.priority.data
        task.category = form.category.data
        task.time_estimate = form.time_estimate.data
        task.recurrence = form.recurrence.data
        task.attachments = form.attachments.data
        task.comments = form.comments.data
        task.status = form.status.data
        task.reminder_date = form.reminder_date.data
        
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('my_todolist'))
    
    return render_template('modify_task.html', form=form, title='Modify Task', task=task)

@app.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    #if task.user_id != current_user.user_id or task.user_id != 1: abort(403) #todo decide if admin can delete any task
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('my_todolist'))

@app.route('/task/view/<int:task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.user_id:
        abort(403)
    return render_template('view_task.html', title=task.title, task=task)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')