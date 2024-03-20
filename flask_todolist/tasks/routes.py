from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from flask_todolist.tasks.forms import TaskCreateForm, TaskModifyForm  # Adjust the import path as needed
from flask_todolist.models import Task
from flask_todolist import db  # Adjust the import path as needed

tasks = Blueprint('tasks', __name__)

@tasks.route('/task/new', methods=['GET', 'POST'])
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
        return redirect(url_for('todolist.my_todolist'))

    return render_template('create_task.html', title='New Task', form=form, legend='New Task')




@tasks.route('/task/modify/<int:task_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('todolist.my_todolist'))
    
    return render_template('modify_task.html', form=form, title='Modify Task', task=task)

@tasks.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    #if task.user_id != current_user.user_id or task.user_id != 1: abort(403) #todo decide if admin can delete any task
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('todolist.my_todolist'))

@tasks.route('/task/view/<int:task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.user_id:
        abort(403)
    return render_template('view_task.html', title=task.title, task=task)


